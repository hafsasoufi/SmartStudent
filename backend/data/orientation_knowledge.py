"""
Base de connaissances statique — Orientation Agent (SmartStudent / ENIAD Berkane)
Couvre : métiers, parcours, guide CV, templates LM, questions d'entretien, certifications.
Indexée dans la collection ChromaDB 'orientation_kb' au démarrage.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 1. PROFILS MÉTIERS — par filière ENIAD
# ═══════════════════════════════════════════════════════════════════════════════

CAREER_PROFILES = [

    # ── Intelligence Artificielle ────────────────────────────────────────────
    {
        "id": "career_data_scientist",
        "category": "career_profile",
        "subcategory": "data_science",
        "relevant_majors": "IA,GINF",
        "title": "Data Scientist",
        "content": """Métier : Data Scientist

Description :
Le Data Scientist collecte, nettoie et analyse des données massives pour en extraire des insights business et construire des modèles prédictifs.

Tâches quotidiennes au Maroc :
- Collecte et nettoyage de données (Python, Pandas, SQL)
- Exploration et visualisation (Matplotlib, Seaborn, Power BI)
- Construction de modèles ML (scikit-learn, XGBoost, LightGBM)
- Déploiement de modèles (Flask/FastAPI, Docker)
- Communication des résultats aux équipes métier

Compétences requises :
Techniques : Python, SQL, Machine Learning, statistiques, visualisation de données, Git
Soft skills : communication, esprit analytique, curiosité, pédagogie envers les non-téchniques

Salaires au Maroc (2025-2026) :
- Débutant (0-2 ans) : 7 000 – 12 000 MAD/mois
- Confirmé (3-5 ans) : 15 000 – 25 000 MAD/mois
- Senior (5+ ans) : 28 000 – 45 000 MAD/mois

Entreprises qui recrutent au Maroc :
OCP Group, Attijariwafa Bank, BMCE Bank, HPS (HighTech Payment Systems), CGI Maroc, Capgemini Maroc, SQR Group, Sqli Maroc, CDG, CIH Bank, Lydec, Maroc Telecom

Formations adaptées à l'ENIAD :
Filière IA (cycle ingénieur 3 ans), Master Data Science UMP

Perspectives d'évolution :
Data Scientist → Lead Data Scientist → Head of Data → Chief Data Officer (CDO)

Stage PFA/PFE recommandé : chercher des missions sur Rekrute.ma avec mots-clés 'Data Science stage Maroc' ou 'Machine Learning ingénieur'
""",
    },

    {
        "id": "career_ml_engineer",
        "category": "career_profile",
        "subcategory": "data_science",
        "relevant_majors": "IA,GINF",
        "title": "Machine Learning Engineer",
        "content": """Métier : ML Engineer (Ingénieur Machine Learning)

Description :
Le ML Engineer conçoit, entraîne et met en production des modèles d'apprentissage automatique à grande échelle. Il fait le lien entre la recherche et la production.

Tâches quotidiennes :
- Conception de pipelines ML (MLflow, Kubeflow, Airflow)
- Entraînement et optimisation de modèles (TensorFlow, PyTorch)
- Déploiement et monitoring en production (MLOps, Docker, Kubernetes)
- Optimisation des performances (quantisation, distillation)
- Collaboration avec équipes Data Science et DevOps

Compétences requises :
Python, TensorFlow/PyTorch, Docker, Kubernetes, Cloud (AWS/Azure/GCP), MLOps, CI/CD, SQL, Git

Salaires au Maroc (2025) :
- Débutant : 10 000 – 16 000 MAD/mois
- Confirmé : 18 000 – 30 000 MAD/mois

Entreprises qui recrutent : OCP Digital Factory, Capgemini, IBM Maroc, Microsoft Maroc, startups deeptech marocaines

Certifications recommandées :
AWS Machine Learning Specialty, Google Professional ML Engineer, TensorFlow Developer Certificate
""",
    },

    {
        "id": "career_nlp_engineer",
        "category": "career_profile",
        "subcategory": "data_science",
        "relevant_majors": "IA",
        "title": "Ingénieur NLP / IA Générative",
        "content": """Métier : Ingénieur NLP / IA Générative

Description :
Spécialiste du traitement automatique du langage naturel et des modèles de langage (LLM). Développe des chatbots, systèmes de résumé, traduction automatique, RAG.

Compétences clés :
Python, Hugging Face Transformers, LangChain, LangGraph, OpenAI API, RAG (Retrieval-Augmented Generation), embeddings, bases vectorielles (ChromaDB, Pinecone, Weaviate)

Tâches :
- Fine-tuning de LLMs (LLaMA, Mistral, GPT)
- Développement de pipelines RAG
- Intégration d'agents IA dans des applications web

Salaires Maroc : 12 000 – 35 000 MAD/mois selon expérience

Ce métier est en très forte croissance depuis 2023 au Maroc, notamment dans les banques, telcos et cabinets de conseil.
""",
    },

    # ── Génie Informatique ───────────────────────────────────────────────────
    {
        "id": "career_fullstack_dev",
        "category": "career_profile",
        "subcategory": "software_engineering",
        "relevant_majors": "GINF,IA",
        "title": "Développeur Full-Stack",
        "content": """Métier : Développeur Full-Stack

Description :
Développe à la fois la partie front-end (interface utilisateur) et back-end (serveur, base de données, API) d'une application web ou mobile.

Stack techniques populaires au Maroc :
- Front-end : React.js, Vue.js, Angular, Flutter
- Back-end : Node.js (Express), Django/FastAPI (Python), Spring Boot (Java), Laravel (PHP)
- Bases de données : PostgreSQL, MySQL, MongoDB, Redis
- DevOps : Docker, Git, CI/CD GitHub Actions

Tâches quotidiennes :
- Développement de fonctionnalités front et back
- Conception d'APIs REST/GraphQL
- Review de code, tests unitaires
- Déploiement sur serveurs (VPS, AWS, OVH)

Salaires au Maroc :
- Junior : 6 000 – 10 000 MAD/mois
- Confirmé : 12 000 – 22 000 MAD/mois
- Senior : 25 000 – 40 000 MAD/mois

Top recruteurs Maroc : Sqli, CGI, HPS, Webhelp, Intelcia, SQR Group, startups (Chari, Yabadoo, Clediss), agences digitales

Formations ENIAD adaptées : Génie Informatique (GINF)
""",
    },

    {
        "id": "career_devops",
        "category": "career_profile",
        "subcategory": "cloud_devops",
        "relevant_majors": "GINF,IRSI",
        "title": "Ingénieur DevOps / Cloud",
        "content": """Métier : Ingénieur DevOps / Cloud

Description :
Automatise le cycle de vie du logiciel (build, test, deploy) et gère l'infrastructure cloud. Fait le lien entre développement et opérations.

Compétences clés :
Linux, Docker, Kubernetes, Terraform, Ansible, Jenkins, GitHub Actions, AWS/Azure/GCP, monitoring (Prometheus, Grafana), scripting Bash/Python

Salaires Maroc :
- Débutant : 9 000 – 14 000 MAD/mois
- Confirmé : 16 000 – 28 000 MAD/mois

Certifications les plus demandées : AWS Solutions Architect, CKA (Certified Kubernetes Administrator), HashiCorp Terraform Associate

Recruteurs Maroc : Atos Maroc, Capgemini, IBM, Orange Business Services, banques (BMCE, Attijariwafa), OCP
""",
    },

    {
        "id": "career_software_architect",
        "category": "career_profile",
        "subcategory": "software_engineering",
        "relevant_majors": "GINF",
        "title": "Architecte Logiciel",
        "content": """Métier : Architecte Logiciel

Description :
Conçoit la structure globale des systèmes logiciels : choix technologiques, patterns architecturaux, scalabilité, sécurité.

Profil requis : 5-8 ans d'expérience en développement avant d'accéder au rôle.

Compétences : Design patterns (SOLID, MVC, microservices, event-driven), cloud architecture, sécurité applicative, leadership technique

Salaires Maroc : 35 000 – 60 000 MAD/mois (profil senior, rare au Maroc, très demandé)

Évolution depuis GINF :
Développeur Junior → Développeur Senior → Tech Lead → Architecte Logiciel
""",
    },

    # ── IRSI ─────────────────────────────────────────────────────────────────
    {
        "id": "career_cybersecurity",
        "category": "career_profile",
        "subcategory": "cybersecurity",
        "relevant_majors": "IRSI,GINF",
        "title": "Ingénieur Cybersécurité",
        "content": """Métier : Ingénieur Cybersécurité

Description :
Protège les systèmes, réseaux et données contre les cyberattaques. Effectue des audits, tests d'intrusion et déploie des solutions de sécurité.

Spécialités :
- Pentest (test d'intrusion offensif)
- SOC Analyst (surveillance et réponse aux incidents)
- GRC (Gouvernance, Risque, Conformité)
- Sécurité applicative (DevSecOps)

Compétences : Linux, réseaux TCP/IP, Kali Linux, Metasploit, Wireshark, Nessus, SIEM (Splunk, IBM QRadar), Python scripting, ISO 27001, OWASP

Certifications clés : CompTIA Security+, CEH (Certified Ethical Hacker), OSCP (Offensive Security), CISSP (senior)

Salaires Maroc :
- Débutant SOC Analyst : 7 000 – 12 000 MAD/mois
- Pentest Engineer : 14 000 – 25 000 MAD/mois
- CISO (Chief Information Security Officer) : 40 000 – 70 000 MAD/mois

Marché très porteur au Maroc : banques, télécoms, OCP, administrations publiques (DGSSI), cabinets de conseil

Formation adaptée : IRSI (ENIAD)
""",
    },

    {
        "id": "career_network_engineer",
        "category": "career_profile",
        "subcategory": "network_engineering",
        "relevant_majors": "IRSI",
        "title": "Ingénieur Réseaux & Systèmes",
        "content": """Métier : Ingénieur Réseaux & Systèmes

Description :
Conçoit, installe et maintient les infrastructures réseau d'une organisation (LAN, WAN, VPN, WiFi, firewall, etc.).

Compétences : TCP/IP, OSPF, BGP, MPLS, Cisco IOS, Juniper, VPN (IPSec, SSL), VLAN, QoS, administration Linux/Windows Server, virtualisation VMware/Hyper-V

Certifications : Cisco CCNA, CCNP, Juniper JNCIA

Salaires Maroc :
- Ingénieur réseaux junior : 7 000 – 11 000 MAD/mois
- Senior : 15 000 – 25 000 MAD/mois

Recruteurs Maroc : Maroc Telecom, Inwi, Orange, Atos, Capgemini, banques

Formation adaptée : IRSI (ENIAD)
""",
    },

    # ── ROC ──────────────────────────────────────────────────────────────────
    {
        "id": "career_iot_engineer",
        "category": "career_profile",
        "subcategory": "robotics_iot",
        "relevant_majors": "ROC",
        "title": "Ingénieur IoT / Systèmes Embarqués",
        "content": """Métier : Ingénieur IoT / Systèmes Embarqués

Description :
Conçoit des objets connectés et des systèmes embarqués : capteurs, microcontrôleurs, communication sans fil, traitement de signal en temps réel.

Compétences : C/C++ embarqué, STM32, Arduino, ESP32, Raspberry Pi, protocoles (MQTT, LoRa, Zigbee, BLE, I2C, SPI, UART), RTOS (FreeRTOS), PCB design (KiCad)

Domaines d'application : agriculture connectée (très fort en région orientale Maroc), smart city, industrie 4.0, santé connectée

Salaires Maroc :
- Junior : 7 000 – 12 000 MAD/mois
- Confirmé : 14 000 – 22 000 MAD/mois

Recruteurs : LEONI (Berkane), Yazaki, industries agroalimentaires région orientale, startups agritech

Formation adaptée : ROC (ENIAD Berkane)
""",
    },

    {
        "id": "career_robotics_engineer",
        "category": "career_profile",
        "subcategory": "robotics_iot",
        "relevant_majors": "ROC",
        "title": "Ingénieur Robotique",
        "content": """Métier : Ingénieur Robotique

Description :
Conçoit et programme des robots industriels et autonomes. Travaille sur la mécatronique, la vision par ordinateur appliquée, et les systèmes de contrôle.

Compétences : ROS/ROS2 (Robot Operating System), Python, C++, OpenCV (vision), SLAM (navigation autonome), automates programmables (PLC), simulation (Gazebo, Webots)

Salaires Maroc :
- Junior : 8 000 – 13 000 MAD/mois
- Confirmé : 16 000 – 28 000 MAD/mois

Opportunités : industrie automobile (région Tanger), mines (OCP), agroalimentaire, recherche universitaire

Formation adaptée : ROC (ENIAD)
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 2. PARCOURS DE CARRIÈRE — de la formation au premier emploi
# ═══════════════════════════════════════════════════════════════════════════════

CAREER_PATHS = [

    {
        "id": "path_ia_to_career",
        "category": "career_path",
        "relevant_majors": "IA",
        "title": "Parcours carrière — Filière Intelligence Artificielle ENIAD",
        "content": """Parcours type d'un étudiant IA ENIAD vers le premier emploi

ÉTAPES ACADÉMIQUES :
S5-S6 (1ère année ingénieur) → Fondamentaux ML, Python, Math
S7-S8 (2ème année ingénieur) → Deep Learning, Computer Vision, NLP, Big Data
  → Stage d'été (2 mois) entre S6 et S7 : stage découverte, pas besoin d'expertise
  → Stage d'été (2 mois) entre S8 et S9 : stage technique, montrer des compétences concrètes
S9-S10 (3ème année ingénieur) → PFA (Projet de Fin d'Études) 4-6 mois en entreprise

CALENDRIER RECOMMANDÉ :
- S6 (printemps) : candidater pour stage été S6-S7 (avril-mai)
- S8 (printemps) : candidater pour stage PFE/été (mars-avril) → être sélectionné en mai
- S9 (automne) : choisir sujet PFA + commencer recherche emploi en parallèle

PREMIERS EMPLOIS ACCESSIBLES APRÈS ENIAD IA :
1. Data Scientist junior (le plus courant)
2. ML Engineer
3. Développeur IA / NLP
4. Consultant Data & IA (cabinets)
5. Ingénieur R&D IA

CONSEILS SPÉCIFIQUES FILIÈRE IA :
- Avoir un portfolio GitHub avec 3-5 projets ML/DL visibles (Kaggle, projets personnels, PFA)
- Participer à au moins 1 compétition Kaggle pendant la formation
- Apprendre à déployer (FastAPI + Docker = base minimum pour être employable)
- Créer un profil LinkedIn structuré dès la 2ème année
""",
    },

    {
        "id": "path_ginf_to_career",
        "category": "career_path",
        "relevant_majors": "GINF",
        "title": "Parcours carrière — Filière Génie Informatique ENIAD",
        "content": """Parcours type d'un étudiant GINF ENIAD vers le premier emploi

PREMIERS EMPLOIS ACCESSIBLES :
1. Développeur Full-Stack (React/Node, Django/Vue, Spring/Angular)
2. Développeur Mobile (Flutter ou React Native)
3. Ingénieur DevOps junior
4. Chef de projet IT junior (après 2-3 ans dev)

STACK MINIMALE POUR ÊTRE EMPLOYABLE EN 2025-2026 :
- 1 framework front : React.js OU Vue.js (React est plus demandé)
- 1 framework back : Node.js/Express OU Django/FastAPI OU Spring Boot
- Base de données : PostgreSQL + notions MongoDB
- Docker (base)
- Git / GitHub (indispensable)
- Déploiement : Heroku ou Railway ou VPS basique

PROJETS À AVOIR DANS SON PORTFOLIO :
1. Une application web complète (CRUD + auth + déployée)
2. Une API REST documentée (Swagger)
3. Si possible : une app mobile Flutter
4. Le PFA (doit être le projet le plus complet)

SALAIRES PREMIER EMPLOI GINF MAROC :
6 000 – 10 000 MAD/mois selon entreprise et stack maîtrisée
""",
    },

    {
        "id": "path_irsi_to_career",
        "category": "career_path",
        "relevant_majors": "IRSI",
        "title": "Parcours carrière — Filière IRSI ENIAD",
        "content": """Parcours type d'un étudiant IRSI ENIAD vers le premier emploi

PREMIERS EMPLOIS ACCESSIBLES :
1. Ingénieur réseaux junior (Cisco, administration LAN/WAN)
2. Administrateur systèmes (Linux, Windows Server)
3. SOC Analyst L1/L2 (surveillance sécurité)
4. Ingénieur cybersécurité (après spécialisation ou certification)

CERTIFICATIONS PRIORITAIRES PENDANT LA FORMATION :
Niveau 1 : CompTIA Network+ (3ème année EPSI ou 1ère année ingénieur)
Niveau 2 : Cisco CCNA (1ère ou 2ème année ingénieur) — OBLIGATOIRE pour réseau
Niveau 3 selon spécialité :
  → Sécurité : CompTIA Security+, puis CEH
  → Cloud : AWS Cloud Practitioner, puis AWS Solutions Architect
  → Systèmes : LPIC-1 (Linux), puis MCSA (Windows)

ENVIRONNEMENT LAB :
- GNS3 ou Cisco Packet Tracer pour la pratique réseau
- TryHackMe / HackTheBox pour la pratique sécurité

SALAIRES PREMIER EMPLOI IRSI MAROC :
7 000 – 11 000 MAD/mois (réseau)
8 000 – 13 000 MAD/mois (sécurité — plus rare donc mieux payé)
""",
    },

    {
        "id": "path_roc_to_career",
        "category": "career_path",
        "relevant_majors": "ROC",
        "title": "Parcours carrière — Filière ROC ENIAD",
        "content": """Parcours type d'un étudiant ROC ENIAD vers le premier emploi

PREMIER EMPLOIS ACCESSIBLES :
1. Ingénieur systèmes embarqués (STM32, ESP32)
2. Ingénieur IoT (solutions connectées agriculture/industrie)
3. Automaticien / Ingénieur contrôle-commande
4. Ingénieur robotique (R&D, peu de postes Maroc mais bien payés)

OPPORTUNITÉS LOCALES (région Berkane / Oriental) :
- LEONI Wire Systems (Berkane) : ingénieurs embarqués, automation
- Yazaki Maroc : câblage automobile, automatisation
- Secteur agroalimentaire : IoT irrigation, monitoring serres
- OCP Groupe : automation, robotique mines

PROJETS CONSEILLÉS PENDANT FORMATION :
1. Station météo connectée (ESP32 + MQTT + dashboard)
2. Bras robotique contrôlé par ML (vision + servo)
3. Système de surveillance agricole IoT (capteurs sol + LoRa + app mobile)

COMPÉTENCES À DÉVELOPPER EN DEHORS DES COURS :
- ROS2 (très valorisé, peu enseigné dans les écoles marocaines)
- MATLAB/Simulink (simulation systèmes de contrôle)
- SolidWorks ou FreeCAD (conception mécanique)
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 3. GUIDE CV — Structure, sections, erreurs courantes
# ═══════════════════════════════════════════════════════════════════════════════

CV_GUIDES = [

    {
        "id": "cv_structure_generale",
        "category": "cv_guide",
        "subcategory": "structure",
        "title": "Structure et format d'un CV ingénieur ENIAD",
        "content": """Guide CV — Structure recommandée pour étudiant ingénieur ENIAD

FORMAT GÉNÉRAL :
- Longueur : 1 page (1ère et 2ème année ingénieur), 2 pages maximum (3ème année + PFA)
- Police : Arial, Calibri ou Roboto — taille 10-11pt corps, 14-16pt nom
- Marges : 1.5 cm sur tous les côtés
- Format fichier : PDF (jamais Word ou .pages)
- Photo : OBLIGATOIRE pour les candidatures marocaines, OPTIONNELLE pour les candidatures européennes

ORDRE DES SECTIONS (CV Maroc ingénieur) :
1. En-tête : Prénom NOM — Filière — Email | Téléphone | LinkedIn (optionnel)
2. Résumé professionnel (3 lignes max — optionnel mais recommandé)
3. Formation (du plus récent au plus ancien)
4. Expériences professionnelles (stages, projets freelance)
5. Projets académiques / techniques
6. Compétences techniques (organisées par catégorie)
7. Compétences linguistiques
8. Certifications (si existantes)
9. Loisirs / Activités extrascolaires (optionnel)

SECTION COMPÉTENCES — organisation recommandée :
Langages : Python, Java, C/C++, JavaScript
Frameworks : React, Django, TensorFlow, Spring Boot
Outils : Git, Docker, Jupyter, VS Code
Bases de données : PostgreSQL, MySQL, MongoDB
Cloud : AWS (bases), Azure (bases)

SECTION FORMATION :
ENIAD Berkane — École Nationale de l'Intelligence Artificielle et du Digital
Cycle Ingénieur en [filière] | Sept. 2023 – Juin 2026 (prévu)
Principaux modules : Machine Learning, Deep Learning, Bases de données, Algorithmique…
""",
    },

    {
        "id": "cv_erreurs_courantes",
        "category": "cv_guide",
        "subcategory": "common_mistakes",
        "title": "Erreurs courantes dans les CV des étudiants ENIAD",
        "content": """Erreurs à éviter absolument dans votre CV — ENIAD Berkane

ERREURS DE CONTENU :
❌ Lister les noms de modules de cours ("j'ai suivi Algorithmique et BDD")
✅ Lister les compétences acquises ("Python, SQL, Algorithmique avancée")

❌ "Bonne maîtrise de Microsoft Office" comme compétence technique
✅ Mettre uniquement les outils réellement utilisés en projet

❌ Objectif générique : "Je suis motivé et dynamique à la recherche d'un stage"
✅ Objectif ciblé : "Étudiant ingénieur IA 3ème année, cherche un PFA en Data Science / NLP (4-6 mois)"

❌ Mentionner des projets sans résultats : "Projet de classification d'images"
✅ Avec résultats : "Modèle CNN de classification de maladies agricoles — précision 94% sur dataset Kaggle"

❌ Email non professionnel : mido_gaming99@gmail.com
✅ Email professionnel : prenom.nom@gmail.com ou prénom.nom@ump.ac.ma

ERREURS DE FORMAT :
❌ CV de 3 ou 4 pages pour un étudiant sans expérience
❌ Mélanger 3 couleurs différentes et 2 polices
❌ Envoyer le CV en format .docx
❌ Mettre une photo de mauvaise qualité ou non professionnelle
❌ Fautes d'orthographe (utiliser Grammarly ou Antidote)

ERREURS LIÉES AU CONTEXTE MAROCAIN :
❌ Omettre la date de naissance sur un CV marocain (les RH la demandent souvent)
❌ Ne pas préciser le niveau d'arabe (langue de travail dans beaucoup d'entreprises marocaines)
❌ Oublier la nationalité si vous postulez en dehors du Maroc
""",
    },

    {
        "id": "cv_exemple_ia",
        "category": "cv_guide",
        "subcategory": "examples_by_major",
        "title": "Exemple de CV — Étudiant IA 3ème année ENIAD (PFA)",
        "content": """Exemple de CV structuré — Étudiant IA 3ème année ENIAD — Recherche PFA

────────────────────────────────────────────
KHALID BENMOUSSA
Ingénieur IA — 3ème Année | ENIAD Berkane
📧 khalid.benmoussa@gmail.com | 📱 +212 6 12 34 56 78
🔗 linkedin.com/in/khalid-benmoussa | 🐙 github.com/khalid-benmoussa
────────────────────────────────────────────

OBJECTIF
Étudiant en 3ème année filière Intelligence Artificielle à l'ENIAD, cherche un PFA de 4 à 6 mois
en Data Science / NLP. Solide expérience en Python, ML et déploiement d'API.

FORMATION
École Nationale de l'Intelligence Artificielle et du Digital (ENIAD) — Berkane
Cycle Ingénieur — Filière Intelligence Artificielle | 2023 – 2026 (prévu)
Principaux modules : Machine Learning, Deep Learning, NLP, Computer Vision, Big Data,
                     Statistiques, Bases de données, Architecture logicielle

Baccalauréat Sciences Mathématiques B — Mention Très Bien | Juin 2023

EXPÉRIENCES
Stage technique — [Entreprise X] — Casablanca | Juillet – Août 2025 (2 mois)
• Développement d'un modèle de prédiction de churn client (XGBoost, précision 87%)
• Création d'un dashboard Power BI pour visualisation des KPIs client
• Technologies : Python, Pandas, XGBoost, Power BI, Git

PROJETS ACADÉMIQUES
Système de recommandation de films (S7)
• Filtrage collaboratif + TF-IDF | dataset MovieLens 1M | précision MAP@10 = 0.82
• GitHub : github.com/khalid/movie-rec

Classification de maladies agricoles par CNN (S8)
• Dataset : 54 000 images de feuilles (kaggle) | ResNet-50 fine-tuning | F1-score : 0.94
• Déploiement API FastAPI + Docker | GitHub : github.com/khalid/agri-disease

COMPÉTENCES
Langages : Python ★★★, SQL ★★★, Java ★★☆, C++ ★★☆, JavaScript ★★☆
ML/DL : scikit-learn, TensorFlow, PyTorch, Hugging Face, Pandas, NumPy, Matplotlib
Outils : Git, Docker, FastAPI, Jupyter, VS Code, Postman
Cloud & DBs : PostgreSQL, MySQL, MongoDB, bases AWS (EC2, S3)

LANGUES
Arabe : Langue maternelle | Français : C1 | Anglais : B2 (TOEIC 720)

CERTIFICATIONS
Google Data Analytics Certificate (Coursera) — Juin 2025
AWS Cloud Practitioner — Juillet 2025
────────────────────────────────────────────
""",
    },

    {
        "id": "cv_section_competences",
        "category": "cv_guide",
        "subcategory": "sections",
        "title": "Comment rédiger la section compétences selon votre filière ENIAD",
        "content": """Section Compétences — Guide par filière ENIAD

FILIÈRE IA — Compétences à lister :
Langages de programmation : Python (principal), R (optionnel), SQL, Java/C++ (bases)
Machine Learning : scikit-learn, XGBoost, LightGBM, statsmodels
Deep Learning : TensorFlow, Keras, PyTorch
NLP & LLMs : Hugging Face, LangChain, spaCy, NLTK
Computer Vision : OpenCV, YOLO, EfficientNet
MLOps : MLflow, DVC, Docker, FastAPI
Visualisation : Matplotlib, Seaborn, Plotly, Power BI
Big Data : Spark (bases), Hadoop (notions)

FILIÈRE GINF — Compétences à lister :
Langages : JavaScript, Python, Java, PHP, SQL, TypeScript
Front-end : React.js, Vue.js, HTML5/CSS3, Tailwind CSS
Back-end : Node.js, Django, Spring Boot, Laravel, FastAPI
Bases de données : PostgreSQL, MySQL, MongoDB, Redis
Mobile : Flutter, React Native
DevOps : Docker, Git, CI/CD, Linux
APIs : REST, GraphQL, Postman

FILIÈRE IRSI — Compétences à lister :
Réseaux : TCP/IP, OSPF, BGP, VLAN, VPN, Wi-Fi, Cisco IOS, Juniper
Sécurité : Firewall (pfSense, Fortinet), IDS/IPS, Kali Linux, Wireshark, Nessus, OWASP
Systèmes : Linux (administration), Windows Server, VMware, Active Directory
Cloud : AWS/Azure (notions), OpenStack
Scripting : Python, Bash

FILIÈRE ROC — Compétences à lister :
Langages embarqués : C, C++, Python, MATLAB
Microcontrôleurs : STM32, Arduino, ESP32, Raspberry Pi
Protocoles IoT : MQTT, LoRa, Zigbee, BLE, I2C, SPI, UART
Systèmes temps réel : FreeRTOS, Zephyr
Robotique : ROS/ROS2, Gazebo, OpenCV
Conception : KiCad (PCB), SolidWorks (bases), CAO
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 4. LETTRES DE MOTIVATION — templates et guide
# ═══════════════════════════════════════════════════════════════════════════════

MOTIVATION_LETTER_GUIDES = [

    {
        "id": "lm_structure_guide",
        "category": "motivation_letter",
        "subcategory": "guide_structure",
        "title": "Structure d'une lettre de motivation — Stage / PFA ingénieur ENIAD",
        "content": """Guide : Structure de la lettre de motivation pour étudiant ENIAD

RÈGLES DE BASE :
- Longueur : 1 page strictement (300-400 mots)
- Police : identique au CV (Arial ou Calibri 11pt)
- Ton : professionnel mais pas froid, personnalisé et précis
- Éviter absolument : "Je suis motivé et dynamique" (cliché repéré immédiatement)

STRUCTURE EN 4 PARTIES :

PARTIE 1 — Accroche (1 paragraphe, 3-4 lignes)
→ Pourquoi CETTE entreprise, pas une autre
→ Montrer que vous connaissez l'entreprise (projet, produit, valeur, actualité)
→ Annoncer le poste et le type de stage (PFA, été, PFE)

EXEMPLE D'ACCROCHE FORTE :
"Vos récents travaux sur l'IA appliquée à la détection de fraude dans le secteur bancaire,
présentés lors du Forum Entreprises ENIAD 2025, ont retenu toute mon attention.
C'est dans cet esprit d'innovation appliquée que je vous soumets ma candidature
pour un PFA de 5 mois en Data Science au sein de votre équipe technique."

PARTIE 2 — Votre profil académique (1 paragraphe)
→ Formation (ENIAD, filière, année)
→ 1-2 compétences techniques clés en lien avec le poste
→ 1 projet concret (résultat chiffré)

PARTIE 3 — Votre valeur ajoutée (1 paragraphe)
→ Ce que vous pouvez apporter à l'entreprise (pas l'inverse)
→ Lien entre vos compétences et leurs besoins spécifiques
→ Une soft skill prouvée par un exemple réel

PARTIE 4 — Appel à l'action (3-4 lignes)
→ Disponibilité (dates du stage)
→ Invitation à un entretien
→ Formule de politesse complète

PHRASES À ÉVITER ABSOLUMENT :
- "Je suis motivé et dynamique" → trop générique
- "Votre entreprise est leader dans son domaine" → flatterie vide
- "Ce stage me permettra d'acquérir de l'expérience" → centré sur vous, pas eux
- "Dans l'espoir d'une réponse favorable" → trop passif
- "Je reste à votre entière disposition" → formule dépassée
""",
    },

    {
        "id": "lm_template_startup",
        "category": "motivation_letter",
        "subcategory": "template_startup",
        "title": "Template LM — Stage dans une startup tech marocaine",
        "content": """Template — Lettre de motivation pour startup tech marocaine (PFA / stage été)

[Prénom NOM]
[Email] | [Téléphone] | [LinkedIn]
[Date]

[Nom de la startup]
À l'attention de [Prénom NOM du recruteur, si connu, sinon "l'équipe RH"]

Objet : Candidature pour un stage [PFA / PFE / été] en [domaine] — [Filière ENIAD], 3ème année

---

[PARAGRAPHE 1 — Accroche startup]
Votre approche [mentionner un produit, une technologie ou une valeur de la startup que vous avez réellement recherchée] m'a convaincu que [startup] est l'environnement dans lequel je souhaite contribuer concrètement pendant mon PFA. En tant qu'étudiant en [filière] à l'ENIAD Berkane, je recherche une mission de [durée] à partir de [date de début] pour mettre en pratique mes compétences en [domaine technique lié au poste].

[PARAGRAPHE 2 — Profil et compétences]
Ma formation à l'ENIAD m'a permis de maîtriser [compétences clés]. Dans le cadre de mes projets académiques, j'ai notamment [décrire un projet pertinent avec un résultat mesurable, ex: "développé un système de détection d'anomalies atteignant 92% de précision sur un dataset industriel"]. Cette expérience m'a appris à travailler de façon autonome, à itérer rapidement et à livrer des résultats concrets dans des délais contraints — des qualités essentielles dans un environnement startup.

[PARAGRAPHE 3 — Valeur ajoutée]
Je suis convaincu que [compétence 1] et [compétence 2] me permettront de contribuer rapidement à [mission ou problème spécifique de la startup, montrant que vous avez fait vos recherches]. Je suis également à l'aise avec [outil ou pratique startup : Git, Agile, déploiement continu] et habitué à apprendre rapidement de nouveaux outils selon les besoins du projet.

[PARAGRAPHE 4 — Clôture]
Disponible à partir du [date] pour une durée de [X] mois, je serais ravi d'échanger avec vous lors d'un entretien pour vous présenter plus en détail mon parcours et discuter de la façon dont je pourrais contribuer à [startup]. Je reste joignable au [téléphone] ou par email.

Veuillez agréer, [Madame/Monsieur], l'expression de mes salutations respectueuses.

[Prénom NOM]
""",
    },

    {
        "id": "lm_template_multinational",
        "category": "motivation_letter",
        "subcategory": "template_multinational",
        "title": "Template LM — Stage dans une multinationale (Capgemini, IBM, Atos, OCP…)",
        "content": """Template — Lettre de motivation pour grande entreprise / multinationale présente au Maroc

[Prénom NOM]
[Email] | [Téléphone] | [LinkedIn]
[Date]

[Nom de l'entreprise]
Direction des Ressources Humaines
[Adresse ou ville]

Objet : Candidature pour un stage de fin d'études (PFA) — [Intitulé du poste] — Filière [filière] ENIAD

---

Madame, Monsieur,

[PARAGRAPHE 1 — Accroche multinationale]
[Nom de l'entreprise] s'est imposé comme [positionnement réel de l'entreprise, ex: "l'un des acteurs de référence en transformation digitale des entreprises marocaines"]. Votre récent investissement dans [projet ou initiative connu, ex: "le développement d'un centre d'excellence IA à Casablanca" ou "votre partenariat avec le Ministère de l'Industrie"] confirme votre engagement dans l'innovation. C'est dans ce cadre que je vous soumets ma candidature pour un PFA de [X] mois au sein de votre département [nom du département].

[PARAGRAPHE 2 — Formation et compétences ciblées]
Actuellement en 3ème année du cycle ingénieur en [filière] à l'ENIAD Berkane (École Nationale de l'Intelligence Artificielle et du Digital), ma formation m'a permis d'acquérir de solides compétences en [compétences 1, 2, 3]. Mon projet de [description projet académique concret] — mené en équipe de [X] personnes — m'a permis de [résultat mesurable] et de renforcer mes capacités en gestion de projet technique et en travail collaboratif.

[PARAGRAPHE 3 — Adéquation poste / profil]
Le poste de [intitulé] que vous proposez correspond précisément à la direction que je souhaite donner à ma carrière en [domaine]. Ma maîtrise de [compétence clé en lien avec l'offre] et mon expérience avec [outil ou technologie mentionné dans l'offre] me permettront de m'intégrer rapidement et d'apporter une contribution effective dès les premières semaines de stage.

[PARAGRAPHE 4 — Clôture formelle]
Disponible à partir du [date de début] pour une durée de [X] mois, je serais honoré de vous présenter ma candidature lors d'un entretien à votre convenance. Vous trouverez ci-joint mon curriculum vitæ.

Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, l'expression de mes sincères salutations.

[Prénom NOM]
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 5. QUESTIONS D'ENTRETIEN TECHNIQUES — par filière
# ═══════════════════════════════════════════════════════════════════════════════

INTERVIEW_TECHNICAL = [

    {
        "id": "interview_tech_ia_ml",
        "category": "interview_technical",
        "subcategory": "python_ml",
        "relevant_majors": "IA,GINF",
        "title": "Questions techniques d'entretien — Machine Learning / Data Science",
        "content": """Questions fréquentes en entretien technique — Machine Learning & Data Science

NIVEAU DÉBUTANT (stage été / PFA 1ère candidature) :
1. Quelle est la différence entre l'apprentissage supervisé et non supervisé ?
   → Supervisé : les données ont des labels (ex: classification chat/chien). Non supervisé : pas de labels, on cherche des structures cachées (clustering, réduction de dimensionnalité).

2. Qu'est-ce que le surapprentissage (overfitting) ? Comment le détecter et le corriger ?
   → Le modèle mémorise les données d'entraînement mais ne généralise pas. Détection : faible erreur train, haute erreur validation. Correction : régularisation (L1/L2), dropout, early stopping, plus de données, cross-validation.

3. Expliquez la différence entre précision (precision) et rappel (recall). Quand privilégier l'un ou l'autre ?
   → Précision = TP/(TP+FP) — Rappel = TP/(TP+FN). Privilégier précision quand les faux positifs coûtent cher (spam). Privilégier rappel quand les faux négatifs coûtent cher (cancer, fraude bancaire).

4. Qu'est-ce qu'une forêt aléatoire (Random Forest) ? Comment fonctionne-t-elle ?
   → Ensemble de N arbres de décision entraînés sur des sous-ensembles aléatoires (bagging). La prédiction finale est la moyenne (régression) ou le vote majoritaire (classification). Réduit la variance vs un seul arbre.

5. Comment gérez-vous les valeurs manquantes dans un dataset ?
   → Imputation (moyenne, médiane, mode, KNN Imputer, MICE), suppression si peu de données affectées, ou modéliser la valeur manquante comme feature (indicateur binaire).

NIVEAU CONFIRMÉ (PFE, entretien entreprise) :
6. Expliquez le gradient descent et ses variantes (SGD, Adam, RMSProp).
7. Qu'est-ce que la régularisation L1 vs L2 ? Quel effet sur les coefficients ?
8. Comment fonctionne l'algorithme XGBoost ? Quels sont ses hyperparamètres clés ?
9. Quelle est la différence entre bagging et boosting ?
10. Comment évaluer un modèle de clustering (K-Means) ? (Silhouette score, Elbow method)

QUESTION PRATIQUE FRÉQUENTE :
"Vous avez un dataset de 1 million de lignes avec 30% de valeurs manquantes dans une colonne cible. Comment vous procédez ?"
→ Montrer votre démarche : analyse des patterns de valeurs manquantes (MCAR/MAR/MNAR), choix d'imputation, validation de l'impact sur le modèle.
""",
    },

    {
        "id": "interview_tech_python",
        "category": "interview_technical",
        "subcategory": "python_ml",
        "relevant_majors": "IA,GINF,IRSI",
        "title": "Questions techniques d'entretien — Python",
        "content": """Questions fréquentes en entretien technique — Python

QUESTIONS DE BASE :
1. Quelle est la différence entre une liste et un tuple en Python ?
   → Liste : mutable (modifiable), [1,2,3]. Tuple : immutable, (1,2,3). Tuple plus rapide, utilisé pour données constantes.

2. Qu'est-ce qu'un décorateur (@) en Python ? Donnez un exemple.
   → Fonction qui enveloppe une autre fonction pour modifier son comportement. Ex: @property, @staticmethod, @lru_cache

3. Expliquez les compréhensions de liste. Quelle est leur avantage ?
   → [x**2 for x in range(10) if x % 2 == 0] — plus lisible et plus rapide que boucle for équivalente.

4. Quelle est la différence entre == et is en Python ?
   → == compare les valeurs, is compare les identités en mémoire (même objet). None s'utilise avec is None, pas == None.

5. Qu'est-ce que GIL (Global Interpreter Lock) ? Pourquoi est-ce important ?
   → Mutex qui empêche plusieurs threads Python d'exécuter du bytecode simultanément. Impact : threading ne parallélise pas le CPU. Solution : multiprocessing ou asyncio pour I/O.

QUESTIONS INTERMÉDIAIRES :
6. Expliquez *args et **kwargs. Quand les utilise-t-on ?
7. Qu'est-ce qu'un générateur (yield) ? Avantage vs liste ?
8. Différence entre deepcopy et copy en Python ?
9. Comment fonctionne la gestion de la mémoire en Python (garbage collector) ?
10. Qu'est-ce que les context managers (with statement) ? Implémentez __enter__ et __exit__.
""",
    },

    {
        "id": "interview_tech_ginf_web",
        "category": "interview_technical",
        "subcategory": "java_web",
        "relevant_majors": "GINF",
        "title": "Questions techniques d'entretien — Développement Web / Full-Stack",
        "content": """Questions fréquentes en entretien technique — Web / Full-Stack (GINF)

JAVASCRIPT / REACT :
1. Quelle est la différence entre var, let et const ?
   → var : portée fonction, hoisting. let/const : portée bloc (ES6). const : référence immuable (l'objet peut changer).

2. Qu'est-ce que le closure en JavaScript ?
   → Fonction qui a accès aux variables de son scope parent même après la fin d'exécution de ce scope.

3. Comment React gère-t-il le re-rendering ? Qu'est-ce que le Virtual DOM ?
   → React maintient un Virtual DOM en mémoire, compare (diffing) avec le DOM réel, et ne met à jour que les parties changées.

4. Quelle est la différence entre useState et useReducer ?
   → useState pour état simple. useReducer pour état complexe avec logique de transitions (similaire à Redux).

5. Qu'est-ce que CORS ? Comment le gérer côté back-end ?
   → Cross-Origin Resource Sharing — mécanisme de sécurité navigateur. Configurer les headers Access-Control-Allow-Origin côté serveur.

BASES DE DONNÉES :
6. Différence entre SQL et NoSQL ? Quand choisir l'un ou l'autre ?
7. Qu'est-ce qu'un index en SQL ? Comment améliore-t-il les performances ?
8. Expliquez les transactions ACID.
9. Qu'est-ce que N+1 problem en ORM ? Comment l'éviter ?

REST APIs :
10. Quels sont les codes HTTP importants à connaître ? (200, 201, 400, 401, 403, 404, 422, 500)
11. Différence entre PUT et PATCH ?
12. Qu'est-ce que JWT ? Comment fonctionne l'authentification JWT ?
""",
    },

    {
        "id": "interview_tech_irsi_networks",
        "category": "interview_technical",
        "subcategory": "networks_security",
        "relevant_majors": "IRSI",
        "title": "Questions techniques d'entretien — Réseaux & Cybersécurité",
        "content": """Questions fréquentes en entretien technique — Réseaux & Sécurité (IRSI)

RÉSEAUX :
1. Expliquez le modèle OSI. Citez les 7 couches et leur rôle.
   → Physique, Liaison, Réseau, Transport, Session, Présentation, Application.
   TCP/IP = 4 couches : Accès réseau, Internet, Transport, Application.

2. Quelle est la différence entre TCP et UDP ?
   → TCP : connexion orientée, fiable, contrôle de flux (HTTP, FTP, SSH). UDP : sans connexion, plus rapide, pas de garantie (DNS, vidéo streaming, VoIP).

3. Expliquez le processus de handshake TCP (three-way handshake).
   → Client envoie SYN → Serveur répond SYN-ACK → Client confirme ACK. Connexion établie.

4. Qu'est-ce que le subnetting ? Calculez le subnet pour 192.168.1.0/26.
   → /26 = masque 255.255.255.192 = 64 adresses par réseau, 62 hôtes utilisables.
   Réseaux : .0, .64, .128, .192

5. Différence entre routage statique et dynamique (OSPF, BGP) ?

CYBERSÉCURITÉ :
6. Qu'est-ce qu'une attaque SQL injection ? Comment la prévenir ?
   → Injection de SQL malicieux via input. Prévention : requêtes préparées (prepared statements), ORMs, validation/sanitisation des inputs.

7. Expliquez les attaques XSS (Cross-Site Scripting). Comment les contrer ?
8. Qu'est-ce que le principe du moindre privilège (least privilege) ?
9. Expliquez la différence entre chiffrement symétrique et asymétrique. Exemples (AES, RSA).
10. Qu'est-ce qu'un certificat SSL/TLS ? Comment fonctionne HTTPS ?
11. Qu'est-ce qu'un VLAN et pourquoi l'utiliser en sécurité ?
""",
    },

    {
        "id": "interview_tech_roc_embedded",
        "category": "interview_technical",
        "subcategory": "embedded_iot",
        "relevant_majors": "ROC",
        "title": "Questions techniques d'entretien — Systèmes Embarqués & IoT",
        "content": """Questions fréquentes en entretien technique — Embarqué & IoT (ROC)

SYSTÈMES EMBARQUÉS :
1. Quelle est la différence entre un microcontrôleur et un microprocesseur ?
   → Microcontrôleur : CPU + mémoire + périphériques intégrés sur une puce (STM32, Arduino). Microprocesseur : CPU seul, nécessite composants externes (Raspberry Pi, PC).

2. Qu'est-ce qu'un RTOS ? Pourquoi l'utiliser dans un système embarqué ?
   → Real-Time Operating System : OS déterministe garantissant des temps de réponse prévisibles. Utile pour systèmes temps-réel (contrôle moteur, médical). FreeRTOS est le plus utilisé.

3. Expliquez les protocoles de communication I2C et SPI. Différences ?
   → I2C : 2 fils (SDA, SCL), adressage, multi-esclave, plus lent. SPI : 4 fils (MOSI, MISO, CLK, CS), plus rapide, full-duplex.

4. Qu'est-ce qu'un watchdog timer ? Pourquoi est-il important ?
   → Timer matériel qui redémarre le système si le firmware ne le remet pas à zéro dans le temps imparti. Sécurité contre les blocages système (hang).

5. Comment gérez-vous la consommation d'énergie dans un système IoT fonctionnant sur batterie ?
   → Sleep modes (deep sleep, light sleep), réveil par interruption, optimisation fréquence CPU, duty cycling des radios.

IoT :
6. Quelle différence entre MQTT et HTTP pour les communications IoT ?
7. Expliquez LoRaWAN. Pour quels cas d'usage est-il adapté au Maroc ?
8. Comment sécurisez-vous un dispositif IoT ? (firmware signing, secure boot, TLS)
9. Qu'est-ce que le Edge Computing ? Avantages pour l'IoT ?
10. Comment déboguez-vous un firmware embarqué sans système d'exploitation ?
""",
    },

    {
        "id": "interview_tech_databases",
        "category": "interview_technical",
        "subcategory": "databases_sql",
        "relevant_majors": "IA,GINF,IRSI",
        "title": "Questions techniques d'entretien — Bases de données & SQL",
        "content": """Questions fréquentes en entretien — Bases de données & SQL

REQUÊTES SQL :
1. Écrivez une requête pour trouver les 3 employés les mieux payés par département.
   → SELECT dept, nom, salaire FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salaire DESC) as rn FROM employes) WHERE rn <= 3;

2. Différence entre INNER JOIN, LEFT JOIN, RIGHT JOIN et FULL OUTER JOIN ?
   → INNER : intersection. LEFT : tous de gauche + correspondances droite. RIGHT : inverse. FULL OUTER : tout.

3. Qu'est-ce qu'un index ? Quand NE PAS indexer ?
   → Structure accélérant les SELECT (B-tree, hash). Ne pas indexer : colonnes rarement interrogées, tables très petites, colonnes avec peu de cardinalité.

4. Expliquez les formes normales (1NF, 2NF, 3NF).
5. Qu'est-ce qu'une vue (VIEW) ? Avantages et limites ?
6. Différence entre DELETE, TRUNCATE et DROP ?

OPTIMISATION :
7. Comment optimisez-vous une requête SQL lente ? (EXPLAIN ANALYZE)
8. Qu'est-ce que le problème N+1 et comment l'éviter ?
9. Différence entre BASE de données relationnelle et NoSQL pour un use case e-commerce ?

TRANSACTIONS :
10. Qu'est-ce que les propriétés ACID ? Donnez un exemple de transaction bancaire.
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 6. QUESTIONS D'ENTRETIEN COMPORTEMENTALES (STAR)
# ═══════════════════════════════════════════════════════════════════════════════

INTERVIEW_BEHAVIORAL = [

    {
        "id": "interview_behavioral_star",
        "category": "interview_behavioral",
        "subcategory": "star_method",
        "title": "Méthode STAR pour les entretiens comportementaux",
        "content": """La méthode STAR — Répondre aux questions comportementales en entretien

Qu'est-ce que la méthode STAR ?
STAR = Situation, Tâche, Action, Résultat
C'est la méthode universelle pour structurer les réponses aux questions comportementales.
Elle transforme une réponse vague en une réponse convaincante et mémorable.

STRUCTURE D'UNE RÉPONSE STAR :
S — Situation : Décrivez le contexte (projet académique, stage, club étudiant)
T — Tâche : Quel était votre rôle / défi spécifique ?
A — Action : Qu'avez-vous fait concrètement ? (pas "nous avons" — "J'ai")
R — Résultat : Quel a été l'impact mesurable ?

EXEMPLES DE RÉPONSES STAR POUR ÉTUDIANTS ENIAD :

Question : "Parlez-moi d'une fois où vous avez dû travailler en équipe sur un projet difficile."
Mauvaise réponse : "J'ai fait beaucoup de projets en équipe à l'ENIAD et ça s'est bien passé."

Bonne réponse (STAR) :
"S : En 2ème année, notre équipe de 4 devait livrer un système de recommandation en 3 semaines.
T : J'étais responsable du module ML et du déploiement API.
A : La semaine avant la deadline, un coéquipier a décroché du projet. J'ai redistribué les tâches,
    j'ai pris la partie front-end Streamlit en plus, et j'ai organisé des sessions de travail nocturnes.
R : On a livré à temps avec une précision de 87%. Le prof a noté 18/20 et a cité notre déploiement
    FastAPI comme exemple pour les promotions suivantes."

QUESTIONS COMPORTEMENTALES FRÉQUENTES EN ENTRETIEN MAROC :
1. Parlez-moi de vous et de votre parcours.
2. Pourquoi avez-vous choisi la filière [IA/GINF/IRSI/ROC] ?
3. Quel est votre plus grand succès académique ?
4. Racontez une situation où vous avez échoué. Qu'avez-vous appris ?
5. Comment gérez-vous les conflits dans une équipe ?
6. Décrivez un moment où vous avez dû apprendre rapidement une nouvelle technologie.
7. Pourquoi vous et pas un autre candidat ?
8. Où vous voyez-vous dans 5 ans ?
9. Quels sont vos points forts ? Vos points d'amélioration ?
10. Pourquoi voulez-vous travailler chez nous ?
""",
    },

    {
        "id": "interview_behavioral_teamwork",
        "category": "interview_behavioral",
        "subcategory": "teamwork",
        "title": "Questions entretien comportemental — Travail en équipe",
        "content": """Questions comportementales — Teamwork & Collaboration

Q : "Décrivez une situation où vous avez eu un désaccord avec un coéquipier. Comment l'avez-vous résolu ?"

Conseil STAR :
S : Projet de fin de semestre — désaccord sur l'architecture (microservices vs monolithe)
T : Trouver consensus pour avancer avant la deadline
A : Proposé un PoC de 2 jours pour les deux approches, présentation des métriques (vitesse dev, complexité déploiement)
R : Équipe a choisi l'approche monolithe pour ce projet, mais le coéquipier a maintenu sa logique pour le PFA suivant. Pas de conflit persistant.

CONSEIL RH MAROC :
Les recruteurs marocains apprécient particulièrement les candidats qui montrent une capacité à écouter ET à défendre leur point de vue avec données/arguments — pas juste la soumission ou l'entêtement.

Q : "Comment organisez-vous le travail en équipe quand tout le monde a des emplois du temps différents ?"
→ Mentionner Trello/Jira pour la gestion de tâches, Git pour collaboration code, Discord/WhatsApp pour communication, Google Meet pour synchronisation.
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 7. CERTIFICATIONS & COMPÉTENCES À ACQUÉRIR
# ═══════════════════════════════════════════════════════════════════════════════

SKILLS_CERTIFICATIONS = [

    {
        "id": "cert_free_path_all",
        "category": "skills_certification",
        "subcategory": "free_resources",
        "title": "Certifications gratuites recommandées pour étudiants ENIAD",
        "content": """Certifications GRATUITES accessibles pendant la formation à l'ENIAD

TOUTES FILIÈRES :
1. Google IT Support Certificate (Coursera — gratuit avec aide financière)
   Durée : 6 mois | Niveau : débutant | Valeur : très reconnue par les PME marocaines
   Lien : coursera.org/professional-certificates/google-it-support

2. Google Data Analytics Certificate (Coursera — gratuit avec aide financière)
   Durée : 6 mois | Niveau : débutant-intermédiaire
   Lien : coursera.org/professional-certificates/google-data-analytics

3. Microsoft Azure Fundamentals AZ-900
   Gratuit via Microsoft Learn (cours) + examen 165$ (demander sponsoring employeur ou ENIAD)
   Prépare en ~20h d'auto-formation : learn.microsoft.com

4. AWS Cloud Practitioner (CLF-C02)
   Cours gratuits : AWS Skill Builder (skillbuilder.aws)
   Examen : ~100$ | Durée préparation : 2-3 semaines

FILIÈRE IA :
5. TensorFlow Developer Certificate — Google | 100$ | Très demandé recruteurs IA
6. DeepLearning.AI Specialization (Andrew Ng, Coursera) — Référence mondiale ML
   5 cours + certificat | Gratuit en audit | Payant pour certificat ($49/mois)

FILIÈRE GINF :
7. Meta Front-End Developer Certificate (Coursera) | Gratuit avec aide financière
8. Oracle Certified Associate Java SE 8 — reconnu partout | Préparation : 3 mois

FILIÈRE IRSI :
9. CompTIA Network+ — certification réseau de base, reconnue au Maroc
10. Cisco CCNA — indispensable pour tout poste réseau Maroc | ~300$
11. TryHackMe — pas un certificat mais une plateforme de pratique sécurité | GRATUIT

FILIÈRE ROC :
12. Arduino Official Certification — peu coûteuse, reconnue industrie embarquée
13. ARM Accredited Engineer (AAE) — systèmes embarqués ARM, reconnu industrie
""",
    },

    {
        "id": "cert_cloud_path",
        "category": "skills_certification",
        "subcategory": "cloud",
        "title": "Parcours certifications Cloud — AWS, Azure, GCP pour ENIAD",
        "content": """Parcours de certifications Cloud recommandé — ENIAD

POURQUOI LE CLOUD EST IMPORTANT AU MAROC :
- La majorité des offres d'emploi tech au Maroc mentionnent AWS, Azure ou GCP depuis 2023
- OCP, Maroc Telecom, banques : migration cloud massive en cours
- Salaire +15-25% pour ingénieur cloud vs développeur classique

PARCOURS AWS (le plus demandé au Maroc) :
Niveau 1 : AWS Cloud Practitioner (CLF-C02) — 2-3 semaines — ~100$
Niveau 2 : AWS Solutions Architect Associate (SAA-C03) — 2-3 mois — ~150$
Niveau 3 (spécialité) :
  → IA/Data : AWS Machine Learning Specialty
  → IRSI/DevOps : AWS DevOps Engineer Professional
  → GINF : AWS Developer Associate

PARCOURS AZURE :
AZ-900 (Fundamentals) → AZ-104 (Administrator) → AZ-204 (Developer)

PARCOURS GCP :
Associate Cloud Engineer → Professional Cloud Architect

CONSEIL PRATIQUE :
Préparez AWS Cloud Practitioner en 2ème année ingénieur (20h de cours AWS Skill Builder gratuit).
C'est le meilleur investissement temps/argent pour améliorer votre employabilité immédiate.
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 8. OFFRES DE STAGE — exemples et plateformes (données statiques)
# ═══════════════════════════════════════════════════════════════════════════════

INTERNSHIP_GUIDES = [

    {
        "id": "internship_platforms_morocco",
        "category": "internship_offer",
        "subcategory": "platforms",
        "title": "Plateformes et méthodes pour trouver un stage au Maroc",
        "content": """Guide — Trouver un stage / PFA / PFE au Maroc

PLATEFORMES DÉDIÉES :
1. Rekrute.ma — Le plus grand job board Maroc
   URL : rekrute.com | Filtre : Type = Stage | Niveau = Bac+5 | Ville + Secteur
   Astuce : Activer les alertes email par mots-clés ("Data Science stage", "Développeur Python stage")

2. Stage.ma — Spécialisé stages Maroc
   URL : stagema.ma | Idéal pour stages courts (1-3 mois)

3. LinkedIn Maroc — Pour multinationales et startups
   Recherche : "stage" + [technologie] + [ville] | Se connecter avec alumni ENIAD

4. Indeed Maroc — indeed.ma | Agrège plusieurs sources

5. AIESEC Maroc — Stages internationaux | aiesec.ma

MÉTHODE DE CANDIDATURE SPONTANÉE :
1. Identifier 20 entreprises cibles (secteur + ville)
2. Trouver le contact RH ou le manager technique sur LinkedIn
3. Envoyer email avec objet précis : "Candidature PFA — Data Science — Étudiant ENIAD 3ème année"
4. CV + LM en PDF en pièce jointe
5. Relancer après 7 jours si pas de réponse

CALENDRIER DES CANDIDATURES :
Pour stage d'été (juillet-août) : candidater en AVRIL-MAI
Pour PFA (septembre-janvier) : candidater en JUIN-JUILLET
Pour PFE (mars-août) : candidater en DÉCEMBRE-JANVIER

ENTREPRISES QUI RECRUTENT RÉGULIÈREMENT DES STAGIAIRES ENIAD :
OCP Group (Khouribga, Casablanca), HPS (Casablanca), CGI Maroc, Capgemini Maroc,
Attijariwafa Bank (Lab Digital), BMCE Bank (DSI), SQR Group, SQLI Maroc,
Maroc Telecom (DSI), Intelcia Group, Webhelp Maroc, Leoni Berkane (ROC/IRSI)

FORUM ENTREPRISES ENIAD :
L'ENIAD organise chaque année un Forum Entreprises (généralement mars-avril).
C'est l'opportunité de rencontrer directement les recruteurs et déposer son CV en main propre.
Préparer 10 copies de son CV et une courte présentation orale (1 minute).
""",
    },

    {
        "id": "internship_convention_process",
        "category": "internship_offer",
        "subcategory": "administrative",
        "title": "Procédure convention de stage ENIAD — étapes complètes",
        "content": """Procédure pour obtenir et valider une convention de stage — ENIAD Berkane

QUAND EN AVEZ-VOUS BESOIN ?
Pour tout stage d'été, PFA ou PFE, une convention signée est OBLIGATOIRE avant le premier jour.
Sans convention, le stage n'est pas validé et vous n'avez aucune couverture légale.

ÉTAPES :
1. Trouver l'entreprise et obtenir une validation orale du tuteur de stage
2. Télécharger la convention vierge : https://eniad.ump.ma/storage/files/1/Convention de stage/68234cd5a6293.pdf
3. Remplir vos coordonnées, les dates, la description de la mission, et le nom du tuteur
4. Faire signer le tuteur en entreprise (signature + cachet entreprise)
5. Déposer à la Scolarité ENIAD pour signature du Directeur
6. Récupérer la convention signée des deux parties
7. Remettre une copie à l'entreprise, garder l'original

DÉLAI : Prévoir 1 semaine pour la signature côté ENIAD. Déposez AVANT la date de début.

CONTENU DE LA MISSION :
Remplir la partie "Description du travail confié" avec précision :
Ex: "Développement d'un modèle de classification d'images agricoles par deep learning (CNN/ResNet)
      et déploiement via API FastAPI. Évaluation sur dataset de 50 000 images."

RAPPORT DE STAGE :
À rendre à la fin du stage à l'ENIAD. Format : 30-50 pages selon le type de stage.
Contenu : contexte entreprise, problématique, solution développée, résultats, bilan personnel.
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 9. CONSEILS RÉSEAU PROFESSIONNEL
# ═══════════════════════════════════════════════════════════════════════════════

NETWORKING_TIPS = [

    {
        "id": "networking_linkedin",
        "category": "networking_tips",
        "subcategory": "linkedin_profile",
        "title": "Créer et optimiser son profil LinkedIn — Guide étudiant ENIAD",
        "content": """Optimiser son profil LinkedIn en tant qu'étudiant ENIAD

POURQUOI LINKEDIN EST INDISPENSABLE AU MAROC :
- 80% des offres de stages tech au Maroc sont publiées en premier sur LinkedIn
- Les recruteurs contactent directement les profils actifs
- Les alumni ENIAD sont sur LinkedIn et peuvent recommander

PHOTO DE PROFIL :
✅ Photo professionnelle (fond uni, tenue correcte, sourire)
✅ Taille 400x400px minimum
❌ Photo floue, selfie, photo de sortie

TITRE PROFESSIONNEL (juste sous le nom) :
Format recommandé : "Étudiant Ingénieur [Filière] @ENIAD | [Compétence 1] | [Compétence 2] | En recherche de [type de stage]"
Exemple : "Étudiant Ingénieur IA @ENIAD Berkane | Python · Machine Learning · Deep Learning | Cherche PFA Data Science"

RÉSUMÉ (section À propos) :
3-4 lignes max :
"Étudiant en 3ème année filière Intelligence Artificielle à l'ENIAD Berkane (UMP). Passionné par le Machine Learning appliqué et le NLP, j'ai développé plusieurs projets mettant en œuvre des modèles de classification, de recommandation et de détection d'anomalies. Je recherche un PFA de 4 à 6 mois à partir de septembre 2026 dans un environnement technique stimulant."

SECTION EXPÉRIENCES :
→ Ajouter les stages même courts
→ Ajouter les projets académiques importants comme des "expériences"
→ Résultats quantifiés : "Modèle atteint 94% de précision", "Livré en 3 semaines"

COMPÉTENCES À AFFICHER (les 5 premières sont les plus visibles) :
Mettez Python, Machine Learning, SQL, Git, et votre framework principal en premier.

ACTIONS HEBDOMADAIRES RECOMMANDÉES :
- Liker/commenter 3 posts de professionnels du domaine
- Envoyer 2-3 demandes de connexion avec note personnalisée
- Partager 1 article ou résultat de projet personnel/mois
""",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# COLLECTION COMPLÈTE — pour indexation ChromaDB
# ═══════════════════════════════════════════════════════════════════════════════

ALL_ORIENTATION_DOCUMENTS = (
    CAREER_PROFILES
    + CAREER_PATHS
    + CV_GUIDES
    + MOTIVATION_LETTER_GUIDES
    + INTERVIEW_TECHNICAL
    + INTERVIEW_BEHAVIORAL
    + SKILLS_CERTIFICATIONS
    + INTERNSHIP_GUIDES
    + NETWORKING_TIPS
)
