# -*- coding: utf-8 -*-
"""
Générateur des fiches "module" pour eniad_knowledge.py
Source des données : plan_filiere.pdf (officiel ENIAD, fourni par l'utilisateur)
Une fiche = un module (avec son/ses élément(s) de module si découpé en sous-parties).
"""

import unicodedata
import re


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


# Légende VH : Cours, TD, TP, AP, EV -> volume horaire global (VH/VHG)
# Format de chaque ligne module :
# (intitule_module, [ (element_de_module, cours, td, tp, ap, ev, vh) , ... ])

FILIERES = {}

# ───────────────────────────── EPSI (S1 à S4) ─────────────────────────────
FILIERES["EPSI"] = {
    "nom_complet": "Études Préparatoires en Sciences de l'Ingénieur",
    "semestres": {
        "S1": [
            ("ALGEBRE 1", [("ALGEBRE 1", 21, 24, 0, 0, 3, 48)]),
            ("ANALYSE 1", [("ANALYSE 1", 21, 24, 0, 0, 3, 48)]),
            ("MECANIQUE DU POINT", [("MECANIQUE DU POINT", 21, 15, 9, 0, 3, 48)]),
            ("ELECTROCINETIQUE", [("ELECTROCINETIQUE", 21, 15, 9, 0, 3, 48)]),
            ("ALGORITHMIQUE ET ARCHITECTURE DES ORDINATEURS", [("ALGORITHMIQUE ET ARCHITECTURE DES ORDINATEURS", 21, 15, 9, 0, 3, 48)]),
            ("METHODOLOGIE DE TRAVAIL UNIVERSITAIRE", [("METHODOLOGIE DE TRAVAIL UNIVERSITAIRE", 21, 0, 0, 24, 3, 48)]),
            ("LANGUES ET COMMUNICATIONS 1", [
                ("FRANCAIS 1", 7, 0, 0, 15, 2, 24),
                ("ANGLAIS 1", 7, 0, 0, 15, 2, 24),
            ]),
        ],
        "S2": [
            ("ALGEBRE 2", [("ALGEBRE 2", 21, 24, 0, 0, 3, 48)]),
            ("ANALYSE 2", [("ANALYSE 2", 21, 24, 0, 0, 3, 48)]),
            ("ÉLECTROMAGNÉTISME", [("ÉLECTROMAGNÉTISME", 21, 15, 9, 0, 3, 48)]),
            ("ELECTRONIQUE ANALOGIQUE", [("ELECTRONIQUE ANALOGIQUE", 21, 15, 9, 0, 3, 48)]),
            ("PROGRAMMATION EN C", [("PROGRAMMATION EN C", 21, 0, 24, 0, 3, 48)]),
            ("CULTURE DIGITALE", [("CULTURE DIGITALE", 21, 0, 24, 0, 3, 48)]),
            ("LANGUES ET COMMUNICATIONS 2", [
                ("FRANCAIS 2", 7, 0, 0, 15, 2, 24),
                ("ANGLAIS 2", 7, 0, 0, 15, 2, 24),
            ]),
        ],
        "S3": [
            ("ALGEBRE 3", [("ALGEBRE 3", 21, 24, 0, 0, 3, 48)]),
            ("ANALYSE 3", [("ANALYSE 3", 21, 24, 0, 0, 3, 48)]),
            ("TRAITEMENT DU SIGNAL ET SYSTÈMES NUMÉRIQUES", [("TRAITEMENT DU SIGNAL ET SYSTÈMES NUMÉRIQUES", 21, 24, 0, 0, 3, 48)]),
            ("ALGORITHMIQUE AVANCE & STRUCTURE DES DONNEES", [("ALGORITHMIQUE AVANCE & STRUCTURE DES DONNEES", 21, 12, 12, 0, 3, 48)]),
            ("PROGRAMMATION PYTHON", [("PROGRAMMATION PYTHON", 21, 0, 24, 0, 3, 48)]),
            ("SYSTÈMES D'INFORMATIONS ET BASES DE DONNÉES", [("SYSTÈMES D'INFORMATIONS ET BASES DE DONNÉES", 21, 12, 12, 0, 3, 48)]),
            ("LANGUES ET COMMUNICATIONS 3", [
                ("FRANCAIS 3", 7, 0, 0, 15, 2, 24),
                ("ANGLAIS 3", 7, 0, 0, 15, 2, 24),
            ]),
        ],
        "S4": [
            ("ANALYSE 4", [("ANALYSE 4", 21, 24, 0, 0, 3, 48)]),
            ("STATISTIQUES & PROBABILITES", [("STATISTIQUES & PROBABILITES", 21, 24, 0, 0, 3, 48)]),
            ("INTRODUCTION AUX RESEAUX INFORMATIQUES ET SYSTEMES D'EXPLOITATION", [("INTRODUCTION AUX RESEAUX INFORMATIQUES ET SYSTEMES D'EXPLOITATION", 21, 12, 12, 0, 3, 48)]),
            ("ANALYSE NUMERIQUE", [("ANALYSE NUMERIQUE", 21, 18, 6, 0, 3, 48)]),
            ("DEVELOPPEMENT WEB", [("DEVELOPPEMENT WEB", 21, 0, 24, 0, 3, 48)]),
            ("ÉLECTRONIQUE NUMÉRIQUE", [("ÉLECTRONIQUE NUMÉRIQUE", 21, 12, 12, 0, 3, 48)]),
            ("LANGUES ET COMMUNICATIONS 4", [
                ("FRANCAIS 4", 7, 0, 0, 15, 2, 24),
                ("ANGLAIS 4", 7, 0, 0, 15, 2, 24),
            ]),
        ],
    }
}

# ───────────────────────────── IA (S5 à S9) ─────────────────────────────
FILIERES["IA"] = {
    "nom_complet": "Intelligence Artificielle",
    "semestres": {
        "S5": [
            ("PROGRAMMATION ORIENTE OBJET EN JAVA", [("PROGRAMMATION ORIENTE OBJET EN JAVA", 18, 0, 21, 0, 3, 42)]),
            ("PROGRAMMATION ORIENTE OBJET EN PYTHON", [("PROGRAMMATION ORIENTE OBJET EN PYTHON", 18, 0, 21, 0, 3, 42)]),
            ("INGENIERIE DES BASES DE DONNEES AVANCEE", [("INGENIERIE DES BASES DE DONNEES AVANCEE", 18, 0, 21, 0, 3, 42)]),
            ("SYSTEME D'EXPLOITATION ET PROGRAMMATION SYSTEMES", [("SYSTEME D'EXPLOITATION ET PROGRAMMATION SYSTEMES", 18, 0, 21, 0, 3, 42)]),
            ("DEVELOPPEMENT D'APPLICATIONS WEB", [("DEVELOPPEMENT D'APPLICATIONS WEB", 18, 0, 21, 0, 3, 42)]),
            ("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", [("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", 18, 12, 9, 0, 3, 42)]),
            ("COMPTABILITE ET CALCUL DES COUTS", [("COMPTABILITE ET CALCUL DES COUTS", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 1", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 1", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 1", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S6": [
            ("DEVELOPPEMENT D'APPLICATIONS WEB AVANCE", [("DEVELOPPEMENT D'APPLICATIONS WEB AVANCE", 18, 0, 21, 0, 3, 42)]),
            ("MACHINE LEARNING", [("MACHINE LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("RESEAUX INFORMATIQUE", [("RESEAUX INFORMATIQUE", 18, 12, 9, 0, 3, 42)]),
            ("MODELISATION LOGICIELLE ET DONNEES STRUCTUREES", [("MODELISATION LOGICIELLE ET DONNEES STRUCTUREES", 18, 0, 21, 0, 3, 42)]),
            ("ANALYSE DE DONNEES", [("ANALYSE DE DONNEES", 18, 12, 9, 0, 3, 42)]),
            ("RECHERCHE OPERATIONNELLE", [("RECHERCHE OPERATIONNELLE", 18, 12, 9, 0, 3, 42)]),
            ("INGÉNIERIE DU PROMPTING", [("INGÉNIERIE DU PROMPTING", 18, 12, 9, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 2", [
                ("LANGUES ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 2", 7, 0, 0, 12, 2, 21),
                ("LANGUES ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 2", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S7": [
            ("DEEP LEARNING", [("DEEP LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("VISION ARTIFICIELLE", [("VISION ARTIFICIELLE", 18, 0, 21, 0, 3, 42)]),
            ("GESTION AGILE DE PROJET INFORMATIQUE", [("GESTION AGILE DE PROJET INFORMATIQUE", 18, 12, 9, 0, 3, 42)]),
        ],
        "S8": [
            ("GESTION AGILE DE PROJET INFORMATIQUE", [("GESTION AGILE DE PROJET INFORMATIQUE", 18, 9, 12, 0, 3, 42)]),
            ("DÉVELOPPEMENT MOBILE MULTIPLATFORME", [("DÉVELOPPEMENT MOBILE MULTIPLATFORME", 18, 0, 21, 0, 3, 42)]),
            ("MACHINE LEARNING", [("MACHINE LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("VISION ARTIFICIELLE", [("VISION ARTIFICIELLE", 18, 0, 21, 0, 3, 42)]),
            ("MANAGEMENT ET MARKETING", [("MANAGEMENT ET MARKETING", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 3", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 3", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 3", 7, 0, 0, 12, 2, 21),
            ]),
            ("SYSTEMES MULTI AGENTS", [("SYSTEMES MULTI AGENTS", 18, 0, 21, 0, 3, 42)]),
            ("BUSSINESS INTELLIGENCE ET ERP", [("BUSSINESS INTELLIGENCE ET ERP", 18, 0, 21, 0, 3, 42)]),
            ("IA EMBARQUÉE & EDGE AI", [("IA EMBARQUÉE & EDGE AI", 18, 0, 21, 0, 3, 42)]),
            ("REINFORCEMENT LEARNING", [("REINFORCEMENT LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER DES ACTIVITES PRATIQUES ET PROJETS", [("ATELIER DES ACTIVITES PRATIQUES ET PROJETS", 0, 0, 0, 39, 3, 42)]),
            ("DEVELOPPEMENT PERSONNEL", [("DEVELOPPEMENT PERSONNEL", 18, 0, 0, 21, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 4", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 4", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 4", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S9": [
            ("INGENIERIE BIG DATA", [("INGENIERIE BIG DATA", 18, 0, 21, 0, 3, 42)]),
            ("REALITE VIRTUEL ET REALITE AUGMENTEE", [("REALITE VIRTUEL ET REALITE AUGMENTEE", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER ROBOTIQUE AVANCEE (COBOTIQUE, MOBILITE)", [("ATELIER ROBOTIQUE AVANCEE (COBOTIQUE, MOBILITE)", 18, 9, 12, 0, 3, 42)]),
            ("TECHNOLOGIES POUR L'AUTOMOBILE, L'AÉRONAUTIQUE ET LES DRONES", [("TECHNOLOGIES POUR L'AUTOMOBILE, L'AÉRONAUTIQUE ET LES DRONES", 18, 0, 21, 0, 3, 42)]),
            ("CLOUD COMPUTING ET VIRTUALISATION", [("CLOUD COMPUTING ET VIRTUALISATION", 18, 0, 21, 0, 3, 42)]),
            ("CYBERSECURITY POUR ET L'IA LA ROBOTIQUE", [("CYBERSECURITY POUR ET L'IA LA ROBOTIQUE", 18, 0, 21, 0, 3, 42)]),
            ("ETHIQUES ET DROITS", [("ETHIQUES ET DROITS", 18, 0, 0, 21, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 5", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 5", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 5", 7, 0, 0, 12, 2, 21),
            ]),
        ],
    }
}

# ───────────────────────────── GINF (S5 à S9) ─────────────────────────────
FILIERES["GINF"] = {
    "nom_complet": "Génie Informatique",
    "semestres": {
        "S5": [
            ("PROGRAMMATION ORIENTE OBJET EN JAVA", [("PROGRAMMATION ORIENTE OBJET EN JAVA", 18, 0, 21, 0, 3, 42)]),
            ("PROGRAMMATION ORIENTE OBJET EN PYTHON", [("PROGRAMMATION ORIENTE OBJET EN PYTHON", 18, 0, 21, 0, 3, 42)]),
            ("INGÉNIERIE DES BASES DE DONNÉES AVANCÉE", [("INGÉNIERIE DES BASES DE DONNÉES AVANCÉE", 18, 0, 21, 0, 3, 42)]),
            ("DEVELOPPEMENT D'APPLICATIONS WEB", [("DEVELOPPEMENT D'APPLICATIONS WEB", 18, 0, 21, 0, 3, 42)]),
            ("SYSTÈMES D'EXPLOITATION ET PROGRAMMATION SYSTÈME", [("SYSTÈMES D'EXPLOITATION ET PROGRAMMATION SYSTÈME", 18, 0, 21, 0, 3, 42)]),
            ("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", [("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", 18, 15, 6, 0, 3, 42)]),
            ("COMPTABILITE ET CALCUL DES COUTS", [("COMPTABILITE ET CALCUL DES COUTS", 18, 21, 0, 0, 3, 42)]),
            ("LANGUE ET TECHNIQUES DE COMMUNICATION 1", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 1", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 1", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S6": [
            ("PROGRAMMATION ORIENTE OBJET EN C++", [("PROGRAMMATION ORIENTE OBJET EN C++", 18, 0, 21, 0, 3, 42)]),
            ("MODÉLISATION LOGICIELLE ET DONNÉES STRUCTURÉES", [("MODÉLISATION LOGICIELLE ET DONNÉES STRUCTURÉES", 18, 0, 21, 0, 3, 42)]),
            ("DEVELOPPEMENT D'APPLICATIONS WEB AVANCÉ", [("DEVELOPPEMENT D'APPLICATIONS WEB AVANCÉ", 18, 0, 21, 0, 3, 42)]),
            ("RÉSEAUX INFORMATIQUES", [("RÉSEAUX INFORMATIQUES", 18, 12, 9, 0, 3, 42)]),
            ("ANALYSE DES DONNEES", [("ANALYSE DES DONNEES", 18, 21, 0, 0, 3, 42)]),
            ("RECHERCHE OPERATIONNELLE ET OPTIMISATION COMBINATOIRE", [("RECHERCHE OPERATIONNELLE ET OPTIMISATION COMBINATOIRE", 18, 21, 0, 0, 3, 42)]),
            ("INGÉNIERIE DU PROMPTING", [("INGÉNIERIE DU PROMPTING", 18, 12, 9, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 2", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 2", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 2", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S7": [
            ("INGÉNIERIE JEE ET APPLICATIONS DISTRIBUÉES", [("INGÉNIERIE JEE ET APPLICATIONS DISTRIBUÉES", 18, 0, 21, 0, 3, 42)]),
        ],
        "S8": [
            ("DÉVELOPPEMENT D'APPLICATION .NET", [("DÉVELOPPEMENT D'APPLICATION .NET", 18, 0, 21, 0, 3, 42)]),
            ("DÉVELOPPEMENT MOBILE MULTIPLATFORME", [("DÉVELOPPEMENT MOBILE MULTIPLATFORME", 18, 0, 21, 0, 3, 42)]),
            ("ADMINISTRATION DES SYSTÈMES", [("ADMINISTRATION DES SYSTÈMES", 18, 0, 21, 0, 3, 42)]),
            ("MACHINE LEARNING", [("MACHINE LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("GESTION AGILE DE PROJET INFORMATIQUE", [("GESTION AGILE DE PROJET INFORMATIQUE", 18, 12, 9, 0, 3, 42)]),
            ("MANAGEMENT ET MARKETING", [("MANAGEMENT ET MARKETING", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 3", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 3", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 3", 7, 0, 0, 12, 2, 21),
            ]),
            ("INGÉNIERIE DEVOPS", [("INGÉNIERIE DEVOPS", 18, 0, 21, 0, 3, 42)]),
            ("ADMINISTRATION DE BASES DE DONNÉES", [("ADMINISTRATION DE BASES DE DONNÉES", 18, 0, 21, 0, 3, 42)]),
            ("DEEP LEARNING", [("DEEP LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("APPRENTISSAGE PAR RENFORCEMENT", [("APPRENTISSAGE PAR RENFORCEMENT", 18, 0, 21, 0, 3, 42)]),
            ("BUSSINESS INTELLIGENCE ET ERP", [("BUSSINESS INTELLIGENCE ET ERP", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER DES ACTIVITES PRATIQUES ET PROJETS", [("ATELIER DES ACTIVITES PRATIQUES ET PROJETS", 0, 0, 0, 39, 3, 42)]),
            ("DEVELOPPEMENT PERSONNEL", [("DEVELOPPEMENT PERSONNEL", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 4", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 4", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 4", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S9": [
            ("URBANISATION DES SYSTÈMES D'INFORMATION", [("URBANISATION DES SYSTÈMES D'INFORMATION", 18, 0, 21, 0, 3, 42)]),
            ("ARCHITECTURE LOGICIELLE ET DESIGN PATTERNS", [("ARCHITECTURE LOGICIELLE ET DESIGN PATTERNS", 18, 0, 21, 0, 3, 42)]),
            ("INGÉNIERIE BIG DATA", [("INGÉNIERIE BIG DATA", 18, 0, 21, 0, 3, 42)]),
            ("CLOUD COMPUTING ET VIRTUALISATION", [("CLOUD COMPUTING ET VIRTUALISATION", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER PENTESTING WEB", [("ATELIER PENTESTING WEB", 18, 0, 21, 0, 3, 42)]),
            ("INTERCONNEXION RESEAUX ET SECURITE RESEAUX", [("INTERCONNEXION RESEAUX ET SECURITE RESEAUX", 18, 0, 21, 0, 3, 42)]),
            ("ETHIQUES ET DROITS", [("ETHIQUES ET DROITS", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 5", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 5", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 5", 7, 0, 0, 12, 2, 21),
            ]),
        ],
    }
}

# ───────────────────────────── IRSI (S5 à S9) ─────────────────────────────
FILIERES["IRSI"] = {
    "nom_complet": "Ingénierie Réseaux et Sécurité Informatique",
    "semestres": {
        "S5": [
            ("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", [("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", 18, 12, 9, 0, 3, 42)]),
            ("PROGRAMMATION ORIENTE OBJET EN PYTHON", [("PROGRAMMATION ORIENTE OBJET EN PYTHON", 18, 0, 21, 0, 3, 42)]),
            ("SYSTEME D'EXPLOITATION ET PROGRAMMATION SYSTEMES", [("SYSTEME D'EXPLOITATION ET PROGRAMMATION SYSTEMES", 18, 0, 21, 0, 3, 42)]),
            ("RESEAUX INFORMATIQUE", [("RESEAUX INFORMATIQUE", 18, 12, 9, 0, 3, 42)]),
            ("DEVELOPPEMENT D'APPLICATIONS WEB", [("DEVELOPPEMENT D'APPLICATIONS WEB", 18, 0, 21, 0, 3, 42)]),
            ("PROGRAMMATION ORIENTE OBJET EN JAVA", [("PROGRAMMATION ORIENTE OBJET EN JAVA", 18, 0, 21, 0, 3, 42)]),
            ("COMPTABILITE ET CALCUL DES COUTS", [("COMPTABILITE ET CALCUL DES COUTS", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 1", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 1", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 1", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S6": [
            ("ANALYSE DE DONNEES", [("ANALYSE DE DONNEES", 18, 12, 9, 0, 3, 42)]),
            ("RECHERCHE OPERATIONNELLE ET OPTIMISATION COMBINATOIRE", [("RECHERCHE OPERATIONNELLE ET OPTIMISATION COMBINATOIRE", 18, 12, 9, 0, 3, 42)]),
            ("ADMINISTRATION SYSTEMES LINUX", [("ADMINISTRATION SYSTEMES LINUX", 18, 0, 21, 0, 3, 42)]),
            ("INTERCONNEXION DES RESEAUX", [("INTERCONNEXION DES RESEAUX", 18, 0, 21, 0, 3, 42)]),
            ("INGÉNIERIE DES BASES DE DONNEES AVANCEE", [("INGÉNIERIE DES BASES DE DONNEES AVANCEE", 18, 0, 21, 0, 3, 42)]),
            ("PROGRAMMATION SHELL & POWERSHELL", [("PROGRAMMATION SHELL & POWERSHELL", 18, 0, 21, 0, 3, 42)]),
            ("INGÉNIERIE DU PROMPTING", [("INGÉNIERIE DU PROMPTING", 18, 12, 9, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 2", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANÇAIS 2", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 2", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S7": [
            ("INTERCONNEXION DES RESEAUX AVANCEE", [("INTERCONNEXION DES RESEAUX AVANCEE", 18, 0, 21, 0, 3, 42)]),
            ("ADMINISTRATION ET SECURITE DES SERVICES", [("ADMINISTRATION ET SECURITE DES SERVICES", 18, 0, 21, 0, 3, 42)]),
            ("GESTION AGILE DE PROJET INFORMATIQUE", [("GESTION AGILE DE PROJET INFORMATIQUE", 18, 0, 21, 0, 3, 42)]),
            ("DÉVELOPPEMENT MOBILE MULTIPLATFORME", [("DÉVELOPPEMENT MOBILE MULTIPLATFORME", 18, 0, 21, 0, 3, 42)]),
            ("OPTIMISATION COMBINATOIRE ET MÉTAHEURISTIQUES", [("OPTIMISATION COMBINATOIRE ET MÉTAHEURISTIQUES", 18, 0, 21, 0, 3, 42)]),
            ("RESEAUX DE COMMUNICATION IOT", [("RESEAUX DE COMMUNICATION IOT", 18, 9, 12, 0, 3, 42)]),
            ("MANAGEMENT ET MARKETING", [("MANAGEMENT ET MARKETING", 18, 12, 0, 9, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 3", [
                ("LANGUES ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 3", 7, 0, 0, 12, 2, 21),
                ("LANGUES ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 3", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S8": [
            ("SYSTEMES MULTI AGENTS", [("SYSTEMES MULTI AGENTS", 18, 0, 21, 0, 3, 42)]),
            ("BUSSINESS INTELLIGENCE ET ERP", [("BUSSINESS INTELLIGENCE ET ERP", 18, 0, 21, 0, 3, 42)]),
            ("SECURITE DES RESEAUX", [("SECURITE DES RESEAUX", 18, 0, 21, 0, 3, 42)]),
            ("CLOUD COMPIUTING ET VIRTUALISATION", [("CLOUD COMPIUTING ET VIRTUALISATION", 18, 0, 21, 0, 3, 42)]),
            ("DEEP LEARNING", [("DEEP LEARNING", 18, 0, 21, 0, 3, 42)]),
            ("APPRENTISSAGE PAR RENFORCEMENT", [("APPRENTISSAGE PAR RENFORCEMENT", 18, 0, 21, 0, 3, 42)]),
            ("CYBERSECURITE", [("CYBERSECURITE", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER DES ACTIVITES PRATIQUES ET PROJETS", [("ATELIER DES ACTIVITES PRATIQUES ET PROJETS", 0, 0, 0, 39, 3, 42)]),
            ("DEVELOPPEMENT PERSONNEL", [("DEVELOPPEMENT PERSONNEL", 18, 0, 0, 21, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 4", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 4", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 4", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S9": [
            ("ATELIER PENTESTING WEB", [("ATELIER PENTESTING WEB", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER ETHICAL HACKING", [("ATELIER ETHICAL HACKING", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER FIREWALL", [("ATELIER FIREWALL", 18, 0, 21, 0, 3, 42)]),
            ("TECHNOLOGIE BLOCKCHAIN", [("TECHNOLOGIE BLOCKCHAIN", 18, 0, 21, 0, 3, 42)]),
            ("GOUVERNANCE DE LA SECURITE ET ANALYSE DES RISQUES", [("GOUVERNANCE DE LA SECURITE ET ANALYSE DES RISQUES", 18, 0, 21, 0, 3, 42)]),
            ("ATELIER DEVSECOPS & SOC", [("ATELIER DEVSECOPS & SOC", 18, 0, 21, 0, 3, 42)]),
            ("ETHIQUES ET DROITS", [("ETHIQUES ET DROITS", 18, 0, 0, 21, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 5", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 5", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 5", 7, 0, 0, 12, 2, 21),
            ]),
        ],
    }
}

# ───────────────────────────── ROC (S5 à S7, données partielles dans le PDF) ─────────────────────────────
FILIERES["ROC"] = {
    "nom_complet": "Robotique et Objets Connectés",
    "semestres": {
        "S5": [
            ("PROGRAMMATION ORIENTE OBJET EN JAVA", [("PROGRAMMATION ORIENTE OBJET EN JAVA", 18, 0, 21, 0, 3, 42)]),
            ("PROGRAMMATION EMBARQUÉE", [("PROGRAMMATION EMBARQUÉE", 18, 0, 21, 0, 3, 42)]),
            ("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", [("STATISTIQUES DESCRIPTIVES, INFÉRENTIELLES ET EXPLORATOIRES", 18, 12, 9, 0, 3, 42)]),
            ("DEVELOPPEMENT D'APPLICATIONS WEB", [("DEVELOPPEMENT D'APPLICATIONS WEB", 18, 0, 21, 0, 3, 42)]),
            ("SYSTEME D'EXPLOITATION ET PROGRAMMATION SYSTEMES", [("SYSTEME D'EXPLOITATION ET PROGRAMMATION SYSTEMES", 18, 0, 21, 0, 3, 42)]),
            ("PERCEPTION ET CAPTEURS POUR OBJETS ET ROBOTS CONNECTÉS", [("PERCEPTION ET CAPTEURS POUR OBJETS ET ROBOTS CONNECTÉS", 18, 12, 9, 0, 3, 42)]),
            ("COMPTABILITE ET CALCUL DES COUTS", [("COMPTABILITE ET CALCUL DES COUTS", 18, 21, 0, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 1", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 1", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 1", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S6": [
            ("DEVELOPPEMENT D'APPLICATIONS WEB AVANCÉ", [("DEVELOPPEMENT D'APPLICATIONS WEB AVANCÉ", 18, 0, 21, 0, 3, 42)]),
            ("ROBOT OPERATING SYSTEM (ROS 1 & 2, RTOS)", [("ROBOT OPERATING SYSTEM (ROS 1 & 2, RTOS)", 18, 0, 21, 0, 3, 42)]),
            ("RESEAUX INFORMATIQUE", [("RESEAUX INFORMATIQUE", 18, 12, 9, 0, 3, 42)]),
            ("MÉTHODOLOGIES DE NAVIGATION ET DE LOCALISATION DES ROBOTS", [("MÉTHODOLOGIES DE NAVIGATION ET DE LOCALISATION DES ROBOTS", 18, 12, 9, 0, 3, 42)]),
            ("ANALYSE DE DONNEES", [("ANALYSE DE DONNEES", 18, 12, 9, 0, 3, 42)]),
            ("RECHERCHE OPERATIONNELLE ET OPTIMISATION COMBINATOIRE", [("RECHERCHE OPERATIONNELLE ET OPTIMISATION COMBINATOIRE", 18, 12, 9, 0, 3, 42)]),
            ("INGÉNIERIE DU PROMPTING", [("INGÉNIERIE DU PROMPTING", 18, 12, 9, 0, 3, 42)]),
            ("LANGUES ET TECHNIQUES DE COMMUNICATION 2", [
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN FRANCAIS 2", 7, 0, 0, 12, 2, 21),
                ("LANGUE ET TECHNIQUES DE COMMUNICATION EN ANGLAIS 2", 7, 0, 0, 12, 2, 21),
            ]),
        ],
        "S7": [
            ("PROGRAMMATION EN ROBOTIQUE ET CONCEPTION 3D", [("PROGRAMMATION EN ROBOTIQUE ET CONCEPTION 3D", 18, 9, 12, 0, 3, 42)]),
            ("RESEAUX DE COMMUNICATION IOT", [("RESEAUX DE COMMUNICATION IOT", 18, 9, 12, 0, 3, 42)]),
        ],
        # S8/S9 ROC : données non disponibles dans le PDF fourni — à compléter.
    }
}

VHG_LEGEND = (
    "Cours=heures de cours magistraux, TD=Travaux Diriges, TP=Travaux Pratiques, "
    "AP=Activites Pratiques, EV=Evaluations, VH=Volume Horaire global du module (en heures)."
)


def build_module_entries():
    """Génère une fiche RAG par module (id, category, title, content)."""
    entries = []
    seen_ids = {}
    for filiere_code, fdata in FILIERES.items():
        for semestre, modules in fdata["semestres"].items():
            for intitule, elements in modules:
                base_id = f"module_{filiere_code.lower()}_{semestre.lower()}_{slugify(intitule)}"
                uid = base_id
                counter = 2
                while uid in seen_ids:
                    uid = f"{base_id}_{counter}"
                    counter += 1
                seen_ids[uid] = True

                vh_total = sum(e[6] for e in elements)

                lines = []
                lines.append(f"Module : {intitule}")
                lines.append(f"Filière : {fdata['nom_complet']} ({filiere_code})")
                lines.append(f"Semestre : {semestre}")
                if len(elements) == 1:
                    e = elements[0]
                    lines.append(
                        f"Volume horaire global : {e[6]}h "
                        f"(Cours: {e[1]}h, TD: {e[2]}h, TP: {e[3]}h, AP: {e[4]}h, Evaluations: {e[5]}h)"
                    )
                else:
                    lines.append(
                        f"Volume horaire global du module : {vh_total}h, "
                        f"reparti en {len(elements)} elements :"
                    )
                    for e in elements:
                        lines.append(
                            f"  - {e[0]} : {e[6]}h "
                            f"(Cours: {e[1]}h, TD: {e[2]}h, TP: {e[3]}h, AP: {e[4]}h, Evaluations: {e[5]}h)"
                        )
                lines.append(f"Legende : {VHG_LEGEND}")
                lines.append("Source : Plan de filiere officiel ENIAD (programme 2025-2026).")
                lines.append(
                    "Note : Prof. responsable non communique dans le plan de filiere "
                    "— voir emploi du temps ou contacter la scolarite pour l'enseignant assigne cette annee."
                )

                entries.append({
                    "id": uid,
                    "category": "module",
                    "title": f"{intitule} — {filiere_code} {semestre}",
                    "content": "\n".join(lines),
                })
    return entries


def build_synthese_entries():
    """Une fiche de synthèse par filière+semestre (utile pour 'quels modules en S6 IA ?')."""
    entries = []
    for filiere_code, fdata in FILIERES.items():
        for semestre, modules in fdata["semestres"].items():
            uid = f"synthese_{filiere_code.lower()}_{semestre.lower()}"
            intitules = [m[0] for m in modules]
            vh_total = sum(sum(e[6] for e in m[1]) for m in modules)
            lines = []
            lines.append(f"Filière : {fdata['nom_complet']} ({filiere_code}) — Semestre {semestre}")
            lines.append(f"Nombre de modules : {len(intitules)}")
            lines.append(f"Volume horaire global du semestre : {vh_total}h")
            lines.append("Liste des modules :")
            for i in intitules:
                lines.append(f"  - {i}")
            lines.append("Source : Plan de filiere officiel ENIAD (programme 2025-2026).")
            entries.append({
                "id": uid,
                "category": "synthese_semestre",
                "title": f"Modules {filiere_code} {semestre}",
                "content": "\n".join(lines),
            })
    return entries


# Liste combinée prête pour le RAG
ALL_MODULE_ENTRIES = build_module_entries() + build_synthese_entries()


if __name__ == "__main__":
    mods = build_module_entries()
    syns = build_synthese_entries()
    print(f"Total fiches modules    : {len(mods)}")
    print(f"Total fiches synthese   : {len(syns)}")
    print(f"Total entrees RAG       : {len(mods) + len(syns)}")
