"""
Agent Navigation — SmartStudent ENIAD Berkane
Guide intelligent de navigation : oriente l'étudiant vers le bon agent/fonctionnalité.
Stratégie : règles exhaustives (zéro token) → LLM fallback enrichi.
"""
from __future__ import annotations

import logging
import unicodedata
from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


# ── Normalisation ─────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Minuscules, sans accents, apostrophes/tirets → espace."""
    text = text.lower()
    for ch in ("'", "'", "`", "-", "_"):
        text = text.replace(ch, " ")
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


# ── Base de règles exhaustive ─────────────────────────────────────────────────
# Format : (liste de mots-clés à détecter dans le message normalisé, réponse)

NAV_RULES: List[tuple[list[str], str]] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # PRÉSENTATION GÉNÉRALE DE L'APPLICATION
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["quels agents", "quels modules", "que contient l application",
         "que fait l application", "qu est ce que smartstudent",
         "comment fonctionne l application", "comment utiliser l application",
         "aide moi a utiliser", "guide de l application", "presentation",
         "fonctionnalites disponibles", "quelles fonctionnalites",
         "quelles sections", "quelles parties"],
        (
            "SmartStudent contient **6 agents** accessibles depuis la page d'accueil :\n\n"
            "• **Admin** → attestations, conventions de stage/PFA/PFE, réclamations, Wi-Fi/Moodle, bourses\n"
            "• **Examens** → quiz, planning officiel des examens, analyse PDF, statistiques\n"
            "• **Planning** → tâches, deadlines, emploi du temps, plan de révision\n"
            "• **Orientation** → CV, lettres de motivation, stage/emploi, entretiens\n"
            "• **Campus** → règlement intérieur, clubs étudiants, événements, bibliothèque\n"
            "• **Bien-être** → gestion du stress, soutien psychologique, suivi d'humeur\n\n"
            "Appuyez sur la carte correspondante depuis la page d'accueil pour y accéder."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT ADMIN
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["a quoi sert la partie admin", "a quoi sert l agent admin",
         "que fait l agent admin", "role de l agent admin",
         "role de admin", "a quoi sert admin", "que fait admin",
         "expliquer admin", "presentation admin", "description admin"],
        (
            "L'agent **Admin** est votre assistant administratif. Il vous aide à :\n\n"
            "• Générer des **documents officiels** : attestation de scolarité, relevé de notes, "
            "convention de stage/PFA/PFE\n"
            "• Effectuer des **réclamations** : note erronée, absence injustifiée\n"
            "• Résoudre des **problèmes informatiques** : Wi-Fi, Moodle, compte bloqué\n"
            "• Obtenir des infos sur les **bourses et aides sociales**\n"
            "• Gérer les procédures d'**inscription et de réinscription**\n\n"
            "**Pour y accéder :** Appuyez sur la carte **Admin** depuis la page d'accueil."
        ),
    ),
    (
        ["convention de stage", "convention stage", "convention pfa", "convention pfe",
         "generer une convention", "creer une convention", "faire une convention",
         "je veux une convention", "obtenir une convention", "demander une convention"],
        (
            "Pour générer une **convention de stage**, accédez à l'agent **Admin** "
            "depuis la page d'accueil, puis demandez une **convention de stage**.\n\n"
            "L'agent vous guidera étape par étape pour remplir les informations "
            "(entreprise, dates, encadrant) et générer le document officiel."
        ),
    ),
    (
        ["attestation de scolarite", "attestation scolarite", "attestation",
         "je veux une attestation", "obtenir une attestation", "generer une attestation",
         "demander une attestation", "certificat de scolarite"],
        (
            "Pour obtenir une **attestation de scolarité**, accédez à l'agent **Admin** "
            "depuis la page d'accueil, puis demandez une **attestation de scolarité**.\n\n"
            "L'agent vous indiquera la procédure ou générera le document directement."
        ),
    ),
    (
        ["releve de notes", "releve notes", "mes notes", "voir mes notes",
         "obtenir mon releve", "telecharger mon releve"],
        (
            "Pour obtenir votre **relevé de notes**, accédez à l'agent **Admin** "
            "depuis la page d'accueil, puis demandez votre **relevé de notes**."
        ),
    ),
    (
        ["reclamation", "faire une reclamation", "je souhaite faire une reclamation",
         "contester une note", "note erronee", "note incorrecte", "erreur sur ma note",
         "probleme avec ma note", "signaler un probleme", "absence injustifiee",
         "justifier une absence", "contester"],
        (
            "Pour effectuer une **réclamation**, accédez à l'agent **Admin** depuis la page "
            "d'accueil, puis décrivez votre problème (note erronée, absence injustifiée, etc.).\n\n"
            "L'agent vous guidera dans la procédure de réclamation et vous indiquera "
            "le service compétent à contacter."
        ),
    ),
    (
        ["wifi", "wi fi", "connexion internet", "probleme internet", "reseau",
         "moodle", "acces plateforme", "compte bloque", "mot de passe oublie",
         "reinitialiser mot de passe", "support informatique", "support it",
         "probleme informatique", "compte desactive"],
        (
            "Pour un problème de **Wi-Fi, Moodle ou compte bloqué**, accédez à l'agent **Admin** "
            "depuis la page d'accueil, puis décrivez votre problème technique.\n\n"
            "L'agent vous guidera vers le support informatique ou la procédure de "
            "réinitialisation adaptée."
        ),
    ),
    (
        ["bourse", "aide sociale", "aide financiere", "aide financiere", "crous",
         "bourse etudiant", "demande de bourse"],
        (
            "Pour des informations sur les **bourses et aides sociales**, accédez à l'agent "
            "**Admin** depuis la page d'accueil, puis demandez des informations sur les bourses."
        ),
    ),
    (
        ["inscription", "reinscription", "procedure d inscription", "s inscrire",
         "renouveler inscription", "dossier d inscription"],
        (
            "Pour les procédures d'**inscription ou de réinscription**, accédez à l'agent "
            "**Admin** depuis la page d'accueil. Il vous détaillera les étapes et documents requis."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT EXAMENS
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["a quoi sert l agent exams", "a quoi sert l agent examens",
         "a quoi sert la partie examens", "que fait l agent exams",
         "role de l agent examens", "presentation examens", "description examens",
         "a quoi sert exams"],
        (
            "L'agent **Examens** est votre assistant de préparation académique. Il offre :\n\n"
            "• Onglet **Agent IA** → quiz personnalisés, examens blancs, conseils de révision\n"
            "• Onglet **Planning** → planning officiel des examens (dates, salles, horaires)\n"
            "• Onglet **Assistant PDF** → posez des questions sur vos cours PDF\n"
            "• Onglet **Modules** → liste de vos modules par semestre\n"
            "• Onglet **Stats** → vos statistiques et historique de quiz\n\n"
            "**Pour y accéder :** Appuyez sur la carte **Examens** depuis la page d'accueil."
        ),
    ),
    (
        ["planning officiel", "planning des examens", "planning d examens",
         "dates des examens", "salles des examens", "horaires des examens",
         "calendrier des examens", "quand sont mes examens", "voir le planning des examens",
         "consulter le planning", "je veux le planning", "voir le planning"],
        (
            "Pour consulter le **planning officiel des examens**, accédez à l'agent **Examens** "
            "depuis la page d'accueil, puis ouvrez l'onglet **Planning**.\n\n"
            "Vous y trouverez les dates, horaires et salles de tous vos examens."
        ),
    ),
    (
        ["preparer mes examens", "preparer a l examen", "preparer l examen",
         "reviser", "faire des revisions", "revision", "entrainement",
         "faire un quiz", "generer un quiz", "quiz", "qcm", "examen blanc",
         "tester mes connaissances", "exercices", "questions"],
        (
            "Pour **préparer vos examens**, accédez à l'agent **Examens** depuis la page "
            "d'accueil, puis utilisez l'onglet **Agent IA**.\n\n"
            "L'agent peut générer des quiz, des QCM, des examens blancs et vous donner "
            "des stratégies de révision adaptées à vos matières."
        ),
    ),
    (
        ["analyser un pdf", "analyser mon cours", "importer un pdf", "pdf cours",
         "assistant pdf", "poser des questions sur mon cours", "questions sur le pdf",
         "analyser document", "uploader un cours"],
        (
            "Pour analyser un cours PDF, accédez à l'agent **Examens** depuis la page "
            "d'accueil, puis ouvrez l'onglet **Assistant PDF**.\n\n"
            "Vous pouvez importer votre cours et poser des questions directement dessus."
        ),
    ),
    (
        ["mes modules", "liste des modules", "voir mes modules", "trouver mes modules",
         "ou puis-je trouver mes modules", "ou sont mes modules",
         "ou trouver mes modules", "acceder a mes modules",
         "comment voir mes modules"],
        (
            "Pour voir la liste de vos **modules**, accédez à l'agent **Examens** depuis la page "
            "d'accueil, puis ouvrez l'onglet **Modules**.\n\n"
            "Vous pouvez sélectionner votre semestre pour afficher les modules correspondants."
        ),
    ),
    (
        ["voir mes examens", "comment voir mes examens", "trouver mes examens",
         "ou sont mes examens", "acceder aux examens", "mes examens",
         "ou puis je voir mes examens"],
        (
            "Pour accéder à vos **examens**, appuyez sur la carte **Examens** depuis la page d'accueil.\n\n"
            "Vous y trouverez :\n"
            "• L'onglet **Planning** → les dates et salles des examens officiels\n"
            "• L'onglet **Modules** → vos matières par semestre\n"
            "• L'onglet **Agent IA** → préparation, quiz et révisions"
        ),
    ),
    (
        ["mes statistiques", "ma progression", "mes performances",
         "historique quiz", "historique examens", "voir mes resultats"],
        (
            "Pour consulter vos **statistiques**, accédez à l'agent **Examens** depuis la page "
            "d'accueil, puis ouvrez l'onglet **Stats** ou **Historique**."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT PLANNING
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["a quoi sert l agent planning", "a quoi sert la partie planning",
         "que fait l agent planning", "role de l agent planning",
         "presentation planning", "description planning", "a quoi sert planning"],
        (
            "L'agent **Planning** est votre gestionnaire de temps personnel. Il propose :\n\n"
            "• Onglet **Agent IA** → créer un plan de révision, gérer les deadlines par conversation\n"
            "• Onglet **Urgent** → tâches prioritaires à traiter en premier\n"
            "• Onglet **Tâches** → toutes vos tâches en cours\n"
            "• Onglet **Terminé** → historique des tâches complétées\n\n"
            "**Pour y accéder :** Appuyez sur la carte **Planning** depuis la page d'accueil."
        ),
    ),
    (
        ["emploi du temps", "ou consulter mon emploi du temps",
         "ou puis-je consulter mon planning", "consulter mon planning",
         "voir mon planning", "mon emploi du temps", "edt",
         "ou est mon planning", "acceder au planning"],
        (
            "Pour consulter votre **emploi du temps et planning personnel**, accédez à l'agent "
            "**Planning** depuis la page d'accueil.\n\n"
            "• Onglet **Tâches** → vos tâches et deadlines personnels\n"
            "• Onglet **Urgent** → ce qui est prioritaire\n\n"
            "Pour le planning officiel des **examens**, rendez-vous dans l'agent **Examens** "
            "→ onglet **Planning**."
        ),
    ),
    (
        ["organiser mon temps", "organiser mes revisions", "gerer mes deadlines",
         "gestion du temps", "ajouter une tache", "creer une tache",
         "planifier ma semaine", "rappel", "deadline", "plan de revision",
         "plan d etude", "generer un plan"],
        (
            "Pour organiser votre temps et gérer vos deadlines, accédez à l'agent **Planning** "
            "depuis la page d'accueil, puis utilisez l'onglet **Agent IA**.\n\n"
            "L'agent peut créer des tâches, fixer des deadlines et générer un plan de "
            "révision personnalisé selon vos matières et la date de vos examens."
        ),
    ),
    (
        ["mes taches", "voir mes taches", "liste des taches", "taches en cours",
         "taches urgentes", "taches terminees"],
        (
            "Pour gérer vos **tâches**, accédez à l'agent **Planning** depuis la page d'accueil :\n\n"
            "• Onglet **Urgent** → tâches prioritaires\n"
            "• Onglet **Tâches** → toutes les tâches en cours\n"
            "• Onglet **Terminé** → tâches complétées\n\n"
            "Vous pouvez aussi appuyer sur le bouton **+ Ajouter** pour créer une nouvelle tâche."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT ORIENTATION
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["a quoi sert l agent orientation", "que fait l agent orientation",
         "role de l agent orientation", "presentation orientation",
         "description orientation", "a quoi sert orientation",
         "comment utiliser l agent orientation", "comment utiliser orientation"],
        (
            "L'agent **Orientation** est votre conseiller carrière. Il vous aide à :\n\n"
            "• Rédiger ou améliorer votre **CV**\n"
            "• Rédiger des **lettres de motivation**\n"
            "• Rechercher des **offres de stage ou d'emploi**\n"
            "• Préparer vos **entretiens d'embauche**\n"
            "• Explorer les **métiers et débouchés** de votre filière\n\n"
            "**Pour y accéder :** Appuyez sur la carte **Orientation** depuis la page d'accueil."
        ),
    ),
    (
        ["rediger mon cv", "creer mon cv", "ameliorer mon cv", "mon cv", "cv"],
        (
            "Pour rédiger ou améliorer votre **CV**, accédez à l'agent **Orientation** "
            "depuis la page d'accueil, puis demandez de l'aide pour votre CV."
        ),
    ),
    (
        ["lettre de motivation", "lettre motivation", "rediger une lettre"],
        (
            "Pour rédiger une **lettre de motivation**, accédez à l'agent **Orientation** "
            "depuis la page d'accueil, puis demandez de l'aide pour votre lettre de motivation."
        ),
    ),
    (
        ["chercher un stage", "trouver un stage", "offre de stage", "recherche stage",
         "chercher un emploi", "trouver un emploi", "offre emploi", "job",
         "alternance", "recherche d emploi"],
        (
            "Pour chercher un **stage ou un emploi**, accédez à l'agent **Orientation** "
            "depuis la page d'accueil. L'agent vous aidera à cibler les offres adaptées "
            "à votre profil et filière."
        ),
    ),
    (
        ["preparer un entretien", "entretien d embauche", "entretien",
         "conseil carriere", "orientation professionnelle",
         "metier", "debouche", "avenir professionnel"],
        (
            "Pour préparer un **entretien** ou obtenir des conseils de carrière, accédez à "
            "l'agent **Orientation** depuis la page d'accueil."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT CAMPUS
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["a quoi sert l agent campus", "a quoi sert la partie campus",
         "que fait l agent campus", "role de l agent campus",
         "presentation campus", "description campus", "a quoi sert campus"],
        (
            "L'agent **Campus** couvre toute la vie étudiante à l'ENIADB. Il propose :\n\n"
            "• Onglet **Agent IA** → règlement intérieur, clubs, infos campus\n"
            "• Onglet **Événements** → événements à venir et passés\n"
            "• Onglet **Clubs** → les 6 clubs étudiants (SECORA, ENNOVERS, NURLIA, RIOT, AL ATAA, Enactus)\n"
            "• Onglet **Groupes** → groupes de travail par matière\n\n"
            "**Pour y accéder :** Appuyez sur la carte **Campus** depuis la page d'accueil."
        ),
    ),
    (
        ["reglement interieur", "ou trouver le reglement interieur",
         "consulter le reglement", "absences autorisees", "nombre d absences",
         "combien d absences", "discipline", "sanction", "tenue vestimentaire",
         "dress code", "comportement", "interdit", "regle de l ecole",
         "regles de l eniad", "regles eniad"],
        (
            "Pour consulter le **règlement intérieur**, accédez à l'agent **Campus** depuis "
            "la page d'accueil, puis posez votre question dans l'onglet **Agent IA**.\n\n"
            "L'agent connaît tous les articles du règlement : absences autorisées, examens, "
            "discipline, tenue vestimentaire, sanctions, etc."
        ),
    ),
    (
        ["clubs etudiants", "club etudiant", "rejoindre un club", "clubs disponibles",
         "secora", "ennovers", "nurlia", "riot", "al ataa", "enactus", "aei",
         "activites parascolaires", "activites extrascolaires", "vie associative"],
        (
            "Pour vous informer sur les **clubs étudiants**, accédez à l'agent **Campus** "
            "depuis la page d'accueil, puis ouvrez l'onglet **Clubs**.\n\n"
            "Clubs disponibles à l'ENIADB :\n"
            "• **SECORA** → Cybersécurité\n"
            "• **ENNOVERS** → Génie informatique\n"
            "• **NURLIA** → IA & Data Science\n"
            "• **RIOT** → Robotique\n"
            "• **AL ATAA** → Social & humanitaire\n"
            "• **Enactus** → Entrepreneuriat social\n\n"
            "Vous pouvez rejoindre un club directement depuis l'onglet **Clubs**."
        ),
    ),
    (
        ["evenements", "evenements campus", "activites campus",
         "conference", "hackathon", "forum entreprise", "portes ouvertes",
         "gala", "workshop", "agenda campus"],
        (
            "Pour consulter les **événements** de l'ENIADB, accédez à l'agent **Campus** "
            "depuis la page d'accueil, puis ouvrez l'onglet **Événements**.\n\n"
            "Vous y trouverez les événements à venir et passés (conférences, workshops, "
            "hackathons, forums entreprises, etc.)."
        ),
    ),
    (
        ["bibliotheque", "livre", "ouvrage", "emprunter un livre",
         "reference bibliographique", "ressources documentaires"],
        (
            "Pour rechercher un ouvrage à la **bibliothèque**, accédez à l'agent **Campus** "
            "depuis la page d'accueil, puis posez votre question dans l'onglet **Agent IA**.\n\n"
            "L'agent connaît les livres disponibles avec leurs numéros de référence."
        ),
    ),
    (
        ["groupes de travail", "groupe de travail", "groupe d etude",
         "travailler en groupe", "equipe de revision"],
        (
            "Pour rejoindre un **groupe de travail**, accédez à l'agent **Campus** depuis "
            "la page d'accueil, puis ouvrez l'onglet **Groupes**.\n\n"
            "Vous y trouverez des groupes de révision par matière (Machine Learning, "
            "Algorithmique, BDD, Réseaux, etc.)."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT BIEN-ÊTRE
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["a quoi sert l agent bien etre", "a quoi sert l agent wellbeing",
         "que fait l agent bien etre", "role de l agent bien etre",
         "presentation bien etre", "description bien etre",
         "a quoi sert bien etre", "a quoi sert wellbeing",
         "comment acceder a l agent well being",
         "comment acceder a l agent bien etre"],
        (
            "L'agent **Bien-être** est votre soutien psychologique et santé mentale. Il propose :\n\n"
            "• Onglet **Agent IA** → écoute empathique, gestion du stress, conseils personnalisés\n"
            "• Onglet **Mon humeur** → suivi quotidien de votre humeur (1 à 5 étoiles)\n"
            "• Onglet **Conseils** → techniques anti-stress, sommeil, alimentation, Pomodoro\n"
            "• Onglet **Support ENIAD** → contacts de la cellule d'écoute et ressources\n\n"
            "**Pour y accéder :** Appuyez sur la carte **Well-being** depuis la page d'accueil.\n\n"
            "Urgence mentale : **080 100 47 47** (gratuit, 24h/24)."
        ),
    ),
    (
        ["stress", "stresse", "anxiete", "anxieux", "burnout",
         "epuise", "fatigue", "demotive", "je me sens mal",
         "je suis deprime", "mal a l aise", "peur", "panique",
         "concentrer", "sommeil", "seul", "isole", "triste",
         "pleure", "perdu", "depasse", "imposteur", "motivation",
         "aide psychologique", "soutien", "detresse", "souffre"],
        (
            "Pour gérer votre **stress, anxiété ou mal-être**, accédez à l'agent **Bien-être** "
            "depuis la page d'accueil, puis ouvrez l'onglet **Agent IA**.\n\n"
            "L'agent vous écoutera sans jugement et vous proposera des stratégies concrètes.\n\n"
            "En cas d'urgence : **080 100 47 47** (gratuit, 24h/24)."
        ),
    ),
    (
        ["suivi humeur", "mon humeur", "enregistrer mon humeur",
         "humeur du jour", "tracker humeur", "comment je me sens"],
        (
            "Pour suivre votre **humeur**, accédez à l'agent **Bien-être** depuis la page "
            "d'accueil, puis ouvrez l'onglet **Mon humeur**.\n\n"
            "Vous pouvez noter votre humeur de 1 à 5 et voir votre historique hebdomadaire."
        ),
    ),
    (
        ["conseils bien etre", "conseils anti stress", "technique pomodoro",
         "techniques de relaxation", "mieux dormir", "sante mentale",
         "gestion du stress", "coherence cardiaque"],
        (
            "Pour accéder aux **conseils bien-être**, accédez à l'agent **Bien-être** "
            "depuis la page d'accueil, puis ouvrez l'onglet **Conseils**.\n\n"
            "Vous y trouverez des techniques : Pomodoro, cohérence cardiaque, règles du "
            "sommeil, alimentation, pause active, etc."
        ),
    ),
    (
        ["cellule d ecoute", "service medical", "psychologue", "support eniad",
         "numero urgence", "080 100 47 47", "aide professionnelle"],
        (
            "Pour contacter le **support psychologique ENIAD**, accédez à l'agent **Bien-être** "
            "depuis la page d'accueil, puis ouvrez l'onglet **Support ENIAD**.\n\n"
            "Ressources disponibles :\n"
            "• **Cellule d'écoute ENIAD** : secrétariat pédagogique, bâtiment principal\n"
            "• **Service médical UMP** : consultations gratuites, campus UMP Oujda\n"
            "• **Ligne nationale** : 080 100 47 47 (gratuit, 24h/24)"
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # NAVIGATION DIRECTE — "Comment accéder à..."
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["comment acceder a l admin", "ou est l admin", "ouvrir admin",
         "trouver admin", "aller sur admin", "agent admin"],
        "Pour accéder à l'agent **Admin**, appuyez sur la carte **Admin** depuis la page d'accueil.",
    ),
    (
        ["comment acceder aux examens", "ou sont mes examens", "ouvrir examens",
         "trouver examens", "aller sur examens", "comment voir mes examens",
         "agent examens", "agent exams"],
        (
            "Pour accéder à l'agent **Examens**, appuyez sur la carte **Examens** depuis la page d'accueil.\n\n"
            "Vous y trouverez 5 onglets : Agent IA, Planning, Assistant PDF, Modules, Stats."
        ),
    ),
    (
        ["comment acceder au planning", "ou est le planning", "ouvrir planning",
         "trouver planning", "aller sur planning", "agent planning"],
        (
            "Pour accéder à l'agent **Planning**, appuyez sur la carte **Planning** depuis la page d'accueil.\n\n"
            "Vous y gérez vos tâches, deadlines et emploi du temps personnel."
        ),
    ),
    (
        ["comment acceder a l orientation", "ou est l orientation", "ouvrir orientation",
         "trouver orientation", "aller sur orientation", "agent orientation"],
        (
            "Pour accéder à l'agent **Orientation**, appuyez sur la carte **Orientation** depuis la page d'accueil.\n\n"
            "Il vous aide avec votre CV, lettres de motivation, recherche de stage et préparation d'entretiens."
        ),
    ),
    (
        ["comment acceder au campus", "ou est le campus", "ouvrir campus",
         "trouver campus", "aller sur campus", "agent campus"],
        (
            "Pour accéder à l'agent **Campus**, appuyez sur la carte **Campus** depuis la page d'accueil.\n\n"
            "Vous y trouverez 4 onglets : Agent IA, Événements, Clubs, Groupes."
        ),
    ),
    (
        ["comment acceder au bien etre", "ou est le bien etre",
         "comment acceder au wellbeing", "ou est le wellbeing",
         "ouvrir bien etre", "trouver bien etre", "aller sur bien etre",
         "agent bien etre", "agent wellbeing", "well being"],
        (
            "Pour accéder à l'agent **Bien-être**, appuyez sur la carte **Well-being** depuis la page d'accueil.\n\n"
            "Vous y trouverez 4 onglets : Agent IA, Mon humeur, Conseils, Support ENIAD."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    # INFORMATIONS ÉCOLE
    # ═══════════════════════════════════════════════════════════════════════════
    (
        ["adresse", "ou se trouve l eniad", "localisation eniad",
         "comment aller a l eniad", "l ecole"],
        (
            "L'**ENIADB** (École Nationale de l'Intelligence Artificielle et du Digital de Berkane) "
            "se trouve à :\n\n"
            "📍 Route Aklim, Km 1, Berkane\n"
            "🌐 www.eniad.ump.ma\n"
            "📧 eniad@ump.ac.ma\n\n"
            "Pour plus d'informations sur l'école, posez votre question à l'agent **Campus**."
        ),
    ),
    (
        ["contact", "telephone", "email eniad", "secretariat",
         "contacter l administration", "service scolarite"],
        (
            "Pour contacter l'**administration ENIADB** :\n\n"
            "🌐 www.eniad.ump.ma\n"
            "📧 eniad@ump.ac.ma\n\n"
            "Pour des démarches administratives, utilisez l'agent **Admin** depuis la page d'accueil."
        ),
    ),
]


# ── Moteur de règles ──────────────────────────────────────────────────────────

def _rule_based_response(message: str) -> Optional[str]:
    """Retourne la réponse de la première règle correspondante, ou None."""
    msg_norm = _normalize(message)
    for keywords, response in NAV_RULES:
        for kw in keywords:
            if _normalize(kw) in msg_norm:
                return response
    return None


# ── Connaissance complète pour le LLM (fallback) ─────────────────────────────

APP_KNOWLEDGE = """
SMARTSTUDENT — ENIADB (École Nationale de l'Intelligence Artificielle et du Digital de Berkane)
Adresse : Route Aklim, Km 1, Berkane | Site : www.eniad.ump.ma | Email : eniad@ump.ac.ma

═══ 6 AGENTS ACCESSIBLES DEPUIS LA PAGE D'ACCUEIL ═══

[ADMIN] Carte "Admin"
Rôle : Assistant administratif — documents, réclamations, support IT, bourses
Fonctionnalités :
  - Attestation de scolarité
  - Relevé de notes
  - Convention de stage / PFA / PFE
  - Réclamation (note erronée, absence injustifiée)
  - Wi-Fi / Moodle / compte bloqué
  - Bourses et aides sociales
  - Inscription / réinscription

[EXAMENS] Carte "Exams"
Rôle : Préparation aux examens et suivi académique
Onglets :
  - Agent IA → quiz, QCM, examens blancs, stratégies de révision
  - Planning → planning officiel (dates, salles, horaires)
  - Assistant PDF → analyser un cours PDF et poser des questions
  - Modules → liste des modules par semestre
  - Stats → statistiques et historique de quiz

[PLANNING] Carte "Planning"
Rôle : Gestion du temps et organisation personnelle
Onglets :
  - Agent IA → créer plan de révision, gérer deadlines en conversation
  - Urgent → tâches prioritaires
  - Tâches → toutes les tâches en cours
  - Terminé → historique des tâches complétées
Bouton FAB "Ajouter" → créer une tâche manuellement

[ORIENTATION] Carte "Orientation"
Rôle : Conseiller carrière et préparation professionnelle
Fonctionnalités :
  - Rédiger / améliorer le CV
  - Rédiger lettres de motivation
  - Rechercher stages et emplois
  - Préparer les entretiens d'embauche
  - Explorer les métiers et débouchés

[CAMPUS] Carte "Campus"
Rôle : Vie étudiante, règlement, clubs, événements
Onglets :
  - Agent IA → règlement intérieur, infos clubs, bibliothèque
  - Événements → agenda (conférences, hackathons, forums, workshops)
  - Clubs → SECORA (cybersécurité), ENNOVERS (génie info), NURLIA (IA/data), RIOT (robotique), AL ATAA (humanitaire), Enactus (entrepreneuriat)
  - Groupes → groupes de travail par matière

[BIEN-ÊTRE] Carte "Well-being"
Rôle : Soutien psychologique et santé mentale
Onglets :
  - Agent IA → écoute empathique, gestion stress/burnout/anxiété
  - Mon humeur → suivi quotidien (1-5 étoiles), historique 7 jours
  - Conseils → Pomodoro, cohérence cardiaque, sommeil, alimentation
  - Support ENIAD → Cellule d'écoute ENIAD, Service médical UMP, 080 100 47 47 (urgence, gratuit 24h/24)
"""

SYSTEM_PROMPT = f"""Tu es le **Guide Intelligent** de SmartStudent (ENIADB Berkane).
Tu connais PARFAITEMENT l'application et tu guides les étudiants vers la bonne section.

{APP_KNOWLEDGE}

RÈGLES ABSOLUES :
1. Tu guides et expliques — tu n'exécutes PAS les tâches à la place des autres agents.
2. Réponds en français, clairement, avec les étapes précises de navigation.
3. Mentionne toujours le nom de l'agent en **gras** et l'onglet exact si applicable.
4. Format préféré : "Pour [action], accédez à l'agent **[Nom]** depuis la page d'accueil[, puis onglet **[Tab]**]."
5. Si tu ne connais pas la fonctionnalité, dis-le honnêtement — ne l'invente pas.
6. Réponse concise : 1 à 5 lignes maximum.
"""


# ── Agent ────────────────────────────────────────────────────────────────────

class NavigationAgent:
    """Guide intelligent de l'application — règles exhaustives puis LLM fallback."""

    async def process(
        self,
        message: str,
        history: List[Dict[str, str]],
        user_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        # ── 1. Règles directes (zéro token) ──────────────────────────────────
        rule_response = _rule_based_response(message)
        if rule_response:
            return {"response": rule_response, "agent": "home"}

        # ── 2. LLM fallback enrichi ───────────────────────────────────────────
        try:
            from backend.agents.orchestrator import get_llm
            llm = get_llm()

            context_note = ""
            filiere = user_context.get("major") or ""
            annee = user_context.get("year") or ""
            if filiere:
                context_note += f"\nÉtudiant en {filiere}"
            if annee:
                context_note += f", année {annee}."

            messages = [SystemMessage(content=SYSTEM_PROMPT + context_note)]

            for h in (history or [])[-4:]:
                role = h.get("role", "")
                content = h.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                else:
                    from langchain_core.messages import AIMessage
                    messages.append(AIMessage(content=content))

            messages.append(HumanMessage(content=message))
            resp = await llm.ainvoke(messages)
            return {"response": resp.content, "agent": "home"}

        except Exception as e:
            logger.error("NavigationAgent LLM error: %s", e)
            err_str = str(e)
            if "429" in err_str or "rate limit" in err_str.lower():
                fallback = (
                    "Le service IA est momentanément indisponible. "
                    "Accédez directement aux agents depuis la page d'accueil :\n\n"
                    "• **Admin** → attestations, conventions, réclamations\n"
                    "• **Examens** → quiz, planning officiel, analyse PDF\n"
                    "• **Planning** → deadlines, emploi du temps\n"
                    "• **Orientation** → CV, stage, entretiens\n"
                    "• **Campus** → règlement, clubs, événements\n"
                    "• **Bien-être** → stress, soutien psychologique"
                )
            else:
                fallback = "Désolé, une erreur est survenue. Réessayez dans quelques instants."
            return {"response": fallback, "agent": "home"}
