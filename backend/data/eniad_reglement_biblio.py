# -*- coding: utf-8 -*-
# =============================================================================
# ENIAD KNOWLEDGE BASE — Règlement des études + Catalogue bibliothèque
# Sources : règlement_intérieur_eniad.pdf + biblio_Connect.pdf
# Format  : liste de dicts { id, category, title, content }
# =============================================================================

KNOWLEDGE_BASE = [

    # ── Accès & Inscription ──────────────────────────────────────────────────

    {
        "id": "regl_001",
        "category": "inscription",
        "title": "Accès à l'école",
        "content": (
            "L'ENIAD est un établissement à accès régulé. "
            "L'accès aux classes préparatoires et au cycle ingénieur se fait par voie de concours."
        ),
    },
    {
        "id": "regl_002",
        "category": "inscription",
        "title": "Durée de la formation",
        "content": (
            "Les études à l'ENIAD durent 5 ans (10 semestres), réparties en deux cycles :\n"
            "- Cycle préparatoire (CP) : 2 ans (4 semestres)\n"
            "- Cycle ingénieur d'état (CI) : 3 ans (6 semestres), incluant le Projet de Fin d'Études (PFE) "
            "réalisé durant tout le 6e semestre."
        ),
    },
    {
        "id": "regl_003",
        "category": "inscription",
        "title": "Statut d'élève ingénieur",
        "content": (
            "Est considéré élève à l'ENIAD toute personne ayant réussi un concours d'accès et régulièrement inscrite. "
            "L'élève perd son statut s'il est exclu ou a obtenu son diplôme. "
            "Les droits et obligations sont précisés aux articles 69 à 76 de la loi 01-00."
        ),
    },
    {
        "id": "regl_004",
        "category": "inscription",
        "title": "Conditions d'inscription",
        "content": (
            "- L'inscription est annuelle et s'effectue dans les délais fixés par le Directeur.\n"
            "- Inscription en 1ère année : ouverte aux titulaires du baccalauréat.\n"
            "- Inscription en 3ème année : ouverte aux titulaires d'un DUT/DEUST, DEUG ou licence "
            "(Pro/fondamentale/Sciences et techniques).\n"
            "- Un élève ne peut s'inscrire que dans une seule filière d'ingénierie.\n"
            "- Après inscription, une carte d'élève ingénieur est délivrée (pièce d'identité obligatoire aux examens).\n"
            "- Une assurance annuelle est obligatoire pour toute inscription ou réinscription."
        ),
    },
    {
        "id": "regl_005",
        "category": "inscription",
        "title": "Réinscription à un module non validé",
        "content": (
            "Un élève peut se réinscrire une fois à un module non validé. "
            "Une 2e et dernière réinscription peut être accordée par dérogation du Directeur."
        ),
    },
    {
        "id": "regl_006",
        "category": "inscription",
        "title": "Choix des filières du cycle ingénieur",
        "content": (
            "Le choix de spécialité est arrêté à la fin de la 2e année du CP, selon les voeux des élèves, "
            "leur classement (basé sur les notes du CP) et la capacité d'accueil de chaque filière. "
            "Le choix des options au sein d'une filière est arrêté par l'équipe pédagogique de cette filière."
        ),
    },

    # ── Assiduité & Absences ─────────────────────────────────────────────────

    {
        "id": "regl_007",
        "category": "assiduite",
        "title": "Présence obligatoire",
        "content": (
            "La présence est obligatoire à toutes les activités pédagogiques : cours magistraux, TD, TP, "
            "ateliers, séminaires, visites, contrôles et examens. "
            "L'absence est gérée par les filières et prise en compte lors des délibérations de fin d'année."
        ),
    },
    {
        "id": "regl_008",
        "category": "assiduite",
        "title": "Justification d'absence",
        "content": (
            "Toute absence doit être justifiée dans un délai de 48 heures auprès de l'enseignant responsable "
            "et du service de scolarité (ainsi que du secrétariat du directeur adjoint et du coordinateur de filière). "
            "Seule la commission pédagogique de la filière valide la justification."
        ),
    },
    {
        "id": "regl_009",
        "category": "assiduite",
        "title": "Motifs d'absence acceptés",
        "content": (
            "Motifs acceptés et justificatifs requis :\n"
            "- Maladie/accident : certificat médical (imprimé fourni par l'école)\n"
            "- Hospitalisation : attestation d'hospitalisation (imprimé fourni par l'école)\n"
            "- Convocation administrative (police, consulat, entretien de stage, activité socioculturelle) : "
            "copie certifiée conforme de la convocation\n"
            "- Stage autorisé par l'école : copie de la convention + attestation de stage + autorisation écrite "
            "du coordinateur de filière\n"
            "- Décès d'un proche du 1er ou 2e degré (parents, grands-parents, frères/soeurs, enfants) : "
            "copie certifiée conforme de l'attestation de décès\n"
            "- État de santé avec absences répétitives dépassant 30 absences (15 jours) : "
            "dossier médical détaillé signé par une entité médicale reconnue"
        ),
    },
    {
        "id": "regl_010",
        "category": "assiduite",
        "title": "Retards",
        "content": (
            "Tout retard risque d'entraîner une exclusion de la séance, comptabilisée comme absence non justifiée. "
            "Cette décision n'engage pas la responsabilité civile de l'enseignant."
        ),
    },
    {
        "id": "regl_011",
        "category": "assiduite",
        "title": "Règles spécifiques aux TP",
        "content": (
            "- Absence injustifiée à une séance de TP : peut entraîner la non-validation du module en session ordinaire. "
            "La séance ne peut jamais être rattrapée.\n"
            "- Absence justifiée à une séance de TP : non pénalisante, mais la séance ne peut être rattrapée.\n"
            "- Absence à plus d'une séance de TP d'un même module : compromet la validation du module.\n"
            "- Absence à plus de 2 séances de Cours ou TD d'un même module : compromet la validation du module."
        ),
    },
    {
        "id": "regl_012",
        "category": "assiduite",
        "title": "Sanctions liées aux absences",
        "content": (
            "Absences non justifiées cumulées sur plusieurs modules (par semestre) :\n"
            "- 3 absences : avertissement (copie transmise à l'élève)\n"
            "- 5 absences : blâme (copie transmise aux parents)\n"
            "- 7 absences : conseil de discipline + décision d'exclusion\n\n"
            "Absences non justifiées cumulées sur un seul module :\n"
            "- 3 absences à un élément de module : annulation de l'élément\n"
            "- 5 absences à un module : annulation du module\n\n"
            "Cumul justifiées + non justifiées >= 15% du volume horaire du semestre : annulation de la session de rattrapage.\n\n"
            "NB : Toutes les sanctions sont prises en compte par les jurys et l'administration "
            "(recommandations stages, bourses, etc.)."
        ),
    },

    # ── Contrôles & Examens ──────────────────────────────────────────────────

    {
        "id": "regl_013",
        "category": "examens",
        "title": "Présence aux contrôles et examens",
        "content": (
            "La présence à tous les contrôles et examens est obligatoire.\n"
            "- Absence justifiée en session ordinaire : droit uniquement à la session de rattrapage.\n"
            "- Absence non justifiée en session ordinaire : peut demander une dérogation exceptionnelle "
            "étudiée par la direction après avis de la commission pédagogique."
        ),
    },
    {
        "id": "regl_014",
        "category": "examens",
        "title": "Calendrier et sessions d'examen",
        "content": (
            "- Le calendrier est établi par le directeur adjoint chargé de la pédagogie avec les coordonnateurs.\n"
            "- Les élèves sont informés au moins une semaine avant.\n"
            "- Session normale : date communiquée par affichage au plus tard une semaine avant.\n"
            "- Session de rattrapage : au moins une semaine après la proclamation des résultats de la session normale.\n"
            "- Un élève n'a droit qu'à un seul rattrapage par module."
        ),
    },
    {
        "id": "regl_015",
        "category": "examens",
        "title": "Accès aux salles d'examen",
        "content": (
            "- Les élèves doivent consulter les plannings à l'avance et se présenter 10 minutes avant le début.\n"
            "- La carte d'élève ingénieur (ou CIN) est obligatoire.\n"
            "- Retard inférieur au tiers de la durée : accès autorisé si aucun élève n'a quitté la salle, "
            "mais sans temps supplémentaire."
        ),
    },
    {
        "id": "regl_016",
        "category": "examens",
        "title": "Devoirs de l'élève durant l'épreuve",
        "content": (
            "L'élève doit :\n"
            "- Inscrire nom, prénom et code Apogée sur la copie, et signer la feuille de présence.\n"
            "- Composer seul et personnellement.\n"
            "- Remettre obligatoirement sa copie avant de quitter la salle.\n"
            "- Déposer sacs et objets encombrants à l'entrée ou en bout de rangée.\n\n"
            "Il est interdit :\n"
            "- De communiquer entre candidats ou avec l'extérieur.\n"
            "- D'utiliser ou conserver des documents/matériels non autorisés.\n"
            "- D'utiliser téléphone, tablette ou tout appareil électronique non autorisé "
            "(laissés obligatoirement hors de la salle)."
        ),
    },
    {
        "id": "regl_017",
        "category": "examens",
        "title": "Sortie de salle d'examen",
        "content": (
            "- Aucun candidat ne peut quitter la salle avant la moitié de la durée de l'épreuve.\n"
            "- Sortie temporaire uniquement avec accord du responsable et accompagnement d'un surveillant "
            "(un par un, copie remise au surveillant avec heure de sortie/retour notée).\n"
            "- Infraction : note zéro à l'épreuve et aucun rattrapage possible."
        ),
    },
    {
        "id": "regl_018",
        "category": "examens",
        "title": "Fraude aux examens",
        "content": (
            "Tout manquement aux consignes constitue une fraude. "
            "La fraude entraîne une convocation devant le conseil de discipline. "
            "Les surveillants rédigent un rapport détaillé et signé. "
            "L'élève peut continuer son épreuve en attendant la décision. "
            "Le plagiat lors d'activités hors établissement (PFE, projets, devoirs) est traité de même. "
            "La direction se réserve le droit d'engager des poursuites judiciaires."
        ),
    },

    # ── Évaluation & Validation ──────────────────────────────────────────────

    {
        "id": "regl_019",
        "category": "evaluation",
        "title": "Évaluation des connaissances",
        "content": (
            "L'évaluation se fait par contrôle continu (examens, tests, devoirs, exposés, rapports de stage, etc.). "
            "Un examen final peut être organisé en plus si besoin. "
            "Les examens de TP sont pratiques (l'écrit/oral doit rester exceptionnel et justifié). "
            "Au minimum 2 contrôles écrits par élément de module sont organisés : un à mi-session, un en fin de session. "
            "Les évaluations écrites se déroulent en présence de l'enseignant responsable. "
            "Une vérification de note (pas une discussion) est possible dans les 2 jours ouvrables suivant la publication, "
            "par demande écrite au secrétariat du Directeur Adjoint. "
            "Les notes de nature orale ou pratique ne peuvent pas être vérifiées."
        ),
    },
    {
        "id": "regl_020",
        "category": "evaluation",
        "title": "Admission et validation d'un module",
        "content": (
            "Un module est validé si la moyenne générale est au moins :\n"
            "- 10/20 pour le CP\n"
            "- 12/20 pour le CI\n\n"
            "Note éliminatoire : strictement inférieure à 7/20 (CP et CI).\n\n"
            "Conditions de passage à l'année supérieure :\n"
            "- CP : valider 12 modules sur 14 (12/14)\n"
            "- CI 3e année (tronc commun) : 12/14\n"
            "- CI 4e et 5e années : 10/14\n\n"
            "Un élève n'ayant pas validé un module est convoqué à un rattrapage. "
            "En cas de non-passage, le chef d'établissement peut accorder une année de réserve "
            "(une seule fois par cycle)."
        ),
    },

    # ── Comportement & Vie à l'école ─────────────────────────────────────────

    {
        "id": "regl_021",
        "category": "comportement",
        "title": "Liberté d'opinion",
        "content": (
            "L'enseignement implique l'objectivité du savoir et la tolérance des opinions. "
            "Il est incompatible avec toute forme de propagande et doit rester hors de toute emprise "
            "politique, philosophique ou religieuse."
        ),
    },
    {
        "id": "regl_022",
        "category": "comportement",
        "title": "Discipline et conduite",
        "content": (
            "Tout manquement à la discipline (indiscipline, manque de respect, dégradation de matériel...) "
            "fait l'objet d'un rapport officiel transmis à la direction dans les 48h. "
            "Le Conseil d'établissement réuni en Conseil de Discipline statue sur les sanctions. "
            "Les élèves doivent respecter l'ensemble du personnel (pédagogique, administratif, technique)."
        ),
    },
    {
        "id": "regl_023",
        "category": "comportement",
        "title": "Respect du patrimoine",
        "content": (
            "Les élèves doivent :\n"
            "- Veiller à l'état et à la propreté des bâtiments (salles, labos, ateliers, toilettes...).\n"
            "- Prendre soin du matériel. Toute dégradation est sanctionnée et remboursée.\n"
            "- Prendre soin des livres empruntés à la bibliothèque. Tout ouvrage abimé ou déchiré doit être remboursé "
            "et peut entraîner une privation d'accès temporaire.\n"
            "- Ne pas diffuser sur Internet les contenus de cours, TD, TP "
            "(propriété exclusive de l'enseignant). Infraction : conseil de discipline."
        ),
    },
    {
        "id": "regl_024",
        "category": "comportement",
        "title": "Dispositions générales — interdictions",
        "content": (
            "- Photos/vidéos en classe sans autorisation préalable : interdites. "
            "Mise en ligne sans consentement : sanctions pouvant aller jusqu'à l'exclusion + confiscation de l'appareil "
            "+ poursuites judiciaires.\n"
            "- Tenue excentrique ou attirant l'attention : interdite.\n"
            "- Bizutage : strictement interdit.\n"
            "- Tabac : interdit dans tous les locaux (loi n°15-91).\n"
            "- Cigarette électronique, stupéfiants, alcool, psychotropes : sanction disciplinaire majeure + poursuite judiciaire.\n"
            "- Réunions/assemblées/activités : nécessitent une autorisation écrite de la direction.\n"
            "- Appareils électroniques en salle : interdits sauf autorisation."
        ),
    },
    {
        "id": "regl_025",
        "category": "comportement",
        "title": "Interlocuteurs de l'administration",
        "content": (
            "Les étudiants majeurs sont les seuls interlocuteurs de l'administration et des équipes pédagogiques. "
            "Aucun tiers (parent, ami) ne peut les représenter."
        ),
    },

    # ── Bibliothèque ─────────────────────────────────────────────────────────

    {
        "id": "biblio_001",
        "category": "bibliotheque",
        "title": "Catalogue de la bibliothèque — Vue d'ensemble",
        "content": (
            "La bibliothèque de l'ENIAD dispose d'un fonds de plus de 210 ouvrages numérotés, "
            "couvrant les domaines suivants : Intelligence Artificielle, Machine Learning, Deep Learning, "
            "NLP, Cybersécurité, Robotique, Développement logiciel, DevOps, Mathématiques, "
            "Statistiques, Langages de programmation (Python, R, C++, Kotlin, Flutter/Dart), "
            "Développement personnel et gestion de projet."
        ),
    },
    {
        "id": "biblio_ia",
        "category": "bibliotheque",
        "title": "Livres — Intelligence Artificielle & Machine Learning",
        "content": (
            "- Deep Learning — Ian Goodfellow, Yoshua Bengio, Aaron Courville (n°127,128)\n"
            "- Artificial Intelligence: A Modern Approach — Stuart Russell, Peter Norvig (n°165,166)\n"
            "- Artificial Intelligence: A Guide to Intelligent Systems — Michael Negnevitsky (n°17,18)\n"
            "- Reinforcement Learning: An Introduction — Sutton & Barto (n°152,153,154)\n"
            "- Explainable AI: Interpreting, Explaining and Visualizing Deep Learning — Samek & Wiegand (n°81,82)\n"
            "- Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow — Aurélien Géron (n°122,123 + n°124,126)\n"
            "- Machine learning avec Scikit-learn — Aurélien Géron (n°95,96,97)\n"
            "- Deep Learning with Python — François Chollet (n°31,32)\n"
            "- Deep learning avec Keras et TensorFlow — Aurélien Géron (n°85,86)\n"
            "- Generative Deep Learning — David Foster (n°53,54,55)\n"
            "- AI Ethics — Mark Coeckelbergh (n°144,145)\n"
            "- AI Superpowers — Kai-Fu Lee (n°174,175,176)\n"
            "- Artificial Intelligence and Machine Learning for Business — Steven Finlay (n°58,59,60)\n"
            "- Deep Medicine — Eric Topol (n°110,111,112)\n"
            "- Data Science for Business — Provost & Fawcett (n°160,161,62)\n"
            "- Data mining — Daniel T. Larose (n°46,47)\n"
            "- Building Computer Vision Applications Using Artificial Neural Networks — Shamshad Ansari (n°119,120,121)"
        ),
    },
    {
        "id": "biblio_nlp",
        "category": "bibliotheque",
        "title": "Livres — NLP & LLM",
        "content": (
            "- Transformers for Natural Language Processing — Denis Rothman (n°139,140)\n"
            "- Hands-On Large Language Models — Jay Alammar, Maarten Grootendorst (n°183,184)\n"
            "- Deep Learning for Natural Language Processing — Stephan Raaijmakers (n°185,186)\n"
            "- Mastering NLP from Foundations to LLMs — Lior Gazit (n°38,39,40)"
        ),
    },
    {
        "id": "biblio_secu",
        "category": "bibliotheque",
        "title": "Livres — Cybersécurité & Réseaux",
        "content": (
            "- Hacking: The Art of Exploitation — Jon Erickson (n°137,138)\n"
            "- Cybersecurity and Cyberwar — P.W. Singer, Allan Friedman (n°19,208,71)\n"
            "- Network Security Essentials — William Stallings (n°69,70)\n"
            "- Cryptography and Network Security — William Stallings (n°132,133)\n"
            "- Security Engineering — Ross Anderson (n°172,173)\n"
            "- La sécurité logicielle : une approche défensive — Raphaël Khoury (n°89,90,91)\n"
            "- Résistez aux hackeurs ! — Cédric Bertrand (n°9,10)"
        ),
    },
    {
        "id": "biblio_robotique",
        "category": "bibliotheque",
        "title": "Livres — Robotique & Mécatronique",
        "content": (
            "- Introduction to Robotics: Mechanics and Control — John J. Craig (n°44,45)\n"
            "- Modern Robotics — Kevin M. Lynch, Frank C. Park (n°192,193)\n"
            "- Robotics: Modelling, Planning and Control — Bruno Siciliano et al. (n°129,130,131)\n"
            "- La robotique par la pratique — Jacques A. Gangloff (n°101,102,103)\n"
            "- Fondamentaux de la robotique — Clément Gosselin (n°41,42,43)\n"
            "- Analyse et modélisation des robots manipulateurs — Etienne Dombre (n°209,210)\n"
            "- Mécatronique — Lionel Birglen (n°29,30)\n"
            "- Atelier de robotique — Nicolas Monmarché (n°27,28)\n"
            "- L'avenir des robots et l'intelligence humaine — Hans Moravec (n°24,25,26)"
        ),
    },
    {
        "id": "biblio_dev",
        "category": "bibliotheque",
        "title": "Livres — Développement logiciel & Architecture",
        "content": (
            "- Clean Code — Robert C. Martin (n°72,74 + n°75,76)\n"
            "- The Pragmatic Programmer — Andrew Hunt, David Thomas (n°107,109)\n"
            "- Design Patterns — Erich Gamma et al. (n°1,2 + n°3,4,5)\n"
            "- Head First Design Patterns — Eric Freeman (n°48,49)\n"
            "- The Art of Computer Programming — Donald Knuth (n°158,159)\n"
            "- Designing Data-Intensive Applications — Martin Kleppmann (n°61,62)\n"
            "- Microservice Architecture — Irakli Nadareishvili (n°134,135,136)\n"
            "- Spring in Action — Craig Walls (n°163,164)\n"
            "- Spring Microservices in Action — Craig Walls (n°167,168)\n"
            "- Computer Organization and Design (RISC-V) — Patterson & Hennessy (n°104,105,106)"
        ),
    },
    {
        "id": "biblio_devops",
        "category": "bibliotheque",
        "title": "Livres — DevOps & Conteneurisation",
        "content": (
            "- The DevOps Handbook — Kim, Humble, Debois, Willis (n°169,170,171)\n"
            "- Effective DevOps — Jennifer Davis (n°33,34,35)\n"
            "- Docker Deep Dive — Nigel Poulton (n°56,57)\n"
            "- The Docker Book — James Turnbull (n°206,207,208)"
        ),
    },
    {
        "id": "biblio_langages",
        "category": "bibliotheque",
        "title": "Livres — Langages de programmation (Python, R, C++, Kotlin, Flutter)",
        "content": (
            "Python :\n"
            "- Python pour le data scientist — Emmanuel Jakobowicz (n°92,93,94)\n"
            "- Programmation en Python pour les mathématiques — Casamayou-Boucau (n°146,147,148)\n"
            "- Méthodes numériques avec Python — Michaël Baudin (n°141,142,143)\n\n"
            "R :\n"
            "- R pour les scientifiques — François Rebaudo (n°66,67,68)\n"
            "- Initiation à la statistique avec R — Frédéric Bertrand (n°21,22,23)\n"
            "- Le langage R au quotidien — Olivier Decourt (n°199,200)\n"
            "- Traitements statistiques et programmation avec R — Gilles Hunault (n°14,15,16)\n\n"
            "C++ :\n"
            "- Programmer en C++ moderne (C++11 à C++20) — Claude Delannoy (n°116,117,118)\n\n"
            "Kotlin & Android :\n"
            "- Kotlin — Les fondamentaux du développement d'applications Android — Anthony Cosson (n°98,99,100)\n"
            "- Head First Kotlin — Dawn & David Griffiths (n°6,7,8)\n\n"
            "Flutter/Dart :\n"
            "- Flutter & Dart : Le Guide Complet pour Débutants — Anatol Ramon (n°78,79,80)"
        ),
    },
    {
        "id": "biblio_maths",
        "category": "bibliotheque",
        "title": "Livres — Mathématiques & Statistiques",
        "content": (
            "- Calculus Made Easy — Silvanus P. Thompson (n°190,191)\n"
            "- Toutes les mathématiques et les bases de l'informatique — Horst Stocker (n°113,114,115)\n"
            "- Statistique et probabilités pour l'ingénieur — Renée Veysseyre (n°201,202)"
        ),
    },
    {
        "id": "biblio_devperso",
        "category": "bibliotheque",
        "title": "Livres — Développement personnel & Gestion de projet",
        "content": (
            "- Atomic Habits — James Clear (n°50,51,52)\n"
            "- Mindset: The New Psychology of Success — Carol S. Dweck (n°180,181,182)\n"
            "- Getting Things Done — David Allen (n°187,188,189)\n"
            "- Emotional Intelligence 2.0 — Travis Bradberry, Jean Greaves (n°155,156,157)\n"
            "- Soft Skills: The Software Developer's Life Manual — John Sonmez (n°36,37)\n"
            "- Extreme Ownership — Jocko Willink, Leif Babin (n°11,12,13)\n"
            "- Scrum: The Art of Doing Twice the Work in Half the Time — Jeff Sutherland (n°87,88)\n"
            "- The Lean Startup — Eric Ries (n°63,64,65)\n"
            "- The Art of Project Management — Scott Berkun (n°203,204,205)\n"
            "- Hello World: How to be Human in the Age of the Machine — Hannah Fry (n°194,195,13)"
        ),
    },
    {
        "id": "biblio_recherche",
        "category": "bibliotheque",
        "title": "Livres — Rédaction scientifique & Recherche",
        "content": (
            "- How to Write a Lot — Paul J. Silvia (n°83,84)\n"
            "- The Craft of Research — Booth, Colomb, Williams (n°177,178,179)\n"
            "- Writing Science — Joshua Schimel (n°149,150,151)\n"
            "- Medkhal ila al-falsafa al-siyasiya lil-dhaka' al-ishtina'i (arabe) — Abd al-Nour Khraqi (n°197,198)"
        ),
    },
]

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------

def search(query: str) -> list:
    """Recherche simple par mots-clés dans title + content."""
    query_lower = query.lower()
    return [
        e for e in KNOWLEDGE_BASE
        if query_lower in e["title"].lower()
        or query_lower in e["content"].lower()
        or query_lower in e["category"].lower()
    ]


def get_by_category(category: str) -> list:
    return [e for e in KNOWLEDGE_BASE if e["category"] == category]


def get_by_id(entry_id: str):
    return next((e for e in KNOWLEDGE_BASE if e["id"] == entry_id), None)


CATEGORIES = sorted(set(e["category"] for e in KNOWLEDGE_BASE))

if __name__ == "__main__":
    print(f"Base chargée : {len(KNOWLEDGE_BASE)} entrées")
    print(f"Catégories : {', '.join(CATEGORIES)}")
    results = search("absence")
    print(f"Recherche 'absence' : {len(results)} résultat(s)")
    for r in results:
        print(f"  [{r['id']}] {r['title']}")
