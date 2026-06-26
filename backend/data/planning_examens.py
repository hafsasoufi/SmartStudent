"""
Planning officiel des examens - Session de Printemps 2025/2026
ENIAD Berkane — extrait du PDF "planing des examans.pdf"

Structure : PLANNING[cle_filiere]["planning"][jour][créneau] = {module, coordonnateur, salle}
"""

SESSION = "Session de Printemps 2025/2026"

# Clés filière → (nom complet, semestre)
FILIERES_INFO = {
    "EPSI":    ("Études Préparatoires en Sciences de l'Ingénieur", "S2"),
    "GINF_S6": ("Génie Informatique",                              "S6"),
    "GINF_S8": ("Génie Informatique",                              "S8"),
    "IA_S6":   ("Intelligence Artificielle",                       "S6"),
    "IA_S8":   ("Intelligence Artificielle",                       "S8"),
    "ROC_S6":  ("Robotique et Objets Connectés",                   "S6"),
    "ROC_S8":  ("Robotique et Objets Connectés",                   "S8"),
    "IRSI_S6": ("Ingénierie Réseaux et Sécurité Informatique",     "S6"),
    "IRSI_S8": ("Ingénierie Réseaux et Sécurité Informatique",     "S8"),
}

PLANNING: dict[str, dict] = {

    # ── EPSI — Semestre 2 ────────────────────────────────────────────────────
    "EPSI": {
        "Lundi": {
            "09h00-10h30": {"module": "Algèbre 2",                 "coordonnateur": "PR. HARCHA HANANE",   "salle": "AMPHI 1, 2, 3"},
            "11h00-12h30": {"module": "Électronique Analogique",   "coordonnateur": "PR. BOUTOUBA MOHAMED","salle": "AMPHI 1, 2, 3"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Analyse 2",                 "coordonnateur": "PR. ALLAOUI MOSTAFA", "salle": "AMPHI 1, 2, 3"},
            "11h00-12h30": {"module": "Programmation en C",        "coordonnateur": "PR. AISSI MOHAMMED",  "salle": "AMPHI 1, 2, 3"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Électromagnétisme",         "coordonnateur": "PR. SEDDIK MOHAMMED", "salle": "AMPHI 1, 2, 3"},
            "11h00-12h30": {"module": "Culture Digitale",          "coordonnateur": "PR. ADDOU EL HOUCINE","salle": "AMPHI 1, 2, 3"},
        },
        "Jeudi": {
            "14h00-15h30": {"module": "Anglais 2",                 "coordonnateur": "PR. FATMI ABDERRAHIM","salle": "AMPHI 1, 2, 3"},
            "16h00-17h30": {"module": "Français 2",                "coordonnateur": "PR. BENTALEB HAYAT",  "salle": "AMPHI 1, 2, 3"},
        },
    },

    # ── GINF — Semestre 6 ────────────────────────────────────────────────────
    "GINF_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                              "coordonnateur": "PR. LABLOUL BOUCHRA",    "salle": "AMPHI 4"},
            "16h00-17h30": {"module": "Développement d'Applications Web Avancé",          "coordonnateur": "PR. KADDARI ZAKARIA",    "salle": "AMPHI 4"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire","coordonnateur": "PR. LAMOUDAN TARIK",  "salle": "AMPHI 4"},
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

    # ── IA — Semestre 6 ──────────────────────────────────────────────────────
    "IA_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                              "coordonnateur": "PR. EL IDRISSI MOURAD", "salle": "AMPHI 2"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire","coordonnateur": "PR. LAMOUDAN TARIK", "salle": "AMPHI 2"},
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

    # ── ROC — Semestre 6 ─────────────────────────────────────────────────────
    "ROC_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                              "coordonnateur": "PR. EL IDRISSI MOURAD", "salle": "AMPHI 3"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire","coordonnateur": "PR. LAMOUDAN TARIK", "salle": "AMPHI 3"},
            "16h00-17h30": {"module": "Méthodologies de Navigation et de Localisation des Robots","coordonnateur": "PR. KHIATI WASSIM","salle": "AMPHI 3"},
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

    # ── IRSI — Semestre 6 ────────────────────────────────────────────────────
    "IRSI_S6": {
        "Lundi": {
            "14h00-15h30": {"module": "Analyse des Données",                              "coordonnateur": "PR. LABLOUL BOUCHRA",  "salle": "AMPHI 3"},
        },
        "Mardi": {
            "14h00-15h30": {"module": "Recherche Opérationnelle et Optimisation Combinatoire","coordonnateur": "PR. LAMOUDAN TARIK","salle": "AMPHI 3"},
            "16h00-17h30": {"module": "Ingénierie des Bases de Données Avancée",           "coordonnateur": "PR. BENHAR HOUDA",     "salle": "AMPHI 3"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Administration de Systèmes Linux",                  "coordonnateur": "PR. BOUGHANJA MANALE","salle": "AMPHI 3"},
            "11h00-12h30": {"module": "Programmation Shell et PowerShell",                 "coordonnateur": "PR. BOUGHANJA MANALE","salle": "AMPHI 3"},
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

    # ── GINF — Semestre 8 ────────────────────────────────────────────────────
    "GINF_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Deep Learning",                                    "coordonnateur": "PR. MHAMMEDI SAJIDA",  "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Business Intelligence et ERP",                     "coordonnateur": "PR. KHIATI WASSIM",    "salle": "AMPHI 4"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Administration de Bases de Données",               "coordonnateur": "PR. BADIY MOHAMED",    "salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Ingénierie DevOps",                                "coordonnateur": "PR. ALAMI NABIL",      "salle": "AMPHI 4"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Apprentissage par Renforcement",                   "coordonnateur": "PR. ADDOU EL HOUCINE","salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Développement Personnel",                          "coordonnateur": "PR. MHAMDI KHALID",   "salle": "AMPHI 4"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                        "coordonnateur": "PR. KACHADE ROMAYSAE","salle": "AMPHI 4"},
            "11h00-12h30": {"module": "Français 4",                                       "coordonnateur": "PR. MHAMDI KHALID",   "salle": "AMPHI 4"},
        },
    },

    # ── IA — Semestre 8 ──────────────────────────────────────────────────────
    "IA_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Business Intelligence et ERP",                     "coordonnateur": "PR. BADIY MOHAMED",    "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Systèmes Multi-Agents",                            "coordonnateur": "PR. MHAMMEDI SAJIDA",  "salle": "AMPHI 5"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Vision par Ordinateur et Intelligence Artificielle","coordonnateur": "PR. BOUTAHIR MOHAMED KHALIFA","salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Apprentissage par Renforcement",                   "coordonnateur": "PR. EL HABCHI ALI",    "salle": "AMPHI 5"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Deep Learning",                                    "coordonnateur": "PR. AISSI MOHAMMED",   "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Développement Personnel",                          "coordonnateur": "PR. MHAMDI KHALID",    "salle": "AMPHI 5"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                        "coordonnateur": "PR. KACHADE ROMAYSAE", "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Français 4",                                       "coordonnateur": "PR. MHAMDI KHALID",    "salle": "AMPHI 5"},
        },
    },

    # ── ROC — Semestre 8 ─────────────────────────────────────────────────────
    "ROC_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Méthodologies de Navigation et Localisation des Robots","coordonnateur": "PR. SEJAI MOHAMED","salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Systèmes Multi-Agents",                            "coordonnateur": "PR. MHAMMEDI SAJIDA",  "salle": "AMPHI 5"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Apprentissage par Renforcement",                   "coordonnateur": "PR. BOUTAHIR MOHAMED KHALIFA","salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Réseaux de Communication IoT",                     "coordonnateur": "PR. FARTITCHOU MOHAMED","salle": "AMPHI 6"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Deep Learning",                                    "coordonnateur": "PR. AISSI MOHAMMED",   "salle": "AMPHI 5"},
            "11h00-12h30": {"module": "Développement Personnel",                          "coordonnateur": "PR. MHAMDI KHALID",    "salle": "AMPHI 6"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                        "coordonnateur": "PR. KACHADE ROMAYSAE", "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Français 4",                                       "coordonnateur": "PR. MHAMDI KHALID",    "salle": "AMPHI 6"},
        },
    },

    # ── IRSI — Semestre 8 ────────────────────────────────────────────────────
    "IRSI_S8": {
        "Lundi": {
            "09h00-10h30": {"module": "Deep Learning",                                    "coordonnateur": "PR. MHAMMEDI SAJIDA",  "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Cloud Computing et Virtualisation",                "coordonnateur": "PR. FARTITCHOU MOHAMED","salle": "AMPHI 6"},
        },
        "Mardi": {
            "09h00-10h30": {"module": "Administration et Sécurité des Services",          "coordonnateur": "PR. HANDOUF SARA",     "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Réseaux de Communication IoT",                     "coordonnateur": "PR. FARTITCHOU MOHAMED","salle": "AMPHI 6"},
        },
        "Mercredi": {
            "09h00-10h30": {"module": "Sécurité des Réseaux",                             "coordonnateur": "PR. BAKRAOUY ZINEB",   "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Développement Personnel",                          "coordonnateur": "PR. MHAMDI KHALID",    "salle": "AMPHI 6"},
        },
        "Jeudi": {
            "09h00-10h30": {"module": "Anglais 4",                                        "coordonnateur": "PR. KACHADE ROMAYSAE", "salle": "AMPHI 6"},
            "11h00-12h30": {"module": "Français 4",                                       "coordonnateur": "PR. MHAMDI KHALID",    "salle": "AMPHI 6"},
        },
    },
}


def get_planning_for_filiere(major: str, semestre: str | None = None) -> dict | None:
    """Retourne le planning pour une filière donnée (fuzzy match)."""
    m = (major or "").lower()
    s = (semestre or "").upper()

    # Mapping filière → clés PLANNING
    candidates: list[str] = []
    if any(k in m for k in ["intelligence artificielle", " ia", "artificial"]):
        candidates = ["IA_S6", "IA_S8"]
    elif any(k in m for k in ["robotique", "roc", "objet"]):
        candidates = ["ROC_S6", "ROC_S8"]
    elif any(k in m for k in ["réseau", "reseau", "sécurité", "securite", "irsi"]):
        candidates = ["IRSI_S6", "IRSI_S8"]
    elif any(k in m for k in ["génie informatique", "genie informatique", "ginf"]):
        candidates = ["GINF_S6", "GINF_S8"]
    elif any(k in m for k in ["préparatoire", "preparatoire", "epsi"]):
        candidates = ["EPSI"]
    else:
        return None

    if s:
        for key in candidates:
            if key.endswith(s) or key == s:
                info = FILIERES_INFO.get(key, ("", ""))
                return {"filiere": info[0], "semestre": info[1], "key": key, "planning": PLANNING[key]}

    # Retourner le premier trouvé
    key = candidates[0]
    info = FILIERES_INFO.get(key, ("", ""))
    return {"filiere": info[0], "semestre": info[1], "key": key, "planning": PLANNING[key]}


def search_module_in_planning(module_query: str) -> list[dict]:
    """Cherche un module dans tous les plannings et retourne ses créneaux."""
    q = module_query.lower()
    results = []
    for key, jours in PLANNING.items():
        filiere_nom, semestre = FILIERES_INFO.get(key, ("?", "?"))
        for jour, creneaux in jours.items():
            for creneau, info in creneaux.items():
                if q in info["module"].lower():
                    results.append({
                        "filiere": filiere_nom,
                        "semestre": semestre,
                        "jour": jour,
                        "creneau": creneau,
                        "module": info["module"],
                        "coordonnateur": info["coordonnateur"],
                        "salle": info["salle"],
                    })
    return results
