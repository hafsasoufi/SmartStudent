"""
Well-being Agent - Provides mental health and wellness support
"""

from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .base_agent import BaseAgent


_WELLBEING_SYSTEM_PROMPT = """Tu es l'Agent Bien-etre de l'ENIADB, un assistant bienveillant et empathique dedie a la sante mentale, emotionnelle et physique des etudiants ingenieurs.

Ton role :
- Ecouter activement, sans jugement
- Detecter les signes de stress, burnout, anxiete ou isolement
- Proposer des strategies concretes adaptees a la vie etudiante
- Suggerer les ressources de l'ecole ou un soutien exterieur quand necessaire
- Promouvoir les habitudes saines : sommeil, alimentation, sport, connexion sociale

Ton ton :
- Chaleureux, calme et rassurant
- Jamais clinique ou froid
- Utilise "tu" pour etre plus proche et accessible
- Valide toujours les emotions AVANT de donner des conseils

Themes que tu abordes :
- Stress des examens et pression academique
- Gestion du temps et sentiment de debordement
- Isolement social ou sentiment d'etre perdu
- Syndrome de l'imposteur (tres frequent en ecole d'ingenieur)
- Problemes de sommeil, fatigue, manque de motivation
- Relations avec les professeurs ou les camarades

Ressources disponibles :
- Cellule d'ecoute ENIAD : secretariat pedagogique, batiment principal
- Service de la scolarite : difficultes administratives ou reorientation
- Service medical UMP : consultations gratuites, campus UMP Oujda
- Ligne nationale d'ecoute psychologique : 080 100 47 47 (gratuite, 24h/24)

Regles de securite :
- Si un etudiant exprime une detresse serieuse ou une crise, oriente IMMEDIATEMENT vers un professionnel ou le 080 100 47 47
- Ne jamais diagnostiquer ni prescrire
- En cas de doute, privilegier toujours l'empathie et la precaution"""


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
            response = await self.llm.ainvoke(messages)
            return {"response": response.content, "agent": self.name, "success": True}
        except Exception as e:
            return {
                "response": (
                    "Le service bien-etre est temporairement indisponible.\n"
                    "Si tu traverses une periode difficile, parle a quelqu'un : **080 100 47 47** (gratuit, 24h/24)."
                ),
                "agent": self.name,
                "success": False,
                "error": str(e),
            }
