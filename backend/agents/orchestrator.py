"""
LangGraph-style Orchestrator — Architecture Agentique
Implémente le cycle : Percevoir → Planifier → Agir → Observer → Répondre
via un graphe d'états explicite (StateGraph pattern).
"""

from typing import Dict, List, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
import json

try:
    from langchain_openai import ChatOpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    ChatOpenAI = None

try:
    from langchain_groq import ChatGroq
    _GROQ_AVAILABLE = True
except ImportError:
    _GROQ_AVAILABLE = False
    ChatGroq = None

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from backend.config import get_settings

settings = get_settings()


# ── État du graphe ─────────────────────────────────────────────────────────────

@dataclass
class AgentState:
    """
    État partagé entre tous les noeuds du graphe.
    Chaque noeud lit et enrichit cet état.
    """
    # Entrée
    user_message: str = ""
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    user_context: Dict[str, Any] = field(default_factory=dict)

    # Noeud PERCEVOIR
    intent: str = ""
    intent_confidence: float = 0.0
    keywords_detected: List[str] = field(default_factory=list)

    # Noeud PLANIFIER
    selected_agent: str = "admin"
    plan: str = ""
    sub_tasks: List[str] = field(default_factory=list)

    # Noeud AGIR
    agent_response: str = ""
    action_taken: str = ""

    # Noeud OBSERVER
    response_quality: float = 0.0
    needs_retry: bool = False
    iteration_count: int = 0
    max_iterations: int = 2
    observation_notes: str = ""

    # Noeud RÉPONDRE
    final_response: str = ""
    agent_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Contrôle du graphe
    current_node: str = "percevoir"
    error: Optional[str] = None


# ── Nœuds du graphe ────────────────────────────────────────────────────────────

class GraphNodes:
    """Implémentation des 5 noeuds du cycle agentique."""

    AGENTS_CONFIG = {
        "admin": {
            "name": "Agent Administratif",
            "keywords": ["faq", "document", "procedure", "regle", "formulaire",
                         "attestation", "inscription", "administratif", "guide",
                         "emploi du temps", "horaire", "eniad", "filiere", "convention",
                         "stage", "bourse", "scolarite", "semestre", "examen date",
                         "planning examen", "calendrier examen", "campus"],
            "prompt": """Tu es l'Agent Administratif de SmartStudent.
Tu aides les étudiants avec : FAQ institutionnelles, procédures administratives,
génération de documents, règlement intérieur.
Sois précis, clair et oriente l'étudiant vers les bons services si nécessaire."""
        },
        "planning": {
            "name": "Agent Planning",
            "keywords": ["calendrier", "planning", "deadline", "date", "devoir",
                         "emploi du temps", "rappel", "semaine", "planifier", "organiser"],
            "prompt": """Tu es l'Agent Planning de SmartStudent.
Tu aides les étudiants avec : gestion du temps, deadlines, emploi du temps,
organisation des révisions, rappels intelligents.
Donne des conseils pratiques et structurés."""
        },
        "exams": {
            "name": "Agent Examens",
            "keywords": ["examen", "quiz", "test", "revision", "note", "qcm",
                         "exercice", "controle", "score", "evaluat"],
            "prompt": """Tu es l'Agent Examens de SmartStudent.
Tu aides les étudiants avec : préparation aux examens, quiz génératifs,
stratégies de révision, feedback adaptatif, suivi de progression.
Sois encourageant et pédagogue."""
        },
        "orientation": {
            "name": "Agent Orientation",
            "keywords": ["stage", "emploi", "cv", "lettre", "metier", "carriere",
                         "professionnel", "orientation", "entreprise", "job"],
            "prompt": """Tu es l'Agent Orientation de SmartStudent.
Tu aides les étudiants avec : conseils carrière, rédaction CV/LM,
recherche de stages, orientation professionnelle.
Sois inspirant et donne des conseils concrets."""
        },
        "campus": {
            "name": "Agent Campus",
            "keywords": ["evenement", "club", "association", "campus", "activite",
                         "groupe", "sport", "sortie", "conference", "workshop"],
            "prompt": """Tu es l'Agent Campus de SmartStudent.
Tu informes les étudiants sur : événements campus, clubs, associations,
activités parascolaires, formation de groupes de travail.
Sois enthousiaste et crée du lien social."""
        },
        "wellbeing": {
            "name": "Agent Bien-être",
            "keywords": ["stress", "anxiete", "sante", "bien-etre", "fatigue",
                         "motivation", "aide", "soutien", "depression", "mental"],
            "prompt": """Tu es l'Agent Bien-être de SmartStudent.
Tu soutiens les étudiants sur : gestion du stress, santé mentale, motivation,
équilibre vie étudiante, ressources d'aide psychologique.
Sois empathique, bienveillant et oriente vers des professionnels si nécessaire."""
        },
    }

    def __init__(self, llm):
        self.llm = llm

    # ── PERCEVOIR ──────────────────────────────────────────────────────────────
    def percevoir(self, state: AgentState) -> AgentState:
        """
        Noeud 1 : Analyse le message entrant.
        Extrait l'intention et les mots-clés détectés.
        """
        message_lower = state.user_message.lower()

        # Calcul du score pour chaque agent
        scores: Dict[str, int] = {}
        detected: Dict[str, List[str]] = {}

        for agent_id, config in self.AGENTS_CONFIG.items():
            matched = [kw for kw in config["keywords"] if kw in message_lower]
            scores[agent_id] = len(matched)
            detected[agent_id] = matched

        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]

        # Détection de la langue
        lang = state.user_context.get("language", "fr")

        # Catégorisation de l'intention
        if best_score >= 2:
            intent = f"demande_{best_agent}_precise"
            confidence = min(0.5 + best_score * 0.15, 0.95)
        elif best_score == 1:
            intent = f"demande_{best_agent}"
            confidence = 0.6
        else:
            intent = "demande_generale"
            confidence = 0.4
            best_agent = "admin"

        all_kw = [kw for kws in detected.values() for kw in kws]

        state.intent = intent
        state.intent_confidence = confidence
        state.keywords_detected = all_kw
        state.current_node = "planifier"
        return state

    # ── PLANIFIER ──────────────────────────────────────────────────────────────
    def planifier(self, state: AgentState) -> AgentState:
        """
        Noeud 2 : Sélectionne l'agent et planifie la réponse.
        Utilise le LLM pour un routage intelligent si l'intention est ambiguë.
        """
        # Si confiance élevée → routage direct
        if state.intent_confidence >= 0.6:
            agent_id = state.intent.replace("demande_", "").replace("_precise", "")
            agent_id = agent_id if agent_id in self.AGENTS_CONFIG else "admin"
            state.selected_agent = agent_id
            state.plan = f"Traitement direct par {self.AGENTS_CONFIG[agent_id]['name']}"
            state.sub_tasks = [f"Répondre à: {state.user_message[:80]}"]
        else:
            # Routage LLM pour les cas ambigus
            agents_desc = "\n".join(
                f"- {aid}: {cfg['name']} ({', '.join(cfg['keywords'][:4])})"
                for aid, cfg in self.AGENTS_CONFIG.items()
            )
            routing_prompt = f"""Tu es le routeur de SmartStudent.
Agents disponibles:
{agents_desc}

Message de l'étudiant: "{state.user_message}"

Réponds UNIQUEMENT avec un objet JSON sur une seule ligne:
{{"agent": "<id_agent>", "raison": "<courte raison>"}}"""

            try:
                resp = self.llm.invoke([HumanMessage(content=routing_prompt)])
                result = json.loads(resp.content.strip())
                state.selected_agent = result.get("agent", "admin")
                state.plan = result.get("raison", "Routage LLM")
            except Exception:
                state.selected_agent = "admin"
                state.plan = "Routage par défaut"

            state.sub_tasks = [f"Analyser: {state.user_message[:80]}",
                               "Générer une réponse adaptée"]

        state.current_node = "agir"
        return state

    # ── AGIR ───────────────────────────────────────────────────────────────────
    def agir(self, state: AgentState) -> AgentState:
        """
        Noeud 3 : Exécute l'action — appelle l'agent spécialisé.
        """
        agent_id = state.selected_agent
        config = self.AGENTS_CONFIG.get(agent_id, self.AGENTS_CONFIG["admin"])

        # Construction du prompt système personnalisé
        system_prompt = config["prompt"]
        uc = state.user_context
        if uc:
            name = uc.get("full_name") or uc.get("username", "l'étudiant(e)")
            system_prompt += f"\n\nTu parles à {name}"
            if uc.get("major"):
                system_prompt += f", en {uc['major']}"
            if uc.get("year"):
                system_prompt += f", année {uc['year']}"
            system_prompt += "."

            # Injection de la mémoire long terme
            memories = uc.get("memories", [])
            if memories:
                memory_text = "\n".join(f"- [{m.get('category','info')}] {m.get('content','')}" for m in memories[:8])
                system_prompt += (
                    "\n\nMÉMOIRE LONG TERME (ce que tu sais déjà sur cet étudiant) :\n"
                    + memory_text
                    + "\nUtilise ces informations pour personnaliser ta réponse."
                )

        # Injection du contexte RAG pour l'agent admin
        if agent_id == "admin":
            try:
                from backend.services.rag_service import get_rag_service
                rag = get_rag_service()
                if rag.is_ready:
                    rag_context = rag.build_context(state.user_message, n_results=4)
                    if rag_context:
                        system_prompt += (
                            "\n\nCONTEXTE DOCUMENTAIRE ENIAD (utilise ces informations pour répondre) :\n"
                            + rag_context
                        )
            except Exception:
                pass

        # Construction des messages
        messages = [SystemMessage(content=system_prompt)]

        # Historique (5 derniers messages)
        for msg in state.conversation_history[-5:]:
            if msg.get("role") == "user":
                messages.append(HumanMessage(content=msg.get("content", "")))
            else:
                messages.append(AIMessage(content=msg.get("content", "")))

        messages.append(HumanMessage(content=state.user_message))

        try:
            response = self.llm.invoke(messages)
            state.agent_response = response.content
            state.action_taken = f"Appel {config['name']} (itération {state.iteration_count + 1})"
        except Exception as e:
            error_msg = str(e)
            import logging
            logging.getLogger(__name__).error(f"LLM error in agir node: {error_msg}")
            if "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
                state.agent_response = (
                    "⚠️ Le service IA est temporairement indisponible "
                    "(quota OpenAI dépassé). Veuillez réessayer plus tard "
                    "ou contacter l'administrateur."
                )
            elif "api" in error_msg.lower() and "key" in error_msg.lower():
                state.agent_response = (
                    "⚠️ Clé API OpenAI non configurée ou invalide."
                )
            else:
                state.agent_response = (
                    "Je rencontre une difficulté technique. "
                    "Veuillez réessayer ou contacter le support."
                )
            state.error = error_msg

        state.iteration_count += 1
        state.current_node = "observer"
        return state

    # ── OBSERVER ───────────────────────────────────────────────────────────────
    def observer(self, state: AgentState) -> AgentState:
        """
        Noeud 4 : Évalue la qualité de la réponse.
        Décide si une nouvelle itération est nécessaire.
        """
        response = state.agent_response
        notes = []
        quality = 1.0

        # Critères de qualité
        if len(response) < 30:
            quality -= 0.4
            notes.append("Réponse trop courte")

        if state.error:
            quality -= 0.5
            notes.append(f"Erreur: {state.error}")

        error_phrases = ["je ne sais pas", "i don't know", "erreur", "error"]
        if any(p in response.lower() for p in error_phrases):
            quality -= 0.2
            notes.append("Réponse incertaine détectée")

        if len(response) > 100 and "?" not in response[-100:]:
            quality += 0.1
            notes.append("Réponse complète et structurée")

        state.response_quality = max(0.0, min(quality, 1.0))
        state.observation_notes = "; ".join(notes) if notes else "Réponse satisfaisante"

        # Décision de réessayer
        state.needs_retry = (
            state.response_quality < 0.5
            and state.iteration_count < state.max_iterations
        )

        state.current_node = "agir" if state.needs_retry else "repondre"
        return state

    # ── RÉPONDRE ──────────────────────────────────────────────────────────────
    def repondre(self, state: AgentState) -> AgentState:
        """
        Noeud 5 : Formate et retourne la réponse finale.
        """
        agent_id = state.selected_agent
        config = self.AGENTS_CONFIG.get(agent_id, self.AGENTS_CONFIG["admin"])

        state.final_response = state.agent_response
        state.agent_name = config["name"]
        groq_key = getattr(settings, "GROQ_API_KEY", "")
        model_used = "llama-3.3-70b-versatile" if (groq_key and groq_key not in ("", "your-groq-api-key")) else settings.OPENAI_MODEL
        state.metadata = {
            "model": model_used,
            "agent_id": agent_id,
            "agent_name": config["name"],
            "intent": state.intent,
            "intent_confidence": round(state.intent_confidence, 2),
            "keywords": state.keywords_detected,
            "plan": state.plan,
            "iterations": state.iteration_count,
            "response_quality": round(state.response_quality, 2),
            "observation": state.observation_notes,
        }
        state.current_node = "end"
        return state


# ── Graphe d'états ─────────────────────────────────────────────────────────────

class LangGraphOrchestrator:
    """
    Orchestrateur basé sur le pattern StateGraph de LangGraph.

    Graphe d'exécution :

      [START]
         │
         ▼
    ┌─────────────┐
    │  PERCEVOIR  │  ← Analyse message + extraction intention
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  PLANIFIER  │  ← Sélection agent + construction plan
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐ ◄─────────────────────────────────┐
    │    AGIR     │  ← Appel agent spécialisé (LLM)   │
    └──────┬──────┘                                   │
           │                                          │
           ▼                                          │
    ┌─────────────┐       needs_retry == True         │
    │  OBSERVER   │ ─────────────────────────────────►┘
    └──────┬──────┘
           │ needs_retry == False
           ▼
    ┌─────────────┐
    │  RÉPONDRE   │  ← Formatage réponse finale
    └──────┬──────┘
           │
         [END]
    """

    def __init__(self):
        self.llm = self._build_llm()
        self.nodes = GraphNodes(self.llm)

        self._graph = {
            "percevoir": self.nodes.percevoir,
            "planifier": self.nodes.planifier,
            "agir":      self.nodes.agir,
            "observer":  self.nodes.observer,
            "repondre":  self.nodes.repondre,
        }

        self._transitions = {
            "percevoir": lambda s: "planifier",
            "planifier": lambda s: "agir",
            "agir":      lambda s: "observer",
            "observer":  lambda s: "agir" if s.needs_retry else "repondre",
            "repondre":  lambda s: "end",
        }

    def _build_llm(self):
        """Essaie Groq (gratuit) d'abord, replie sur OpenAI."""
        groq_key = getattr(settings, "GROQ_API_KEY", None)
        if _GROQ_AVAILABLE and groq_key and groq_key not in ("", "your-groq-api-key"):
            try:
                import logging
                logging.getLogger(__name__).info("LLM: utilisation de Groq (llama-3.1-70b)")
                return ChatGroq(
                    api_key=groq_key,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Groq init échoué: {e}. Repli sur OpenAI.")
        if _OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
            import logging
            logging.getLogger(__name__).info("LLM: utilisation de OpenAI")
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
                temperature=0.7,
            )
        raise RuntimeError("Aucun LLM disponible. Configure GROQ_API_KEY ou OPENAI_API_KEY dans backend/.env")

    def _run_graph(self, initial_state: AgentState) -> AgentState:
        """Exécute le graphe d'états jusqu'à END."""
        state = initial_state
        node_name = "percevoir"
        visited = []

        while node_name != "end":
            visited.append(node_name)
            # Exécute le noeud
            state = self._graph[node_name](state)
            # Détermine la transition suivante
            node_name = self._transitions[node_name](state)

            # Sécurité anti-boucle infinie
            if len(visited) > 20:
                state.final_response = state.agent_response
                break

        return state

    async def process_message(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Point d'entrée principal — interface compatible avec l'ancien orchestrateur.
        """
        # Initialisation de l'état
        initial_state = AgentState(
            user_message=user_message,
            conversation_history=conversation_history or [],
            user_context=user_context or {},
        )

        # Exécution du graphe
        final_state = self._run_graph(initial_state)

        return {
            "response":   final_state.final_response,
            "agent":      final_state.selected_agent,
            "agent_name": final_state.agent_name,
            "metadata":   final_state.metadata,
        }

    def get_graph_info(self) -> Dict[str, Any]:
        """Retourne la structure du graphe (utile pour la documentation)."""
        return {
            "nodes": list(self._graph.keys()) + ["end"],
            "edges": [
                {"from": "percevoir", "to": "planifier", "condition": "always"},
                {"from": "planifier", "to": "agir",      "condition": "always"},
                {"from": "agir",      "to": "observer",  "condition": "always"},
                {"from": "observer",  "to": "agir",      "condition": "needs_retry == True"},
                {"from": "observer",  "to": "repondre",  "condition": "needs_retry == False"},
                {"from": "repondre",  "to": "end",       "condition": "always"},
            ],
            "cycle": "Percevoir → Planifier → Agir → Observer → (Agir)* → Répondre",
        }


# Instance globale
orchestrator = LangGraphOrchestrator()

# Alias de compatibilité
Orchestrator = LangGraphOrchestrator
