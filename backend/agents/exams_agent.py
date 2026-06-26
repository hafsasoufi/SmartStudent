"""
Agent Examens — SmartStudent LangGraph ReAct Agent
Fonctionnalités : quiz QCM/ouvert/exercices, analyse de PDF de cours, résumés structurés,
examens blancs, identification de notions clés, planning de révision personnalisé.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

logger = logging.getLogger(__name__)


# ── State ─────────────────────────────────────────────────────────────────────

class ExamsAgentState(TypedDict, total=False):
    messages:     Annotated[list, add_messages]
    user_id:      int
    user_context: dict


# ── Helpers ───────────────────────────────────────────────────────────────────

def _db():
    from backend.database import get_db
    return next(get_db())


def _get_llm():
    from backend.agents.orchestrator import get_llm
    return get_llm()


def _llm_json(prompt: str) -> dict | list:
    """Call LLM and parse JSON response, stripping code fences if present."""
    resp = _get_llm().invoke([HumanMessage(content=prompt)])
    text = resp.content.strip()
    for fence in ("```json", "```"):
        if fence in text:
            text = text.split(fence, 1)[1].split("```", 1)[0].strip()
            break
    return json.loads(text)


def _truncate(text: str, max_chars: int = 6000) -> str:
    """Truncate course content to fit in LLM context."""
    return text[:max_chars] + "\n[... contenu tronqué ...]" if len(text) > max_chars else text


def _user_profile(user_id: int) -> dict:
    """Fetch user profile fields useful for exam context."""
    try:
        from backend.models import User, UserProfile
        db = _db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            return {
                "full_name": user.full_name if user else "",
                "major": profile.major if profile else "",
                "year": profile.year if profile else 1,
            }
        finally:
            db.close()
    except Exception:
        return {}


# ── Tools ─────────────────────────────────────────────────────────────────────

@tool
def generer_quiz(
    user_id: int,
    matiere: str,
    sujet: str,
    nb_questions: int = 5,
    difficulte: str = "moyen",
    type_questions: str = "qcm",
) -> str:
    """Génère un quiz personnalisé et le sauvegarde.
    type_questions: 'qcm' (choix multiple A/B/C/D), 'ouvert' (réponse libre),
                    'vrai_faux', 'mixte' (mélange des trois).
    difficulte: 'facile', 'moyen', 'difficile'.
    nb_questions: entre 3 et 15."""
    try:
        from backend.models import Exam
        nb_questions = max(3, min(15, int(nb_questions)))

        if type_questions == "qcm":
            schema = (
                '{"questions": [{"id": 1, "type": "qcm", "question": "...", '
                '"options": ["A. ...", "B. ...", "C. ...", "D. ..."], '
                '"reponse_correcte": "A", "explication": "...", "points": 2}]}'
            )
            rules = "- 4 options par question (A/B/C/D). reponse_correcte est la lettre uniquement."
        elif type_questions == "vrai_faux":
            schema = (
                '{"questions": [{"id": 1, "type": "vrai_faux", "question": "...", '
                '"reponse_correcte": "Vrai", "explication": "...", "points": 1}]}'
            )
            rules = "- reponse_correcte est 'Vrai' ou 'Faux' uniquement."
        elif type_questions == "ouvert":
            schema = (
                '{"questions": [{"id": 1, "type": "ouvert", "question": "...", '
                '"elements_reponse": ["point clé 1", "point clé 2"], "explication": "...", "points": 4}]}'
            )
            rules = "- elements_reponse liste les points clés attendus dans la réponse."
        else:  # mixte
            schema = (
                '{"questions": [{"id": 1, "type": "qcm|vrai_faux|ouvert", "question": "...", '
                '"options": ["A..","B..","C..","D.."] (si qcm), '
                '"reponse_correcte": "A|Vrai|null", '
                '"elements_reponse": [...] (si ouvert), '
                '"explication": "...", "points": 2}]}'
            )
            rules = "- Mélange QCM, vrai/faux et questions ouvertes. Varier les types."

        prompt = (
            f"Génère un quiz de {nb_questions} questions pour un étudiant ingénieur.\n"
            f"Matière: {matiere} | Sujet: {sujet} | Difficulté: {difficulte} | Type: {type_questions}\n\n"
            "Réponds UNIQUEMENT avec ce JSON (aucun texte avant ou après):\n"
            f"{schema}\n\n"
            "RÈGLES:\n"
            "- Questions précises et adaptées niveau ingénieur.\n"
            f"{rules}\n"
            "- Explication pédagogique de 1-2 phrases.\n"
            "- Difficulté cohérente avec le paramètre."
        )

        quiz_data = _llm_json(prompt)
        questions = quiz_data.get("questions", [])
        if not questions:
            return "Erreur: aucune question générée. Précise davantage le sujet."

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

            # Display without correct answers
            display = []
            for q in questions:
                d = {"id": q["id"], "type": q.get("type", type_questions),
                     "question": q["question"], "points": q.get("points", 2)}
                if "options" in q:
                    d["options"] = q["options"]
                if q.get("type") == "vrai_faux":
                    d["options"] = ["Vrai", "Faux"]
                display.append(d)

            return json.dumps({
                "success": True,
                "exam_id": exam.id,
                "titre": exam.title,
                "matiere": matiere,
                "sujet": sujet,
                "type": type_questions,
                "nb_questions": len(questions),
                "total_points": total_points,
                "difficulte": difficulte,
                "questions": display,
            }, ensure_ascii=False)
        finally:
            db.close()

    except json.JSONDecodeError:
        return "Erreur: format invalide. Précise le sujet."
    except Exception as e:
        logger.error("generer_quiz error: %s", e)
        return f"Erreur génération quiz: {e}"


@tool
def soumettre_reponses(exam_id: int, reponses_json: str) -> str:
    """Corrige les réponses de l'étudiant et calcule le score.
    reponses_json: JSON {\"1\": \"A\", \"2\": \"Vrai\", \"3\": \"ma réponse libre\", ...}"""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exam = db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam:
                return f"Quiz {exam_id} introuvable."
            if exam.status == "completed":
                return f"Quiz déjà corrigé. Score: {exam.score}/{exam.total_points}."

            user_answers = json.loads(reponses_json)
            questions = exam.questions or []
            score = 0
            corrections = []

            for q in questions:
                q_id = str(q.get("id", ""))
                q_type = q.get("type", "qcm")
                user_ans = str(user_answers.get(q_id, "")).strip()
                points = int(q.get("points", 2))

                if q_type in ("qcm", "vrai_faux"):
                    correct = str(q.get("reponse_correcte", "")).strip()
                    is_correct = user_ans.upper() == correct.upper()
                    pts = points if is_correct else 0
                else:
                    # Open question: partial credit via keyword matching
                    elements = [str(e).lower() for e in q.get("elements_reponse", [])]
                    ans_lower = user_ans.lower()
                    matched = sum(1 for e in elements if e in ans_lower)
                    pts = round((matched / len(elements)) * points) if elements else 0
                    is_correct = pts == points
                    correct = " | ".join(q.get("elements_reponse", []))

                score += pts
                corrections.append({
                    "question_id": q_id,
                    "question": q.get("question", ""),
                    "ta_reponse": user_ans or "—",
                    "bonne_reponse": correct,
                    "correct": is_correct,
                    "points_obtenus": pts,
                    "points_max": points,
                    "explication": q.get("explication", ""),
                })

            note = round((score / exam.total_points) * 20, 2) if exam.total_points else 0
            appreciation = (
                "Excellent !" if note >= 16 else
                "Très bien !" if note >= 14 else
                "Bien !" if note >= 12 else
                "Passable — continue à réviser." if note >= 10 else
                "À améliorer — revois les points faibles."
            )

            exam.score = score
            exam.answers = user_answers
            exam.status = "completed"
            exam.completed_at = datetime.utcnow()
            db.commit()

            return json.dumps({
                "success": True,
                "exam_id": exam_id,
                "score": score,
                "total_points": exam.total_points,
                "note_sur_20": note,
                "appreciation": appreciation,
                "bonnes_reponses": sum(1 for c in corrections if c["correct"]),
                "nb_questions": len(questions),
                "corrections": corrections,
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("soumettre_reponses error: %s", e)
        return f"Erreur correction: {e}"


@tool
def obtenir_historique_examens(user_id: int) -> str:
    """Récupère l'historique des quiz et examens passés avec leurs scores."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exams = (db.query(Exam).filter(Exam.user_id == user_id)
                     .order_by(Exam.created_at.desc()).limit(20).all())
            if not exams:
                return "Aucun examen trouvé. Lance ton premier quiz !"

            result = []
            for e in exams:
                note = round((e.score / e.total_points) * 20, 2) if e.score is not None and e.total_points else None
                result.append({
                    "id": e.id, "titre": e.title, "matiere": e.subject or "—",
                    "statut": e.status, "note_sur_20": note,
                    "score": e.score, "total": e.total_points,
                    "date": e.created_at.strftime("%d/%m/%Y") if e.created_at else "?",
                })
            return json.dumps({"examens": result, "total": len(result)}, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("obtenir_historique_examens error: %s", e)
        return f"Erreur historique: {e}"


@tool
def obtenir_statistiques_examens(user_id: int) -> str:
    """Calcule les statistiques de performance : moyenne, meilleure/pire matière, progression."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exams = db.query(Exam).filter(Exam.user_id == user_id, Exam.status == "completed").all()
            if not exams:
                return "Aucun examen complété. Génère un quiz pour commencer !"

            by_subject: dict = {}
            all_notes = []
            for e in exams:
                if e.score is None or not e.total_points:
                    continue
                note = round((e.score / e.total_points) * 20, 2)
                all_notes.append(note)
                by_subject.setdefault(e.subject or "Autre", []).append(note)

            avg_by_subj = {s: round(sum(n) / len(n), 2) for s, n in by_subject.items()}
            return json.dumps({
                "examens_completes": len(exams),
                "moyenne_generale": round(sum(all_notes) / len(all_notes), 2) if all_notes else None,
                "par_matiere": avg_by_subj,
                "meilleure_matiere": max(avg_by_subj, key=avg_by_subj.get) if avg_by_subj else None,
                "matiere_a_ameliorer": min(avg_by_subj, key=avg_by_subj.get) if avg_by_subj else None,
                "progression": "En hausse" if len(all_notes) >= 2 and all_notes[-1] > all_notes[0] else "Stable",
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("obtenir_statistiques error: %s", e)
        return f"Erreur statistiques: {e}"


@tool
def analyser_lacunes(user_id: int) -> str:
    """Identifie les matières faibles (< 12/20) et recommande les priorités de révision."""
    try:
        from backend.models import Exam
        db = _db()
        try:
            exams = db.query(Exam).filter(Exam.user_id == user_id, Exam.status == "completed").all()
            if not exams:
                return "Pas encore d'examens. Commence par générer des quiz !"

            by_subject: dict = {}
            for e in exams:
                if e.score is None or not e.total_points:
                    continue
                note = round((e.score / e.total_points) * 20, 2)
                by_subject.setdefault(e.subject or "Autre", []).append(note)

            weak, strong = [], []
            for subj, notes in by_subject.items():
                avg = round(sum(notes) / len(notes), 2)
                if avg < 12:
                    weak.append({"matiere": subj, "moyenne": avg, "quiz": len(notes)})
                else:
                    strong.append({"matiere": subj, "moyenne": avg})

            weak.sort(key=lambda x: x["moyenne"])
            return json.dumps({
                "matieres_faibles": weak,
                "matieres_fortes": strong,
                "recommandation": (
                    f"Priorité : {', '.join(w['matiere'] for w in weak[:3])}" if weak
                    else "Bonne progression ! Continue sur toutes les matières."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("analyser_lacunes error: %s", e)
        return f"Erreur analyse: {e}"


# ── Nouveau : Planning des examens ────────────────────────────────────────────

@tool
def enregistrer_planning_examen(
    user_id: int,
    matiere: str,
    date_examen: str,
    semestre: str = "",
    salle: str = "",
    coefficient: float = 1.0,
    notes: str = "",
) -> str:
    """Enregistre la date d'un examen officiel dans le planning.
    date_examen: format 'JJ/MM/AAAA' ou 'JJ/MM/AAAA HH:MM'.
    semestre: ex. 'S3', 'S4'.
    coefficient: coefficient de la matière (défaut 1.0)."""
    try:
        from backend.models import ExamSchedule
        for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(date_examen.strip(), fmt)
                break
            except ValueError:
                continue
        else:
            return "Format de date invalide. Utilise JJ/MM/AAAA ou JJ/MM/AAAA HH:MM."

        db = _db()
        try:
            entry = ExamSchedule(
                user_id=user_id, matiere=matiere, date_examen=dt,
                semestre=semestre or None, salle=salle or None,
                coefficient=coefficient, notes=notes or None,
            )
            db.add(entry)
            db.commit()
            db.refresh(entry)
            days_left = (dt - datetime.utcnow()).days
            return json.dumps({
                "success": True,
                "id": entry.id,
                "matiere": matiere,
                "date": dt.strftime("%d/%m/%Y %H:%M"),
                "jours_restants": max(0, days_left),
                "message": f"Examen '{matiere}' enregistré — dans {max(0, days_left)} jour(s).",
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("enregistrer_planning error: %s", e)
        return f"Erreur enregistrement: {e}"


@tool
def obtenir_planning_examens(user_id: int) -> str:
    """Récupère le planning complet des examens à venir, triés par date, avec les jours restants."""
    try:
        from backend.models import ExamSchedule
        db = _db()
        try:
            now = datetime.utcnow()
            exams = (db.query(ExamSchedule)
                     .filter(ExamSchedule.user_id == user_id, ExamSchedule.date_examen >= now)
                     .order_by(ExamSchedule.date_examen).all())
            past = (db.query(ExamSchedule)
                    .filter(ExamSchedule.user_id == user_id, ExamSchedule.date_examen < now)
                    .order_by(ExamSchedule.date_examen.desc()).limit(5).all())

            def fmt(e):
                days = max(0, (e.date_examen - now).days)
                return {
                    "id": e.id, "matiere": e.matiere,
                    "date": e.date_examen.strftime("%d/%m/%Y %H:%M"),
                    "semestre": e.semestre or "", "salle": e.salle or "",
                    "coefficient": e.coefficient, "jours_restants": days,
                    "urgence": "URGENT" if days <= 3 else "Proche" if days <= 7 else "Normal",
                }

            return json.dumps({
                "examens_a_venir": [fmt(e) for e in exams],
                "examens_passes": [fmt(e) for e in past],
                "prochain": fmt(exams[0]) if exams else None,
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("obtenir_planning error: %s", e)
        return f"Erreur planning: {e}"


# ── Nouveau : Analyse de cours PDF ────────────────────────────────────────────

@tool
def analyser_document_cours(
    user_id: int,
    matiere: str,
    contenu_texte: str,
    titre: str = "",
) -> str:
    """Stocke le contenu d'un cours (texte extrait d'un PDF) et génère automatiquement
    un résumé structuré + les notions clés importantes.
    contenu_texte: texte brut du cours (copié depuis le PDF ou extrait automatiquement).
    titre: titre du document/chapitre (optionnel)."""
    try:
        from backend.models import CourseDocument

        content_trunc = _truncate(contenu_texte, 6000)

        # Generate summary + key concepts in one LLM call
        prompt = (
            f"Tu es un expert pédagogique. Analyse ce cours de '{matiere}' pour un étudiant ingénieur.\n\n"
            f"--- CONTENU DU COURS ---\n{content_trunc}\n--- FIN ---\n\n"
            "Réponds UNIQUEMENT avec ce JSON:\n"
            '{"resume": "résumé structuré en markdown (titres, points clés, formules importantes) — 300-500 mots", '
            '"notions_cles": ["notion 1", "notion 2", ...], '
            '"points_examen": ["point susceptible d\'apparaître à l\'examen 1", ...], '
            '"prerequis": ["prérequis 1", ...]}'
        )

        data = _llm_json(prompt)

        db = _db()
        try:
            # Check if document for this matiere already exists
            existing = (db.query(CourseDocument)
                        .filter(CourseDocument.user_id == user_id,
                                CourseDocument.matiere == matiere)
                        .first())
            if existing:
                existing.contenu = contenu_texte
                existing.titre = titre or existing.titre
                existing.resume = data.get("resume", "")
                existing.notions_cles = {
                    "notions": data.get("notions_cles", []),
                    "points_examen": data.get("points_examen", []),
                    "prerequis": data.get("prerequis", []),
                }
                existing.updated_at = datetime.utcnow()
                doc_id = existing.id
            else:
                doc = CourseDocument(
                    user_id=user_id,
                    matiere=matiere,
                    titre=titre or f"Cours — {matiere}",
                    contenu=contenu_texte,
                    resume=data.get("resume", ""),
                    notions_cles={
                        "notions": data.get("notions_cles", []),
                        "points_examen": data.get("points_examen", []),
                        "prerequis": data.get("prerequis", []),
                    },
                )
                db.add(doc)
                db_commit = db.commit
                db_commit()
                db.refresh(doc)
                doc_id = doc.id
            db.commit()

            return json.dumps({
                "success": True,
                "doc_id": doc_id,
                "matiere": matiere,
                "resume": data.get("resume", ""),
                "notions_cles": data.get("notions_cles", []),
                "points_examen": data.get("points_examen", []),
                "nb_notions": len(data.get("notions_cles", [])),
            }, ensure_ascii=False)
        finally:
            db.close()

    except json.JSONDecodeError:
        return "Erreur: impossible d'analyser le contenu. Vérifie que le texte est lisible."
    except Exception as e:
        logger.error("analyser_document_cours error: %s", e)
        return f"Erreur analyse: {e}"


@tool
def generer_resume_cours(user_id: int, matiere: str) -> str:
    """Génère ou récupère le résumé structuré du cours enregistré pour une matière.
    Inclut : plan du cours, formules clés, définitions importantes."""
    try:
        from backend.models import CourseDocument
        db = _db()
        try:
            doc = (db.query(CourseDocument)
                   .filter(CourseDocument.user_id == user_id,
                           CourseDocument.matiere == matiere).first())
            if not doc:
                return f"Aucun cours enregistré pour '{matiere}'. Utilise analyser_document_cours d'abord."

            if doc.resume:
                return json.dumps({
                    "matiere": matiere,
                    "titre": doc.titre,
                    "resume": doc.resume,
                    "notions_cles": (doc.notions_cles or {}).get("notions", []),
                    "points_examen": (doc.notions_cles or {}).get("points_examen", []),
                    "date_import": doc.updated_at.strftime("%d/%m/%Y") if doc.updated_at else "?",
                }, ensure_ascii=False)

            # Re-generate if missing
            content_trunc = _truncate(doc.contenu, 6000)
            prompt = (
                f"Génère un résumé structuré du cours '{matiere}' pour révision d'examen.\n\n"
                f"--- COURS ---\n{content_trunc}\n--- FIN ---\n\n"
                "Format markdown avec : ## Chapitres, **définitions**, formules en blocs code.\n"
                "Sois complet et pédagogique (400-600 mots)."
            )
            resp = _get_llm().invoke([HumanMessage(content=prompt)])
            resume = resp.content.strip()
            doc.resume = resume
            db.commit()
            return json.dumps({"matiere": matiere, "resume": resume}, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("generer_resume error: %s", e)
        return f"Erreur résumé: {e}"


@tool
def identifier_notions_cles(user_id: int, matiere: str) -> str:
    """Identifie les notions importantes et les points susceptibles d'apparaître à l'examen
    à partir du cours enregistré pour cette matière."""
    try:
        from backend.models import CourseDocument
        db = _db()
        try:
            doc = (db.query(CourseDocument)
                   .filter(CourseDocument.user_id == user_id,
                           CourseDocument.matiere == matiere).first())
            if not doc:
                return f"Cours '{matiere}' introuvable. Importe d'abord ton cours."

            stored = doc.notions_cles or {}
            notions = stored.get("notions", [])
            points_exam = stored.get("points_examen", [])

            if notions and points_exam:
                return json.dumps({
                    "matiere": matiere,
                    "notions_importantes": notions,
                    "points_probables_examen": points_exam,
                    "prerequis": stored.get("prerequis", []),
                    "nb_notions": len(notions),
                }, ensure_ascii=False)

            # Generate if missing
            content_trunc = _truncate(doc.contenu, 5000)
            prompt = (
                f"Analyse ce cours de '{matiere}' et identifie :\n\n"
                f"--- COURS ---\n{content_trunc}\n--- FIN ---\n\n"
                "Réponds UNIQUEMENT avec ce JSON:\n"
                '{"notions_importantes": ["notion 1 avec définition courte", ...],'
                ' "points_probables_examen": ["ce qui risque d\'apparaître à l\'exam 1", ...],'
                ' "formules_cles": ["formule ou algorithme clé 1", ...],'
                ' "pieges_frequents": ["erreur classique à éviter 1", ...]}'
            )
            data = _llm_json(prompt)
            doc.notions_cles = {
                "notions": data.get("notions_importantes", []),
                "points_examen": data.get("points_probables_examen", []),
                "formules": data.get("formules_cles", []),
                "pieges": data.get("pieges_frequents", []),
            }
            db.commit()
            return json.dumps({
                "matiere": matiere,
                "notions_importantes": data.get("notions_importantes", []),
                "points_probables_examen": data.get("points_probables_examen", []),
                "formules_cles": data.get("formules_cles", []),
                "pieges_frequents": data.get("pieges_frequents", []),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("identifier_notions error: %s", e)
        return f"Erreur notions: {e}"


@tool
def generer_questions_revision(
    user_id: int,
    matiere: str,
    type_questions: str = "mixte",
    nb_questions: int = 8,
    difficulte: str = "moyen",
) -> str:
    """Génère des questions de révision basées sur le contenu du cours importé.
    type_questions: 'qcm', 'ouvert', 'vrai_faux', 'exercice', 'mixte'.
    Les questions sont directement tirées du cours pour une révision ciblée."""
    try:
        from backend.models import CourseDocument, Exam
        db = _db()
        try:
            doc = (db.query(CourseDocument)
                   .filter(CourseDocument.user_id == user_id,
                           CourseDocument.matiere == matiere).first())
            if not doc:
                return f"Cours '{matiere}' non trouvé. Importe d'abord ton cours."

            nb_questions = max(3, min(15, int(nb_questions)))
            content_trunc = _truncate(doc.contenu, 5000)

            if type_questions == "exercice":
                schema = (
                    '{"questions": [{"id": 1, "type": "exercice", '
                    '"enonce": "énoncé complet de l\'exercice avec données", '
                    '"etapes": ["étape 1", "étape 2"], '
                    '"solution": "solution détaillée avec calculs", "points": 5}]}'
                )
            elif type_questions == "ouvert":
                schema = (
                    '{"questions": [{"id": 1, "type": "ouvert", '
                    '"question": "...", "elements_reponse": ["point attendu 1", ...], '
                    '"explication": "...", "points": 4}]}'
                )
            elif type_questions == "qcm":
                schema = (
                    '{"questions": [{"id": 1, "type": "qcm", "question": "...", '
                    '"options": ["A. ...", "B. ...", "C. ...", "D. ..."], '
                    '"reponse_correcte": "A", "explication": "...", "points": 2}]}'
                )
            else:  # mixte ou vrai_faux
                schema = (
                    '{"questions": [{"id": 1, "type": "qcm|ouvert|exercice|vrai_faux", '
                    '"question": "...", "options": [...] (si qcm), '
                    '"reponse_correcte": "A|Vrai|null", '
                    '"elements_reponse": [...] (si ouvert), '
                    '"enonce": "..." (si exercice), "solution": "..." (si exercice), '
                    '"explication": "...", "points": 2}]}'
                )

            prompt = (
                f"Génère {nb_questions} questions de révision BASÉES DIRECTEMENT sur ce cours.\n"
                f"Matière: {matiere} | Type: {type_questions} | Difficulté: {difficulte}\n\n"
                f"--- COURS ---\n{content_trunc}\n--- FIN ---\n\n"
                "IMPORTANT: Les questions doivent provenir DIRECTEMENT du contenu du cours.\n"
                "Réponds UNIQUEMENT avec ce JSON:\n"
                f"{schema}"
            )

            data = _llm_json(prompt)
            questions = data.get("questions", [])
            if not questions:
                return "Erreur: aucune question générée."

            total_points = sum(q.get("points", 2) for q in questions)
            exam = Exam(
                user_id=user_id,
                title=f"Questions révision — {matiere}",
                subject=matiere,
                questions=questions,
                total_points=total_points,
                status="in_progress",
                started_at=datetime.utcnow(),
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)

            # Strip answers for display
            display = []
            for q in questions:
                d = {"id": q["id"], "type": q.get("type", type_questions),
                     "question": q.get("question") or q.get("enonce", ""),
                     "points": q.get("points", 2)}
                if "options" in q:
                    d["options"] = q["options"]
                if q.get("type") == "exercice":
                    d["enonce"] = q.get("enonce", "")
                    d["etapes"] = q.get("etapes", [])
                display.append(d)

            return json.dumps({
                "success": True,
                "exam_id": exam.id,
                "matiere": matiere,
                "type": type_questions,
                "nb_questions": len(questions),
                "total_points": total_points,
                "questions": display,
                "source": "cours importé",
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("generer_questions_revision error: %s", e)
        return f"Erreur génération: {e}"


@tool
def generer_examen_blanc(
    user_id: int,
    matiere: str,
    duree_minutes: int = 90,
    nb_questions: int = 20,
) -> str:
    """Génère un examen blanc complet basé sur le cours importé.
    Inclut QCM, questions ouvertes et exercices, répartis selon la durée.
    L'examen est calibré pour simuler les conditions réelles."""
    try:
        from backend.models import CourseDocument, Exam
        db = _db()
        try:
            doc = (db.query(CourseDocument)
                   .filter(CourseDocument.user_id == user_id,
                           CourseDocument.matiere == matiere).first())
            if not doc:
                return f"Cours '{matiere}' non trouvé. Importe ton cours d'abord."

            nb_questions = max(5, min(30, int(nb_questions)))
            content_trunc = _truncate(doc.contenu, 5000)
            notions = (doc.notions_cles or {}).get("notions", [])

            prompt = (
                f"Génère un examen blanc complet de '{matiere}' (durée: {duree_minutes} min).\n"
                f"Nombre de questions: {nb_questions} — mélange QCM + questions ouvertes + exercices.\n"
                f"Notions importantes à couvrir: {', '.join(notions[:10]) if notions else 'selon le cours'}\n\n"
                f"--- COURS ---\n{content_trunc}\n--- FIN ---\n\n"
                "Réponds UNIQUEMENT avec ce JSON:\n"
                '{"titre_examen": "Examen Blanc — Matière", '
                '"duree_minutes": 90, '
                '"instructions": "instructions générales pour l\'étudiant", '
                '"sections": ['
                '  {"titre": "Partie I — QCM (X points)", "questions": ['
                '    {"id": 1, "type": "qcm", "question": "...", '
                '     "options": ["A...","B...","C...","D..."], '
                '     "reponse_correcte": "A", "explication": "...", "points": 2}'
                '  ]},'
                '  {"titre": "Partie II — Questions ouvertes (X points)", "questions": ['
                '    {"id": N, "type": "ouvert", "question": "...", '
                '     "elements_reponse": ["..."], "explication": "...", "points": 5}'
                '  ]},'
                '  {"titre": "Partie III — Exercice (X points)", "questions": ['
                '    {"id": N, "type": "exercice", "enonce": "...", '
                '     "etapes": ["..."], "solution": "...", "points": 8}'
                '  ]}'
                ']}'
            )

            data = _llm_json(prompt)
            sections = data.get("sections", [])
            all_questions = []
            for sec in sections:
                all_questions.extend(sec.get("questions", []))

            if not all_questions:
                return "Erreur: examen blanc non généré correctement."

            total_points = sum(q.get("points", 2) for q in all_questions)
            exam = Exam(
                user_id=user_id,
                title=data.get("titre_examen", f"Examen Blanc — {matiere}"),
                subject=matiere,
                questions=all_questions,
                total_points=total_points,
                status="in_progress",
                started_at=datetime.utcnow(),
            )
            db.add(exam)
            db.commit()
            db.refresh(exam)

            # Build display (no answers)
            display_sections = []
            for sec in sections:
                disp_qs = []
                for q in sec.get("questions", []):
                    d = {"id": q["id"], "type": q.get("type"),
                         "question": q.get("question") or q.get("enonce", ""),
                         "points": q.get("points", 2)}
                    if "options" in q:
                        d["options"] = q["options"]
                    if q.get("type") == "exercice":
                        d["enonce"] = q.get("enonce", "")
                        d["etapes"] = q.get("etapes", [])
                    disp_qs.append(d)
                display_sections.append({"titre": sec["titre"], "questions": disp_qs})

            return json.dumps({
                "success": True,
                "exam_id": exam.id,
                "titre": exam.title,
                "matiere": matiere,
                "duree_minutes": duree_minutes,
                "instructions": data.get("instructions", ""),
                "nb_questions": len(all_questions),
                "total_points": total_points,
                "sections": display_sections,
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("generer_examen_blanc error: %s", e)
        return f"Erreur examen blanc: {e}"


@tool
def chercher_planning_officiel(
    module_query: str = "",
    filiere: str = "",
    semestre: str = "",
    annee: int = 0,
) -> str:
    """Consulte le planning officiel des examens (ENIAD Berkane).
    IMPORTANT : fournir TOUJOURS annee = année d'étude de l'étudiant (1-4).
    L'outil filtre automatiquement pour ne retourner QUE le planning de cette année.
    Ne jamais afficher de plannings d'autres années.
    module_query: rechercher un module précis par nom.
    filiere: 'Génie Informatique', 'Intelligence Artificielle', 'IRSI', 'ROC', 'EPSI'...
    semestre: 'S1','S2','S5','S6','S7','S8' (optionnel si annee fourni).
    annee: 1=S1/S2, 2=S3/S4, 3=S5/S6, 4=S7/S8."""
    try:
        from backend.data.planning_examens import (
            get_planning_for_filiere, get_planning_for_year,
            search_module_in_planning, FILIERES_INFO,
            SESSION_HIVER, SESSION_PRINTEMPS, YEAR_TO_SEMESTERS,
        )

        target_sems: set[str] = set(YEAR_TO_SEMESTERS.get(annee, [])) if annee > 0 else set()

        # ── Search by module name ─────────────────────────────────────────────
        if module_query:
            results = search_module_in_planning(module_query)
            if annee > 0:
                results = [r for r in results if r.get("semestre") in target_sems]
            if not results:
                msg = f"Aucun module correspondant à '{module_query}'"
                if annee > 0:
                    sems = YEAR_TO_SEMESTERS.get(annee, [])
                    msg += f" pour la {annee}ème année ({'/'.join(sems)})"
                msg += " dans le planning officiel."
                return json.dumps({"found": False, "query": module_query, "message": msg}, ensure_ascii=False)
            return json.dumps({
                "found": True,
                "query": module_query,
                "annee_filtre": annee if annee > 0 else "toutes",
                "results": results,
            }, ensure_ascii=False)

        # ── Year + filière (+ optional semestre) → filtered planning ────────
        if annee > 0 and filiere:
            if semestre:
                # Show only the specified semester
                result = get_planning_for_filiere(filiere, semestre)
                if not result:
                    return json.dumps({
                        "found": False,
                        "annee": annee,
                        "filiere": filiere,
                        "semestre": semestre,
                        "message": f"Aucun planning disponible pour {filiere} en {semestre}.",
                    }, ensure_ascii=False)
                return json.dumps({"found": True, "annee": annee, "semestre": semestre, "plannings": [result]}, ensure_ascii=False)
            else:
                plans = get_planning_for_year(annee, filiere)
                if not plans:
                    sems = YEAR_TO_SEMESTERS.get(annee, [])
                    return json.dumps({
                        "found": False,
                        "annee": annee,
                        "filiere": filiere,
                        "semesters_attendus": sems,
                        "message": (
                            f"Aucun planning disponible pour {filiere} "
                            f"en {annee}ème année ({'/'.join(sems)}). "
                            "Vérifie l'orthographe de la filière."
                        ),
                    }, ensure_ascii=False)
                return json.dumps({"found": True, "annee": annee, "plannings": plans}, ensure_ascii=False)

        # ── Year only → list available plannings for that year ────────────────
        if annee > 0:
            sems = YEAR_TO_SEMESTERS.get(annee, [])
            available = [
                {"cle": k, "nom": v[0], "semestre": v[1], "session": v[2]}
                for k, v in FILIERES_INFO.items() if v[1] in target_sems
            ]
            return json.dumps({
                "annee": annee,
                "semesters": sems,
                "plannings_disponibles": available,
                "message": f"Pour la {annee}ème année ({'/'.join(sems)}), précise ta filière.",
            }, ensure_ascii=False)

        # ── Filière without year ──────────────────────────────────────────────
        if filiere:
            result = get_planning_for_filiere(filiere, semestre or None)
            if not result:
                return json.dumps({
                    "found": False,
                    "filiere": filiere,
                    "available": [
                        {"cle": k, "nom": v[0], "semestre": v[1], "session": v[2]}
                        for k, v in FILIERES_INFO.items()
                    ],
                    "message": "Filière non trouvée. Précise aussi ton année d'étude.",
                }, ensure_ascii=False)
            return json.dumps({"found": True, **result}, ensure_ascii=False)

        # ── No params → list all ──────────────────────────────────────────────
        return json.dumps({
            "message": "Précise ton année d'étude et ta filière pour consulter le planning.",
            "filieres_disponibles": [
                {"cle": k, "nom": v[0], "semestre": v[1], "session": v[2]}
                for k, v in FILIERES_INFO.items()
            ],
        }, ensure_ascii=False)

    except Exception as e:
        logger.error("chercher_planning_officiel error: %s", e)
        return f"Erreur planning officiel: {e}"


@tool
def generer_planning_revision(user_id: int) -> str:
    """Génère un planning de révision personnalisé basé sur :
    - Les dates d'examen enregistrées (urgence)
    - Les matières faibles identifiées dans l'historique (priorité)
    - Les cours importés disponibles
    Retourne un planning jour par jour jusqu'au premier examen."""
    try:
        from backend.models import ExamSchedule, Exam, CourseDocument
        db = _db()
        try:
            now = datetime.utcnow()

            # Get upcoming exams
            exams_schedule = (db.query(ExamSchedule)
                              .filter(ExamSchedule.user_id == user_id,
                                      ExamSchedule.date_examen >= now)
                              .order_by(ExamSchedule.date_examen).all())

            # Get weak subjects from history
            completed = (db.query(Exam)
                         .filter(Exam.user_id == user_id, Exam.status == "completed").all())
            by_subject: dict = {}
            for e in completed:
                if e.score is not None and e.total_points:
                    note = (e.score / e.total_points) * 20
                    by_subject.setdefault(e.subject or "Autre", []).append(note)
            avg_by_subj = {s: sum(n) / len(n) for s, n in by_subject.items()}

            # Get available course documents
            docs = db.query(CourseDocument).filter(CourseDocument.user_id == user_id).all()
            has_docs = {d.matiere for d in docs}

            # Profile
            profile = _user_profile(user_id)

            if not exams_schedule:
                # No exams scheduled: build generic plan from weak subjects
                context = f"L'étudiant n'a pas d'examens planifiés.\n"
                context += f"Matières avec scores: {json.dumps(avg_by_subj)}\n"
                context += f"Cours importés: {', '.join(has_docs) or 'aucun'}"
            else:
                context_parts = [f"Planning des examens à venir:"]
                for es in exams_schedule[:6]:
                    days = max(0, (es.date_examen - now).days)
                    context_parts.append(
                        f"- {es.matiere}: dans {days} jours "
                        f"(coefficient {es.coefficient}, salle {es.salle or '?'})"
                    )
                context = "\n".join(context_parts)
                context += f"\n\nPerformances par matière: {json.dumps({k: round(v, 1) for k, v in avg_by_subj.items()})}"
                context += f"\nCours importés disponibles: {', '.join(has_docs) or 'aucun'}"

            prompt = (
                f"Tu es un coach académique. Génère un planning de révision personnalisé.\n"
                f"Étudiant: {profile.get('full_name', 'Étudiant')} | "
                f"Filière: {profile.get('major', '—')} | Année: {profile.get('year', 1)}\n\n"
                f"{context}\n\n"
                "Génère un planning RÉALISTE sur les prochains jours. Priorité aux matières faibles et urgentes.\n"
                "Réponds UNIQUEMENT avec ce JSON:\n"
                '{"horizon_jours": 14, '
                '"strategie": "explication courte de la stratégie", '
                '"planning": ['
                '  {"jour": "Lundi 23/06", "date": "2026-06-23", '
                '   "sessions": ['
                '     {"matiere": "...", "duree_h": 2, "activite": "Révision chapitre X / Quiz / Exercices", '
                '      "priorite": "haute|moyenne|faible", "ressource": "cours importé|quiz SmartStudent|manuel"}'
                '   ]}'
                '], '
                '"conseils": ["conseil 1", "conseil 2", ...]}'
            )

            data = _llm_json(prompt)

            return json.dumps({
                "success": True,
                "horizon_jours": data.get("horizon_jours", 14),
                "strategie": data.get("strategie", ""),
                "planning": data.get("planning", []),
                "conseils": data.get("conseils", []),
                "examens_couverts": len(exams_schedule),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("generer_planning_revision error: %s", e)
        return f"Erreur planning révision: {e}"


# ── Tool list ─────────────────────────────────────────────────────────────────

_TOOLS = [
    # Quiz & correction
    generer_quiz,
    soumettre_reponses,
    # Historique & stats
    obtenir_historique_examens,
    obtenir_statistiques_examens,
    analyser_lacunes,
    # Planning des examens
    enregistrer_planning_examen,
    obtenir_planning_examens,
    chercher_planning_officiel,
    # Analyse de cours
    analyser_document_cours,
    generer_resume_cours,
    identifier_notions_cles,
    # Génération avancée
    generer_questions_revision,
    generer_examen_blanc,
    generer_planning_revision,
]


# ── Agent Node ────────────────────────────────────────────────────────────────

async def agent_node(state: ExamsAgentState) -> dict:
    user_id = state.get("user_id", 0)
    ctx = state.get("user_context") or {}
    nom = ctx.get("full_name") or ctx.get("username") or "l'étudiant"
    filiere = ctx.get("major") or "filière non renseignée"
    annee = ctx.get("year") or "?"
    semestre_selectionne = ctx.get("semestre") or ""

    # Build planning tool call based on selected semester
    if semestre_selectionne:
        planning_call = f"chercher_planning_officiel(annee={annee}, filiere='{filiere}', semestre='{semestre_selectionne}')"
        module_call   = f"chercher_planning_officiel(annee={annee}, module_query='X', semestre='{semestre_selectionne}')"
        sem_info      = f"Semestre sélectionné dans Modules : **{semestre_selectionne}**"
    else:
        planning_call = f"chercher_planning_officiel(annee={annee}, filiere='{filiere}')"
        module_call   = f"chercher_planning_officiel(annee={annee}, module_query='X')"
        sem_info      = f"Année: {annee}"

    system_prompt = (
        f"Tu es l'Agent Examens de SmartStudent — ENIAD Berkane.\n"
        f"Tu parles à {nom} | Filière: {filiere} | {sem_info} | ID: {user_id}.\n\n"

        "══════════════════════════════════════════════════════════\n"
        "CAPACITÉS PRINCIPALES\n"
        "══════════════════════════════════════════════════════════\n"
        "1. QUIZ & ENTRAÎNEMENT\n"
        f"   • generer_quiz(user_id={user_id}, matiere=..., sujet=..., nb_questions=..., difficulte=..., type_questions='qcm|ouvert|vrai_faux|mixte')\n"
        f"   • soumettre_reponses(exam_id=..., reponses_json='{{\"1\":\"A\",\"2\":\"Vrai\"}}')\n\n"

        "2. HISTORIQUE & PERFORMANCE\n"
        f"   • obtenir_historique_examens(user_id={user_id})\n"
        f"   • obtenir_statistiques_examens(user_id={user_id})\n"
        f"   • analyser_lacunes(user_id={user_id})\n\n"

        "3. PLANNING DES EXAMENS\n"
        f"   • enregistrer_planning_examen(user_id={user_id}, matiere=..., date_examen='JJ/MM/AAAA', semestre=..., coefficient=...)\n"
        f"   • obtenir_planning_examens(user_id={user_id})\n"
        f"   • {planning_call} → planning officiel du semestre actuel\n"
        f"     ou {module_call.replace('X', 'nom du module')}\n\n"

        "4. ANALYSE DE COURS PDF\n"
        f"   • analyser_document_cours(user_id={user_id}, matiere=..., contenu_texte=..., titre=...)\n"
        f"     → Stocke le cours et génère automatiquement résumé + notions clés\n"
        f"   • generer_resume_cours(user_id={user_id}, matiere=...)\n"
        f"   • identifier_notions_cles(user_id={user_id}, matiere=...)\n\n"

        "5. GÉNÉRATION AVANCÉE\n"
        f"   • generer_questions_revision(user_id={user_id}, matiere=..., type_questions=..., nb_questions=..., difficulte=...)\n"
        f"     → Questions tirées DIRECTEMENT du cours importé\n"
        f"   • generer_examen_blanc(user_id={user_id}, matiere=..., duree_minutes=90, nb_questions=20)\n"
        f"     → Examen complet multi-parties (QCM + ouvert + exercice)\n"
        f"   • generer_planning_revision(user_id={user_id})\n"
        f"     → Planning jour par jour basé sur examens planifiés + lacunes\n\n"

        "══════════════════════════════════════════════════════════\n"
        "COMPORTEMENT\n"
        "══════════════════════════════════════════════════════════\n"
        + (
            f"• RÈGLE ABSOLUE : l'étudiant a sélectionné le semestre {semestre_selectionne}.\n"
            f"  Utilise TOUJOURS semestre='{semestre_selectionne}' dans chercher_planning_officiel.\n"
            f"  N'affiche JAMAIS le planning d'un autre semestre.\n"
            if semestre_selectionne else
            f"• RÈGLE ABSOLUE : chercher_planning_officiel doit TOUJOURS inclure annee={annee}.\n"
            f"  Ne jamais omettre ce paramètre. Ne jamais afficher de planning d'une autre année.\n"
        ) +
        f"• Quand l'étudiant demande 'quand est mon examen de X' → {module_call.replace('X', 'X')}\n"
        f"• Quand l'étudiant demande son planning → {planning_call}\n"
        f"• Quand l'étudiant demande un quiz → utilise d'abord {planning_call}\n"
        f"  pour identifier les modules, puis génère le quiz sur l'un de ces modules.\n"
        f"  Précise toujours 'Cet examen est prévu [jour] [créneau] salle [salle]'.\n"
        "• Si l'étudiant envoie du texte de cours → analyser_document_cours automatiquement\n"
        "• Après un quiz → attendre les réponses avant de corriger\n"
        "• Adapter la difficulté : consulte analyser_lacunes pour les matières faibles\n"
        "• Pour un planning de révision → obtenir_planning_examens + analyser_lacunes d'abord\n"
        "• Commente les résultats de façon encourageante et pédagogique\n"
        "• Réponds en français, sois concis et structuré."
    )

    try:
        llm = _get_llm().bind_tools(_TOOLS)
        messages = [SystemMessage(content=system_prompt)] + list(state.get("messages", []))
        resp = await llm.ainvoke(messages)
        return {"messages": [resp]}
    except Exception as e:
        logger.error("exams agent_node error: %s", e)
        return {"messages": [AIMessage(content="Service temporairement indisponible. Réessaie dans quelques instants.")]}


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
            return {"response": "Service IA temporairement indisponible. Réessaie."}
        last_ai = next(
            (m for m in reversed(result.get("messages", [])) if isinstance(m, AIMessage)),
            None,
        )
        return {"response": str(last_ai.content) if last_ai else "Erreur interne."}


def get_exams_agent() -> ExamsAgent:
    return ExamsAgent()
