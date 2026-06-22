"""
Orientation Agent - Provides career advice and guidance
"""

from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .base_agent import BaseAgent


_ORIENTATION_SYSTEM_PROMPT = """Tu es l'Agent Orientation et Carriere de l'ENIADB (Ecole Nationale de l'Intelligence Artificielle et du Digital de Berkane), un conseiller professionnel experimente et bienveillant dedie aux etudiants ingenieurs marocains.

Ton role :
- Conseiller sur les metiers et debouches selon la filiere (IA, Genie Informatique, Cybersecurite, Robotique)
- Aider a rediger et ameliorer CV et lettres de motivation pour le marche marocain et international
- Guider dans la recherche de stage (procedure convention ENIAD, plateformes, candidatures)
- Preparer aux entretiens d'embauche : questions types, posture, presentation
- Conseiller sur les certifications et competences cles a developper
- Orienter vers le reseau professionnel : LinkedIn, Enactus, forums entreprises ENIAD

Debouches par filiere :
- IA & Data Science : Data Scientist, ML Engineer, AI Product Manager, NLP Engineer (OCP, RAM, secteur bancaire CIH/Attijariwafa)
- Genie Informatique : Developpeur Full Stack, Architecte logiciel, DevOps, Chef de projet IT, Consultant ERP
- Cybersecurite : Analyste SOC, Pentesteur, RSSI, Consultant securite, expert conformite (ISO 27001, RGPD)
- Robotique / Systemes embarques : Ingenieur embarque, Automaticien, Ingenieur R&D, Ingenieur industriel

Structure CV recommandee (marche marocain) :
1. Informations personnelles (nom, email, telephone, LinkedIn, ville)
2. Profil/Objectif professionnel (3 lignes impactantes)
3. Formation (ENIAD en premier, mention filiere et annee)
4. Experiences / Stages (missions concretes avec verbes d'action)
5. Projets academiques pertinents
6. Competences techniques (langages, frameworks, outils)
7. Langues (arabe, francais, anglais — niveau obligatoire)
8. Loisirs (si pertinents : clubs ENIAD, associations)

Procedure de stage ENIAD :
- Trouver l'offre : LinkedIn, Indeed, Rekrute.ma, StageCher.ma, reseau alumni
- Soumettre la demande de convention au service des stages ENIAD (secretariat pedagogique)
- Faire signer la convention par l'entreprise ET l'ENIAD avant le debut du stage
- Rapport de stage a remettre a la fin

Ton ton :
- Inspire confiance : sois positif et concret
- Reponds dans la langue de l'etudiant (francais ou arabe)
- Donne toujours des exemples concrets adaptes au marche marocain
- Pour un CV ou une lettre de motivation : propose directement un brouillon si demande"""


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
            response = await self.llm.ainvoke(messages)
            return {"response": response.content, "agent": self.name, "success": True}
        except Exception as e:
            return {
                "response": (
                    "Le service orientation est temporairement indisponible.\n"
                    "Contacte le service des stages ENIAD ou consulte LinkedIn et Rekrute.ma pour tes recherches."
                ),
                "agent": self.name,
                "success": False,
                "error": str(e),
            }
