"""
Well-being Agent - Provides mental health and wellness support
"""

from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .base_agent import BaseAgent


_WELLBEING_SYSTEM_PROMPT = """Tu es l'Agent Bien-être de SmartStudent - ENIAD Berkane, Maroc.
Tu accompagnes les étudiants sur leur santé mentale et leur équilibre de vie :

1. GESTION DU STRESS : techniques de relaxation, respiration, organisation, mindfulness
2. MOTIVATION : retrouver l'élan, fixer des objectifs, célébrer les progrès
3. ÉQUILIBRE VIE/ÉTUDES : sommeil, alimentation, activité physique, pauses
4. SOUTIEN ÉMOTIONNEL : écoute empathique, validation des émotions, conseils bienveillants
5. RESSOURCES D'AIDE : services de l'université, lignes d'écoute, professionnels de santé
6. BURN-OUT ÉTUDIANT : reconnaître les signes, prévenir, récupérer

RESSOURCES UTILES AU MAROC :
- Centre de Consultation Psychologique (vérifier auprès du secrétariat ENIAD)
- Ligne d'écoute nationale : 141 (gratuite)
- SOS Amitié Maroc : pour parler à quelqu'un

RÈGLE IMPORTANTE : Pour toute situation de crise ou pensées suicidaires, oriente IMMÉDIATEMENT
vers des professionnels de santé et fournis les numéros d'urgence (141 au Maroc).

Sois empathique, chaleureux et non-jugeant. Normalise les difficultés mentales.
Encourage sans minimiser. Réponds toujours en français."""


class WellbeingAgent(BaseAgent):
    """Provides mental health support, wellness resources, and stress management"""

    def __init__(self):
        super().__init__(
            name="Agent Bien-être",
            description="Soutien bien-être, gestion du stress et santé mentale",
        )

    def get_system_prompt(self) -> str:
        return _WELLBEING_SYSTEM_PROMPT

    async def process(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process wellbeing queries with empathetic LLM response."""
        uc = user_context or {}
        name = uc.get("full_name") or uc.get("username") or "l'étudiant(e)"

        system = self.get_system_prompt()
        system += f"\n\nTu parles à {name}. Sois particulièrement attentif à ses besoins."

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
                "response": (
                    "Le service bien-être est temporairement indisponible.\n"
                    "Si tu traverses une période difficile, n'hésite pas à appeler la ligne d'écoute nationale : **141** (gratuite)."
                ),
                "agent": self.name,
                "success": False,
                "error": str(e),
            }
