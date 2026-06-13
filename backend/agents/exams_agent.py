"""
Agent Examens — SmartStudent LangGraph ReAct Agent
Architecture: agent_node <-> tools_node loop (ReAct pattern)
Outils: generer_quiz, obtenir_historique_examens, obtenir_statistiques_examens,
        analyser_lacunes, soumettre_reponses
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

logger = logging.getLogger(__name__)


# ── State ────────────────────────────────────────────────────────────────────

class ExamsAgentState(TypedDict, total=False):
    messages:     Annotated[list, add_messages]
    user_id:      int
    user_context: dict


# ── Helpers ──────────────────────────────────────────────────────────────────

def _db():
    from backend.database import get_db
    return next(get_db())


def _get_llm():
    from backend.agents.orchestrator import get_llm
    return get_llm()


# ── Tools ────────────────────────────────────────────────────────────────────

@tool
def generer_quiz(
    user_id: int,
    matiere: str,
    sujet: str,
    nb_questions: int = 5,
    difficulte: str = "moyen",
) -> str:
    """Génère un quiz QCM personnalisé sur une matière et le sauvegarde en base de données.
    matiere: nom de la matière (ex: 'Machine Learning', 'Algorithmique', 'Réseaux').
    sujet: sous-sujet précis (ex: 'arbres de décision', 'tri rapide', 'protocole TCP').
    nb_questions: nombre de questions (entre 3 et 15).
    difficulte: 'facile', 'moyen', ou 'difficile'."""
    try:
        from backend.models import Exam
        from langchain_core.messages import HumanMessage as HM

        nb_questions = max(3, min(15, int(nb_questions)))
        prompt = (
            f"Génère un quiz QCM de {nb_questions} questions pour un étudiant ingénieur.\n"
            f"Matière: {matiere}\n"
            f"Sujet: {sujet}\n"
            f"Difficulté: {difficulte}\n\n"
            "Réponds UNIQUEMENT avec ce JSON (aucun texte avant ou après):\n"
            '{"questions": [{"id": 1, "question": "...", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], '
            '"reponse_correcte": "A", "explication": "...", "points": 2}]}\n\n'
            "RÈGLES:\n"
            "- Questions précises et adaptées au niveau ingénieur.\n"
            "- 4 options par question (A, B, C, D).\n"
            "- reponse_correcte est la LETTRE uniquement (A, B, C ou D).\n"
            "- Explication courte et pédagogique (1-2 phrases).\n"
            "- Difficulté cohérente avec le paramètre demandé."
        )

        resp = _get_llm().invoke([HM(content=prompt)])
        text = resp.content.strip()
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].strip()

        quiz_data = json.loads(text)
        questions = quiz_data.get("questions", [])
        if not questions:
            return "Erreur: le LLM n'a pas généré de questions valides. Réessaie."

        total_points = sum(q.get("points", 2) for q in questions)

        db = _db()
        try:
            exam = Exam(
                user_id=user_id,
                title=f"Quiz — {matiere} : {sujet}",
                subject=matiere,
                questions=questions,
                total_points=total_points,
                status="in_progress",
                started_at=datetime.utcnow(),
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)

            # Format questions for display (without correct answers)
            display_qs = []
            for q in questions:
                display_qs.append({
                    "id": q["id"],
                    "question": q["question"],
                    "options": q["options"],
                    "points": q.get("points", 2),
                })

            return json.dumps({
                "success": True,
                "exam_id": exam.id,
                "titre": exam.title,
                "matiere": matiere,
                "sujet": sujet,
                "nb_questions": len(questions),
                "total_points": total_points,
                "difficulte": difficulte,
                "questions": display_qs,
                "message": (
                    f"Quiz généré avec succès !\n"
                    f"- {len(questions)} questions sur '{sujet}' ({matiere})\n"
                    f"- Difficulté: {difficulte} | Total: {total_points} points\n"
                    f"- ID du quiz: {exam.id}\n"
                    "Réponds à chaque question en indiquant la lettre (A, B, C ou D)."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()

    except json.JSONDecodeError:
        return "Erreur: le format du quiz généré est invalide. Réessaie avec un sujet plus précis."
    except Exception as e:
        logger.error("generer_quiz error: %s", e)
        return f"Erreur lors de la génération du quiz: {e}"


@tool
def obtenir_historique_examens(user_id: int) -> str:
    """Récupère l'historique complet des quiz et examens passés par l'étudiant avec leurs scores."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exams = (
                db.query(Exam)
                .filter(Exam.user_id == user_id)
                .order_by(Exam.created_at.desc())
                .limit(20)
                .all()
            )
            if not exams:
                return "Aucun examen ou quiz trouvé pour cet étudiant."

            result = []
            for exam in exams:
                note = None
                if exam.score is not None and exam.total_points:
                    note = round((exam.score / exam.total_points) * 20, 2)
                result.append({
                    "id": exam.id,
                    "titre": exam.title,
                    "matiere": exam.subject or "Non spécifiée",
                    "statut": exam.status,
                    "score": exam.score,
                    "total_points": exam.total_points,
                    "note_sur_20": note,
                    "date": exam.created_at.strftime("%d/%m/%Y") if exam.created_at else "?",
                })
            return json.dumps({"examens": result, "total": len(result)}, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("obtenir_historique_examens error: %s", e)
        return f"Erreur lors de la récupération de l'historique: {e}"


@tool
def obtenir_statistiques_examens(user_id: int) -> str:
    """Calcule les statistiques de performance de l'étudiant : moyenne générale, meilleure/pire matière,
    nombre de quiz complétés, progression."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exams = (
                db.query(Exam)
                .filter(Exam.user_id == user_id, Exam.status == "completed")
                .all()
            )
            if not exams:
                return "Aucun examen complété. Génère ton premier quiz pour commencer !"

            scores_by_subject: dict = {}
            all_notes = []
            for exam in exams:
                if exam.score is not None and exam.total_points:
                    note = round((exam.score / exam.total_points) * 20, 2)
                    all_notes.append(note)
                    subj = exam.subject or "Autre"
                    scores_by_subject.setdefault(subj, []).append(note)

            moyenne_generale = round(sum(all_notes) / len(all_notes), 2) if all_notes else None
            subject_averages = {
                subj: round(sum(notes) / len(notes), 2)
                for subj, notes in scores_by_subject.items()
            }
            best_subject = max(subject_averages, key=subject_averages.get) if subject_averages else None
            worst_subject = min(subject_averages, key=subject_averages.get) if subject_averages else None

            return json.dumps({
                "examens_completes": len(exams),
                "moyenne_generale_sur_20": moyenne_generale,
                "par_matiere": subject_averages,
                "meilleure_matiere": best_subject,
                "matiere_a_ameliorer": worst_subject,
                "progression": "En hausse" if len(all_notes) >= 2 and all_notes[-1] > all_notes[0] else "Stable",
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("obtenir_statistiques_examens error: %s", e)
        return f"Erreur lors du calcul des statistiques: {e}"


@tool
def analyser_lacunes(user_id: int) -> str:
    """Identifie les matières les plus faibles de l'étudiant et recommande les sujets à réviser
    en priorité, basé sur l'historique des examens."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exams = (
                db.query(Exam)
                .filter(Exam.user_id == user_id, Exam.status == "completed")
                .all()
            )
            if not exams:
                return "Aucun examen complété. Commence par passer quelques quiz pour que je puisse analyser tes lacunes."

            subject_data: dict = {}
            for exam in exams:
                if exam.score is None or not exam.total_points:
                    continue
                note = round((exam.score / exam.total_points) * 20, 2)
                subj = exam.subject or "Autre"
                subject_data.setdefault(subj, []).append(note)

            if not subject_data:
                return "Pas assez de données scorées pour analyser les lacunes."

            weak_subjects = []
            strong_subjects = []
            for subj, notes in subject_data.items():
                avg = round(sum(notes) / len(notes), 2)
                if avg < 12:
                    weak_subjects.append({"matiere": subj, "moyenne": avg, "nb_quiz": len(notes)})
                else:
                    strong_subjects.append({"matiere": subj, "moyenne": avg})

            weak_subjects.sort(key=lambda x: x["moyenne"])

            return json.dumps({
                "matieres_faibles": weak_subjects,
                "matieres_fortes": strong_subjects,
                "recommandation": (
                    f"Concentre-toi sur : {', '.join(w['matiere'] for w in weak_subjects[:3])}"
                    if weak_subjects else "Bonne progression ! Continue à t'entraîner sur toutes les matières."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("analyser_lacunes error: %s", e)
        return f"Erreur lors de l'analyse: {e}"


@tool
def soumettre_reponses(exam_id: int, reponses_json: str) -> str:
    """Soumet les réponses de l'étudiant à un quiz et calcule le score automatiquement.
    reponses_json: JSON string avec les réponses. Format: {"1": "A", "2": "C", "3": "B", ...}
    où la clé est l'ID de la question et la valeur est la lettre choisie (A, B, C ou D)."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exam = db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam:
                return f"Aucun examen trouvé avec l'ID {exam_id}."
            if exam.status == "completed":
                return f"Ce quiz est déjà complété. Score obtenu: {exam.score}/{exam.total_points}."

            try:
                user_answers = json.loads(reponses_json)
            except json.JSONDecodeError:
                return "Format de réponses invalide. Utilise: {\"1\": \"A\", \"2\": \"B\", ...}"

            questions = exam.questions or []
            score = 0
            corrections = []
            for q in questions:
                q_id = str(q.get("id", ""))
                correct = str(q.get("reponse_correcte", "")).upper()
                user_ans = str(user_answers.get(q_id, "")).upper()
                points = int(q.get("points", 2))
                is_correct = user_ans == correct

                if is_correct:
                    score += points

                corrections.append({
                    "question_id": q_id,
                    "question": q.get("question", ""),
                    "ta_reponse": user_ans or "Non répondu",
                    "bonne_reponse": correct,
                    "correct": is_correct,
                    "points_obtenus": points if is_correct else 0,
                    "explication": q.get("explication", ""),
                })

            note_sur_20 = round((score / exam.total_points) * 20, 2) if exam.total_points else 0

            exam.score = score
            exam.answers = user_answers
            exam.status = "completed"
            exam.completed_at = datetime.utcnow()
            db.commit()

            appreciation = (
                "Excellent !" if note_sur_20 >= 16 else
                "Très bien !" if note_sur_20 >= 14 else
                "Bien !" if note_sur_20 >= 12 else
                "Passable — continue à réviser." if note_sur_20 >= 10 else
                "À améliorer — revois les points faibles."
            )

            return json.dumps({
                "success": True,
                "exam_id": exam_id,
                "score": score,
                "total_points": exam.total_points,
                "note_sur_20": note_sur_20,
                "appreciation": appreciation,
                "nb_bonnes_reponses": sum(1 for c in corrections if c["correct"]),
                "nb_questions": len(questions),
                "corrections": corrections,
                "message": (
                    f"Quiz terminé !\n"
                    f"Score: {score}/{exam.total_points} → {note_sur_20}/20\n"
                    f"{appreciation}\n"
                    f"{sum(1 for c in corrections if c['correct'])}/{len(questions)} bonnes réponses."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("soumettre_reponses error: %s", e)
        return f"Erreur lors de la soumission: {e}"


_TOOLS = [generer_quiz, obtenir_historique_examens, obtenir_statistiques_examens,
          analyser_lacunes, soumettre_reponses]


# ── Agent Node ───────────────────────────────────────────────────────────────

async def agent_node(state: ExamsAgentState) -> dict:
    user_id = state.get("user_id", 0)
    ctx = state.get("user_context") or {}
    nom = ctx.get("full_name") or ctx.get("username") or "l'étudiant"
    filiere = ctx.get("major") or "filière non renseignée"

    system_prompt = (
        f"Tu es l'Agent Examens de SmartStudent — ENIAD Berkane.\n"
        f"Tu parles à {nom}, filière {filiere}. ID: {user_id}.\n\n"
        "OUTILS DISPONIBLES — utilise-les systématiquement:\n"
        f"1. Générer un quiz QCM → generer_quiz(user_id={user_id}, matiere=..., sujet=..., nb_questions=..., difficulte=...)\n"
        f"2. Voir l'historique des examens → obtenir_historique_examens(user_id={user_id})\n"
        f"3. Statistiques de performance → obtenir_statistiques_examens(user_id={user_id})\n"
        f"4. Analyser les matières faibles → analyser_lacunes(user_id={user_id})\n"
        f"5. Corriger les réponses → soumettre_reponses(exam_id=..., reponses_json=...)\n\n"
        "COMPORTEMENT:\n"
        "- Pour générer un quiz: demande la matière et le sujet précis si non fournis.\n"
        "- Après avoir affiché les questions, attends les réponses de l'étudiant avant de corriger.\n"
        "- Pour la correction: utilise soumettre_reponses avec les réponses fournies.\n"
        "- Commente les résultats de façon pédagogique et encourageante.\n"
        "- Suggère des révisions sur les points faibles identifiés.\n"
        "- Réponds en français."
    )

    try:
        llm = _get_llm().bind_tools(_TOOLS)
        messages = [SystemMessage(content=system_prompt)] + list(state.get("messages", []))
        resp = await llm.ainvoke(messages)
        return {"messages": [resp]}
    except Exception as e:
        logger.error("exams agent_node error: %s", e)
        return {"messages": [AIMessage(content="Le service IA est temporairement indisponible. Veuillez reessayer dans quelques instants.")]}


# ── Graph compilation ─────────────────────────────────────────────────────────

def _build_exams_graph():
    g = StateGraph(ExamsAgentState)
    g.add_node("agent", agent_node)
    g.add_node("tools", ToolNode(_TOOLS))
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", tools_condition)
    g.add_edge("tools", "agent")
    return g.compile(checkpointer=MemorySaver())


_graph_instance = None


def get_compiled_exams_graph():
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = _build_exams_graph()
        logger.info("ExamsAgent ReAct graph compiled")
    return _graph_instance


# ── Public API ────────────────────────────────────────────────────────────────

class ExamsAgent:
    def __init__(self):
        self._graph = get_compiled_exams_graph()

    async def process(
        self,
        user_message: str,
        user_id: int,
        user_context: dict,
        conversation_id: str = "default",
    ) -> dict:
        thread_id = f"exams_{conversation_id}"
        initial: ExamsAgentState = {
            "messages": [HumanMessage(content=user_message)],
            "user_id": user_id,
            "user_context": user_context,
        }
        config = {"configurable": {"thread_id": thread_id}}
        try:
            result = await self._graph.ainvoke(initial, config=config)
        except Exception as e:
            logger.error("ExamsAgent.process graph error: %s", e)
            return {"response": "Le service IA est temporairement indisponible. Veuillez reessayer."}
        last_ai = next(
            (m for m in reversed(result.get("messages", [])) if isinstance(m, AIMessage)),
            None,
        )
        return {"response": str(last_ai.content) if last_ai else "Erreur interne."}


def get_exams_agent() -> ExamsAgent:
    return ExamsAgent()
