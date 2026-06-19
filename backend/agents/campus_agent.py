"""
Campus Agent - Handles campus events and community information
"""

from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .base_agent import BaseAgent


_CAMPUS_SYSTEM_PROMPT = """Tu es l'Agent Campus de SmartStudent - ENIAD Berkane, Maroc.
Tu informes et conseilles les étudiants sur :

1. ÉVÉNEMENTS CAMPUS : conférences, workshops, hackathons, portes ouvertes, journées culturelles
2. CLUBS & ASSOCIATIONS : clubs sportifs, culturels, techniques (robotique, informatique, art...)
3. VIE ÉTUDIANTE : cafétéria, bibliothèque, salles de travail, horaires des installations
4. GROUPES DE TRAVAIL : formation de groupes d'étude, collaboration entre étudiants
5. ACTIVITÉS PARASCOLAIRES : sports, musique, théâtre, bénévolat

Sois enthousiaste, accueillant et encourageant.
Aide les étudiants à s'intégrer et à profiter pleinement de la vie à l'ENIAD.
Si tu n'as pas d'information précise sur un événement spécifique, propose des alternatives ou
encourage l'étudiant à consulter le tableau d'affichage ou le secrétariat.
Réponds toujours en français."""


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
        """Process campus-related queries with LLM + database context injection."""
        uc = user_context or {}
        name = uc.get("full_name") or uc.get("username") or "l'étudiant(e)"

        system = self.get_system_prompt()
        system += f"\n\nTu parles à {name}."

        # Inject upcoming events from database if available
        events_context = await self._get_events_context()
        if events_context:
            system += f"\n\nÉVÉNEMENTS CAMPUS ACTUELS :\n{events_context}"

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
            response = self.llm.invoke(messages)
            return {"response": response.content, "agent": self.name, "success": True}
        except Exception as e:
            return {
                "response": "Le service campus est temporairement indisponible. Consultez le tableau d'affichage ou le secrétariat ENIAD.",
                "agent": self.name,
                "success": False,
                "error": str(e),
            }

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
                    .filter(Event.date >= datetime.utcnow())
                    .order_by(Event.date.asc())
                    .limit(5)
                    .all()
                )
                if not events:
                    return ""
                lines = []
                for e in events:
                    date_str = e.date.strftime("%d/%m/%Y %H:%M") if e.date else "?"
                    lines.append(f"- {e.title} le {date_str}" + (f" ({e.location})" if e.location else ""))
                return "\n".join(lines)
            finally:
                db.close()
        except Exception:
            return ""
