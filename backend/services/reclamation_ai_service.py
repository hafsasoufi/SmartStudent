"""AI-powered analysis for student complaints (réclamations)."""
from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def analyze_complaint(category: str, description: str) -> dict:
    """
    Call the LLM to classify a complaint and produce a suggested admin reply.

    Returns a dict with keys:
      ai_categorie         – refined category string
      ai_priorite          – int 1 (high) | 2 (medium) | 3 (low)
      ai_resume            – 1-2 sentence summary
      ai_reponse_suggeree  – draft reply for the admin (2-3 sentences)
    """
    prompt = (
        "Tu es un assistant administratif de l'ENIAD "
        "(École Nationale de l'Intelligence Artificielle et du Digital).\n\n"
        "Analyse cette réclamation d'étudiant et réponds UNIQUEMENT avec un objet JSON valide "
        "(sans texte avant ni après) :\n\n"
        f"Catégorie déclarée : {category}\n"
        f"Description : {description}\n\n"
        "Format attendu :\n"
        "{\n"
        '  "ai_categorie": "pédagogique|administratif|financier|infrastructure|autre",\n'
        '  "ai_priorite": 1,\n'
        '  "ai_resume": "Résumé en 1-2 phrases.",\n'
        '  "ai_reponse_suggeree": "Réponse suggérée professionnelle en 2-3 phrases."\n'
        "}\n\n"
        "Règles pour ai_priorite : 1 = urgence haute (bloque les études/droits), "
        "2 = urgence moyenne (gênant mais pas bloquant), 3 = faible (informatif)."
    )

    try:
        from langchain_core.messages import HumanMessage
        from backend.agents.orchestrator import get_llm

        llm = get_llm()
        resp = llm.invoke([HumanMessage(content=prompt)])
        raw = resp.content.strip()

        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(raw[start:end])
            return {
                "ai_categorie":        str(data.get("ai_categorie", category))[:50],
                "ai_priorite":         int(data.get("ai_priorite", 2)),
                "ai_resume":           str(data.get("ai_resume", ""))[:500],
                "ai_reponse_suggeree": str(data.get("ai_reponse_suggeree", ""))[:1000],
            }
    except Exception as exc:
        logger.warning("reclamation_ai_service: LLM call failed: %s", exc)

    # Fallback — deterministic, never fails
    priority = 1 if any(w in description.lower() for w in ["urgent", "bloqué", "examen", "diplôme", "erreur grave"]) else 2
    return {
        "ai_categorie":        category,
        "ai_priorite":         priority,
        "ai_resume":           (description[:120] + "…") if len(description) > 120 else description,
        "ai_reponse_suggeree": (
            "Votre réclamation a bien été reçue et enregistrée sous un numéro de suivi. "
            "Notre équipe l'examinera dans les meilleurs délais et vous contactera par email "
            "pour vous informer de la suite donnée à votre demande."
        ),
    }
