"""
Planning officiel des examens — ENIAD Berkane
Session Hiver   (Janvier 2026)   : S1 (Prépa), S5, S7, S9  — source: planingdeprmiersemsters.pdf
Session Printemps 2025/2026      : S2 (EPSI),  S6, S8       — source: planing des examans.pdf
"""

SESSION_HIVER     = "Session de Janvier 2025/2026"
SESSION_PRINTEMPS = "Session de Printemps 2025/2026"
SESSION = SESSION_PRINTEMPS  # alias backward-compat

# Année d'étude → semestres correspondants
YEAR_TO_SEMESTERS: dict[int, list[str]] = {
    1: ["S1", "S2"],
    2: ["S3", "S4"],
    3: ["S5", "S6"],
    4: ["S7", "S8"],
    5: ["S9", "S10"],
}

# Clés filière → (nom complet, semestre, session)
FILIERES_INFO: dict[str, tuple] = {
    # ── Session Hiver (Janvier 2026) ──────────────────────────────────────────
    "PREPA_S1": ("Cycle Préparatoire (1ère année)",                        "S1", SESSION_HIVER),
    "GINF_S5":  ("Génie Informatique",                                      "S5", SESSION_HIVER),
    "IA_S5":    ("Intelligence Artificielle",                               "S5", SESSION_HIVER),
    "ROC_S5":   ("Robotique et Objets Connectés",                           "S5", SESSION_HIVER),
    "IRSI_S5":  ("Ingénierie Réseaux et Sécurité Informatique",             "S5", SESSION_HIVER),
    "IA_S7":    ("Intelligence Artificielle",                               "S7", SESSION_HIVER),
    "GINF_S7":  ("Génie Informatique",                                      "S7", SESSION_HIVER),
    "ROC_S7":   ("Robotique et Objets Connectés",                           "S7", SESSION_HIVER),
    "IRSI_S7":  ("Ingénierie Réseaux et Sécurité Informatique",             "S7", SESSION_HIVER),
    "IA_S9":    ("Intelligence Artificielle",                               "S9", SESSION_HIVER),
    "GINF_S9":  ("Génie Informatique",                                      "S9", SESSION_HIVER),
    "ROC_S9":   ("Robotique et Objets Connectés",                           "S9", SESSION_HIVER),
    "IRSI_S9":  ("Ingénierie Réseaux et Sécurité Informatique",             "S9", SESSION_HIVER),
    # ── Session Printemps 2025/2026 ───────────────────────────────────────────
    "EPSI":     ("Études Préparatoires en Sciences de l'Ingénieur",         "S2", SESSION_PRINTEMPS),
    "GINF_S6":  ("Génie Informatique",                                      "S6", SESSION_PRINTEMPS),
    "GINF_S8":  ("Génie Informatique",                                      "S8", SESSION_PRINTEMPS),
    "IA_S6":    ("Intelligence Artificielle",                               "S6", SESSION_PRINTEMPS),
    "IA_S8":    ("Intelligence Artificielle",                               "S8", SESSION_PRINTEMPS),
    "ROC_S6":   ("Robotique et Objets Connectés",                           "S6", SESSION_PRINTEMPS),
    "ROC_S8":   ("Robotique et Objets Connectés",                           "S8", SESSION_PRINTEMPS),
    "IRSI_S6":  ("Ingénierie Réseaux et Sécurité Informatique",             "S6", SESSION_PRINTEMPS),
    "IRSI_S8":  ("Ingénierie Réseaux et Sécurité Informatique",             "S8", SESSION_PRINTEMPS),
}

PLANNING: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════════════
    # SESSION HIVER — Janvier 2026
    # Source : planingdeprmiersemsters.pdf
    # ══════════════════════════════════════════════════════════════════════════

    # ── PREPA — Semestre 1 ────────────────────────────────────────────────────
    # Groupe A → AMPHI 1 / Groupe B → AMPHI 2 / Groupe C → AMPHI 3
    "PREPA_S1": {
        "Lundi 12/01": {
            "08H30-10H00": {"module": "Analyse 1",                                    "coordonnateur": "PR. MOSTAFA ALLAOUI",   "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
            "10H30-12H00": {"module": "Algorithmique et Architecture des Ordinateurs", "coordonnateur": "PR. MOHAMED BADIY",     "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
        },
        "Mardi 13/01": {
            "08H30-10H00": {"module": "Électrocinétique",                              "coordonnateur": "PR. MOHAMMED SEDDIK",   "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
            "10H30-12H00": {"module": "Algèbre 1",                                    "coordonnateur": "PR. TARIK LAMOUDAN",    "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
        },
        "Jeudi 15/01": {
            "13H30-15H30": {"module": "Mécanique du Point",                            "coordonnateur": "PR. YOUSSEF EL AOUNI",  "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
            "16H00-17H30": {"module": "Anglais",                                      "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
        },
        "Vendredi 16/01": {
            "14H30-16H00": {"module": "Méthodologie de Travail Universitaire",         "coordonnateur": "PR. HICHAME ELKHALI",   "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
            "16H30-18H00": {"module": "Français",                                     "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 1 (Gr A) / AMPHI 2 (Gr B) / AMPHI 3 (Gr C)"},
        },
    },

    # ── GINF — Semestre 5 ─────────────────────────────────────────────────────
    "GINF_S5": {
        "Lundi 12/01": {
            "08H30-10H00": {"module": "Programmation Orientée Objet en Java",           "coordonnateur": "PR. YOUSSEF MELLAH",    "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Statistiques Descriptives, Inférentielles et Exploratoires", "coordonnateur": "PR. MOSTAPHA HADDAOUI", "salle": "AMPHI 4"},
        },
        "Mardi 13/01": {
            "08H30-10H00": {"module": "Système d'Exploitation et Programmation Systèmes", "coordonnateur": "PR. MANALE BOUGHANJA", "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Développement d'Applications Web",                 "coordonnateur": "PR. ZAKARIA KADDARI",   "salle": "AMPHI 4"},
        },
        "Jeudi 15/01": {
            "14H00-15H30": {"module": "Programmation Orientée Objet en Python",          "coordonnateur": "PR. MOHAMED BOUDCHICHE","salle": "AMPHI 4"},
            "16H00-17H30": {"module": "Ingénierie des Bases de Données Avancée",         "coordonnateur": "PR. HOUDA BENHAR",      "salle": "AMPHI 4"},
        },
        "Vendredi 16/01": {
            "14H30-16H00": {"module": "Français 1",                                     "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 4"},
            "16H30-18H00": {"module": "Anglais 1",                                      "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 4"},
        },
        "Samedi 17/01": {
            "10H30-12H00": {"module": "Comptabilité et Calcul des Coûts",               "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 4"},
        },
    },

    # ── IA — Semestre 5 ───────────────────────────────────────────────────────
    "IA_S5": {
        "Lundi 12/01": {
            "08H30-10H00": {"module": "Programmation Orientée Objet en Java",           "coordonnateur": "PR. YOUSSEF MELLAH",    "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Statistiques Descriptives, Inférentielles et Exploratoires", "coordonnateur": "PR. MOSTAPHA HADDAOUI", "salle": "AMPHI 5"},
        },
        "Mardi 13/01": {
            "08H30-10H00": {"module": "Système d'Exploitation et Programmation Systèmes", "coordonnateur": "PR. MANALE BOUGHANJA", "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Développement d'Applications Web",                 "coordonnateur": "PR. ZAKARIA KADDARI",   "salle": "AMPHI 5"},
        },
        "Jeudi 15/01": {
            "14H00-15H30": {"module": "Programmation Orientée Objet en Python",          "coordonnateur": "PR. YOUSSEF MELLAH",    "salle": "AMPHI 5"},
            "16H00-17H30": {"module": "Ingénierie des Bases de Données Avancée",         "coordonnateur": "PR. HOUDA BENHAR",      "salle": "AMPHI 5"},
        },
        "Vendredi 16/01": {
            "14H30-16H00": {"module": "Français 1",                                     "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 5"},
            "16H30-18H00": {"module": "Anglais 1",                                      "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 5"},
        },
        "Samedi 17/01": {
            "10H30-12H00": {"module": "Comptabilité et Calcul des Coûts",               "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 5"},
        },
    },

    # ── IRSI — Semestre 5 ─────────────────────────────────────────────────────
    "IRSI_S5": {
        "Lundi 12/01": {
            "08H30-10H00": {"module": "Programmation Orientée Objet en Java",           "coordonnateur": "PR. YOUSSEF MELLAH",    "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Statistiques Descriptives, Inférentielles et Exploratoires", "coordonnateur": "PR. MOSTAPHA HADDAOUI", "salle": "AMPHI 5"},
        },
        "Mardi 13/01": {
            "08H30-10H00": {"module": "Système d'Exploitation et Programmation Systèmes", "coordonnateur": "PR. MANALE BOUGHANJA", "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Développement d'Applications Web",                 "coordonnateur": "PR. ZAKARIA KADDARI",   "salle": "AMPHI 5"},
        },
        "Jeudi 15/01": {
            "14H00-15H30": {"module": "Programmation Orientée Objet en Python",          "coordonnateur": "PR. MOHAMED BOUDCHICHE","salle": "AMPHI 5"},
            "16H00-17H30": {"module": "Réseaux Informatiques",                           "coordonnateur": "PR. AMINA KHARBACH",    "salle": "AMPHI 5"},
        },
        "Vendredi 16/01": {
            "14H30-16H00": {"module": "Français 1",                                     "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 5"},
            "16H30-18H00": {"module": "Anglais 1",                                      "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 5"},
        },
        "Samedi 17/01": {
            "10H30-12H00": {"module": "Comptabilité et Calcul des Coûts",               "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 5"},
        },
    },

    # ── ROC — Semestre 5 ──────────────────────────────────────────────────────
    "ROC_S5": {
        "Lundi 12/01": {
            "08H30-10H00": {"module": "Programmation Orientée Objet en Java",           "coordonnateur": "PR. YOUSSEF MELLAH",    "salle": "AMPHI 6"},
            "10H30-12H00": {"module": "Statistiques Descriptives, Inférentielles et Exploratoires", "coordonnateur": "PR. MOSTAPHA HADDAOUI", "salle": "AMPHI 6"},
        },
        "Mardi 13/01": {
            "08H30-10H00": {"module": "Système d'Exploitation et Programmation Systèmes", "coordonnateur": "PR. MANALE BOUGHANJA", "salle": "AMPHI 6"},
            "10H30-12H00": {"module": "Développement d'Applications Web",                 "coordonnateur": "PR. ZAKARIA KADDARI",   "salle": "AMPHI 6"},
        },
        "Jeudi 15/01": {
            "14H00-15H30": {"module": "Programmation Embarquée",                         "coordonnateur": "PR. WASSIM KHIATI",     "salle": "AMPHI 6"},
        },
        "Vendredi 16/01": {
            "14H30-16H00": {"module": "Français 1",                                     "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 6"},
            "16H30-18H00": {"module": "Anglais 1",                                      "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 6"},
        },
        "Samedi 17/01": {
            "08H30-10H00": {"module": "Perception et Capteurs pour Objets et Robots Connectés", "coordonnateur": "PR. MOHAMED BOUTOUBA", "salle": "AMPHI 3"},
            "10H30-12H00": {"module": "Comptabilité et Calcul des Coûts",               "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 6"},
        },
    },

    # ── IA — Semestre 7 ───────────────────────────────────────────────────────
    "IA_S7": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Développement Mobile Multiplatforme",            "coordonnateur": "PR. MOHAMED BOUDCHICHE","salle": "AMPHI 1"},
            "16H00-17H30": {"module": "Machine Learning",                               "coordonnateur": "PR. MOHAMED KHALIFA BOUTAHIR", "salle": "AMPHI 1"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Gestion Agile de Projet Informatique",           "coordonnateur": "PR. MOHAMED BADIY",     "salle": "AMPHI 1"},
            "16H00-17H30": {"module": "Optimisation Combinatoire et Métaheuristiques",  "coordonnateur": "PR. TARIK LAMOUDAN",    "salle": "AMPHI 1"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Vision Artificielle",                            "coordonnateur": "PR. ALI EL HABCHI",     "salle": "AMPHI 1"},
            "10H30-12H00": {"module": "Analyse de Données",                             "coordonnateur": "PR. BOUCHRA LABLOUL",   "salle": "AMPHI 1"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Français 2",                                    "coordonnateur": "PR. HICHAM ELRHALI",    "salle": "AMPHI 1"},
            "10H30-12H00": {"module": "Anglais 2",                                     "coordonnateur": "DR. OUALAE HAMZAOUI",   "salle": "AMPHI 1"},
        },
        "Samedi 17/01": {
            "10H30-12H00": {"module": "Management et Marketing",                        "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 1"},
        },
    },

    # ── GINF — Semestre 7 ─────────────────────────────────────────────────────
    "GINF_S7": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Développement Mobile Multiplatforme",            "coordonnateur": "PR. MOHAMED BOUDCHICHE","salle": "AMPHI 2"},
            "16H00-17H30": {"module": "Machine Learning",                               "coordonnateur": "PR. MOHAMED KHALIFA BOUTAHIR", "salle": "AMPHI 2"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Gestion Agile de Projet Informatique",           "coordonnateur": "PR. MOHAMED BADIY",     "salle": "AMPHI 2"},
            "16H00-17H30": {"module": "Ingénierie JEE et Applications Distribuées",     "coordonnateur": "PR. NABIL ALAMI",       "salle": "AMPHI 2"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Développement d'Application .NET",               "coordonnateur": "PR. ZAKARIA KADDARI",   "salle": "AMPHI 2"},
            "10H30-12H00": {"module": "Analyse de Données",                             "coordonnateur": "PR. BOUCHRA LABLOUL",   "salle": "AMPHI 2"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Français 2",                                    "coordonnateur": "PR. HICHAM ELRHALI",    "salle": "AMPHI 2"},
            "10H30-12H00": {"module": "Anglais 2",                                     "coordonnateur": "DR. OUALAE HAMZAOUI",   "salle": "AMPHI 2"},
        },
        "Samedi 17/01": {
            "10H30-12H00": {"module": "Management et Marketing",                        "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 2"},
        },
    },

    # ── ROC — Semestre 7 ──────────────────────────────────────────────────────
    "ROC_S7": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Développement Mobile Multiplatforme",            "coordonnateur": "PR. MOHAMED BOUDCHICHE","salle": "AMPHI 1"},
            "16H00-17H30": {"module": "Machine Learning",                               "coordonnateur": "PR. MOHAMED KHALIFA BOUTAHIR", "salle": "AMPHI 1"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Gestion Agile de Projet Informatique",           "coordonnateur": "PR. MOHAMED BADIY",     "salle": "AMPHI 3"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Vision Artificielle",                            "coordonnateur": "PR. ALI EL HABCHI",     "salle": "AMPHI 1"},
            "10H30-12H00": {"module": "Programmation en Robotique et Conception 3D",    "coordonnateur": "PR. MOHAMED BOUTOUBA",  "salle": "SALLE TP"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Français 2",                                    "coordonnateur": "PR. HICHAM ELRHALI",    "salle": "AMPHI 3"},
            "10H30-12H00": {"module": "Anglais 2",                                     "coordonnateur": "DR. OUALAE HAMZAOUI",   "salle": "AMPHI 3"},
        },
        "Samedi 17/01": {
            "08H30-10H00": {"module": "Perception et Capteurs pour Objets et Robots Connectés", "coordonnateur": "PR. MOHAMED BOUTOUBA", "salle": "AMPHI 3"},
            "10H30-12H00": {"module": "Management et Marketing",                        "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 3"},
        },
    },

    # ── IRSI — Semestre 7 ─────────────────────────────────────────────────────
    "IRSI_S7": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Administration Systèmes Linux",                  "coordonnateur": "PR. MANALE BOUGHANJA",  "salle": "AMPHI 3"},
            "16H00-17H30": {"module": "Machine Learning",                               "coordonnateur": "PR. MOHAMED KHALIFA BOUTAHIR", "salle": "AMPHI 3"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Gestion Agile de Projet Informatique",           "coordonnateur": "PR. MOHAMED BADIY",     "salle": "AMPHI 3"},
            "16H00-17H30": {"module": "Interconnexion des Réseaux",                     "coordonnateur": "PR. ZINEB BAKRAOUY",    "salle": "AMPHI 3"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Cryptographie : Protocoles et Applications",     "coordonnateur": "PR. MOHAMED FARTITCHOU","salle": "AMPHI 3"},
            "10H30-12H00": {"module": "Programmation Shell & PowerShell",               "coordonnateur": "DR. NOUSSAIBA TAZI",    "salle": "AMPHI 3"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Français 2",                                    "coordonnateur": "PR. HICHAM ELRHALI",    "salle": "AMPHI 3"},
            "10H30-12H00": {"module": "Anglais 2",                                     "coordonnateur": "DR. OUALAE HAMZAOUI",   "salle": "AMPHI 3"},
        },
        "Samedi 17/01": {
            "10H30-12H00": {"module": "Management et Marketing",                        "coordonnateur": "DR. NEJJARI",           "salle": "AMPHI 3"},
        },
    },

    # ── IA — Semestre 9 ───────────────────────────────────────────────────────
    "IA_S9": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Modèles de Langage et Traitement Automatique du Texte", "coordonnateur": "PR. ZAKARIA KADDARI", "salle": "AMPHI 4"},
            "16H00-17H30": {"module": "Ingénierie Big Data",                            "coordonnateur": "PR. NABIL ALAMI",       "salle": "AMPHI 4"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "DevOps & MLOps",                                 "coordonnateur": "PR. ALI EL HABCHI",     "salle": "AMPHI 4"},
            "16H00-17H30": {"module": "Cloud Computing et Virtualisation",              "coordonnateur": "PR. MOHAMED FARTITCHOU","salle": "AMPHI 4"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Anglais 3",                                     "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Français 3",                                    "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 4"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Éthiques et Droits",                            "coordonnateur": "DR. KHALID KILOULI",    "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Explainable AI",                                "coordonnateur": "PR. SAJIDA MHAMMEDI",   "salle": "AMPHI 4"},
        },
        "Samedi 17/01": {
            "08H30-10H00": {"module": "Ateliers IA Avancée",                           "coordonnateur": "PR. SAJIDA MHAMMEDI",   "salle": "AMPHI 4"},
        },
    },

    # ── GINF — Semestre 9 ─────────────────────────────────────────────────────
    "GINF_S9": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Interconnexion Réseaux et Sécurité Réseaux",    "coordonnateur": "PR. ZINEB BAKRAOUY",    "salle": "AMPHI 5"},
            "16H00-17H30": {"module": "Ingénierie Big Data",                            "coordonnateur": "PR. NABIL ALAMI",       "salle": "AMPHI 5"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Architecture Logicielle et Design Patterns",    "coordonnateur": "PR. WASSIM KHIATI",     "salle": "AMPHI 5"},
            "16H00-17H30": {"module": "Cloud Computing et Virtualisation",              "coordonnateur": "PR. MOHAMED FARTITCHOU","salle": "AMPHI 5"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Anglais 3",                                     "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Français 3",                                    "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 5"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Éthiques et Droits",                            "coordonnateur": "DR. KHALID KILOULI",    "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Atelier Pentesting Web",                        "coordonnateur": "PR. AMINA KHARBACH",    "salle": "AMPHI 5"},
        },
        "Samedi 17/01": {
            "08H30-10H00": {"module": "Urbanisation des Systèmes d'Information",       "coordonnateur": "PR. ALI EL HABCHI",     "salle": "AMPHI 5"},
        },
    },

    # ── ROC — Semestre 9 ──────────────────────────────────────────────────────
    "ROC_S9": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "IA Embarquée & Edge AI",                        "coordonnateur": "PR. WASSIM KHIATI",     "salle": "AMPHI 5"},
            "16H00-17H30": {"module": "Ingénierie Big Data",                            "coordonnateur": "PR. NABIL ALAMI",       "salle": "AMPHI 5"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Atelier Robotique Avancée (Cobotique, Mobilité)","coordonnateur": "PR. MOHAMMED SAJAI",   "salle": "AMPHI 4"},
            "16H00-17H30": {"module": "Cloud Computing et Virtualisation",              "coordonnateur": "PR. MOHAMED FARTITCHOU","salle": "AMPHI 4"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Anglais 3",                                     "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 5"},
            "10H30-12H00": {"module": "Français 3",                                    "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 5"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Éthiques et Droits",                            "coordonnateur": "DR. KHALID KILOULI",    "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Robot Operating System",                        "coordonnateur": "PR. MOHAMMED SAJAI",    "salle": "AMPHI 4"},
        },
        "Samedi 17/01": {
            "08H30-10H00": {"module": "Réalité Virtuelle et Réalité Augmentée",        "coordonnateur": "PR. MOHAMMED SAJAI",    "salle": "AMPHI 5"},
        },
    },

    # ── IRSI — Semestre 9 ─────────────────────────────────────────────────────
    "IRSI_S9": {
        "Lundi 12/01": {
            "14H00-15H30": {"module": "Atelier Ethical Hacking",                       "coordonnateur": "PR. AMINA KHARBACH",    "salle": "AMPHI 4"},
            "16H00-17H30": {"module": "Gouvernance de la Sécurité et Analyse des Risques", "coordonnateur": "PR. ISMAIL CHAHID", "salle": "AMPHI 4"},
        },
        "Mardi 13/01": {
            "14H00-15H30": {"module": "Technologie Blockchain",                        "coordonnateur": "PR. MOHAMED FARTITCHOU","salle": "AMPHI 5"},
            "16H00-17H30": {"module": "Cybersécurité",                                 "coordonnateur": "PR. ZINEB BAKRAOUY",    "salle": "AMPHI 5"},
        },
        "Jeudi 15/01": {
            "08H30-10H00": {"module": "Anglais 3",                                     "coordonnateur": "PR. ABDERRAHIM FATMI",  "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Français 3",                                    "coordonnateur": "PR. HAYAT BENTALEB",    "salle": "AMPHI 4"},
            "16H00-17H30": {"module": "Atelier Firewall",                              "coordonnateur": "PR. AMINA KHARBACH",    "salle": "AMPHI 6"},
        },
        "Vendredi 16/01": {
            "08H30-10H00": {"module": "Éthiques et Droits",                            "coordonnateur": "DR. KHALID KILOULI",    "salle": "AMPHI 4"},
            "10H30-12H00": {"module": "Atelier Pentesting Web",                        "coordonnateur": "PR. AMINA KHARBACH",    "salle": "AMPHI 5"},
        },
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SESSION PRINTEMPS 2025/2026
    # Source : planing des examans.pdf  (données originales inchangées)
    # ══════════════════════════════════════════════════════════════════════════

    # ── EPSI — Semestre 2 ─────────────────────────────────────────────────────
    "EPSI": {
        "Lundi": {
            "09h00-10h30": {"module": "Algèbre 2",               "coordonnateur": "PR. HARCHA HANANE",    "salle": "AMPHI 1, 2, 3"},
            "11h00-12h30": {"module": "Électronique Analogique", "coordonnateur": "PR. BOUTOUBA MOHAMED", "salle": "AMPHI 1, 2, 3"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Analyse 2",               "coordonnateur": "PR. ALLAOUI MOSTAFA",  "salle": "AMPHI 1, 2, 3"},
            "11h00-12h30": {"module": "Programmation en C",      "coordonnateur": "PR. AISSI MOHAMMED",   "salle": "AMPHI 1, 2, 3"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Électromagnétisme",       "coordonnateur": "PR. SEDDIK MOHAMMED",  "salle": "AMPHI 1, 2, 3"},
            "11h00-12h30": {"module": "Culture Digitale",        "coordonnateur": "PR. ADDOU EL HOUCINE", "salle": "AMPHI 1, 2, 3"},
        },
        "Jeudi": {
            "14h00-15h30": {"module": "Anglais 2",               "coordonnateur": "PR. FATMI ABDERRAHIM", "salle": "AMPHI 1, 2, 3"},
            "16h00-17h30": {"module": "Français 2",              "coordonnateur": "PR. BENTALEB HAYAT",   "salle": "AMPHI 1, 2, 3"},
        },
    },

    # ── GINF — Semestre 6 ─────────────────────────────────────────────────────
    "GINF_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                               "coordonnateur": "PR. LABLOUL BOUCHRA",    "salle": "AMPHI 4"},
            "16h00-17h30": {"module": "Développement d'Applications Web Avancé",           "coordonnateur": "PR. KADDARI ZAKARIA",    "salle": "AMPHI 4"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire", "coordonnateur": "PR. LAMOUDAN TARIK", "salle": "AMPHI 4"},
            "16h00-17h30": {"module": "Programmation Orientée Objet en C++",               "coordonnateur": "PR. BOUDCHICHE MOHAMED","salle": "AMPHI 4"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Réseaux Informatiques et Protocoles",               "coordonnateur": "PR. KHARBACH AMINA",    "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Modélisation Logicielle et Données Structurées",    "coordonnateur": "PR. EL HABCHI ALI",     "salle": "AMPHI 4"},
        },
        "Jeudi": {
            "11h00-12h30": {"module": "Ingénierie du Prompting",                           "coordonnateur": "PR. MOUHIB IMAD",       "salle": "AMPHI 4"},
        },
        "Vendredi": {
            "09h00-10h30": {"module": "Français 2",                                        "coordonnateur": "PR. BENTALEB HAYAT",    "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Anglais 2",                                         "coordonnateur": "PR. FATMI ABDERRAHIM",  "salle": "AMPHI 4"},
        },
    },

    # ── IA — Semestre 6 ───────────────────────────────────────────────────────
    "IA_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                               "coordonnateur": "PR. EL IDRISSI MOURAD", "salle": "AMPHI 2"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire", "coordonnateur": "PR. LAMOUDAN TARIK","salle": "AMPHI 2"},
            "16h00-17h30": {"module": "Machine Learning",                                  "coordonnateur": "PR. MELLAH YOUSSEF",   "salle": "AMPHI 2"},
        },
        "Mercredi": {
            "14h00-15h30": {"module": "Réseaux Informatiques et Protocoles",               "coordonnateur": "PR. HANDOUF SARA",     "salle": "AMPHI 2"},
            "16h00-17h30": {"module": "Modélisation Logicielle et Données Structurées",    "coordonnateur": "PR. LHIADI REDOUANE",  "salle": "AMPHI 2"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Développement d'Applications Web Avancé",           "coordonnateur": "PR. LHIADI REDOUANE",  "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Ingénierie du Prompting",                           "coordonnateur": "PR. MOUHIB IMAD",      "salle": "AMPHI 5"},
        },
        "Vendredi": {
            "09h00-10h30": {"module": "Français 2",                                        "coordonnateur": "PR. BENTALEB HAYAT",   "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Anglais 2",                                         "coordonnateur": "PR. FATMI ABDERRAHIM", "salle": "AMPHI 5"},
        },
    },

    # ── ROC — Semestre 6 ──────────────────────────────────────────────────────
    "ROC_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                               "coordonnateur": "PR. EL IDRISSI MOURAD","salle": "AMPHI 3"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire", "coordonnateur": "PR. LAMOUDAN TARIK","salle": "AMPHI 3"},
            "16h00-17h30": {"module": "Méthodologies de Navigation et de Localisation des Robots", "coordonnateur": "PR. KHIATI WASSIM", "salle": "AMPHI 3"},
        },
        "Mercredi": {
            "14h00-15h30": {"module": "Réseaux Informatiques et Protocoles",               "coordonnateur": "PR. HANDOUF SARA",     "salle": "AMPHI 3"},
            "16h00-17h30": {"module": "Robot Operating System (ROS 1 et 2, RTOS)",         "coordonnateur": "PR. SEJAI MOHAMED",    "salle": "AMPHI 3"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Développement d'Applications Web Avancé",           "coordonnateur": "PR. LHIADI REDOUANE",  "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Ingénierie du Prompting",                           "coordonnateur": "PR. MOUHIB IMAD",      "salle": "AMPHI 6"},
        },
        "Vendredi": {
            "09h00-10h30": {"module": "Français 2",                                        "coordonnateur": "PR. BENTALEB HAYAT",   "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Anglais 2",                                         "coordonnateur": "PR. FATMI ABDERRAHIM", "salle": "AMPHI 6"},
        },
    },

    # ── IRSI — Semestre 6 ─────────────────────────────────────────────────────
    "IRSI_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                               "coordonnateur": "PR. LABLOUL BOUCHRA",  "salle": "AMPHI 3"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire", "coordonnateur": "PR. LAMOUDAN TARIK","salle": "AMPHI 3"},
            "16h00-17h30": {"module": "Ingénierie des Bases de Données Avancée",           "coordonnateur": "PR. BENHAR HOUDA",     "salle": "AMPHI 3"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Administration de Systèmes Linux",                  "coordonnateur": "PR. BOUGHANJA MANALE", "salle": "AMPHI 3"},
            "11h00-12h30": {"module": "Programmation Shell et PowerShell",                 "coordonnateur": "PR. BOUGHANJA MANALE", "salle": "AMPHI 3"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Interconnexion des Réseaux",                        "coordonnateur": "PR. BAKRAOUY ZINEB",   "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Ingénierie du Prompting",                           "coordonnateur": "PR. MOUHIB IMAD",      "salle": "AMPHI 6"},
        },
        "Vendredi": {
            "09h00-10h30": {"module": "Français 2",                                        "coordonnateur": "PR. BENTALEB HAYAT",   "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Anglais",                                           "coordonnateur": "PR. FATMI ABDERRAHIM", "salle": "AMPHI 6"},
        },
    },

    # ── GINF — Semestre 8 ─────────────────────────────────────────────────────
    "GINF_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Deep Learning",                              "coordonnateur": "PR. MHAMMEDI SAJIDA",   "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Business Intelligence et ERP",              "coordonnateur": "PR. KHIATI WASSIM",     "salle": "AMPHI 4"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Administration de Bases de Données",        "coordonnateur": "PR. BADIY MOHAMED",     "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Ingénierie DevOps",                         "coordonnateur": "PR. ALAMI NABIL",       "salle": "AMPHI 4"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Apprentissage par Renforcement",            "coordonnateur": "PR. ADDOU EL HOUCINE",  "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Développement Personnel",                   "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 4"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                 "coordonnateur": "PR. KACHADE ROMAYSAE",  "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Français 4",                                "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 4"},
        },
    },

    # ── IA — Semestre 8 ───────────────────────────────────────────────────────
    "IA_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Business Intelligence et ERP",              "coordonnateur": "PR. BADIY MOHAMED",     "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Systèmes Multi-Agents",                     "coordonnateur": "PR. MHAMMEDI SAJIDA",   "salle": "AMPHI 5"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Vision par Ordinateur et Intelligence Artificielle", "coordonnateur": "PR. BOUTAHIR MOHAMED KHALIFA", "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Apprentissage par Renforcement",            "coordonnateur": "PR. EL HABCHI ALI",     "salle": "AMPHI 5"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Deep Learning",                             "coordonnateur": "PR. AISSI MOHAMMED",    "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Développement Personnel",                   "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 5"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                 "coordonnateur": "PR. KACHADE ROMAYSAE",  "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Français 4",                                "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 5"},
        },
    },

    # ── ROC — Semestre 8 ──────────────────────────────────────────────────────
    "ROC_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Méthodologies de Navigation et Localisation des Robots", "coordonnateur": "PR. SEJAI MOHAMED", "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Systèmes Multi-Agents",                     "coordonnateur": "PR. MHAMMEDI SAJIDA",   "salle": "AMPHI 5"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Apprentissage par Renforcement",            "coordonnateur": "PR. BOUTAHIR MOHAMED KHALIFA", "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Réseaux de Communication IoT",              "coordonnateur": "PR. FARTITCHOU MOHAMED", "salle": "AMPHI 6"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Deep Learning",                             "coordonnateur": "PR. AISSI MOHAMMED",    "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Développement Personnel",                   "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 6"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                 "coordonnateur": "PR. KACHADE ROMAYSAE",  "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Français 4",                                "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 6"},
        },
    },

    # ── IRSI — Semestre 8 ─────────────────────────────────────────────────────
    "IRSI_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Deep Learning",                             "coordonnateur": "PR. MHAMMEDI SAJIDA",   "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Cloud Computing et Virtualisation",         "coordonnateur": "PR. FARTITCHOU MOHAMED", "salle": "AMPHI 6"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Administration et Sécurité des Services",   "coordonnateur": "PR. HANDOUF SARA",      "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Réseaux de Communication IoT",              "coordonnateur": "PR. FARTITCHOU MOHAMED", "salle": "AMPHI 6"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Sécurité des Réseaux",                      "coordonnateur": "PR. BAKRAOUY ZINEB",    "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Développement Personnel",                   "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 6"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                 "coordonnateur": "PR. KACHADE ROMAYSAE",  "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Français 4",                                "coordonnateur": "PR. MHAMDI KHALID",     "salle": "AMPHI 6"},
        },
    },
}


def get_planning_for_filiere(major: str, semestre: str | None = None) -> dict | None:
    """Retourne le planning pour une filière donnée (fuzzy match)."""
    m = (major or "").lower()
    s = (semestre or "").upper()

    if any(k in m for k in ["intelligence artificielle", " ia", "artificial"]):
        candidates = ["IA_S5", "IA_S6", "IA_S7", "IA_S8", "IA_S9"]
    elif any(k in m for k in ["robotique", "roc", "objet"]):
        candidates = ["ROC_S5", "ROC_S6", "ROC_S7", "ROC_S8", "ROC_S9"]
    elif any(k in m for k in ["réseau", "reseau", "sécurité", "securite", "irsi"]):
        candidates = ["IRSI_S5", "IRSI_S6", "IRSI_S7", "IRSI_S8", "IRSI_S9"]
    elif any(k in m for k in ["génie informatique", "genie informatique", "ginf"]):
        candidates = ["GINF_S5", "GINF_S6", "GINF_S7", "GINF_S8", "GINF_S9"]
    elif any(k in m for k in ["préparatoire", "preparatoire", "epsi", "prepa"]):
        candidates = ["PREPA_S1", "EPSI"]
    else:
        return None

    if s:
        for key in candidates:
            if key.endswith(s) or key == s:
                info = FILIERES_INFO.get(key, ("", "", ""))
                return {"filiere": info[0], "semestre": info[1], "session": info[2],
                        "key": key, "planning": PLANNING[key]}

    key = candidates[0]
    info = FILIERES_INFO.get(key, ("", "", ""))
    return {"filiere": info[0], "semestre": info[1], "session": info[2],
            "key": key, "planning": PLANNING[key]}


def get_planning_for_year(year: int, major: str) -> list[dict]:
    """Retourne tous les plannings correspondant à l'année d'étude et à la filière."""
    target_sems = set(YEAR_TO_SEMESTERS.get(year, []))
    m = (major or "").lower()

    if any(k in m for k in ["intelligence artificielle", " ia", "artificial"]):
        prefix = "IA_"
    elif any(k in m for k in ["robotique", "roc", "objet"]):
        prefix = "ROC_"
    elif any(k in m for k in ["réseau", "reseau", "sécurité", "securite", "irsi"]):
        prefix = "IRSI_"
    elif any(k in m for k in ["génie informatique", "genie informatique", "ginf"]):
        prefix = "GINF_"
    else:
        prefix = None  # PREPA / fallback

    results = []
    for key, info in FILIERES_INFO.items():
        if info[1] not in target_sems:
            continue
        if prefix:
            if not key.startswith(prefix):
                continue
        else:
            if key not in ("PREPA_S1", "EPSI") and year > 2:
                continue
        if key in PLANNING:
            results.append({
                "key": key,
                "filiere": info[0],
                "semestre": info[1],
                "session": info[2],
                "planning": PLANNING[key],
            })
    return results


def search_module_in_planning(module_query: str) -> list[dict]:
    """Cherche un module dans tous les plannings et retourne ses créneaux."""
    q = module_query.lower()
    results = []
    for key, jours in PLANNING.items():
        info = FILIERES_INFO.get(key, ("?", "?", "?"))
        filiere_nom, semestre, session = info[0], info[1], info[2] if len(info) > 2 else ""
        for jour, creneaux in jours.items():
            for creneau, data in creneaux.items():
                if q in data["module"].lower():
                    results.append({
                        "filiere": filiere_nom,
                        "semestre": semestre,
                        "session": session,
                        "jour": jour,
                        "creneau": creneau,
                        "module": data["module"],
                        "coordonnateur": data["coordonnateur"],
                        "salle": data["salle"],
                    })
    return results
