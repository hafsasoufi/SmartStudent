"""
Agent Admin — SmartStudent LangGraph ReAct Agent
Architecture: agent_node <-> tools_node loop (ReAct pattern)
Outils: recuperer_profil, recuperer_notes, generer_document_pdf,
        verifier_statut, creer_demande, creer_reclamation, rechercher_rag
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# State
# ─────────────────────────────────────────────────────────────────────────────

class AdminAgentState(TypedDict, total=False):
    messages:     Annotated[list, add_messages]
    user_id:      int
    user_context: dict


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _db_session():
    from backend.database import get_db
    return next(get_db())


def _get_llm():
    from backend.agents.orchestrator import get_llm
    return get_llm()


# ─────────────────────────────────────────────────────────────────────────────
# Tools — actions réelles sur la BD et génération PDF
# ─────────────────────────────────────────────────────────────────────────────

@tool
def recuperer_profil_etudiant(user_id: int) -> str:
    """Recupere les informations completes de l'etudiant depuis la base de donnees: nom, email, filiere, annee, matricule, statut."""
    try:
        from backend.models import User, UserProfile
        db = _db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return f"Aucun etudiant trouve avec l'ID {user_id}."

            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

            info = {
                "id": user.id,
                "nom_complet": user.full_name or user.username,
                "email": user.email,
                "username": user.username,
                "filiere": profile.major if profile else "Non renseignee",
                "annee": profile.year if profile else None,
                "universite": profile.university if profile else "ENIAD",
                "telephone": profile.phone if profile else None,
                "statut": "Actif" if user.is_active else "Inactif",
            }
            return json.dumps(info, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"recuperer_profil_etudiant error: {e}")
        return f"Erreur lors de la recuperation du profil: {e}"


@tool
def recuperer_notes_etudiant(user_id: int) -> str:
    """Recupere les notes et resultats d'examens de l'etudiant depuis la base de donnees."""
    try:
        from backend.models import Exam
        db = _db_session()
        try:
            exams = (
                db.query(Exam)
                .filter(Exam.user_id == user_id, Exam.status == "completed")
                .order_by(Exam.completed_at.desc())
                .all()
            )

            if not exams:
                return "Aucune note disponible pour cet etudiant (aucun examen complete)."

            grades = []
            for exam in exams:
                note_20 = round((exam.score / exam.total_points) * 20, 2) if (exam.score is not None and exam.total_points) else None
                grades.append({
                    "matiere": exam.subject or exam.title,
                    "note_sur_20": note_20,
                    "score": exam.score,
                    "total": exam.total_points,
                    "date": exam.completed_at.strftime("%d/%m/%Y") if exam.completed_at else None,
                })

            valid_notes = [g["note_sur_20"] for g in grades if g["note_sur_20"] is not None]
            moyenne = round(sum(valid_notes) / len(valid_notes), 2) if valid_notes else None

            result = {
                "nombre_examens": len(grades),
                "notes": grades,
                "moyenne_generale": moyenne,
            }
            return json.dumps(result, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"recuperer_notes_etudiant error: {e}")
        return f"Erreur lors de la recuperation des notes: {e}"


@tool
def generer_document_pdf(doc_type: str, user_id: int, donnees_supplementaires: str = "{}") -> str:
    """Genere un document PDF officiel pre-rempli avec les vraies donnees de l'etudiant et l'enregistre en base de donnees.
    Types disponibles: 'Attestation de scolarite', 'Releve de notes', 'Convention de stage', 'Certificat de stage'.
    donnees_supplementaires: JSON string avec infos optionnelles (ex: {\"entreprise\": \"...\", \"poste\": \"...\"} pour convention de stage)."""
    try:
        from backend.models import User, UserProfile, Exam, AdminRequest
        from backend.agents.documents_agent import get_documents_agent

        db = _db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return f"Etudiant introuvable (ID: {user_id})."

            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

            first = user.first_name or (user.full_name or "").split()[0]
            last  = user.last_name  or (" ".join((user.full_name or "").split()[1:]) or "")
            user_data = {
                "full_name":       user.full_name or user.username,
                "first_name":      first,
                "last_name":       last,
                "student_id":      str(user_id),
                "student_card_id": (profile.student_card_id if profile else None) or str(user_id),
                "email":           user.email,
                "major":           profile.major if profile else "Genie Informatique",
                "year":            profile.year if profile else 3,
                "university":      (profile.university if profile else None) or "ENIAD Berkane",
                "phone":           (profile.phone if profile else None) or "",
            }

            # Inject real grades for releve de notes
            if any(k in doc_type.lower() for k in ("releve", "notes")):
                exams = (
                    db.query(Exam)
                    .filter(Exam.user_id == user_id, Exam.status == "completed")
                    .all()
                )
                grades = []
                for exam in exams:
                    if exam.score is not None and exam.total_points:
                        grades.append({
                            "matiere": exam.subject or exam.title,
                            "coefficient": 3,
                            "note": round((exam.score / exam.total_points) * 20, 2),
                        })
                user_data["grades"] = grades

            # Merge supplementary data (company info for convention de stage)
            try:
                sup = json.loads(donnees_supplementaires) if donnees_supplementaires else {}
                user_data.update(sup)
            except Exception:
                pass

            doc_id, _ = get_documents_agent().generate(doc_type, user_data)

            req_id = str(uuid.uuid4())
            req = AdminRequest(
                id=req_id,
                user_id=user_id,
                request_type=doc_type,
                status="validated",
                description=f"Genere par AdminAgent - {doc_type}",
                doc_id=doc_id,
            )
            db.add(req)
            db.commit()

            return json.dumps({
                "success": True,
                "doc_id": doc_id,
                "request_id": req_id,
                "doc_type": doc_type,
                "message": (
                    f"Document '{doc_type}' genere avec succes.\n"
                    f"- Reference: {req_id[:8]}\n"
                    f"- Document ID: {doc_id[:8]}\n"
                    "- Telechargeable depuis l'onglet Documents."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"generer_document_pdf error: {e}")
        return f"Erreur lors de la generation du document: {e}"


@tool
def verifier_statut_demandes(user_id: int) -> str:
    """Consulte le statut reel de toutes les demandes administratives et reclamations de l'etudiant depuis la base de donnees."""
    try:
        from backend.models import AdminRequest, Complaint
        db = _db_session()
        try:
            _LABELS = {
                "pending": "En attente", "in_progress": "En cours",
                "validated": "Validee", "refused": "Refusee",
                "open": "Ouverte", "resolved": "Resolue", "closed": "Fermee",
            }

            requests = (
                db.query(AdminRequest)
                .filter(AdminRequest.user_id == user_id)
                .order_by(AdminRequest.created_at.desc())
                .limit(10)
                .all()
            )
            complaints = (
                db.query(Complaint)
                .filter(Complaint.user_id == user_id)
                .order_by(Complaint.created_at.desc())
                .limit(5)
                .all()
            )

            if not requests and not complaints:
                return "Aucune demande ni reclamation trouvee pour cet etudiant."

            result = {
                "demandes": [
                    {
                        "id": r.id[:8],
                        "type": r.request_type,
                        "statut": _LABELS.get(r.status, r.status),
                        "date": r.created_at.strftime("%d/%m/%Y"),
                        "doc_disponible": r.doc_id is not None,
                    }
                    for r in requests
                ],
                "reclamations": [
                    {
                        "ticket": c.id,
                        "categorie": c.category,
                        "statut": _LABELS.get(c.status, c.status),
                        "date": c.created_at.strftime("%d/%m/%Y"),
                    }
                    for c in complaints
                ],
            }
            return json.dumps(result, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"verifier_statut_demandes error: {e}")
        return f"Erreur lors de la consultation: {e}"


@tool
def creer_demande_administrative(user_id: int, type_demande: str, description: str) -> str:
    """Cree une demande administrative formelle en base de donnees (sans PDF immediat).
    Utiliser pour: redoublement, equivalence, transfert, ou toute demande necessitant traitement manuel par le secretariat."""
    try:
        from backend.models import AdminRequest
        db = _db_session()
        try:
            req_id = str(uuid.uuid4())
            req = AdminRequest(
                id=req_id,
                user_id=user_id,
                request_type=type_demande,
                status="pending",
                description=description[:1000],
            )
            db.add(req)
            db.commit()

            return json.dumps({
                "success": True,
                "request_id": req_id[:8],
                "type": type_demande,
                "statut": "En attente",
                "message": (
                    f"Demande '{type_demande}' enregistree avec succes.\n"
                    f"- Reference: {req_id[:8]}\n"
                    "- Traitement: 3 a 5 jours ouvrables."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"creer_demande_administrative error: {e}")
        return f"Erreur lors de la creation de la demande: {e}"


@tool
def creer_ticket_reclamation(user_id: int, categorie: str, description: str) -> str:
    """Cree un ticket de reclamation officiel avec numero unique COMP-YYYY-XXXXX en base de donnees.
    Categories valides: pedagogique, administratif, financier, infrastructure, autre."""
    try:
        from backend.models import Complaint
        db = _db_session()
        try:
            valid_cats = ["pedagogique", "administratif", "financier", "infrastructure", "autre"]
            if categorie not in valid_cats:
                categorie = "autre"

            count = db.query(Complaint).count() + 1
            ticket_id = f"COMP-{datetime.now().year}-{count:05d}"

            complaint = Complaint(
                id=ticket_id,
                user_id=user_id,
                category=categorie,
                description=description[:1000],
                status="open",
            )
            db.add(complaint)
            db.commit()

            return json.dumps({
                "success": True,
                "ticket_id": ticket_id,
                "categorie": categorie,
                "statut": "Ouverte",
                "message": (
                    f"Reclamation enregistree avec succes.\n"
                    f"- Ticket: {ticket_id}\n"
                    f"- Categorie: {categorie}\n"
                    "- Traitement: 48h ouvrables."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"creer_ticket_reclamation error: {e}")
        return f"Erreur lors de la creation du ticket: {e}"


@tool
def rechercher_info_eniad(requete: str) -> str:
    """Recherche dans les documents officiels ENIAD (reglement, procedures, calendrier academique, contacts) via la base documentaire RAG."""
    try:
        from backend.services.rag_service import get_rag_service
        rag = get_rag_service()
        if not rag.is_ready:
            return (
                "Base documentaire ENIAD non disponible. "
                "Contactez le secretariat ENIAD directement pour toute information officielle."
            )

        results = rag.query(requete, n_results=4)
        if not results:
            return "Aucune information trouvee dans les documents ENIAD pour cette requete."

        parts = [f"[Source {i+1}] {r.get('content', '')[:500]}" for i, r in enumerate(results)]
        return "\n\n".join(parts)
    except Exception as e:
        logger.warning(f"rechercher_info_eniad error: {e}")
        return f"Recherche documentaire indisponible: {e}"


_TOOLS = [
    recuperer_profil_etudiant,
    recuperer_notes_etudiant,
    generer_document_pdf,
    verifier_statut_demandes,
    creer_demande_administrative,
    creer_ticket_reclamation,
    rechercher_info_eniad,
]


# ─────────────────────────────────────────────────────────────────────────────
# Agent Node (ReAct — Reason + Act)
# ─────────────────────────────────────────────────────────────────────────────

async def agent_node(state: AdminAgentState) -> dict:
    user_id = state.get("user_id", 0)
    ctx = state.get("user_context") or {}

    nom = ctx.get("full_name") or ctx.get("username") or "l'etudiant"
    filiere = ctx.get("major") or "filiere non renseignee"
    annee = ctx.get("year") or "annee non renseignee"

    system_prompt = (
        f"Tu es l'Agent Administratif de SmartStudent - ENIAD Berkane, Maroc.\n"
        f"Tu interagis avec: {nom}, Filiere: {filiere}, Annee: {annee}, ID utilisateur: {user_id}.\n\n"
        "REGLES ABSOLUES - TU DOIS TOUJOURS UTILISER TES OUTILS:\n"
        f"1. Profil etudiant -> recuperer_profil_etudiant(user_id={user_id})\n"
        f"2. Notes/resultats -> recuperer_notes_etudiant(user_id={user_id})\n"
        f"3. Generer un document PDF -> generer_document_pdf(doc_type=..., user_id={user_id})\n"
        f"4. Suivi des demandes -> verifier_statut_demandes(user_id={user_id})\n"
        f"5. Demande formelle (redoublement, equivalence) -> creer_demande_administrative(user_id={user_id}, ...)\n"
        f"6. Reclamation/plainte -> creer_ticket_reclamation(user_id={user_id}, ...)\n"
        "7. Info ENIAD (procedures, dates, reglements) -> rechercher_info_eniad(requete=...)\n\n"
        "DOCUMENTS GENERABLES: 'Attestation de scolarite', 'Releve de notes', 'Convention de stage', 'Certificat de stage'\n\n"
        "COMPORTEMENT:\n"
        "- Utilise toujours les outils pour obtenir des donnees reelles, jamais de donnees inventees.\n"
        "- Pour une demande de document: recupere d'abord le profil, puis genere le PDF immediatement.\n"
        "- Pour une convention de stage: demande le nom de l'entreprise et le poste si non fournis.\n"
        "- Reponds en francais, de facon professionnelle et bienveillante.\n"
        "- Apres execution d'un outil, presente les resultats clairement avec les references importantes (ID, ticket...)."
    )

    try:
        llm = _get_llm().bind_tools(_TOOLS)
        messages = [SystemMessage(content=system_prompt)] + list(state.get("messages", []))
        resp = await llm.ainvoke(messages)
        return {"messages": [resp]}
    except Exception as e:
        logger.error(f"agent_node error: {e}")
        err = AIMessage(content="Une erreur est survenue avec le service IA. Veuillez reessayer dans quelques instants ou contacter le secretariat ENIAD.")
        return {"messages": [err]}


# ─────────────────────────────────────────────────────────────────────────────
# Graph compilation — ReAct loop: agent <-> tools
# ─────────────────────────────────────────────────────────────────────────────

def _build_admin_graph():
    g = StateGraph(AdminAgentState)
    g.add_node("agent", agent_node)
    g.add_node("tools", ToolNode(_TOOLS))

    g.set_entry_point("agent")
    g.add_conditional_edges("agent", tools_condition)  # -> "tools" or END
    g.add_edge("tools", "agent")

    return g.compile(checkpointer=MemorySaver())


_graph_instance = None


def get_compiled_admin_graph():
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = _build_admin_graph()
        nodes = list(_graph_instance.get_graph().nodes)
        logger.info(f"AdminAgent ReAct graph compiled - nodes: {nodes}")
    return _graph_instance


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

class AdminAgent:
    def __init__(self):
        self._graph = get_compiled_admin_graph()

    async def process(
        self,
        user_message: str,
        user_id: int,
        user_context: dict,
        conversation_id: str = "default",
    ) -> dict:
        thread_id = f"admin_{conversation_id}"
        initial: AdminAgentState = {
            "messages":     [HumanMessage(content=user_message)],
            "user_id":      user_id,
            "user_context": user_context,
        }
        config = {"configurable": {"thread_id": thread_id}}

        try:
            result = await self._graph.ainvoke(initial, config=config)
        except Exception as e:
            logger.error(f"AdminAgent.process graph error: {e}")
            return {
                "response": "Le service IA est temporairement indisponible. Veuillez reessayer ou contacter le secretariat ENIAD.",
                "doc_id": None,
                "request_id": None,
                "ticket_id": None,
            }

        last_ai = next(
            (m for m in reversed(result.get("messages", [])) if isinstance(m, AIMessage)),
            None,
        )

        # Extract doc/ticket IDs from tool result messages
        doc_id = request_id = ticket_id = None
        for msg in result.get("messages", []):
            content = getattr(msg, "content", "")
            if not isinstance(content, str):
                continue
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    doc_id = doc_id or data.get("doc_id")
                    request_id = request_id or data.get("request_id")
                    ticket_id = ticket_id or data.get("ticket_id")
            except Exception:
                pass

        return {
            "response":   str(last_ai.content) if last_ai else "Une erreur est survenue.",
            "doc_id":     doc_id,
            "request_id": request_id,
            "ticket_id":  ticket_id,
        }


def get_admin_agent() -> AdminAgent:
    return AdminAgent()
