"""
MemoryManager — Extraction LLM, stockage et injection de mémoire long-terme.

Cycle complet :
  1. extract_and_store()  → après chaque échange, identifie et persiste les faits importants
  2. load_memories()      → au début d'une session, charge les mémoires les plus pertinentes

L'extraction est asynchrone et tourne en background pour ne pas bloquer la réponse du chat.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ── Extraction prompt ────────────────────────────────────────────────────────

_EXTRACTION_PROMPT = """Tu es un système d'extraction de mémoire pour un assistant étudiant.
Analyse le message de l'étudiant et la réponse de l'agent.
Extrais UNIQUEMENT les faits importants, persistants et personnels sur cet étudiant.

Catégories valides :
- "academic"     : filière, année, matières, notes, PFA, examens, résultats
- "personal"     : nom, préférence de communication, situation personnelle
- "preferences"  : habitudes de travail, outils préférés, heures d'étude
- "goals"        : objectifs professionnels, recherche de stage, projets futurs

Réponds UNIQUEMENT avec un JSON array. Chaque objet contient :
- "category"  : une des 4 catégories ci-dessus
- "content"   : fait précis en une seule phrase (max 120 caractères)
- "importance": entier 1-10 (10 = très important pour personnaliser les réponses futures)

Exemples de faits à extraire :
- "Je suis en 3ème année IA" → {{"category": "academic", "content": "Étudiant en 3ème année filière IA", "importance": 9}}
- "Mon examen de ML est dans 2 semaines" → {{"category": "academic", "content": "Examen de Machine Learning prévu prochainement", "importance": 7}}
- "Je préfère réviser le soir" → {{"category": "preferences", "content": "Préfère réviser le soir", "importance": 6}}
- "Je cherche un stage en Deep Learning à Casablanca" → {{"category": "goals", "content": "Cherche un stage en Deep Learning à Casablanca", "importance": 8}}

N'extrais PAS :
- Les informations déjà évidentes (l'étudiant est à l'ENIAD)
- Les questions rhétoriques ou demandes ponctuelles sans intérêt futur
- Les informations trop vagues ("je suis fatigué")

Si aucun fait persistant et important n'est détectable, réponds avec: []

Message étudiant: {user_message}
Réponse agent: {agent_response}

JSON uniquement (pas de texte autour) :"""


class MemoryManager:
    """
    Gère le cycle complet de mémoire long-terme des étudiants.
    Thread-safe et non-bloquant — prévu pour usage en BackgroundTasks FastAPI.
    """

    async def extract_and_store(
        self,
        user_id: int,
        user_message: str,
        agent_response: str,
    ) -> int:
        """
        Extrait les faits importants de l'échange via LLM et les persiste en DB.
        Crée sa propre session DB pour usage en background task.
        Retourne le nombre de mémoires ajoutées.
        """
        from backend.database import get_db

        db = next(get_db())
        try:
            facts = await self._extract_facts(user_message, agent_response)
            if not facts:
                return 0

            from backend.models import Memory

            added = 0
            for fact in facts[:5]:
                content = str(fact.get("content", "")).strip()
                category = str(fact.get("category", "personal"))
                importance = min(10, max(1, int(fact.get("importance", 5))))

                if not content or len(content) < 10:
                    continue
                if category not in ("academic", "personal", "preferences", "goals"):
                    category = "personal"

                # Exact-duplicate guard
                exists = (
                    db.query(Memory)
                    .filter(Memory.user_id == user_id, Memory.content == content)
                    .first()
                )
                if exists:
                    continue

                db.add(
                    Memory(
                        user_id=user_id,
                        category=category,
                        content=content,
                        importance=importance,
                        expires_at=datetime.utcnow() + timedelta(days=90),
                    )
                )
                added += 1

            if added > 0:
                db.commit()
                logger.info(
                    "MemoryManager: %d mémoire(s) stockée(s) pour user_id=%s",
                    added,
                    user_id,
                )
            return added

        except Exception as exc:
            logger.error("MemoryManager.extract_and_store error: %s", exc)
            try:
                db.rollback()
            except Exception:
                pass
            return 0
        finally:
            db.close()

    def load_memories(
        self,
        user_id: int,
        db_session,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Charge les mémoires les plus importantes et récentes de l'étudiant.
        Filtre les mémoires expirées.
        """
        try:
            from backend.models import Memory

            now = datetime.utcnow()
            rows = (
                db_session.query(Memory)
                .filter(
                    Memory.user_id == user_id,
                    (Memory.expires_at.is_(None)) | (Memory.expires_at > now),
                )
                .order_by(Memory.importance.desc(), Memory.created_at.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "category": m.category,
                    "content": m.content,
                    "importance": m.importance,
                }
                for m in rows
            ]
        except Exception as exc:
            logger.error("MemoryManager.load_memories error: %s", exc)
            return []

    async def _extract_facts(
        self,
        user_message: str,
        agent_response: str,
    ) -> List[Dict[str, Any]]:
        """Appelle le LLM pour identifier les faits mémorables dans l'échange."""
        try:
            from backend.agents.orchestrator import get_llm
            from langchain_core.messages import HumanMessage

            prompt = _EXTRACTION_PROMPT.format(
                user_message=user_message[:600],
                agent_response=agent_response[:600],
            )

            llm = get_llm()
            resp = await llm.ainvoke([HumanMessage(content=prompt)])
            text = resp.content.strip()

            # Strip markdown code fences if present
            if "```json" in text:
                text = text.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in text:
                text = text.split("```", 1)[1].split("```", 1)[0].strip()

            facts = json.loads(text)
            return facts if isinstance(facts, list) else []

        except json.JSONDecodeError:
            return []
        except Exception as exc:
            logger.warning("Memory extraction LLM error: %s", exc)
            return []


# ── Singleton ────────────────────────────────────────────────────────────────

_instance: Optional[MemoryManager] = None


def get_memory_manager() -> MemoryManager:
    global _instance
    if _instance is None:
        _instance = MemoryManager()
    return _instance
