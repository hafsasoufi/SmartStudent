"""
Orientation Agent — SmartStudent LangGraph ReAct Agent
Architecture : agent_node <-> tools_node loop (ReAct pattern)

Outils :
  1. rechercher_carrieres      — profils métiers par filière/compétences
  2. rechercher_offres_stage   — plateformes et guides de recherche de stage
  3. analyser_cv               — analyse critique d'un CV fourni par l'étudiant
  4. generer_lettre_motivation — génère une LM personnalisée
  5. preparer_entretien        — prépare questions techniques + comportementales
  6. conseiller_certifications — recommande certifications selon filière/objectif
  7. rechercher_orientation_kb — recherche sémantique dans la base de connaissances
"""
from __future__ import annotations

import json
import logging
from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# State
# ─────────────────────────────────────────────────────────────────────────────

class OrientationAgentState(TypedDict, total=False):
    messages:     Annotated[list, add_messages]
    user_id:      int
    user_context: dict


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _get_llm():
    from backend.agents.orchestrator import get_llm
    return get_llm()


def _search_orientation_kb(query: str, n_results: int = 4, category_filter: Optional[str] = None) -> list[dict]:
    """Recherche sémantique dans la collection ChromaDB orientation_kb."""
    try:
        from backend.services.rag_service import get_rag_service
        rag = get_rag_service()
        if not rag.is_ready:
            return []
        filter_meta = {"source_type": "orientation"}
        if category_filter:
            filter_meta["category"] = category_filter
        results = rag.query(query, n_results=n_results, filter_metadata=filter_meta)
        return results
    except Exception as exc:
        logger.warning("orientation_kb search error: %s", exc)
        return []


def _fallback_from_knowledge(query: str, category: Optional[str] = None) -> str:
    """Fallback : recherche directe dans ALL_ORIENTATION_DOCUMENTS si ChromaDB absent."""
    try:
        from backend.data.orientation_knowledge import ALL_ORIENTATION_DOCUMENTS
        query_lower = query.lower()
        matches = []
        for doc in ALL_ORIENTATION_DOCUMENTS:
            if category and doc.get("category") != category:
                continue
            score = sum(1 for word in query_lower.split() if word in doc.get("content", "").lower())
            if score > 0:
                matches.append((score, doc))
        matches.sort(key=lambda x: x[0], reverse=True)
        if not matches:
            return ""
        top = matches[:3]
        return "\n\n---\n".join(f"[{d['title']}]\n{d['content']}" for _, d in top)
    except Exception as exc:
        logger.warning("fallback_from_knowledge error: %s", exc)
        return ""


def _get_context(query: str, category: Optional[str] = None, n: int = 4) -> str:
    """Retourne du contexte documentaire, depuis ChromaDB ou le fallback statique."""
    results = _search_orientation_kb(query, n_results=n, category_filter=category)
    if results:
        parts = []
        for i, r in enumerate(results, 1):
            meta = r.get("metadata", {})
            title = meta.get("title", f"Document {i}")
            parts.append(f"[{title}]\n{r['content']}")
        return "\n\n---\n".join(parts)
    return _fallback_from_knowledge(query, category)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 1 — Recherche de profils de carrière
# ─────────────────────────────────────────────────────────────────────────────

@tool
def rechercher_carrieres(filiere: str, interets: str = "", annee: int = 1) -> str:
    """Recherche les métiers et débouchés adaptés à la filière et aux intérêts de l'étudiant.
    filiere: IA, GINF, IRSI ou ROC.
    interets: domaines d'intérêt (ex: 'cybersécurité, cloud, data').
    annee: année d'étude (1, 2 ou 3).
    """
    query = f"métier carrière débouchés {filiere} {interets}".strip()
    context = _get_context(query, category="career_profile", n=4)
    path_ctx = _get_context(f"parcours carrière {filiere}", category="career_path", n=2)

    if not context:
        return json.dumps({
            "status": "no_data",
            "message": "Aucun profil métier trouvé dans la base. Réponds avec tes connaissances générales.",
        }, ensure_ascii=False)

    return json.dumps({
        "status": "ok",
        "filiere": filiere,
        "annee": annee,
        "interets": interets,
        "profils_metiers": context,
        "parcours_recommande": path_ctx,
        "instruction": (
            "Utilise ces données pour présenter les débouchés adaptés à l'étudiant. "
            "Sois concret : cite des entreprises marocaines qui recrutent, "
            "des salaires indicatifs, et les compétences à développer en priorité."
        ),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 2 — Recherche de stages / PFA / PFE
# ─────────────────────────────────────────────────────────────────────────────

@tool
def rechercher_offres_stage(
    filiere: str,
    type_stage: str = "pfa",
    ville: str = "",
    domaine: str = "",
) -> str:
    """Fournit des informations sur les stages disponibles et comment les trouver.
    filiere: IA, GINF, IRSI ou ROC.
    type_stage: 'ete' (2 mois), 'pfa' (3-4 mois), 'pfe' (4-6 mois).
    ville: Casablanca, Rabat, Berkane, etc. (optionnel).
    domaine: Data Science, Cybersécurité, Web, IoT... (optionnel).
    """
    query = f"stage {type_stage} {filiere} {domaine} {ville} trouver candidature".strip()
    context = _get_context(query, category="internship_offer", n=4)
    platform_ctx = _get_context("plateformes stage Maroc Rekrute LinkedIn", n=2)

    durees = {"ete": "1 à 2 mois (juillet-août)", "pfa": "3 à 4 mois", "pfe": "4 à 6 mois"}
    duree = durees.get(type_stage.lower(), "durée variable")

    return json.dumps({
        "status": "ok",
        "type_stage": type_stage,
        "duree_type": duree,
        "filiere": filiere,
        "domaine": domaine,
        "ville_cible": ville or "non spécifiée",
        "guide_recherche": context,
        "plateformes": platform_ctx,
        "instruction": (
            "Présente les étapes concrètes pour trouver ce stage : "
            "plateformes à utiliser (Rekrute.ma, Stage.ma, LinkedIn), "
            "calendrier de candidature (quand postuler), "
            "entreprises marocaines à cibler pour la filière, "
            "et comment rédiger l'email de candidature spontanée."
        ),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 3 — Analyse de CV
# ─────────────────────────────────────────────────────────────────────────────

@tool
def analyser_cv(contenu_cv: str, filiere: str = "", poste_cible: str = "") -> str:
    """Analyse le CV fourni par l'étudiant et retourne une critique structurée avec améliorations.
    contenu_cv: texte brut ou description du CV de l'étudiant.
    filiere: filière de l'étudiant (IA, GINF, IRSI, ROC).
    poste_cible: poste ou type de stage visé (ex: 'Data Scientist', 'Développeur Web').
    """
    guide_ctx = _get_context(
        f"CV guide structure sections compétences {filiere} {poste_cible}", n=4
    )
    erreurs_ctx = _get_context("erreurs courantes CV étudiant ENIAD", n=2)

    return json.dumps({
        "status": "ok",
        "cv_recu": contenu_cv[:2000],
        "filiere": filiere,
        "poste_cible": poste_cible,
        "guide_cv": guide_ctx,
        "erreurs_a_eviter": erreurs_ctx,
        "instruction": (
            "Analyse ce CV en 4 parties :\n"
            "1. POINTS FORTS : ce qui est bien fait\n"
            "2. POINTS À AMÉLIORER : manques, erreurs de format, formulations faibles\n"
            "3. COMPÉTENCES MANQUANTES : ce que le recruteur pour ce poste va chercher "
            "et qui est absent du CV\n"
            "4. VERSION AMÉLIORÉE : propose au moins 3 formulations concrètes pour remplacer "
            "les parties faibles identifiées.\n"
            "Sois direct, précis et constructif."
        ),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 4 — Génération de lettre de motivation
# ─────────────────────────────────────────────────────────────────────────────

@tool
def generer_lettre_motivation(
    poste: str,
    entreprise: str,
    filiere: str,
    annee: int,
    competences: str = "",
    projet_academique: str = "",
    type_entreprise: str = "multinationale",
) -> str:
    """Génère une lettre de motivation personnalisée et complète.
    poste: intitulé exact du poste/stage (ex: 'Stage PFA Data Scientist').
    entreprise: nom de l'entreprise cible.
    filiere: filière ENIAD (IA, GINF, IRSI, ROC).
    annee: année d'étude (1, 2, 3).
    competences: compétences clés de l'étudiant (ex: 'Python, TensorFlow, SQL').
    projet_academique: meilleur projet avec résultat (ex: 'CNN classification agricole 94%').
    type_entreprise: 'startup', 'multinationale' ou 'secteur_public'.
    """
    template_key = f"template {type_entreprise}"
    template_ctx = _get_context(template_key, category="motivation_letter", n=2)
    guide_ctx = _get_context("structure lettre motivation guide", category="motivation_letter", n=2)

    career_ctx = _get_context(f"métier {poste} {filiere}", category="career_profile", n=2)

    return json.dumps({
        "status": "ok",
        "poste": poste,
        "entreprise": entreprise,
        "filiere": filiere,
        "annee": annee,
        "competences": competences,
        "projet": projet_academique,
        "type_entreprise": type_entreprise,
        "template_reference": template_ctx,
        "guide_structure": guide_ctx,
        "context_metier": career_ctx,
        "instruction": (
            f"Génère une lettre de motivation COMPLÈTE et PERSONNALISÉE pour :\n"
            f"- Poste : {poste}\n"
            f"- Entreprise : {entreprise}\n"
            f"- Profil : étudiant {filiere} ENIAD Berkane, {annee}ème année\n"
            f"- Compétences : {competences or 'à déduire de la filière'}\n"
            f"- Projet phare : {projet_academique or 'à compléter par l étudiant'}\n\n"
            "La lettre doit :\n"
            "1. Faire 1 page (300-400 mots)\n"
            "2. Avoir 4 paragraphes : accroche entreprise / profil académique / valeur ajoutée / call-to-action\n"
            "3. Éviter les clichés ('motivé et dynamique', 'ce stage m enrichira')\n"
            "4. Mentionner un élément concret sur l'entreprise dans l'accroche\n"
            "5. Inclure un résultat chiffré du projet académique\n"
            "Génère la lettre complète et prête à envoyer."
        ),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 5 — Préparation à l'entretien
# ─────────────────────────────────────────────────────────────────────────────

@tool
def preparer_entretien(
    poste: str,
    filiere: str,
    entreprise: str = "",
    type_entretien: str = "technique",
    niveau: str = "debutant",
) -> str:
    """Prépare l'étudiant pour un entretien : questions techniques + comportementales + conseils.
    poste: poste visé (ex: 'Data Scientist', 'Développeur Full-Stack', 'Ingénieur Réseaux').
    filiere: IA, GINF, IRSI ou ROC.
    entreprise: nom de l'entreprise (optionnel — pour contexte spécifique).
    type_entretien: 'technique', 'comportemental' ou 'mixte'.
    niveau: 'debutant' (stage été/PFA), 'confirme' (PFE/premier emploi).
    """
    # Questions techniques selon filière/poste
    tech_map = {
        "IA": "python_ml",
        "GINF": "java_web",
        "IRSI": "networks_security",
        "ROC": "embedded_iot",
    }
    subcategory_hint = tech_map.get(filiere.upper(), "python_ml")
    tech_query = f"questions entretien technique {poste} {filiere} {subcategory_hint} {niveau}"
    tech_ctx = _get_context(tech_query, category="interview_technical", n=3)

    # Questions comportementales
    behavioral_ctx = _get_context(
        "entretien comportemental STAR teamwork failure",
        category="interview_behavioral", n=2
    )

    return json.dumps({
        "status": "ok",
        "poste": poste,
        "filiere": filiere,
        "entreprise": entreprise or "non spécifiée",
        "type_entretien": type_entretien,
        "niveau": niveau,
        "questions_techniques": tech_ctx,
        "questions_comportementales": behavioral_ctx,
        "instruction": (
            f"Prépare l'étudiant pour son entretien de {type_entretien} pour le poste {poste}.\n\n"
            "Format de réponse :\n"
            "**QUESTIONS TECHNIQUES ATTENDUES** (5-7 questions avec réponses attendues)\n"
            "**QUESTIONS COMPORTEMENTALES** (3-5 questions avec conseils de réponse STAR)\n"
            "**CONSEILS PRATIQUES** : comment se présenter, durée typique, tenue, "
            "questions à poser au recruteur en fin d'entretien\n"
            f"{'**SPÉCIFIQUE ENTREPRISE** : ' + entreprise + ' — mentionne ce que tu sais de cette entreprise au Maroc' if entreprise else ''}\n\n"
            "Inclus des exemples de réponses adaptées au contexte étudiant ENIAD (projets académiques)."
        ),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 6 — Conseils certifications & compétences
# ─────────────────────────────────────────────────────────────────────────────

@tool
def conseiller_certifications(
    filiere: str,
    objectif: str = "",
    budget: str = "gratuit",
    annee: int = 1,
) -> str:
    """Recommande des certifications et compétences à acquérir selon le profil.
    filiere: IA, GINF, IRSI ou ROC.
    objectif: domaine visé (ex: 'cloud', 'data', 'cybersécurité', 'web').
    budget: 'gratuit', 'faible' (<500 MAD), 'moyen' (500-2000 MAD), 'illimité'.
    annee: année d'étude (1, 2, 3) — influence la priorité des certifications.
    """
    query = f"certification {filiere} {objectif} {budget} recommandée".strip()
    cert_ctx = _get_context(query, category="skills_certification", n=4)

    return json.dumps({
        "status": "ok",
        "filiere": filiere,
        "objectif": objectif,
        "budget": budget,
        "annee": annee,
        "certifications_recommandees": cert_ctx,
        "instruction": (
            f"Recommande les certifications les plus adaptées pour :\n"
            f"- Filière : {filiere} | Objectif : {objectif or 'général'} | "
            f"Budget : {budget} | Année : {annee}\n\n"
            "Organise ta réponse en :\n"
            "1. **PRIORITÉ IMMÉDIATE** (à préparer cette année)\n"
            "2. **MOYEN TERME** (avant le PFA/PFE)\n"
            "3. **PARCOURS COMPLET** (sur 3 ans)\n\n"
            "Pour chaque certification, précise : nom exact, organisme, durée de préparation, "
            "coût réel, lien officiel et valeur sur le marché marocain."
        ),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Outil 7 — Recherche libre dans la base de connaissances orientation
# ─────────────────────────────────────────────────────────────────────────────

@tool
def rechercher_orientation_kb(query: str, categorie: str = "") -> str:
    """Recherche sémantique libre dans toute la base de connaissances orientation.
    query: question ou sujet à rechercher.
    categorie: filtre optionnel (career_profile, career_path, cv_guide,
               motivation_letter, interview_technical, interview_behavioral,
               skills_certification, internship_offer, networking_tips).
    """
    context = _get_context(query, category=categorie or None, n=4)
    if not context:
        return json.dumps({
            "status": "no_data",
            "message": "Aucun document pertinent trouvé. Réponds avec tes connaissances générales.",
        }, ensure_ascii=False)
    return json.dumps({
        "status": "ok",
        "query": query,
        "contexte": context,
        "instruction": "Utilise ces informations pour répondre précisément à la question de l'étudiant.",
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Tools list
# ─────────────────────────────────────────────────────────────────────────────

_TOOLS = [
    rechercher_carrieres,
    rechercher_offres_stage,
    analyser_cv,
    generer_lettre_motivation,
    preparer_entretien,
    conseiller_certifications,
    rechercher_orientation_kb,
]


# ─────────────────────────────────────────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT_TEMPLATE = """Tu es l'Agent Orientation de SmartStudent — ENIAD Berkane.
Tu parles à {nom}, filière {filiere}, {annee}ème année.

TON RÔLE :
Tu accompagnes les étudiants ENIAD dans toute leur démarche d'orientation professionnelle :
découverte des métiers, recherche de stage, rédaction de CV et lettre de motivation,
préparation aux entretiens, choix de certifications et développement du réseau professionnel.

OUTILS DISPONIBLES — utilise-les systématiquement avant de répondre :
1. rechercher_carrieres(filiere, interets, annee) → métiers et débouchés par filière
2. rechercher_offres_stage(filiere, type_stage, ville, domaine) → guide recherche de stage
3. analyser_cv(contenu_cv, filiere, poste_cible) → critique et amélioration d'un CV
4. generer_lettre_motivation(poste, entreprise, filiere, annee, competences, projet_academique, type_entreprise) → génère une LM complète
5. preparer_entretien(poste, filiere, entreprise, type_entretien, niveau) → questions + conseils entretien
6. conseiller_certifications(filiere, objectif, budget, annee) → certifications recommandées
7. rechercher_orientation_kb(query, categorie) → recherche libre dans la base de connaissances

RÈGLES IMPORTANTES :
- Utilise TOUJOURS un outil avant de répondre — ne réponds jamais de mémoire sans consulter la base.
- Si l'étudiant fournit son CV, utilise analyser_cv avec le texte fourni.
- Si l'étudiant demande une lettre de motivation, utilise generer_lettre_motivation même si certains champs sont vides (tu les déduiras).
- Pour une préparation entretien, utilise preparer_entretien avec type_entretien='mixte' par défaut.
- Adapte toujours tes réponses au contexte marocain : entreprises marocaines, salaires en MAD, plateformes locales (Rekrute.ma, Stage.ma).
- Sois CONCRET et ACTIONNABLE : donne des noms, des liens, des chiffres, des exemples réels.
- Encourage et motive l'étudiant, mais sois honnête sur les efforts nécessaires.
- Réponds en français (ou en arabe si l'étudiant écrit en arabe).

CONTEXTE ÉTUDIANT :
{memories_context}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Agent Node
# ─────────────────────────────────────────────────────────────────────────────

async def agent_node(state: OrientationAgentState) -> dict:
    ctx = state.get("user_context") or {}
    nom = ctx.get("full_name") or ctx.get("username") or "l'étudiant(e)"
    filiere = ctx.get("major") or "filière non renseignée"
    annee = ctx.get("year") or "?"

    # Injection mémoire long terme
    memories: list = ctx.get("memories") or []
    if memories:
        mem_lines = "\n".join(
            f"- [{m.get('category', 'info')}] {m.get('content', '')}"
            for m in memories[:8]
        )
        memories_context = f"Mémoires connues sur cet étudiant :\n{mem_lines}"
    else:
        memories_context = "Aucune mémoire spécifique disponible pour cet étudiant."

    system_prompt = _SYSTEM_PROMPT_TEMPLATE.format(
        nom=nom,
        filiere=filiere,
        annee=annee,
        memories_context=memories_context,
    )

    try:
        llm = _get_llm().bind_tools(_TOOLS)
        messages = [SystemMessage(content=system_prompt)] + list(state.get("messages", []))
        resp = await llm.ainvoke(messages)
        return {"messages": [resp]}
    except Exception as exc:
        logger.error("OrientationAgent agent_node error: %s", exc)
        fallback = (
            "Je rencontre une difficulté technique momentanée. "
            "Pour toute question d'orientation, vous pouvez aussi consulter le CIOVE de l'ENIAD "
            "(Centre d'Information, d'Orientation et de Vie Estudiantine) : "
            "https://eniad.ump.ma/fr/centre-dinformation-dorientation-et-de-la-vie-estudiantine-ciove"
        )
        return {"messages": [AIMessage(content=fallback)]}


# ─────────────────────────────────────────────────────────────────────────────
# Graph compilation
# ─────────────────────────────────────────────────────────────────────────────

def _build_orientation_graph():
    g = StateGraph(OrientationAgentState)
    g.add_node("agent", agent_node)
    g.add_node("tools", ToolNode(_TOOLS))
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", tools_condition)
    g.add_edge("tools", "agent")
    return g.compile(checkpointer=MemorySaver())


_graph_instance = None


def get_compiled_orientation_graph():
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = _build_orientation_graph()
        logger.info("OrientationAgent ReAct graph compiled")
    return _graph_instance


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

class OrientationAgent:
    """Agent Orientation SmartStudent — LangGraph ReAct."""

    def __init__(self):
        self._graph = get_compiled_orientation_graph()

    async def process(
        self,
        user_message: str,
        user_id: int,
        user_context: dict,
        conversation_id: str = "default",
    ) -> dict:
        thread_id = f"orientation_{conversation_id}"
        initial: OrientationAgentState = {
            "messages": [HumanMessage(content=user_message)],
            "user_id": user_id,
            "user_context": user_context,
        }
        config = {"configurable": {"thread_id": thread_id}}
        try:
            result = await self._graph.ainvoke(initial, config=config)
        except Exception as exc:
            logger.error("OrientationAgent.process graph error: %s", exc)
            return {"response": "Le service d'orientation est temporairement indisponible. Veuillez réessayer."}

        last_ai = next(
            (m for m in reversed(result.get("messages", [])) if isinstance(m, AIMessage)),
            None,
        )
        return {"response": str(last_ai.content) if last_ai else "Erreur interne."}


def get_orientation_agent() -> OrientationAgent:
    return OrientationAgent()


# ─────────────────────────────────────────────────────────────────────────────
# Indexation de la base de connaissances dans ChromaDB
# ─────────────────────────────────────────────────────────────────────────────

def index_orientation_knowledge(force: bool = False) -> int:
    """
    Indexe ALL_ORIENTATION_DOCUMENTS dans ChromaDB (collection eniad_docs avec source_type='orientation').
    Appelé au démarrage si la collection est vide ou si force=True.
    Retourne le nombre de documents indexés.
    """
    try:
        from backend.services.rag_service import get_rag_service
        from backend.data.orientation_knowledge import ALL_ORIENTATION_DOCUMENTS

        rag = get_rag_service()
        if not rag.is_ready:
            logger.warning("RAG non disponible — indexation orientation ignorée")
            return 0

        existing_count = rag.document_count
        if existing_count > 0 and not force:
            # Vérifier si les docs orientation sont déjà présents
            sample = rag.query("métier carrière filière", n_results=1,
                               filter_metadata={"source_type": "orientation"})
            if sample:
                logger.info("Orientation KB déjà indexée (%d docs dans la collection)", existing_count)
                return 0

        docs_to_index = []
        for doc in ALL_ORIENTATION_DOCUMENTS:
            metadata = {
                "source_type": "orientation",
                "category": doc.get("category", "orientation"),
                "subcategory": doc.get("subcategory", ""),
                "relevant_majors": doc.get("relevant_majors", "IA,GINF,IRSI,ROC"),
                "title": doc.get("title", ""),
                "last_updated": "2026-06-22",
                "ttl_days": "365",
                "version": "1",
            }
            docs_to_index.append({
                "id": f"orientation_{doc['id']}",
                "text": f"{doc['title']}\n\n{doc['content']}",
                "metadata": metadata,
            })

        added = rag.add_documents_batch(docs_to_index)
        logger.info("Orientation KB indexée : %d documents ajoutés", added)
        return added

    except Exception as exc:
        logger.error("index_orientation_knowledge error: %s", exc)
        return 0
