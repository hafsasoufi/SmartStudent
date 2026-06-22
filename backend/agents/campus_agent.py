"""
Campus Agent - Handles campus events and community information
"""

from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .base_agent import BaseAgent


_CAMPUS_SYSTEM_PROMPT = """Tu es l'Agent Campus de l'ENIADB (Ecole Nationale de l'Intelligence Artificielle et du Digital de Berkane), un assistant intelligent dedie aux etudiants.

Ta base de connaissance couvre :
- Le reglement interieur : absences, examens, regles de notation, discipline, comportements interdits
- Les clubs etudiants : SECORA (cybersecurite), ENNOVERS (genie informatique), NURLIA (IA & data science), RIOT (robotique), AL ATAA (social & humanitaire), Enactus (entrepreneuriat social)
- Les evenements : activites, competitions, workshops, galas, forums entreprises
- La bibliotheque : livres disponibles avec titres, auteurs et numeros de reference
- Infos ecole : adresse (Route Aklim, Km 1, Berkane), site (www.eniad.ump.ma), email (eniad@ump.ac.ma)

Regles de comportement :
- Reponds toujours dans la langue de l'etudiant (francais ou arabe)
- Pour les questions de reglement, cite l'article pertinent avec precision
- Si tu ne sais pas, dis-le clairement - ne jamais inventer d'information
- Reponds de facon concise mais complete
- Pour les questions bibliotheque, donne toujours le(s) numero(s) de livre et la quantite disponible
- Sois enthousiaste, accueillant et encourageant pour les activites parascolaires"""


class CampusAgent(BaseAgent):
    """Provides information about campus events, clubs, and communities"""

    def __init__(self):
        super().__init__(
            name="Agent Campus",
            description="Informations sur les événements campus et la vie étudiante",
        )

    def get_system_prompt(self) -> str:
        return _CAMPUS_SYSTEM_PROMPT

    async def process(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process campus-related queries with LLM + RAG + events context."""
        uc = user_context or {}
        name = uc.get("full_name") or uc.get("username") or "l'étudiant(e)"

        system = self.get_system_prompt()
        system += f"\n\nTu parles a {name}."

        # RAG: inject relevant documents from the knowledge base
        rag_context = await self._get_rag_context(user_message)
        if rag_context:
            system += f"\n\nDOCUMENTS PERTINENTS (base de connaissance ENIADB) :\n{rag_context}"

        # Inject upcoming events from database
        events_context = await self._get_events_context()
        if events_context:
            system += f"\n\nEVENEMENTS CAMPUS A VENIR :\n{events_context}"

        messages = [SystemMessage(content=system)]

        if conversation_history:
            for msg in conversation_history[-6:]:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

        messages.append(HumanMessage(content=user_message))

        try:
            response = await self.llm.ainvoke(messages)
            return {"response": response.content, "agent": self.name, "success": True}
        except Exception as e:
            return {
                "response": (
                    "Le service campus est temporairement indisponible.\n"
                    "Consulte le tableau d'affichage ou le secretariat ENIAD — eniad@ump.ac.ma"
                ),
                "agent": self.name,
                "success": False,
                "error": str(e),
            }

    async def _get_rag_context(self, query: str) -> str:
        """Query RAG for relevant campus/club/regulation documents."""
        try:
            from backend.services.rag_service import get_rag_service
            rag = get_rag_service()
            if not rag.is_ready:
                return ""
            results = rag.query(query, n_results=4)
            if not results:
                return ""
            lines = []
            for r in results:
                if r.get("score", 0) > 0.35:
                    title = r.get("metadata", {}).get("title", "")
                    text = r.get("text", "")[:600]
                    lines.append(f"[{title}]\n{text}")
            return "\n\n".join(lines)
        except Exception:
            return ""

    async def _get_events_context(self) -> str:
        """Fetch upcoming events from database to enrich LLM context."""
        try:
            from backend.database import get_db
            from backend.models import Event
            from datetime import datetime

            db = next(get_db())
            try:
                events = (
                    db.query(Event)
                    .filter(Event.start_date >= datetime.utcnow())
                    .order_by(Event.start_date.asc())
                    .limit(5)
                    .all()
                )
                if not events:
                    return ""
                lines = []
                for e in events:
                    date_str = e.start_date.strftime("%d/%m/%Y a %Hh%M") if e.start_date else "?"
                    lines.append(
                        f"- {e.title} le {date_str}"
                        + (f" ({e.location})" if e.location else "")
                        + (f" : {e.description}" if e.description else "")
                    )
                return "\n".join(lines)
            finally:
                db.close()
        except Exception:
            return ""
