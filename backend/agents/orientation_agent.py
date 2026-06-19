"""
Orientation Agent - Provides career advice and guidance
"""

from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .base_agent import BaseAgent


_ORIENTATION_SYSTEM_PROMPT = """Tu es l'Agent Orientation & Carrière de SmartStudent - ENIAD Berkane, Maroc.
Tu conseilles les étudiants sur leur avenir professionnel :

1. ORIENTATION PROFESSIONNELLE : métiers de l'informatique, génie, management, conseil carrière
2. CV & LETTRE DE MOTIVATION : rédaction, mise en forme, conseils personnalisés pour le Maroc
3. STAGES & EMPLOIS : comment trouver un stage, préparer une candidature, s'entretenir
4. COMPÉTENCES CLÉS : langages de programmation, certifications, compétences recherchées au Maroc
5. RÉSEAU PROFESSIONNEL : LinkedIn, associations professionnelles, événements networking

Domaines de formation à l'ENIAD : Génie Informatique, Génie Industriel, Génie Électrique, Management.
Marché cible : Maroc et Afrique du Nord principalement.

Sois inspirant et pratique. Donne des conseils concrets adaptés au marché marocain.
Pour un CV, propose une structure claire (infos perso, formation, expériences, compétences, langues).
Réponds toujours en français."""


class OrientationAgent(BaseAgent):
    """Provides career advice, CV assistance, and internship guidance"""

    def __init__(self):
        super().__init__(
            name="Agent Orientation",
            description="Conseils carrière, CV et orientation professionnelle",
        )

    def get_system_prompt(self) -> str:
        return _ORIENTATION_SYSTEM_PROMPT

    async def process(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process orientation queries with personalized LLM response."""
        uc = user_context or {}
        name = uc.get("full_name") or uc.get("username") or "l'étudiant(e)"
        major = uc.get("major") or ""
        year = uc.get("year") or ""

        system = self.get_system_prompt()
        system += f"\n\nTu parles à {name}"
        if major:
            system += f", en filière {major}"
        if year:
            system += f", en année {year}"
        system += "."

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
                "response": "Le service orientation est temporairement indisponible. Contactez le service des stages ENIAD.",
                "agent": self.name,
                "success": False,
                "error": str(e),
            }
