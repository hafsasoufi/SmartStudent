"""
Admin Agent — FAQ, documents institutionnels ENIAD, RAG
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent


class AdminAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agent Admin",
            description="Répond aux questions institutionnelles ENIAD avec RAG"
        )

    def get_system_prompt(self) -> str:
        return """Tu es l'assistant administratif de SmartStudent pour l'ENIAD (École Nationale de l'Intelligence Artificielle et du Digital) à Berkane, Maroc.

Tu aides les étudiants avec :
1. EMPLOIS DU TEMPS : horaires par filière (IA, IRSI, ROC, GINF, EPSI) et semestre
2. CALENDRIER : dates d'examens, rattrapages, vacances
3. DOCUMENTS : convention de stage, attestations, règlement intérieur
4. FILIÈRES : présentation des programmes IA, IRSI, ROC, GINF, EPSI
5. VIE ÉTUDIANTE : bourses, santé, clubs, sport
6. PROCÉDURES : admission, inscription, PFA, stages
7. CONTACTS : email eniad@ump.ac.ma, liens du site

Quand tu as des documents de contexte, utilise-les pour répondre précisément.
Si une question dépasse tes connaissances, renvoie vers eniad@ump.ac.ma.
Réponds toujours en français sauf si l'étudiant écrit en arabe ou anglais.
Sois concis, précis et utile."""

    async def retrieve_documents(
        self,
        query: str,
        top_k: int = 4,
    ) -> List[Dict[str, Any]]:
        """Recherche dans ChromaDB les documents ENIAD pertinents."""
        try:
            from backend.services.rag_service import get_rag_service
            rag = get_rag_service()
            if not rag.is_ready:
                return self._fallback_knowledge(query)
            results = rag.query(query, n_results=top_k)
            return results
        except Exception as e:
            return self._fallback_knowledge(query)

    def _fallback_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Réponses de secours si RAG non disponible."""
        query_lower = query.lower()
        fallbacks = []

        if any(w in query_lower for w in ["emploi", "planning", "horaire", "cours", "edt"]):
            fallbacks.append({
                "content": "Emplois du temps disponibles sur https://eniad.ump.ma/fr/emploi-du-temps\nTélécharge le PDF de ta filière (IA, IRSI, ROC, GINF, EPSI) et semestre.",
                "metadata": {"type": "emploi_du_temps", "source": "fallback"},
                "score": 0.8,
            })
        if any(w in query_lower for w in ["exam", "contrôle", "épreuve", "date"]):
            fallbacks.append({
                "content": "Planning des examens : https://eniad.ump.ma/fr/calendrier-des-examens\nSemestres S5/S7 (automne), S6/S8 (printemps).",
                "metadata": {"type": "examen", "source": "fallback"},
                "score": 0.8,
            })
        if any(w in query_lower for w in ["stage", "convention", "entreprise"]):
            fallbacks.append({
                "content": "Convention de stage : https://eniad.ump.ma/storage/files/1/Convention de stage/68234cd5a6293.pdf\nContact : eniad@ump.ac.ma",
                "metadata": {"type": "stage", "source": "fallback"},
                "score": 0.8,
            })

        if not fallbacks:
            fallbacks.append({
                "content": "ENIAD — École Nationale de l'Intelligence Artificielle et du Digital, Berkane.\nContact : eniad@ump.ac.ma | Site : https://eniad.ump.ma/fr",
                "metadata": {"type": "general", "source": "fallback"},
                "score": 0.5,
            })
        return fallbacks

    async def generate_document(
        self,
        document_type: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Génère un document PDF (attestation, lettre...)."""
        try:
            from backend.services.document_service import generate_pdf_document
            result = await generate_pdf_document(document_type, data)
            return result
        except Exception:
            return {
                "document_type": document_type,
                "status": "error",
                "message": "Service de génération de documents non disponible.",
                "url": None,
            }
