"""
LangGraph Orchestrator — SmartStudent
Architecture multi-agents orchestree par un vrai StateGraph LangGraph compile.

Graphe :
  START
    |
    v
 percevoir  (analyse intention + mots-cles)
    |
    v
 planifier  (selectionne l'agent, LLM routing si ambigu)
    |
    v
  agir  <---------+  (appel LLM agent specialise)
    |              |
    v              | needs_retry
 observer ---------+
    |
    v (quality OK)
 repondre
    |
    v
   END
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Any, Dict, List, Literal, Optional, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

try:
    from langchain_groq import ChatGroq
    _GROQ_AVAILABLE = True
except ImportError:
    _GROQ_AVAILABLE = False
    ChatGroq = None  # type: ignore

try:
    from langchain_openai import ChatOpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    ChatOpenAI = None  # type: ignore

from backend.config import get_settings

settings = get_settings()


# ── LLM singleton ──────────────────────────────────────────────────────────────

_llm = None
_llm_api_key = None  # track which key the singleton was built with


def reset_llm():
    """Force re-initialization of the LLM singleton (e.g. after key change)."""
    global _llm, _llm_api_key
    _llm = None
    _llm_api_key = None


def _read_groq_key() -> str:
    """Read GROQ_API_KEY fresh from env file each time (bypasses lru_cache)."""
    import os
    from pathlib import Path
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GROQ_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.getenv("GROQ_API_KEY", "")


def get_llm():
    global _llm, _llm_api_key

    # Always read key fresh from .env to detect changes without restart
    groq_key = _read_groq_key()

    # Re-init only if key changed since last init
    if _llm is not None and _llm_api_key == groq_key:
        return _llm

    if _GROQ_AVAILABLE and groq_key and groq_key not in ("", "your-groq-api-key"):
        try:
            _llm = ChatGroq(
                api_key=groq_key,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            _llm_api_key = groq_key
            logger.info("LLM: Groq llama-3.3-70b-versatile (key: ...%s)", groq_key[-6:])
            return _llm
        except Exception as e:
            logger.warning(f"Groq init failed: {e}")

    openai_key = getattr(settings, "OPENAI_API_KEY", None)
    if _OPENAI_AVAILABLE and openai_key:
        _llm = ChatOpenAI(
            api_key=openai_key,
            model=getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.7,
        )
        _llm_api_key = openai_key
        logger.info("LLM: OpenAI")
        return _llm

    raise RuntimeError(
        "Aucun LLM disponible. Configurez GROQ_API_KEY ou OPENAI_API_KEY dans .env"
    )


# ── Configuration des 6 agents ─────────────────────────────────────────────────

AGENTS_CONFIG: Dict[str, Dict[str, Any]] = {
    "home": {
        "name": "Assistant Navigation",
        "keywords": [
            # Questions sur les agents
            "quoi sert", "a quoi sert", "à quoi sert", "que fait l'agent",
            "agent admin", "agent exams", "agent campus", "agent planning",
            "agent orientation", "agent bien", "agent wellbeing",
            # Navigation dans l'app
            "comment acceder", "comment accéder", "ou trouver", "où trouver",
            "ou puis-je", "où puis-je", "ou faire", "où faire",
            "comment utiliser", "comment naviguer",
            "comment faire une reclamation", "comment faire une réclamation",
            "faire une reclamation", "faire une réclamation",
            "ou reclamation", "où reclamation",
            "comment generer", "comment générer", "trouver mes examens",
            "trouver mes modules", "trouver le planning",
            "consulter le reglement", "reglement interieur", "règlement intérieur",
            "ou est", "où est", "comment fonctionne",
            # Guide général
            "guide", "aide application", "aide app", "fonctionnalite", "fonctionnalité",
            "smartstudent", "application smartstudent",
        ],
        "prompt": "",  # handled by NavigationAgent
    },
    "admin": {
        "name": "Agent Administratif",
        "keywords": [
            # Documents & scolarité
            "attestation", "releve", "releve de notes", "certificat", "diplome",
            "carte etudiant", "carte perdue", "duplicata", "inscription", "reinscription",
            "scolarite", "document", "formulaire", "procedure", "administratif",
            # Changements & problèmes académiques
            "changement filiere", "filiere", "changer filiere", "probleme note",
            "erreur note", "contestation", "absence examen", "justificatif",
            # Stages & PFE
            "stage", "pfa", "pfe", "convention", "convention de stage", "encadrant",
            # IT & Numérique
            "wifi", "wi-fi", "reseau", "connexion", "mot de passe", "mdp",
            "plateforme", "moodle", "acces plateforme", "compte bloque", "support it",
            # Financier & social
            "bourse", "aide sociale", "aide financiere",
            # Vie étudiante
            "evenement", "club", "participer", "conference", "hackathon",
            # Général ENIAD
            "faq", "regle", "reglement", "eniad", "bourse", "scolarite",
        ],
        "prompt": (
            "Tu es l'Assistant Administratif de SmartStudent a l'ENIAD Berkane.\n"
            "Ton role est de GUIDER les etudiants : expliquer les demarches etape par etape,\n"
            "lister les documents requis, indiquer le bon service et la personne responsable.\n"
            "Tu n'agis pas a la place de l'etudiant : tu informes et tu orientes.\n"
            "Sois precis, clair et bienveillant."
        ),
    },
    "planning": {
        "name": "Agent Planning",
        "keywords": [
            "planning", "deadline", "date", "devoir", "emploi du temps",
            "rappel", "semaine", "planifier", "organiser", "tache",
        ],
        "prompt": (
            "Tu es l'Agent Planning de SmartStudent.\n"
            "Tu aides avec : gestion du temps, deadlines, emploi du temps, "
            "organisation des revisions, rappels intelligents.\n"
            "Donne des conseils pratiques et structures."
        ),
    },
    "exams": {
        "name": "Agent Examens",
        "keywords": [
            "examen", "quiz", "test", "revision", "note", "qcm",
            "exercice", "controle", "score", "evaluat",
        ],
        "prompt": (
            "Tu es l'Agent Examens de SmartStudent.\n"
            "Tu aides avec : preparation aux examens, quiz generatifs, "
            "strategies de revision, feedback adaptatif, suivi de progression.\n"
            "Sois encourageant et pedagogue."
        ),
    },
    "orientation": {
        "name": "Agent Orientation",
        "keywords": [
            "stage", "emploi", "cv", "lettre", "metier", "carriere",
            "professionnel", "orientation", "entreprise", "job",
        ],
        "prompt": (
            "Tu es l'Agent Orientation de SmartStudent.\n"
            "Tu aides avec : conseils carriere, redaction CV/LM, "
            "recherche de stages, orientation professionnelle.\n"
            "Sois inspirant et donne des conseils concrets."
        ),
    },
    "campus": {
        "name": "Agent Campus",
        "keywords": [
            "evenement", "club", "association", "activite", "parascolaire",
            "groupe", "sport", "sortie", "conference", "workshop", "atelier",
            "bibliotheque", "cafeteria", "salle", "vie etudiante",
            "absence", "exclusion", "reglement", "discipline", "tenue",
            "dress code", "comportement", "interdit", "sanction", "notation",
            "livre", "ouvrage", "emprunter", "reference", "nurlia", "secora",
            "ennovers", "riot", "al ataa", "enactus", "aei", "campus eniad",
            "gala", "forum entreprise", "hackathon", "portes ouvertes",
        ],
        "prompt": (
            "Tu es l'Agent Campus de l'ENIADB (Ecole Nationale de l'Intelligence Artificielle et du Digital de Berkane).\n"
            "Tu couvres : le reglement interieur (absences, examens, discipline), les clubs etudiants (SECORA, ENNOVERS, NURLIA, RIOT, AL ATAA, Enactus), "
            "les evenements, la bibliotheque (livres avec numeros de reference), et toutes les infos sur la vie a l'ENIADB.\n"
            "Reponds dans la langue de l'etudiant (francais ou arabe). Cite les articles du reglement quand pertinent. Ne jamais inventer d'informations."
        ),
    },
    "wellbeing": {
        "name": "Agent Bien-etre",
        "keywords": [
            "stress", "stresse", "anxiete", "anxieux", "sante", "bien-etre",
            "fatigue", "epuise", "burnout", "motivation", "demotive",
            "aide psychologique", "soutien", "depression", "mental",
            "panique", "surcharge", "difficile", "souffre", "detresse",
            "sommeil", "dors", "concentrer", "peur", "seul", "isole",
            "pleure", "triste", "perdu", "depassé", "depasse", "imposteur",
        ],
        "prompt": (
            "Tu es l'Agent Bien-etre de l'ENIADB, un assistant bienveillant et empathique.\n"
            "Tu ecoutes sans jugement, detects les signes de stress/burnout/anxiete, proposes des strategies concretes.\n"
            "Utilise 'tu', valide les emotions avant de conseiller. Pour les crises, oriente vers le 080 100 47 47 (gratuit, 24h/24).\n"
            "Ne jamais diagnostiquer ni prescrire. Reponds dans la langue de l'etudiant."
        ),
    },
}


# ── Etat partage du graphe (TypedDict LangGraph) ──────────────────────────────

class SmartStudentState(TypedDict, total=False):
    # Conversation — gere automatiquement par add_messages (LangGraph)
    messages: Annotated[list, add_messages]
    # Contexte utilisateur (profil, memoires long terme)
    user_context: Dict[str, Any]
    # Noeud PERCEVOIR
    intent: str
    intent_confidence: float
    keywords_detected: List[str]
    # Noeud PLANIFIER
    selected_agent: str
    plan: str
    # Noeud AGIR
    agent_response: str
    iteration_count: int
    error: Optional[str]
    # Noeud OBSERVER
    response_quality: float
    needs_retry: bool
    # Noeud REPONDRE
    final_response: str
    agent_name: str
    metadata: Dict[str, Any]


# ── Noeud 1 : PERCEVOIR ────────────────────────────────────────────────────────

def percevoir(state: SmartStudentState) -> dict:
    """Analyse le dernier message et extrait l'intention + l'agent cible."""
    # Recuprer le dernier message humain
    user_message = _last_human_message(state)
    uc = state.get("user_context") or {}

    # force_agent permet de bypasser le routage (ex: onglet admin)
    force = uc.get("force_agent")
    if force and force in AGENTS_CONFIG:
        return {
            "intent": f"force_{force}",
            "intent_confidence": 1.0,
            "keywords_detected": [],
            "selected_agent": force,
        }

    msg_lower = user_message.lower()
    scores: Dict[str, int] = {}
    detected: Dict[str, List[str]] = {}
    for agent_id, cfg in AGENTS_CONFIG.items():
        matched = [kw for kw in cfg["keywords"] if kw in msg_lower]
        scores[agent_id] = len(matched)
        detected[agent_id] = matched

    best_agent = max(scores, key=lambda k: scores[k])
    best_score = scores[best_agent]

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
    return {
        "intent": intent,
        "intent_confidence": confidence,
        "keywords_detected": all_kw,
        "selected_agent": best_agent,
    }


# ── Noeud 2 : PLANIFIER ────────────────────────────────────────────────────────

def planifier(state: SmartStudentState) -> dict:
    """Confirme l'agent selectionne. Si ambigu, utilise le LLM pour router."""
    confidence = state.get("intent_confidence") or 0.0
    agent_id = state.get("selected_agent") or "admin"
    intent = state.get("intent") or ""

    # Routage direct si confiance elevee ou force_agent
    if confidence >= 0.6 or intent.startswith("force_"):
        cfg_name = AGENTS_CONFIG.get(agent_id, AGENTS_CONFIG["admin"])["name"]
        return {
            "selected_agent": agent_id,
            "plan": f"Routage direct -> {cfg_name}",
        }

    # Routage LLM pour les cas ambigus
    user_message = _last_human_message(state)
    agents_desc = "\n".join(
        f"- {aid}: {cfg['name']} ({', '.join(cfg['keywords'][:3])})"
        for aid, cfg in AGENTS_CONFIG.items()
    )
    prompt = (
        f"Tu es le routeur de SmartStudent.\nAgents disponibles:\n{agents_desc}\n\n"
        f"Message etudiant: \"{user_message}\"\n\n"
        'Reponds UNIQUEMENT avec: {"agent": "<id>", "raison": "<raison>"}'
    )
    try:
        resp = get_llm().invoke([HumanMessage(content=prompt)])
        result = json.loads(resp.content.strip())
        selected = result.get("agent", "admin")
        if selected not in AGENTS_CONFIG:
            selected = "admin"
        return {"selected_agent": selected, "plan": result.get("raison", "Routage LLM")}
    except Exception:
        return {"selected_agent": "admin", "plan": "Routage par defaut"}


# ── Noeud 3 : AGIR ─────────────────────────────────────────────────────────────

async def agir(state: SmartStudentState) -> dict:
    """
    Dispatch vers le sous-graphe ReAct de l'agent specialise.
    Admin, Planning et Exams ont leurs propres graphes LangGraph avec outils reels.
    Campus, Orientation, Wellbeing utilisent un appel LLM enrichi (RAG + memoire).
    """
    agent_id = state.get("selected_agent") or "admin"
    cfg = AGENTS_CONFIG.get(agent_id, AGENTS_CONFIG["admin"])
    iteration = state.get("iteration_count") or 0
    uc = state.get("user_context") or {}
    user_id = int(uc.get("user_id") or 0)
    conv_id = str(uc.get("conversation_id") or f"user_{user_id}")
    user_msg = _last_human_message(state)

    try:
        # ── Agent Navigation (home) ───────────────────────────────────────────
        if agent_id == "home":
            from backend.agents.navigation_agent import NavigationAgent
            history = _extract_conversation_history(state)
            result = await NavigationAgent().process(user_msg, history, uc)
            response = result.get("response", "")

        # ── Agents avec sous-graphes ReAct complets ──────────────────────────
        elif agent_id == "admin":
            from backend.agents.admin_agent import AdminAgent
            result = await AdminAgent().process(user_msg, user_id, uc, conv_id)
            response = result.get("response", "")

        elif agent_id == "planning":
            from backend.agents.planning_agent import PlanningAgent
            result = await PlanningAgent().process(user_msg, user_id, uc, conv_id)
            response = result.get("response", "")

        elif agent_id == "exams":
            from backend.agents.exams_agent import ExamsAgent
            result = await ExamsAgent().process(user_msg, user_id, uc, conv_id)
            response = result.get("response", "")

        elif agent_id == "campus":
            from backend.agents.campus_agent import CampusAgent
            history = _extract_conversation_history(state)
            result = await CampusAgent().process(user_msg, history, uc)
            response = result.get("response", "")

        elif agent_id == "wellbeing":
            from backend.agents.wellbeing_agent import WellbeingAgent
            history = _extract_conversation_history(state)
            result = await WellbeingAgent().process(user_msg, history, uc)
            response = result.get("response", "")

        # ── Autres agents LLM enrichis (orientation) ─────────────────────────
        else:
            response = await _call_llm_agent(agent_id, cfg, state, uc, user_msg)

        return {
            "agent_response": response,
            "iteration_count": iteration + 1,
            "messages": [AIMessage(content=response, name=cfg["name"])],
            "error": None,
        }

    except Exception as e:
        err = str(e)
        logger.error(f"agir node error [{agent_id}]: {err}")
        if "quota" in err.lower() or "insufficient" in err.lower():
            fallback = "Service IA temporairement indisponible (quota). Reessayez plus tard."
        elif "api" in err.lower() and "key" in err.lower():
            fallback = "Cle API non configuree ou invalide."
        else:
            fallback = "Difficulte technique. Veuillez reessayer."
        return {
            "agent_response": fallback,
            "iteration_count": iteration + 1,
            "error": err,
        }


def _extract_conversation_history(state: SmartStudentState) -> List[Dict[str, str]]:
    """Extrait l'historique de conversation depuis l'etat LangGraph."""
    history = []
    for msg in (state.get("messages") or [])[-8:]:
        if isinstance(msg, HumanMessage):
            history.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            history.append({"role": "assistant", "content": msg.content})
    return history


async def _call_llm_agent(
    agent_id: str,
    cfg: Dict[str, Any],
    state: SmartStudentState,
    uc: Dict[str, Any],
    user_msg: str,
) -> str:
    """Appel LLM direct enrichi pour les agents sans sous-graphe ReAct (Campus, Orientation, Wellbeing)."""
    system_prompt = cfg["prompt"]

    # Personnalisation profil
    name = uc.get("full_name") or uc.get("username") or "l'etudiant(e)"
    system_prompt += f"\n\nTu parles a {name}"
    if uc.get("major"):
        system_prompt += f", en {uc['major']}"
    if uc.get("year"):
        system_prompt += f", annee {uc['year']}"
    system_prompt += "."

    # Injection memoire long terme
    memories: List[Dict] = uc.get("memories") or []
    if memories:
        mem_lines = "\n".join(
            f"- [{m.get('category', 'info')}] {m.get('content', '')}"
            for m in memories[:8]
        )
        system_prompt += (
            "\n\nMEMOIRE LONG TERME :\n" + mem_lines
            + "\nUtilise ces informations pour personnaliser ta reponse."
        )

    # RAG pour campus/orientation si pertinent
    if agent_id in ("campus", "orientation", "admin"):
        try:
            from backend.services.rag_service import get_rag_service
            rag = get_rag_service()
            if rag.is_ready and user_msg:
                rag_ctx = rag.build_context(user_msg, n_results=3)
                if rag_ctx:
                    system_prompt += (
                        "\n\nCONTEXTE DOCUMENTAIRE ENIAD :\n" + rag_ctx
                        + "\nBase ta reponse sur ces documents officiels."
                    )
        except Exception:
            pass

    lc_messages = [SystemMessage(content=system_prompt)]
    for msg in (state.get("messages") or [])[-6:]:
        if isinstance(msg, (HumanMessage, AIMessage, SystemMessage)):
            lc_messages.append(msg)
    if not any(isinstance(m, HumanMessage) for m in lc_messages[1:]):
        if user_msg:
            lc_messages.append(HumanMessage(content=user_msg))

    response = await get_llm().ainvoke(lc_messages)
    return response.content


# ── Noeud 4 : OBSERVER ────────────────────────────────────────────────────────

def observer(state: SmartStudentState) -> dict:
    """Evalue la qualite de la reponse et decide si retry necessaire."""
    response = state.get("agent_response") or ""
    iteration = state.get("iteration_count") or 0
    error = state.get("error")

    quality = 1.0
    if len(response) < 30:
        quality -= 0.4
    if error:
        quality -= 0.5
    if any(p in response.lower() for p in ["je ne sais pas", "i don't know", "erreur technique"]):
        quality -= 0.2
    if len(response) > 100:
        quality += 0.1
    quality = max(0.0, min(quality, 1.0))

    # Retry si qualite insuffisante ET moins de 2 iterations
    needs_retry = quality < 0.5 and iteration < 2

    return {"response_quality": quality, "needs_retry": needs_retry}


# ── Noeud 5 : REPONDRE ────────────────────────────────────────────────────────

def repondre(state: SmartStudentState) -> dict:
    """Formate et retourne la reponse finale enrichie de metadonnees."""
    agent_id = state.get("selected_agent") or "admin"
    cfg = AGENTS_CONFIG.get(agent_id, AGENTS_CONFIG["admin"])
    groq_key = getattr(settings, "GROQ_API_KEY", "")
    model = (
        "llama-3.3-70b-versatile"
        if groq_key and groq_key not in ("", "your-groq-api-key")
        else getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
    )
    return {
        "final_response": state.get("agent_response") or "",
        "agent_name": cfg["name"],
        "metadata": {
            "model": model,
            "agent_id": agent_id,
            "agent_name": cfg["name"],
            "intent": state.get("intent") or "",
            "intent_confidence": round(state.get("intent_confidence") or 0.0, 2),
            "keywords": state.get("keywords_detected") or [],
            "plan": state.get("plan") or "",
            "iterations": state.get("iteration_count") or 0,
            "response_quality": round(state.get("response_quality") or 0.0, 2),
            "graph": "LangGraph StateGraph",
        },
    }


# ── Arete conditionnelle ───────────────────────────────────────────────────────

def _should_retry(state: SmartStudentState) -> Literal["agir", "repondre"]:
    """Retourne le prochain noeud apres observer."""
    return "agir" if state.get("needs_retry") else "repondre"


# ── Construction et compilation du graphe ─────────────────────────────────────

def _build_graph():
    """Construit et compile le StateGraph LangGraph avec MemorySaver."""
    graph = StateGraph(SmartStudentState)

    # Ajout des noeuds
    graph.add_node("percevoir", percevoir)
    graph.add_node("planifier", planifier)
    graph.add_node("agir", agir)
    graph.add_node("observer", observer)
    graph.add_node("repondre", repondre)

    # Aretes fixes
    graph.set_entry_point("percevoir")
    graph.add_edge("percevoir", "planifier")
    graph.add_edge("planifier", "agir")
    graph.add_edge("agir", "observer")
    graph.add_edge("repondre", END)

    # Arete conditionnelle observer -> agir (retry) ou repondre (fin)
    graph.add_conditional_edges(
        "observer",
        _should_retry,
        {"agir": "agir", "repondre": "repondre"},
    )

    # Checkpointer MemorySaver (memoire courte par thread_id)
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# Graphe compile (singleton charge au premier appel)
_compiled_graph = None


def get_compiled_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = _build_graph()
        logger.info("LangGraph StateGraph compile avec MemorySaver")
    return _compiled_graph


# ── Utilitaire interne ─────────────────────────────────────────────────────────

def _last_human_message(state: SmartStudentState) -> str:
    """Retourne le contenu du dernier message humain dans l'etat."""
    for msg in reversed(state.get("messages") or []):
        if isinstance(msg, HumanMessage):
            return msg.content
        if isinstance(msg, dict) and msg.get("role") == "user":
            return msg.get("content", "")
    return ""


# ── Interface publique ─────────────────────────────────────────────────────────

class LangGraphOrchestrator:
    """
    Orchestrateur SmartStudent base sur LangGraph StateGraph.

    Graphe compile :
      [START] -> percevoir -> planifier -> agir -> observer
                                                      |
                                          needs_retry=True -> agir (retry)
                                          needs_retry=False -> repondre -> [END]

    Checkpointer : MemorySaver (memoire courte par thread_id/conversation)
    Memoire longue : injectee depuis PostgreSQL via user_context['memories']
    """

    def __init__(self):
        self._graph = get_compiled_graph()

    async def process_message(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Point d'entree principal.
        Interface backward-compatible avec l'API Flutter existante.

        Args:
            user_message: Message de l'etudiant
            conversation_history: Historique (non utilise — gere par checkpointer)
            user_context: Profil etudiant + memoires long terme + conversation_id
        """
        uc = user_context or {}

        # thread_id = conversation_id unique par module (gere la memoire courte)
        conv_id = uc.get("conversation_id") or uc.get("user_id") or "default"
        thread_id = f"user_{conv_id}" if isinstance(conv_id, int) else str(conv_id)

        initial_state: SmartStudentState = {
            "messages": [HumanMessage(content=user_message)],
            "user_context": uc,
            "intent": "",
            "intent_confidence": 0.0,
            "keywords_detected": [],
            "selected_agent": "admin",
            "plan": "",
            "agent_response": "",
            "iteration_count": 0,
            "response_quality": 0.0,
            "needs_retry": False,
            "final_response": "",
            "agent_name": "",
            "metadata": {},
            "error": None,
        }

        config = {"configurable": {"thread_id": thread_id}}

        try:
            result = await self._graph.ainvoke(initial_state, config=config)
            return {
                "response":   result.get("final_response") or "",
                "agent":      result.get("selected_agent") or "admin",
                "agent_name": result.get("agent_name") or "",
                "metadata":   result.get("metadata") or {},
            }
        except Exception as e:
            logger.error(f"Graph execution error: {e}", exc_info=True)
            return {
                "response":   "Une erreur s'est produite. Veuillez reessayer.",
                "agent":      "admin",
                "agent_name": "Agent Administratif",
                "metadata":   {"error": str(e)},
            }

    def get_graph_info(self) -> Dict[str, Any]:
        """Structure du graphe pour documentation et LangGraph Studio."""
        return {
            "type": "LangGraph StateGraph",
            "version": "0.2.x",
            "checkpointer": "MemorySaver",
            "nodes": ["percevoir", "planifier", "agir", "observer", "repondre"],
            "edges": [
                {"from": "__start__", "to": "percevoir"},
                {"from": "percevoir", "to": "planifier"},
                {"from": "planifier", "to": "agir"},
                {"from": "agir",      "to": "observer"},
                {"from": "observer",  "to": "agir",     "condition": "needs_retry == True"},
                {"from": "observer",  "to": "repondre", "condition": "needs_retry == False"},
                {"from": "repondre",  "to": "__end__"},
            ],
            "agents": list(AGENTS_CONFIG.keys()),
            "cycle": "percevoir -> planifier -> agir -> observer -> (agir)* -> repondre -> END",
        }


# ── Instance globale ───────────────────────────────────────────────────────────

orchestrator = LangGraphOrchestrator()

# Alias de compatibilite
Orchestrator = LangGraphOrchestrator
