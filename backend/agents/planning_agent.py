"""
Agent Planning — SmartStudent LangGraph ReAct Agent
Architecture: agent_node <-> tools_node loop (ReAct pattern)
Outils: lister_taches, creer_tache, modifier_statut_tache,
        supprimer_tache, generer_plan_etude
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

logger = logging.getLogger(__name__)


# ── State ────────────────────────────────────────────────────────────────────

class PlanningAgentState(TypedDict, total=False):
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


def _parse_date(date_str: str) -> Optional[datetime]:
    """Parse ISO date string or relative expressions like 'dans 3 jours'."""
    if not date_str:
        return None
    date_str = date_str.strip().lower()
    if "dans" in date_str:
        import re
        m = re.search(r"(\d+)\s*(jour|semaine|mois)", date_str)
        if m:
            n, unit = int(m.group(1)), m.group(2)
            if "semaine" in unit:
                return datetime.utcnow() + timedelta(weeks=n)
            if "mois" in unit:
                return datetime.utcnow() + timedelta(days=n * 30)
            return datetime.utcnow() + timedelta(days=n)
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


# ── Tools ────────────────────────────────────────────────────────────────────

@tool
def lister_taches(user_id: int) -> str:
    """Liste toutes les tâches et deadlines de l'étudiant depuis la base de données,
    triées par date d'échéance. Inclut le statut (en attente, en cours, terminé)."""
    try:
        from backend.models import Plan
        db = _db()
        try:
            plans = (
                db.query(Plan)
                .filter(Plan.user_id == user_id)
                .order_by(Plan.due_date.asc())
                .all()
            )
            if not plans:
                return "Aucune tâche trouvée pour cet étudiant."

            STATUS_FR = {"pending": "En attente", "in_progress": "En cours", "completed": "Terminé"}
            CAT_FR = {"study": "Révision", "project": "Projet", "personal": "Personnel"}
            result = [
                {
                    "id": p.id,
                    "titre": p.title,
                    "description": p.description or "",
                    "categorie": CAT_FR.get(p.category, p.category),
                    "echeance": p.due_date.strftime("%d/%m/%Y") if p.due_date else "?",
                    "priorite": p.priority,
                    "statut": STATUS_FR.get(p.status, p.status),
                }
                for p in plans
            ]
            return json.dumps({"taches": result, "total": len(result)}, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("lister_taches error: %s", e)
        return f"Erreur lors de la récupération des tâches: {e}"


@tool
def creer_tache(
    user_id: int,
    titre: str,
    description: str,
    categorie: str,
    date_echeance: str,
    priorite: int = 3,
) -> str:
    """Crée une nouvelle tâche ou deadline pour l'étudiant dans la base de données.
    categorie: 'study' (révision), 'project' (projet), 'personal' (personnel).
    date_echeance: format ISO YYYY-MM-DD ou relatif ('dans 3 jours', 'dans 2 semaines').
    priorite: 1 (basse) à 5 (urgente)."""
    try:
        from backend.models import Plan
        db = _db()
        try:
            due = _parse_date(date_echeance) or (datetime.utcnow() + timedelta(days=7))
            cat_map = {
                "study": "study", "revision": "study", "révision": "study",
                "projet": "project", "project": "project",
                "personnel": "personal", "personal": "personal",
            }
            cat = cat_map.get(categorie.lower(), "study")
            plan = Plan(
                user_id=user_id,
                title=titre[:200],
                description=description[:500] if description else None,
                category=cat,
                due_date=due,
                priority=max(1, min(5, int(priorite))),
                status="pending",
            )
            db.add(plan)
            db.commit()
            db.refresh(plan)
            return json.dumps({
                "success": True,
                "id": plan.id,
                "titre": plan.title,
                "echeance": plan.due_date.strftime("%d/%m/%Y"),
                "message": f"Tâche '{plan.title}' créée pour le {plan.due_date.strftime('%d/%m/%Y')}.",
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("creer_tache error: %s", e)
        return f"Erreur lors de la création de la tâche: {e}"


@tool
def modifier_statut_tache(tache_id: int, nouveau_statut: str) -> str:
    """Met à jour le statut d'une tâche existante.
    nouveau_statut: 'pending' (en attente), 'in_progress' (en cours), 'completed' (terminé)."""
    try:
        from backend.models import Plan
        db = _db()
        try:
            plan = db.query(Plan).filter(Plan.id == tache_id).first()
            if not plan:
                return f"Aucune tâche trouvée avec l'ID {tache_id}."
            status_map = {
                "en attente": "pending", "attente": "pending",
                "en cours": "in_progress", "cours": "in_progress",
                "terminé": "completed", "termine": "completed", "fait": "completed", "done": "completed",
            }
            status = status_map.get(nouveau_statut.lower(), nouveau_statut.lower())
            if status not in {"pending", "in_progress", "completed"}:
                status = "in_progress"
            plan.status = status
            plan.updated_at = datetime.utcnow()
            db.commit()
            STATUS_FR = {"pending": "En attente", "in_progress": "En cours", "completed": "Terminé"}
            return json.dumps({
                "success": True,
                "id": tache_id,
                "titre": plan.title,
                "nouveau_statut": STATUS_FR.get(status, status),
                "message": f"Tâche '{plan.title}' → {STATUS_FR.get(status, status)}.",
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("modifier_statut_tache error: %s", e)
        return f"Erreur lors de la modification: {e}"


@tool
def supprimer_tache(tache_id: int) -> str:
    """Supprime définitivement une tâche de la liste de l'étudiant."""
    try:
        from backend.models import Plan
        db = _db()
        try:
            plan = db.query(Plan).filter(Plan.id == tache_id).first()
            if not plan:
                return f"Aucune tâche trouvée avec l'ID {tache_id}."
            titre = plan.title
            db.delete(plan)
            db.commit()
            return json.dumps({"success": True, "message": f"Tâche '{titre}' supprimée."}, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error("supprimer_tache error: %s", e)
        return f"Erreur lors de la suppression: {e}"


@tool
def generer_plan_etude(
    user_id: int,
    matieres: str,
    date_examen: str,
    heures_par_jour: int = 3,
) -> str:
    """Génère un plan de révision structuré et le sauvegarde comme tâches dans la base de données.
    matieres: liste des matières séparées par des virgules (ex: 'Machine Learning, Algorithmique, BDD').
    date_examen: date de l'examen format YYYY-MM-DD ou relatif ('dans 2 semaines').
    heures_par_jour: nombre d'heures de révision quotidiennes disponibles."""
    try:
        from langchain_core.messages import HumanMessage as HM
        from backend.models import Plan

        exam_date = _parse_date(date_examen) or (datetime.utcnow() + timedelta(days=14))
        days_left = max(1, (exam_date - datetime.utcnow()).days)

        prompt = (
            f"Génère un plan de révision structuré en JSON pour un étudiant ingénieur.\n"
            f"Matières: {matieres}\n"
            f"Jours jusqu'à l'examen: {days_left}\n"
            f"Heures par jour: {heures_par_jour}h\n\n"
            "Réponds UNIQUEMENT avec ce JSON (max 10 sessions):\n"
            '{"titre_plan": "...", "sessions": [{"jour": 1, "titre": "Révision — [matière]", '
            '"description": "Détail de ce qu\'il faut réviser", "matiere": "[matière]"}]}'
        )

        resp = _get_llm().invoke([HM(content=prompt)])
        text = resp.content.strip()
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].strip()

        plan_data = json.loads(text)
        sessions = plan_data.get("sessions", [])

        db = _db()
        created = []
        try:
            for i, session in enumerate(sessions[:10]):
                jour = int(session.get("jour", i + 1))
                due = min(datetime.utcnow() + timedelta(days=jour), exam_date - timedelta(hours=12))
                plan = Plan(
                    user_id=user_id,
                    title=session.get("titre", f"Révision — Jour {jour}")[:200],
                    description=session.get("description", "")[:500],
                    category="study",
                    due_date=due,
                    priority=4,
                    status="pending",
                )
                db.add(plan)
                created.append(session.get("titre", f"Session {jour}"))
            db.commit()
        finally:
            db.close()

        return json.dumps({
            "success": True,
            "titre_plan": plan_data.get("titre_plan", "Plan de révision"),
            "sessions_creees": len(created),
            "message": (
                f"Plan de révision créé avec {len(created)} sessions.\n"
                f"Matières: {matieres} | Examen dans: {days_left} jours.\n"
                "Retrouve les sessions dans ton planning."
            ),
        }, ensure_ascii=False)

    except json.JSONDecodeError:
        return "Erreur: impossible de parser le plan généré. Réessaie."
    except Exception as e:
        logger.error("generer_plan_etude error: %s", e)
        return f"Erreur lors de la génération du plan: {e}"


_TOOLS = [lister_taches, creer_tache, modifier_statut_tache, supprimer_tache, generer_plan_etude]


# ── Agent Node ───────────────────────────────────────────────────────────────

async def agent_node(state: PlanningAgentState) -> dict:
    user_id = state.get("user_id", 0)
    ctx = state.get("user_context") or {}
    nom = ctx.get("full_name") or ctx.get("username") or "l'étudiant"
    filiere = ctx.get("major") or "filière non renseignée"
    annee = ctx.get("year") or "?"

    system_prompt = (
        f"Tu es l'Agent Planning de SmartStudent - ENIAD Berkane.\n"
        f"Tu parles a {nom}, filiere {filiere}, annee {annee}. ID utilisateur: {user_id}.\n\n"
        "REGLES ABSOLUES - TU DOIS UTILISER TES OUTILS:\n"
        f"1. Lister les taches -> lister_taches(user_id={user_id})\n"
        f"2. Creer une tache -> creer_tache(user_id={user_id}, titre=..., description=..., categorie=..., date_echeance=..., priorite=...)\n"
        f"3. Modifier statut -> modifier_statut_tache(tache_id=..., nouveau_statut=...)\n"
        f"4. Supprimer tache -> supprimer_tache(tache_id=...)\n"
        f"5. Generer plan de revision -> generer_plan_etude(user_id={user_id}, matieres=..., date_examen=..., heures_par_jour=...)\n\n"
        "COMPORTEMENT:\n"
        "- Commence TOUJOURS par lister les taches existantes avant d'en creer.\n"
        "- Pour un plan de revision: demande les matieres et la date d'examen si non fournis.\n"
        "- Affiche les resultats de facon claire, structuree et motivante.\n"
        "- Reponds en francais."
    )

    try:
        llm = _get_llm().bind_tools(_TOOLS)
        messages = [SystemMessage(content=system_prompt)] + list(state.get("messages", []))
        resp = await llm.ainvoke(messages)
        return {"messages": [resp]}
    except Exception as e:
        logger.error("planning agent_node error: %s", e)
        return {"messages": [AIMessage(content="Le service IA est temporairement indisponible. Veuillez reessayer dans quelques instants.")]}


# ── Graph compilation ─────────────────────────────────────────────────────────

def _build_planning_graph():
    g = StateGraph(PlanningAgentState)
    g.add_node("agent", agent_node)
    g.add_node("tools", ToolNode(_TOOLS))
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", tools_condition)
    g.add_edge("tools", "agent")
    return g.compile(checkpointer=MemorySaver())


_graph_instance = None


def get_compiled_planning_graph():
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = _build_planning_graph()
        logger.info("PlanningAgent ReAct graph compiled")
    return _graph_instance


# ── Public API ────────────────────────────────────────────────────────────────

class PlanningAgent:
    def __init__(self):
        self._graph = get_compiled_planning_graph()

    async def process(
        self,
        user_message: str,
        user_id: int,
        user_context: dict,
        conversation_id: str = "default",
    ) -> dict:
        thread_id = f"planning_{conversation_id}"
        initial: PlanningAgentState = {
            "messages": [HumanMessage(content=user_message)],
            "user_id": user_id,
            "user_context": user_context,
        }
        config = {"configurable": {"thread_id": thread_id}}
        try:
            result = await self._graph.ainvoke(initial, config=config)
        except Exception as e:
            logger.error("PlanningAgent.process graph error: %s", e)
            return {"response": "Le service IA est temporairement indisponible. Veuillez reessayer."}
        last_ai = next(
            (m for m in reversed(result.get("messages", [])) if isinstance(m, AIMessage)),
            None,
        )
        return {"response": str(last_ai.content) if last_ai else "Erreur interne."}


def get_planning_agent() -> PlanningAgent:
    return PlanningAgent()
