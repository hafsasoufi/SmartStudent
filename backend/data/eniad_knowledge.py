"""
Base de connaissances statique de l'ENIAD — Berkane
Source : https://eniad.ump.ma/fr (scraping mai 2026)
Complète les PDFs téléchargés pour le système RAG.
"""

ENIAD_KNOWLEDGE_BASE = [
    # ── Présentation générale ────────────────────────────────────────────────
    {
        "id": "eniad_presentation",
        "category": "institution",
        "title": "Présentation de l'ENIAD",
        "content": """L'École Nationale de l'Intelligence Artificielle et du Digital (ENIAD) est établie à Berkane, Maroc.
Elle fait partie de l'Université Mohammed Ier (UMP) dans la région orientale du Maroc.
Fondée en 1978, l'ENIAD forme des ingénieurs dans les domaines de l'intelligence artificielle, des réseaux, de la robotique et de l'informatique.
Contact : eniad@ump.ac.ma | Téléphone : +212 536
Site web : https://eniad.ump.ma
Plateforme e-learning : http://eniadelearning.ump.ma
Bibliothèque : http://bib.ump.ma
Langues d'enseignement : Français (principal), Arabe, Anglais
L'école se distingue par son accent sur l'intelligence artificielle, le digital et les technologies émergentes.
"""
    },

    # ── Filières ─────────────────────────────────────────────────────────────
    {
        "id": "filiere_ia",
        "category": "formation",
        "title": "Filière Intelligence Artificielle (IA) — Cycle Ingénieur",
        "content": """La filière Intelligence Artificielle (IA) est un cycle ingénieur de 3 ans (6 semestres : S5 à S10).
Semestres : S5, S6 (1ère année ingénieur), S7, S8 (2ème année ingénieur), S9, S10 (3ème année ingénieur).
Cette formation couvre : Machine Learning, Deep Learning, NLP, Computer Vision, Data Science, Big Data.
Les étudiants réalisent un PFA (Projet de Fin d'Études) en 3ème année (S9-S10).
Le PFA est soutenu devant un jury en fin de S10.
Accès : après le cycle préparatoire EPSI (2 ans) ou concours national.
Débouchés : Data Scientist, ML Engineer, AI Engineer, chercheur.
"""
    },
    {
        "id": "filiere_irsi",
        "category": "formation",
        "title": "Filière Ingénierie Réseaux et Sécurité Informatique (IRSI) — Cycle Ingénieur",
        "content": """La filière IRSI (Ingénierie des Réseaux et Sécurité Informatique) est un cycle ingénieur de 3 ans.
Semestres : S5, S6, S7, S8, S9, S10.
Cette formation couvre : Réseaux informatiques, Cybersécurité, Protocoles, Infrastructures réseau, Cloud computing.
Spécialisée dans la sécurité des systèmes d'information et la protection des données.
PFA obligatoire en 3ème année. Soutenance devant jury.
Débouchés : Ingénieur réseau, Expert en cybersécurité, Administrateur système.
"""
    },
    {
        "id": "filiere_roc",
        "category": "formation",
        "title": "Filière Robotique et Objets Connectés (ROC) — Cycle Ingénieur",
        "content": """La filière ROC (Robotique et Objets Connectés) est un cycle ingénieur de 3 ans.
Semestres : S5, S6, S7, S8, S9, S10.
Formation couvrant : Robotique, IoT (Internet of Things), Systèmes embarqués, Électronique, Automatique.
Intègre programmation hardware/software et systèmes cyber-physiques.
PFA obligatoire en 3ème année.
Débouchés : Ingénieur robotique, Développeur IoT, Automaticien.
"""
    },
    {
        "id": "filiere_ginf",
        "category": "formation",
        "title": "Filière Génie Informatique (GINF) — Cycle Ingénieur",
        "content": """La filière GINF (Génie Informatique) est un cycle ingénieur de 3 ans.
Semestres : S5, S6, S7, S8, S9, S10.
Formation couvrant : Développement logiciel, Architecture logicielle, Bases de données, Génie logiciel, Web/Mobile.
PFA obligatoire en 3ème année.
Débouchés : Développeur full-stack, Architecte logiciel, Chef de projet informatique.
"""
    },
    {
        "id": "filiere_epsi",
        "category": "formation",
        "title": "Cycle Préparatoire EPSI — Études Préparatoires en Sciences de l'Ingénieur",
        "content": """L'EPSI (Études Préparatoires en Sciences de l'Ingénieur) est un cycle de 2 ans (S1, S2, S3, S4).
Prépare les étudiants à intégrer le cycle ingénieur.
Matières : Mathématiques, Physique, Informatique, Anglais, Communication.
Les meilleurs étudiants intègrent directement les filières IA, IRSI, ROC ou GINF en S5.
Admission : Bac scientifique ou technique avec mention. Concours national.
Organisation en groupes TD (Travaux Dirigés) et TP (Travaux Pratiques).
"""
    },

    # ── Calendrier académique ──────────────────────────────────────────────
    {
        "id": "calendrier_academique",
        "category": "calendrier",
        "title": "Calendrier Académique 2025-2026",
        "content": """Année académique 2025-2026 :
- Semestre Automne (SA) : Septembre 2025 — Janvier 2026
  * Début des cours : Septembre 2025
  * Examens fin de semestre : Janvier 2026
  * Session de rattrapage : Février 2026
- Semestre Printemps (SP) : Février 2026 — Juin 2026
  * Début des cours : Février 2026
  * Contrôles continus d'avril : Avril 2026
  * Examens fin de semestre : Juin 2026
  * Session de rattrapage : Juin-Juillet 2026

Pour consulter les emplois du temps détaillés par filière, rendez-vous sur :
https://eniad.ump.ma/fr/emploi-du-temps

Pour les plannings d'examens :
https://eniad.ump.ma/fr/calendrier-des-examens
"""
    },

    # ── Emplois du temps ──────────────────────────────────────────────────
    {
        "id": "emplois_du_temps",
        "category": "emploi_du_temps",
        "title": "Emplois du temps 2025-2026 — Liens de téléchargement",
        "content": """Emplois du temps Semestre Automne 2025-2026 :
- EPSI 1ère année (S1) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd014765fb7.pdf
- IA 1ère année ingénieur (S5) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd0162b6a04.pdf
- GINF 1ère année ingénieur (S5) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd0169cbf6e.pdf
- IRSI 1ère année ingénieur (S5) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd016bd63d1.pdf
- ROC 1ère année ingénieur (S5) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd0170506c7.pdf
- IA 2ème année ingénieur (S7) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01a89baf6.pdf
- GINF 2ème année ingénieur (S7) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01ae1e792.pdf
- IRSI 2ème année ingénieur (S7) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01b2df719.pdf
- ROC 2ème année ingénieur (S7) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01b8ae932.pdf
- IA 3ème année ingénieur (S9) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01f5cfc08.pdf
- GINF 3ème année ingénieur (S9) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01fadd5d3.pdf
- IRSI 3ème année ingénieur (S9) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd020426d4d.pdf
- ROC 3ème année ingénieur (S9) : https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd02074b4b2.pdf

Emplois du temps Semestre Printemps 2025-2026 :
- EPSI 1ère année (S2) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/69a80c5055536.pdf
- IA 1ère année ingénieur (S6) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb226c8d62.pdf
- GINF 1ère année ingénieur (S6) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb23951a56.pdf
- IRSI 1ère année ingénieur (S6) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb146658b1.pdf
- ROC 1ère année ingénieur (S6) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb125980f5.pdf
- IA 2ème année ingénieur (S8) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb25158efa.pdf
- GINF 2ème année ingénieur (S8) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4dd2cfaff.pdf
- IRSI 2ème année ingénieur (S8) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4dd75f464.pdf
- ROC 2ème année ingénieur (S8) : https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4ddd3b395.pdf
"""
    },

    # ── Examens ────────────────────────────────────────────────────────────
    {
        "id": "examens_info",
        "category": "examens",
        "title": "Informations sur les examens — ENIAD",
        "content": """Examens de fin de semestre 2025-2026 :
- Planning examens automne 2025-2026 (S5, S7, S9) : https://eniad.ump.ma/storage/files/1/Examen/695fcb78ddf25.pdf
  Dates : Janvier 2026

Types d'évaluation :
1. Contrôle continu (CC) : exercices, quizz, participation en cours
2. Examens de fin de semestre : épreuves écrites par matière
3. TP notés : travaux pratiques évalués
4. Rattrapages : session de rattrapage pour les matières échouées

Pour voir les plannings d'examens par semestre :
https://eniad.ump.ma/fr/calendrier-des-examens

Sections disponibles :
- Planning contrôles fin semestres S5 & S7 (automne)
- Planning rattrapages S5 & S7
- Planning contrôles fin semestres S6 & S8 (printemps)
- Planning rattrapages S6 & S8
- Planning examens TP cycle préparatoire
"""
    },

    # ── Stage et PFA ──────────────────────────────────────────────────────
    {
        "id": "stage_pfa",
        "category": "stage",
        "title": "Stages et PFA — Procédures et documents",
        "content": """Stage d'été (entre S6 et S7, entre S8 et S9) :
- Durée : 4 à 8 semaines minimum
- Convention de stage obligatoire à faire signer par l'entreprise et l'école
- Télécharger la convention : https://eniad.ump.ma/storage/files/1/Convention de stage/68234cd5a6293.pdf
- Rapport de stage à remettre à la fin

PFA (Projet de Fin d'Études) — 3ème année ingénieur :
- Commence en S9, soutenu en S10
- Sujet choisi en début de S8 (processus de sélection)
- En 2025 : sujets PFA disponibles sur https://eniad.ump.ma/fr/pfa
- Soutenance PFA 2025 : planning disponible sur https://eniad.ump.ma/fr/pfa/avis-aux-etudiants-en-s8-planning-des-soutenances-de-pfas-2025
- Jury composé de 2 encadrants + 1 rapporteur

Documents de stage :
https://eniad.ump.ma/fr/documents-de-stage
"""
    },

    # ── Résultats ────────────────────────────────────────────────────────
    {
        "id": "resultats",
        "category": "resultats",
        "title": "Consultation des résultats académiques",
        "content": """Les résultats des examens sont publiés sur le site de l'ENIAD.
Consulter : https://eniad.ump.ma/fr/resultats
Les résultats sont publiés après délibération du jury (généralement 2-3 semaines après les examens).
En cas de contestation, contacter l'administration ou le chef de filière.
Les relevés de notes officiels sont disponibles auprès de la scolarité.
"""
    },

    # ── Vie étudiante ─────────────────────────────────────────────────────
    {
        "id": "vie_etudiante",
        "category": "vie_etudiante",
        "title": "Vie Étudiante — Services et activités",
        "content": """Services étudiants disponibles à l'ENIAD :

1. BOURSES :
Bourses d'études disponibles pour les étudiants éligibles.
Conditions : résultats académiques, situation sociale.
Plus d'infos : https://eniad.ump.ma/fr/bourses

2. CENTRE DE SANTÉ UNIVERSITAIRE :
Service médical disponible pour les étudiants.
https://eniad.ump.ma/fr/centre-de-sante-universitaire

3. ASSURANCE MALADIE OBLIGATOIRE (AMO) :
Couverture santé obligatoire pour tous les étudiants.
Plus d'infos : https://eniad.ump.ma/fr/assurance-maladie-obligatoire

4. CLUBS ET ASSOCIATIONS :
Plusieurs clubs étudiants actifs :
- Club IA & Data Science
- Club Entrepreneuriat
- Club Robotique
- Club Sport & Bien-être
https://eniad.ump.ma/fr/clubs-associations

5. ACTIVITÉS SPORTIVES :
Infrastructure sportive disponible.
https://eniad.ump.ma/fr/activites-sportives

6. ACTIVITÉS CULTURELLES :
Événements culturels, conférences, forums.
https://eniad.ump.ma/fr/activites-culturelles

7. CIOVE (Centre d'Information, d'Orientation et de Vie Estudiantine) :
Orientation professionnelle, aide à la recherche de stage.
https://eniad.ump.ma/fr/centre-dinformation-dorientation-et-de-la-vie-estudiantine-ciove
"""
    },

    # ── Admission ────────────────────────────────────────────────────────
    {
        "id": "admission",
        "category": "admission",
        "title": "Admission et inscription à l'ENIAD",
        "content": """Conditions d'admission :

Cycle Préparatoire (EPSI) :
- Baccalauréat scientifique ou technique avec mention
- Concours national des classes préparatoires
- Sélection sur dossier + entretien

Cycle Ingénieur (IA, IRSI, ROC, GINF) :
- Sortants des classes préparatoires (CPGE ou EPSI)
- Via concours national d'accès aux écoles d'ingénieurs
- Accès possible en 2ème année pour titulaires de DUT/BTS

Pour plus d'informations sur l'admission :
https://eniad.ump.ma/fr/admission

L'ENIAD fait partie du réseau des grandes écoles d'ingénieurs du Maroc.
"""
    },

    # ── Gouvernance ───────────────────────────────────────────────────────
    {
        "id": "gouvernance",
        "category": "gouvernance",
        "title": "Gouvernance et administration de l'ENIAD",
        "content": """Structure de gouvernance de l'ENIAD :
- Direction générale
- Conseil de gestion
- Conseil d'université
- Responsables pédagogiques par filière

Textes de lois et réglements :
https://eniad.ump.ma/fr/textes-lois

Règlement intérieur :
https://eniad.ump.ma/fr/reglement-interieur-de-lecole

Contact administration :
Email : eniad@ump.ac.ma
Messagerie universitaire : https://messagerie.ump.ma
"""
    },

    # ── Recherche ─────────────────────────────────────────────────────────
    {
        "id": "recherche",
        "category": "recherche",
        "title": "Recherche et études doctorales — ENIAD",
        "content": """Pôle des études doctorales :
L'ENIAD propose des formations doctorales dans 3 domaines :
1. Sciences, Technologies, Ingénierie et Santé (STIS)
2. Droit, Sciences Économiques et Gestion (DSEG)
3. Sciences Humaines, Sociales et de l'Éducation (SHSE)

Centres de recherche :
- CUEM : Centre Universitaire d'Études des Migrations
- COSTE : Centre de l'Oriental des Sciences et Technologies de l'Eau
- Musée Universitaire d'Archéologie et du Patrimoine
- CULCOM : Centre Universitaire des Langues et de la Communication

Programme P2E (Partenariat Pour l'Emploi) :
Favorise les partenariats entre l'école et les entreprises.

Laboratoire universitaire :
https://laboratoire.ump.ma
"""
    },

    # ── FAQ Étudiants ─────────────────────────────────────────────────────
    {
        "id": "faq_general",
        "category": "faq",
        "title": "Questions fréquentes des étudiants",
        "content": """Questions fréquentes :

Q: Comment trouver mon emploi du temps ?
R: Rendez-vous sur https://eniad.ump.ma/fr/emploi-du-temps et téléchargez le PDF de votre filière et semestre.

Q: Quand ont lieu les examens ?
R: Consulter https://eniad.ump.ma/fr/calendrier-des-examens pour les dates précises par semestre.

Q: Comment obtenir une convention de stage ?
R: Télécharger sur https://eniad.ump.ma/storage/files/1/Convention de stage/68234cd5a6293.pdf, la faire signer par l'entreprise et la scolarité.

Q: Comment accéder à la plateforme e-learning ?
R: Via http://eniadelearning.ump.ma avec vos identifiants universitaires.

Q: Où consulter mes résultats ?
R: Sur https://eniad.ump.ma/fr/resultats après délibération du jury.

Q: Comment postuler à une bourse ?
R: Consulter https://eniad.ump.ma/fr/bourses pour les conditions et dossier requis.

Q: Quel est le contact de la scolarité ?
R: Email : eniad@ump.ac.ma | Téléphone : +212 536

Q: Quel est le lien pour la bibliothèque ?
R: http://bib.ump.ma pour accès au catalogue et ressources électroniques.

Q: Comment choisir un sujet de PFA ?
R: La procédure est annoncée sur https://eniad.ump.ma/fr/pfa en début de 3ème année.

Q: Quelles sont les filières disponibles ?
R: IA (Intelligence Artificielle), IRSI (Réseaux & Sécurité), ROC (Robotique & IoT), GINF (Génie Informatique), EPSI (Préparatoire).
"""
    },

    # ── Coopération ───────────────────────────────────────────────────────
    {
        "id": "cooperation",
        "category": "cooperation",
        "title": "Coopération nationale et internationale",
        "content": """L'ENIAD développe des partenariats actifs :

Coopération nationale :
- Partenariats avec des entreprises marocaines pour les stages et l'emploi
- Conventions avec d'autres universités marocaines
https://eniad.ump.ma/fr/cooperation-nationale

Coopération internationale :
- Échanges avec des universités européennes et américaines
- Programmes de mobilité étudiante
- Doubles diplômes
https://eniad.ump.ma/fr/cooperation-internationale

Programme P2E : partenariat pour l'emploi facilitant l'insertion professionnelle.
"""
    },
]

# ── URLs PDFs à télécharger ─────────────────────────────────────────────────

PDF_RESOURCES = [
    # Emplois du temps — Automne 2025-2026
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd014765fb7.pdf",
        "filename": "edt_epsi1_s1_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "EPSI", "semester": "S1",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps EPSI 1ère année S1 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd0162b6a04.pdf",
        "filename": "edt_ia1_s5_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "IA", "semester": "S5",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps IA 1ère année ingénieur S5 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd0169cbf6e.pdf",
        "filename": "edt_ginf1_s5_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "GINF", "semester": "S5",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps GINF 1ère année ingénieur S5 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd016bd63d1.pdf",
        "filename": "edt_irsi1_s5_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "IRSI", "semester": "S5",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps IRSI 1ère année ingénieur S5 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd0170506c7.pdf",
        "filename": "edt_roc1_s5_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "ROC", "semester": "S5",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps ROC 1ère année ingénieur S5 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01a89baf6.pdf",
        "filename": "edt_ia2_s7_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "IA", "semester": "S7",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps IA 2ème année ingénieur S7 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01ae1e792.pdf",
        "filename": "edt_ginf2_s7_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "GINF", "semester": "S7",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps GINF 2ème année ingénieur S7 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01b2df719.pdf",
        "filename": "edt_irsi2_s7_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "IRSI", "semester": "S7",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps IRSI 2ème année ingénieur S7 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01b8ae932.pdf",
        "filename": "edt_roc2_s7_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "ROC", "semester": "S7",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps ROC 2ème année ingénieur S7 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01f5cfc08.pdf",
        "filename": "edt_ia3_s9_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "IA", "semester": "S9",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps IA 3ème année ingénieur S9 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd01fadd5d3.pdf",
        "filename": "edt_ginf3_s9_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "GINF", "semester": "S9",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps GINF 3ème année ingénieur S9 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd020426d4d.pdf",
        "filename": "edt_irsi3_s9_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "IRSI", "semester": "S9",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps IRSI 3ème année ingénieur S9 Automne 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/AA ET 25-26/68fd02074b4b2.pdf",
        "filename": "edt_roc3_s9_automne_2526.pdf",
        "type": "emploi_du_temps", "program": "ROC", "semester": "S9",
        "year": "2025-2026", "season": "automne",
        "description": "Emploi du temps ROC 3ème année ingénieur S9 Automne 2025-2026"
    },
    # Groupes TD/TP — Automne
    {
        "url": "https://eniad.ump.ma/storage/files/1/ET 2025-2026/68e001e5066ac.pdf",
        "filename": "groupes_epsi_s1_automne_2526_A.pdf",
        "type": "groupes_td_tp", "program": "EPSI", "semester": "S1",
        "year": "2025-2026", "season": "automne",
        "description": "Répartition groupes TD/TP EPSI S1 Automne 2025-2026 groupe A"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/ET 2025-2026/68e001f33bc89.pdf",
        "filename": "groupes_epsi_s1_automne_2526_B.pdf",
        "type": "groupes_td_tp", "program": "EPSI", "semester": "S1",
        "year": "2025-2026", "season": "automne",
        "description": "Répartition groupes TD/TP EPSI S1 Automne 2025-2026 groupe B"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/ET 2025-2026/68e00204d5183.pdf",
        "filename": "groupes_epsi_s1_automne_2526_C.pdf",
        "type": "groupes_td_tp", "program": "EPSI", "semester": "S1",
        "year": "2025-2026", "season": "automne",
        "description": "Répartition groupes TD/TP EPSI S1 Automne 2025-2026 groupe C"
    },
    # Emplois du temps — Printemps 2025-2026
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/69a80c5055536.pdf",
        "filename": "edt_epsi1_s2_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "EPSI", "semester": "S2",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps EPSI 1ère année S2 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb226c8d62.pdf",
        "filename": "edt_ia1_s6_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "IA", "semester": "S6",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps IA 1ère année ingénieur S6 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb23951a56.pdf",
        "filename": "edt_ginf1_s6_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "GINF", "semester": "S6",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps GINF 1ère année ingénieur S6 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb146658b1.pdf",
        "filename": "edt_irsi1_s6_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "IRSI", "semester": "S6",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps IRSI 1ère année ingénieur S6 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb125980f5.pdf",
        "filename": "edt_roc1_s6_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "ROC", "semester": "S6",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps ROC 1ère année ingénieur S6 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/V2/69aeb25158efa.pdf",
        "filename": "edt_ia2_s8_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "IA", "semester": "S8",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps IA 2ème année ingénieur S8 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4dd2cfaff.pdf",
        "filename": "edt_ginf2_s8_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "GINF", "semester": "S8",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps GINF 2ème année ingénieur S8 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4dd75f464.pdf",
        "filename": "edt_irsi2_s8_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "IRSI", "semester": "S8",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps IRSI 2ème année ingénieur S8 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4ddd3b395.pdf",
        "filename": "edt_roc2_s8_printemps_2526.pdf",
        "type": "emploi_du_temps", "program": "ROC", "semester": "S8",
        "year": "2025-2026", "season": "printemps",
        "description": "Emploi du temps ROC 2ème année ingénieur S8 Printemps 2025-2026"
    },
    # Groupes TD/TP — Printemps
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4e2c25223.pdf",
        "filename": "groupes_epsi_s2_printemps_2526.pdf",
        "type": "groupes_td_tp", "program": "EPSI", "semester": "S2",
        "year": "2025-2026", "season": "printemps",
        "description": "Répartition groupes TD/TP EPSI S2 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4e4a4c82e.pdf",
        "filename": "groupes_ia1_s6_printemps_2526.pdf",
        "type": "groupes_td_tp", "program": "IA", "semester": "S6",
        "year": "2025-2026", "season": "printemps",
        "description": "Répartition groupes TD/TP IA S6 Printemps 2025-2026"
    },
    {
        "url": "https://eniad.ump.ma/storage/files/1/A S PRINTEMPS/699f4e76462a2.pdf",
        "filename": "groupes_ginf1_s6_printemps_2526.pdf",
        "type": "groupes_td_tp", "program": "GINF", "semester": "S6",
        "year": "2025-2026", "season": "printemps",
        "description": "Répartition groupes TD/TP GINF S6 Printemps 2025-2026"
    },
    # Planning d'examens
    {
        "url": "https://eniad.ump.ma/storage/files/1/Examen/695fcb78ddf25.pdf",
        "filename": "planning_examens_s5_s7_automne_2526.pdf",
        "type": "planning_examen", "semester": "S5-S7",
        "year": "2025-2026", "season": "automne",
        "description": "Planning examens fin semestres S5 & S7 Automne 2025-2026 (Janvier 2026)"
    },
    # Convention de stage
    {
        "url": "https://eniad.ump.ma/storage/files/1/Convention de stage/68234cd5a6293.pdf",
        "filename": "convention_de_stage_eniad.pdf",
        "type": "document_administratif",
        "description": "Convention de stage officielle ENIAD"
    },
]
