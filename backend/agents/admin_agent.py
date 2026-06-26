"""
Agent Admin — SmartStudent LangGraph ReAct Agent
Architecture: agent_node <-> tools_node loop (ReAct pattern)
Outils: recuperer_profil, recuperer_notes, generer_document_pdf,
        verifier_statut, creer_demande, rechercher_rag
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# State
# ─────────────────────────────────────────────────────────────────────────────

class AdminAgentState(TypedDict, total=False):
    messages:     Annotated[list, add_messages]
    user_id:      int
    user_context: dict


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _db_session():
    from backend.database import get_db
    return next(get_db())


def _get_llm():
    from backend.agents.orchestrator import get_llm
    return get_llm()


# ─────────────────────────────────────────────────────────────────────────────
# Administrative support mapping + classifier tool
# ─────────────────────────────────────────────────────────────────────────────

ADMIN_SUPPORT_MAP = {

    # ── 1. Perte de la carte d'étudiant ──────────────────────────────────────
    "carte_perdue": {
        "title": "Duplicata de carte étudiant",
        "type": "Scolarité / document administratif",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 2,
        "keywords": [
            "carte", "perdu", "perdue", "duplicata", "carte etudiante",
            "carte etudiant", "perte carte", "carte perdue", "j'ai perdu ma carte",
            "renouveler carte", "nouvelle carte", "faire carte", "obtenir carte",
            "besoin carte", "carte volée", "carte abimée",
        ],
        "documents_requis": [
            "Copie de la CIN",
            "Photo d'identité récente (fond blanc)",
            "Formulaire de demande de duplicata (disponible au guichet)",
        ],
        "process": [
            "Préparer une copie de la CIN",
            "Préparer une photo d'identité récente",
            "Remplir le formulaire de demande de duplicata",
            "Déposer le dossier au Service Scolarité",
            "Récupérer le duplicata au guichet Scolarité",
        ],
        "delai_estime": "3 à 5 jours ouvrables",
        "resultat_attendu": "Nouvelle carte étudiant (duplicata) délivrée au guichet",
    },

    # ── 2. Changement de filière ──────────────────────────────────────────────
    "changement_filiere": {
        "title": "Changement de filière",
        "type": "Scolarité / académique",
        "service": "Chef de filière concerné + Service Scolarité",
        "responsable": "Chef de filière de la spécialité cible",
        "bureau": "Bureau de filière concerné + Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 1,
        "keywords": [
            "changement filiere", "changer filiere", "changement de filiere",
            "changer de filiere", "transfert filiere", "autre filiere",
            "filiere differente", "reinscription filiere",
        ],
        "chefs_filiere": {
            "Intelligence Artificielle": {
                "chef": "Pr. Ahmed Benali", "email": "ia.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 06", "bureau": "Bureau F101",
            },
            "Génie Informatique": {
                "chef": "Pr. Sara El Mansouri", "email": "gi.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 07", "bureau": "Bureau F102",
            },
            "Robotique": {
                "chef": "Pr. Hamza El Fassi", "email": "robotique.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 08", "bureau": "Bureau F103",
            },
            "Réseaux et Systèmes": {
                "chef": "Pr. Yassine Berrada", "email": "reseaux.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 09", "bureau": "Bureau F104",
            },
        },
        "documents_requis": [
            "Relevés de notes des semestres précédents",
            "Lettre de demande de changement motivée",
            "Copie de la CIN",
            "Dossier d'inscription initial",
        ],
        "process": [
            "Vérifier les conditions d'admission dans la filière cible (prérequis, places disponibles)",
            "Préparer votre lettre de demande de changement en indiquant les raisons",
            "Rencontrer le Chef de la filière cible pour validation préalable",
            "Déposer le dossier complet au Service Scolarité (Bureau A01)",
            "Attendre la décision du comité pédagogique",
        ],
        "delai_estime": "1 à 2 semaines (décision du comité)",
        "resultat_attendu": "Réponse officielle de l'administration (acceptation ou refus motivé)",
    },

    # ── 3. Attestation de scolarité ───────────────────────────────────────────
    "attestation": {
        "title": "Attestation de scolarité",
        "type": "Scolarité",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 3,
        "keywords": [
            "attestation", "attestation de scolarite", "attestation inscription",
            "preuve inscription", "justificatif scolarite",
            "besoin attestation", "obtenir attestation", "avoir attestation",
            "je veux attestation", "demande attestation", "comment avoir attestation",
        ],
        "documents_requis": [
            "Carte étudiant (ou CNE)",
            "Formulaire de demande (disponible au guichet ou via SmartStudent)",
        ],
        "process": [
            "Faire une demande en ligne via SmartStudent (onglet Documents) ou se rendre au guichet",
            "Fournir votre numéro de carte étudiant (CNE)",
            "Déposer la demande au Service Scolarité",
            "Récupérer l'attestation signée et cachetée sous 2 à 3 jours",
        ],
        "delai_estime": "2 à 3 jours ouvrables",
        "resultat_attendu": "Attestation de scolarité officielle signée et cachetée",
    },

    # ── 4. Relevé de notes ────────────────────────────────────────────────────
    "releve_notes": {
        "title": "Relevé de notes",
        "type": "Scolarité",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 3,
        "keywords": [
            "releve", "releve de notes", "bulletin", "notes officielles",
            "document notes", "historique notes", "transcript",
            "besoin releve", "obtenir releve", "avoir mes notes", "voir mes notes",
            "comment avoir releve", "je veux mes notes", "releve officiel",
        ],
        "documents_requis": [
            "Carte étudiant (à présenter au guichet)",
        ],
        "process": [
            "Se présenter au guichet du Service Scolarité avec votre carte étudiant",
            "Formuler votre demande de relevé de notes (préciser le semestre ou l'année)",
            "Récupérer le relevé officiel signé et cacheté",
        ],
        "delai_estime": "1 à 3 jours ouvrables",
        "resultat_attendu": "Relevé de notes officiel signé et cacheté par l'administration",
    },

    # ── 5. Problème de note ───────────────────────────────────────────────────
    "probleme_note": {
        "title": "Problème ou contestation de note",
        "type": "Pédagogique / Scolarité",
        "service": "Enseignant concerné → Chef de filière → Service Scolarité",
        "responsable": "Enseignant de la matière puis Chef de filière de votre spécialité",
        "bureau": "Bureau de l'enseignant puis Bureau de filière concerné",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 1,
        "keywords": [
            "probleme note", "erreur note", "note incorrecte", "mauvaise note",
            "note fausse", "contester note", "contestation", "note erronee",
            "note manquante", "note absente", "correction note",
            "ma note", "avec ma note", "probleme avec", "ma note de",
        ],
        "documents_requis": [
            "Copie de la note contestée (relevé ou capture ENT)",
            "Justificatif de présence à l'examen (si disponible)",
        ],
        "process": [
            "Contacter d'abord l'enseignant de la matière pour vérifier la note (erreur de saisie possible)",
            "Si l'erreur est confirmée, préparer une demande écrite de vérification",
            "Déposer la demande auprès du Chef de filière avec les justificatifs",
            "Le Chef de filière transmet au Service Scolarité pour correction officielle",
        ],
        "delai_estime": "3 à 7 jours ouvrables",
        "resultat_attendu": "Correction de la note dans le système ou réponse motivée",
    },

    # ── 6. Absence à un examen ────────────────────────────────────────────────
    "absence_examen": {
        "title": "Absence à un examen",
        "type": "Pédagogique / Affaires Estudiantines",
        "service": "Affaires Estudiantines",
        "responsable": "Meryem Chraibi",
        "bureau": "Bloc Administratif - Bureau A06",
        "email": "etudiant@eniad.ma",
        "telephone": "+212 5 36 00 10 05",
        "priorite": 1,
        "keywords": [
            "absent", "absence", "absence examen", "raté examen", "manque examen",
            "justifier absence", "justificatif", "examen rate", "examen manque",
        ],
        "documents_requis": [
            "Justificatif valide : certificat médical, convocation officielle, etc.",
            "Formulaire de déclaration d'absence (disponible au guichet)",
        ],
        "process": [
            "Rassembler un justificatif valide pour votre absence (certificat médical, etc.)",
            "Se présenter au Service Affaires Estudiantines dans les délais impartis",
            "Déposer le justificatif accompagné du formulaire de déclaration d'absence",
            "Attendre la décision sur la recevabilité du justificatif",
        ],
        "delai_estime": "Dépôt obligatoire dans les 72h suivant l'absence",
        "resultat_attendu": "Absence justifiée et droit à une session de rattrapage accordé si recevable",
    },

    # ── 7. Stage PFA / PFE ────────────────────────────────────────────────────
    "stage_pfa_pfe": {
        "title": "Stage PFA / PFE",
        "type": "Stages / Projets de Fin d'Études",
        "service": "Service Stages et Insertion",
        "responsable": "Khalid Tazi",
        "bureau": "Bloc Administratif - Bureau A05",
        "email": "stages@eniad.ma",
        "telephone": "+212 5 36 00 10 04",
        "priorite": 2,
        "keywords": [
            "pfe", "pfa", "projet fin", "fin d'etude", "stage fin",
            "memoire", "projet de fin", "stage pfa", "stage pfe",
            "encadrant", "sujet pfe", "sujet pfa", "soutenance",
            "comment faire pfe", "comment trouver stage", "valider pfa",
            "besoin encadrant", "cherche entreprise pfe", "rapport pfe",
        ],
        "documents_requis": [
            "Proposition de sujet validée par l'encadrant",
            "Lettre d'acceptation de l'entreprise",
            "Convention de stage signée",
            "Copie de la CIN",
        ],
        "process": [
            "Choisir une entreprise d'accueil et définir le sujet avec votre encadrant",
            "Faire valider le sujet par le Responsable des stages (M. Khalid Tazi)",
            "Déposer la convention de stage signée par toutes les parties",
            "Suivre les instructions de l'encadrant tout au long du projet",
        ],
        "delai_estime": "5 à 10 jours ouvrables pour validation",
        "resultat_attendu": "Stage PFA/PFE officiellement enregistré et convention validée",
    },

    # ── 8. Convention de stage ────────────────────────────────────────────────
    "convention_stage": {
        "title": "Convention de stage",
        "type": "Stages",
        "service": "Service Stages et Insertion",
        "responsable": "Khalid Tazi",
        "bureau": "Bloc Administratif - Bureau A05",
        "email": "stages@eniad.ma",
        "telephone": "+212 5 36 00 10 04",
        "priorite": 2,
        "keywords": [
            "convention", "convention de stage", "signer convention",
            "formulaire stage", "document stage", "convention signee",
            "besoin convention", "comment faire convention", "obtenir convention",
            "telecharger convention", "generer convention", "remplir convention",
        ],
        "documents_requis": [
            "Informations sur l'entreprise (nom, adresse, téléphone)",
            "Nom du tuteur en entreprise",
            "Dates de début et de fin de stage",
            "Sujet / poste de stage",
        ],
        "process": [
            "Télécharger la convention de stage via SmartStudent (onglet Documents) ou la demander au guichet",
            "Remplir la convention avec les informations de l'entreprise et du tuteur",
            "Faire signer la convention par l'entreprise, puis par votre encadrant pédagogique",
            "Déposer la convention signée au Service Stages (Bureau A05) pour validation finale",
        ],
        "delai_estime": "3 à 5 jours ouvrables",
        "resultat_attendu": "Convention de stage validée et enregistrée officiellement",
    },

    # ── 9. Accès plateforme pédagogique ──────────────────────────────────────
    "acces_plateforme": {
        "title": "Accès plateforme pédagogique",
        "type": "Informatique / Numérique",
        "service": "Service Informatique",
        "responsable": "Omar El Alaoui",
        "bureau": "Bloc Technique - Bureau IT01",
        "email": "support@eniad.ma",
        "telephone": "+212 5 36 00 10 03",
        "priorite": 2,
        "keywords": [
            "plateforme", "moodle", "e-learning", "ent", "portail",
            "acces plateforme", "connexion plateforme", "cours en ligne",
            "plateforme pedagogique", "compte plateforme", "identifiant plateforme",
            "besoin acces plateforme", "comment acceder plateforme", "comment se connecter moodle",
            "je peux pas me connecter", "acces cours", "mes cours en ligne",
        ],
        "documents_requis": [
            "Numéro de carte étudiant / matricule",
        ],
        "process": [
            "Vérifier vos identifiants de connexion (matricule + mot de passe par défaut)",
            "Essayer de réinitialiser le mot de passe via la page de récupération",
            "Si le problème persiste, contacter le Service Informatique",
            "Fournir votre matricule pour que le support rétablisse votre accès",
        ],
        "delai_estime": "1 à 2 jours ouvrables",
        "resultat_attendu": "Accès à la plateforme pédagogique rétabli",
    },

    # ── 10. Réinitialisation de mot de passe ─────────────────────────────────
    "reinitialisation_mdp": {
        "title": "Réinitialisation de mot de passe",
        "type": "Informatique / Numérique",
        "service": "Service Informatique",
        "responsable": "Omar El Alaoui",
        "bureau": "Bloc Technique - Bureau IT01",
        "email": "support@eniad.ma",
        "telephone": "+212 5 36 00 10 03",
        "priorite": 2,
        "keywords": [
            "mot de passe", "password", "reinitialisation", "réinitialisation",
            "oublié mot de passe", "reset password", "changer mot de passe",
            "compte bloque", "mdp oublie", "mdp",
            "j'ai oublie mon mot de passe", "je me souviens plus mon mdp",
            "reinitialiser compte", "recuperer compte", "mot de passe oublie",
            "comment changer mdp", "comment reinitialiser",
        ],
        "documents_requis": [
            "Numéro de carte étudiant / matricule",
            "Email académique (@eniad.ma) si disponible",
        ],
        "process": [
            "Utiliser la procédure de récupération de mot de passe sur la page de connexion",
            "Si aucun email de récupération n'est reçu, contacter le Service Informatique",
            "Présenter votre matricule pour vérification d'identité",
            "Le support réinitialisera votre mot de passe et vous communiquera les nouveaux identifiants",
        ],
        "delai_estime": "Quelques heures à 1 jour ouvrable",
        "resultat_attendu": "Mot de passe réinitialisé et accès rétabli",
    },

    # ── 11. Accès WiFi / réseau ───────────────────────────────────────────────
    "wifi": {
        "title": "Accès WiFi et connexion réseau",
        "type": "Informatique / Infrastructure",
        "service": "Service Informatique",
        "responsable": "Omar El Alaoui",
        "bureau": "Bloc Technique - Bureau IT01",
        "email": "support@eniad.ma",
        "telephone": "+212 5 36 00 10 03",
        "priorite": 2,
        "keywords": [
            "wifi", "wi-fi", "réseau", "reseau", "internet",
            "connexion internet", "connexion reseau", "connexion wifi",
            "besoin wifi", "besoin internet", "besoin reseau",
            "point d'acces", "point d'accès", "acces wifi", "acceder wifi",
            "comment se connecter", "comment acceder", "comment acceder au wifi",
            "identifiants wifi", "mot de passe wifi", "mdp wifi",
            "internet ne marche pas", "pas de wifi", "probleme wifi",
            "probleme internet", "signal faible", "deconnexion",
            "pas de connexion", "pas internet", "reseau campus",
        ],
        "documents_requis": [
            "Matricule étudiant (votre numéro d'identifiant ENIAD)",
        ],
        "process": [
            "Connectez-vous au réseau WiFi nommé 'ENIAD-Wifi' sur votre appareil",
            "Utilisez vos identifiants : matricule étudiant + mot de passe par défaut communiqué lors de l'inscription",
            "Si c'est votre première connexion ou que vous avez oublié le mot de passe : contacter le Service Informatique",
            "En cas de problème persistant (signal faible, coupure) : préciser la zone du campus et signaler au support",
        ],
        "delai_estime": "Accès immédiat avec les bons identifiants — ou 1 à 2 jours si intervention technique requise",
        "resultat_attendu": "Connexion WiFi fonctionnelle au réseau ENIAD",
    },

    # ── 12. Bourse ────────────────────────────────────────────────────────────
    "bourse": {
        "title": "Bourse d'études",
        "type": "Affaires Estudiantines / Social",
        "service": "Affaires Estudiantines",
        "responsable": "Meryem Chraibi",
        "bureau": "Bloc Administratif - Bureau A06",
        "email": "etudiant@eniad.ma",
        "telephone": "+212 5 36 00 10 05",
        "priorite": 2,
        "keywords": [
            "bourse", "aide financiere", "aide sociale", "aide etudiant",
            "demande bourse", "bourse etude", "allocation",
            "besoin aide financiere", "comment avoir bourse", "je veux bourse",
            "obtenir bourse", "eligible bourse", "soutien financier",
        ],
        "documents_requis": [
            "Copie de la CIN",
            "Justificatif de revenus familiaux",
            "Attestation de scolarité en cours",
            "Formulaire de demande de bourse (disponible au guichet)",
        ],
        "process": [
            "Vérifier votre éligibilité aux critères de la bourse (revenus, résultats, etc.)",
            "Rassembler tous les documents justificatifs demandés",
            "Déposer le dossier complet au Service Affaires Estudiantines (Bureau A06)",
            "Attendre la décision de la commission d'attribution",
        ],
        "delai_estime": "2 à 4 semaines (décision de commission)",
        "resultat_attendu": "Décision d'attribution ou de refus de bourse notifiée officiellement",
    },

    # ── 13. Participation à un événement ─────────────────────────────────────
    "participation_evenement": {
        "title": "Participation à un événement étudiant",
        "type": "Vie Étudiante",
        "service": "Affaires Estudiantines",
        "responsable": "Meryem Chraibi",
        "bureau": "Bloc Administratif - Bureau A06",
        "email": "etudiant@eniad.ma",
        "telephone": "+212 5 36 00 10 05",
        "priorite": 3,
        "keywords": [
            "evenement", "événement", "inscription evenement", "participer",
            "club", "conference", "workshop", "activite", "concours",
            "hackathon", "seminaire", "forum", "sortie",
        ],
        "documents_requis": [
            "Formulaire d'inscription à l'événement (en ligne ou au guichet)",
            "Carte étudiant (certains événements l'exigent)",
        ],
        "process": [
            "Vérifier les conditions de participation et les dates de l'événement",
            "Remplir le formulaire d'inscription en ligne ou auprès du Service Affaires Estudiantines",
            "Confirmer votre inscription et conserver le récépissé ou la confirmation",
            "Se présenter à l'événement avec votre carte étudiant",
        ],
        "delai_estime": "Inscription à effectuer avant la date limite de l'événement",
        "resultat_attendu": "Inscription confirmée et participation validée à l'événement",
    },

    # ── 14. Demande de certificat ─────────────────────────────────────────────
    "certificat": {
        "title": "Demande de certificat",
        "type": "Scolarité / Documents officiels",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 3,
        "keywords": [
            "certificat", "demande certificat", "certificat etudiant",
            "certificat scolarite", "certificat inscription", "document officiel",
        ],
        "documents_requis": [
            "Copie de la CIN",
            "Formulaire de demande de certificat (disponible au guichet)",
            "Justificatif d'utilisation du certificat (si requis)",
        ],
        "process": [
            "Préparer les pièces justificatives nécessaires",
            "Se rendre au Service Scolarité ou faire la demande en ligne via SmartStudent",
            "Remplir et déposer le formulaire de demande de certificat",
            "Récupérer le certificat signé et cacheté au guichet",
        ],
        "delai_estime": "2 à 4 jours ouvrables",
        "resultat_attendu": "Certificat officiel signé et cacheté délivré",
    },

    # ── 15. Retrait du diplôme ────────────────────────────────────────────────
    "retrait_diplome": {
        "title": "Retrait du diplôme",
        "type": "Scolarité / Diplomation",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 2,
        "keywords": [
            "diplome", "diplôme", "retrait diplome", "recuperer diplome",
            "diplome pret", "graduation", "fin etude diplome",
        ],
        "documents_requis": [
            "Copie de la CIN",
            "Carte étudiant",
            "Quitus (attestation de non-dette envers l'établissement)",
            "Reçu de paiement des frais de scolarité soldés",
        ],
        "process": [
            "Vérifier que toutes les conditions sont remplies : tous les modules validés, aucune dette administrative",
            "Obtenir le quitus auprès de chaque service concerné (bibliothèque, scolarité, etc.)",
            "Prendre rendez-vous au Service Scolarité si une convocation est nécessaire",
            "Se présenter avec l'ensemble des documents requis pour le retrait officiel",
        ],
        "delai_estime": "Variable selon la disponibilité des diplômes (entre 1 et 6 mois après fin d'études)",
        "resultat_attendu": "Diplôme officiel remis en main propre",
    },

    # ── 16. Contact des chefs de filière ──────────────────────────────────────
    "chef_filiere_contact": {
        "title": "Contact des Chefs de Filière",
        "type": "Contact académique",
        "service": "Chefs de Filière ENIAD",
        "responsable": "Chefs de Filière",
        "bureau": "Blocs Pédagogiques",
        "keywords": [
            "chef filiere", "chef de filiere", "chef filière", "chef de filière",
            "contact chef", "contacter chef", "chef ia", "chef gi", "chef robotique",
            "chef reseaux", "chef réseau", "responsable filiere", "responsable filière",
            "email chef", "coordonnees chef", "coordonnées chef",
            "pr ahmed", "pr sara", "pr hamza", "pr yassine",
            "ahmed benali", "sara el mansouri", "hamza el fassi", "yassine berrada",
        ],
        "chefs_filiere": {
            "Intelligence Artificielle": {
                "chef": "Pr. Ahmed Benali",
                "email": "ia.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 06",
                "bureau": "Bureau F101",
            },
            "Génie Informatique": {
                "chef": "Pr. Sara El Mansouri",
                "email": "gi.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 07",
                "bureau": "Bureau F102",
            },
            "Robotique": {
                "chef": "Pr. Hamza El Fassi",
                "email": "robotique.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 08",
                "bureau": "Bureau F103",
            },
            "Réseaux et Systèmes": {
                "chef": "Pr. Yassine Berrada",
                "email": "reseaux.chef@eniad.ma",
                "telephone": "+212 5 36 00 10 09",
                "bureau": "Bureau F104",
            },
        },
        "documents_requis": [],
        "process": [],
        "delai_estime": "",
        "resultat_attendu": "",
    },

    # ── 17. Réinscription annuelle ────────────────────────────────────────────
    "reinscription": {
        "title": "Réinscription annuelle",
        "type": "Scolarité / Administratif",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 2,
        "keywords": [
            "reinscription", "re-inscription", "inscrire nouvelle annee",
            "renouveler inscription", "dossier reinscription", "annee suivante",
            "me reinscrire", "renouvellement", "nouvelle annee scolaire",
        ],
        "documents_requis": [
            "Relevé de notes de l'année précédente (ou PV de délibération)",
            "Reçu de paiement des frais de scolarité",
            "2 photos d'identité récentes (fond blanc)",
            "Copie de la CIN",
            "Formulaire de réinscription (disponible au Bureau A01 ou sur SmartStudent)",
        ],
        "process": [
            "Vérifier votre situation académique (modules validés, passage en année supérieure)",
            "Payer les frais de scolarité au Service Finances (Bureau A03) avant la date limite",
            "Retirer et remplir le formulaire de réinscription au Bureau A01",
            "Déposer le dossier complet avec tous les documents requis",
            "Récupérer la nouvelle carte étudiant et le certificat de réinscription",
            "Activer votre accès à la plateforme pédagogique avec vos nouveaux identifiants",
        ],
        "delai_estime": "Traitement immédiat si dossier complet (avant la date limite de rentrée)",
        "resultat_attendu": "Réinscription validée, nouvelle carte étudiant et accès aux services rétablis",
    },

    # ── 18. Congé académique ──────────────────────────────────────────────────
    "conge_academique": {
        "title": "Congé académique (suspension d'études)",
        "type": "Scolarité / Administratif",
        "service": "Service Scolarité",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 1,
        "keywords": [
            "conge academique", "suspension etudes", "arret etudes", "pause etudes",
            "interrompre etudes", "reprendre etudes", "cesser cours", "conge scolaire",
        ],
        "documents_requis": [
            "Demande écrite adressée au Directeur de l'ENIAD",
            "Justificatif de la raison du congé (certificat médical, convocation, etc.)",
            "Copie de la CIN",
            "Dernier relevé de notes",
        ],
        "process": [
            "Rédiger une demande écrite adressée au Directeur, expliquant clairement les raisons",
            "Joindre les justificatifs nécessaires (certificat médical, convocation, etc.)",
            "Déposer le dossier au Service Scolarité (Bureau A01)",
            "Attendre la décision de la direction (un entretien peut être requis)",
            "En cas d'accord : inscription suspendue jusqu'à la date de reprise convenue",
            "À la date de reprise : effectuer la réinscription normalement au Bureau A01",
        ],
        "delai_estime": "1 à 2 semaines (décision de la direction)",
        "resultat_attendu": "Congé académique accordé, dossier mis en suspens jusqu'à la reprise",
    },

    # ── 19. Équivalence de module ─────────────────────────────────────────────
    "equivalence_module": {
        "title": "Demande d'équivalence de module",
        "type": "Pédagogique / Scolarité",
        "service": "Chef de filière + Service Scolarité",
        "responsable": "Chef de filière concerné",
        "bureau": "Bureau de filière puis Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 2,
        "keywords": [
            "equivalence", "equivalent", "module valide", "reconnaissance module",
            "transfert module", "credits transfert", "validation acquis", "module etranger",
        ],
        "documents_requis": [
            "Relevés de notes officiels de l'établissement d'origine",
            "Syllabus détaillés des modules pour lesquels une équivalence est demandée",
            "Diplôme ou attestation de réussite de l'établissement d'origine",
            "Formulaire de demande d'équivalence (Service Scolarité)",
            "Copie de la CIN",
        ],
        "process": [
            "Préparer les syllabus des modules pour lesquels vous souhaitez une équivalence",
            "Se renseigner auprès du Chef de votre filière sur les critères d'équivalence",
            "Déposer le dossier complet au Service Scolarité (Bureau A01)",
            "Le comité pédagogique étudie les équivalences possibles",
            "Recevoir la décision officielle par voie administrative",
        ],
        "delai_estime": "2 à 4 semaines (étude du dossier par le comité pédagogique)",
        "resultat_attendu": "Validation des équivalences accordées ou refus motivé",
    },

    # ── 20. Emploi du temps ───────────────────────────────────────────────────
    "emploi_temps": {
        "title": "Emploi du temps / Planning des cours",
        "type": "Pédagogique",
        "service": "Secrétariat pédagogique / Chef de filière",
        "responsable": "Chef de votre filière",
        "bureau": "Bureau de votre filière",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 3,
        "keywords": [
            "emploi du temps", "planning cours", "edt", "chevauchement cours",
            "salle cours", "horaire cours", "programme semaine", "calendrier cours",
            "cours annule", "modification cours",
        ],
        "documents_requis": [],
        "process": [
            "Consulter l'emploi du temps sur la plateforme pédagogique (Moodle/ENT) ou le tableau d'affichage",
            "En cas de chevauchement ou d'erreur, contacter le Secrétariat ou votre Chef de filière",
            "Signaler le problème par email en précisant votre promo, groupe et les cours concernés",
            "Attendre la correction et la republication de l'emploi du temps",
        ],
        "delai_estime": "1 à 3 jours ouvrables pour correction",
        "resultat_attendu": "Emploi du temps mis à jour et accessible",
    },

    # ── 21. Programme des examens ─────────────────────────────────────────────
    "programme_examens": {
        "title": "Calendrier des examens",
        "type": "Pédagogique / Scolarité",
        "service": "Service Scolarité / Chef de filière",
        "responsable": "Fatima Zahra El Idrissi",
        "bureau": "Bloc Administratif - Bureau A01",
        "email": "scolarite@eniad.ma",
        "telephone": "+212 5 36 00 10 01",
        "horaires": "08:30 - 16:30",
        "priorite": 3,
        "keywords": [
            "examen", "calendrier examens", "planning examens", "date examen",
            "programme examens", "session examen", "partiel", "final semestre",
            "salle examen", "convocation examen", "rattrapage examen",
        ],
        "documents_requis": [],
        "process": [
            "Consulter la plateforme pédagogique (Moodle/ENT) dans la rubrique 'Examens'",
            "Consulter le tableau d'affichage du Bloc Administratif",
            "En cas d'absence du programme ou d'erreur, contacter le Service Scolarité ou le Chef de filière",
            "Le calendrier S1 est publié en décembre, le S2 en mai — environ 2-3 semaines avant",
        ],
        "delai_estime": "Publié 2 à 3 semaines avant les examens",
        "resultat_attendu": "Programme des examens disponible sur plateforme et tableau d'affichage",
    },

    # ── 22. Bibliothèque ──────────────────────────────────────────────────────
    "bibliotheque": {
        "title": "Bibliothèque — accès et prêt d'ouvrages",
        "type": "Ressources Documentaires",
        "service": "Bibliothèque / Médiathèque",
        "responsable": "Nadia Amrani",
        "bureau": "Bloc Pédagogique - Rez-de-chaussée",
        "email": "bibliotheque@eniad.ma",
        "telephone": "+212 5 36 00 10 10",
        "horaires": "08:00 - 18:00 (Lun-Ven) | 09:00 - 13:00 (Sam)",
        "priorite": 3,
        "keywords": [
            "bibliotheque", "livre", "ouvrage", "emprunter", "pret livre",
            "ressource documentaire", "these", "revue", "mediatheque",
            "acces bibliotheque", "carte bibliotheque", "rendre livre",
        ],
        "documents_requis": [
            "Carte étudiant en cours de validité",
            "Formulaire d'adhésion (première visite uniquement)",
        ],
        "process": [
            "Se présenter à la bibliothèque (Bloc Pédagogique, RDC) avec la carte étudiant",
            "S'inscrire lors de la première visite (formulaire d'adhésion rapide)",
            "Rechercher les ouvrages via le catalogue ou demander assistance au bibliothécaire",
            "Emprunter jusqu'à 3 ouvrages à la fois pour une durée de 2 semaines (renouvelable)",
            "Retourner les ouvrages à temps pour éviter les pénalités",
        ],
        "delai_estime": "Accès immédiat sur présentation de la carte étudiant",
        "resultat_attendu": "Accès aux ressources documentaires et prêt d'ouvrages",
    },

    # ── 23. Paiement des frais de scolarité ───────────────────────────────────
    "paiement_frais": {
        "title": "Paiement des frais de scolarité",
        "type": "Finances / Administratif",
        "service": "Service des Finances",
        "responsable": "Hassan El Ouazzani",
        "bureau": "Bloc Administratif - Bureau A03",
        "email": "finances@eniad.ma",
        "telephone": "+212 5 36 00 10 11",
        "horaires": "08:30 - 15:30 (Lundi - Vendredi)",
        "priorite": 2,
        "keywords": [
            "frais scolarite", "paiement", "payer", "recu paiement", "acquittement",
            "dette financiere", "quitus financier", "frais inscription", "regler frais",
        ],
        "documents_requis": [
            "Copie de la CIN",
            "Formulaire de réinscription (si applicable)",
            "Moyen de paiement (espèces, chèque ou virement bancaire)",
        ],
        "process": [
            "Se renseigner sur le montant exact des frais auprès du Service Finances (Bureau A03)",
            "Effectuer le paiement selon les modalités acceptées (espèces, chèque, virement)",
            "Obtenir et conserver le reçu de paiement officiel",
            "Présenter le reçu lors de la réinscription au Service Scolarité",
        ],
        "delai_estime": "Paiement immédiat au guichet — avant la date limite d'inscription",
        "resultat_attendu": "Reçu de paiement délivré et accès aux services académiques validé",
    },

    # ── 24. Mobilité internationale ────────────────────────────────────────────
    "mobilite_internationale": {
        "title": "Mobilité internationale / Erasmus+",
        "type": "Relations Internationales",
        "service": "Bureau Relations Internationales",
        "responsable": "Leila Benhaddou",
        "bureau": "Bloc Administratif - Bureau A07",
        "email": "ri@eniad.ma",
        "telephone": "+212 5 36 00 10 12",
        "horaires": "09:00 - 16:00 (Lundi - Vendredi)",
        "priorite": 2,
        "keywords": [
            "mobilite internationale", "erasmus", "echange etudiant",
            "universite etrangere", "stage etranger", "bourse internationale",
            "programme echange", "double diplome", "visa etudes", "partir etranger",
        ],
        "documents_requis": [
            "Relevés de notes des deux dernières années",
            "Lettre de motivation (en français et/ou langue du pays cible)",
            "Curriculum Vitae",
            "Passeport en cours de validité",
            "Attestation de niveau de langue si requise",
            "Formulaire de candidature (disponible au Bureau A07)",
        ],
        "process": [
            "Consulter les offres de mobilité disponibles auprès du Bureau RI (Bureau A07)",
            "Vérifier les conditions d'éligibilité (année d'études, niveau académique, langue)",
            "Préparer et déposer le dossier de candidature avant la date limite",
            "Passer les entretiens de sélection si requis",
            "En cas de sélection : préparer visa, logement et formalités administratives avec le Bureau RI",
            "Faire valider les équivalences de modules avec le Chef de filière avant le départ",
        ],
        "delai_estime": "3 à 6 mois avant le départ (processus de sélection compris)",
        "resultat_attendu": "Place dans le programme d'échange confirmée et préparation administrative complète",
    },

    # ── 25. Réclamation administrative ─────────────────────────────────────────
    "reclamation_admin": {
        "title": "Réclamation administrative",
        "type": "Réclamations",
        "service": "Service Réclamations",
        "responsable": "Salma Benjelloun",
        "bureau": "Bloc Administratif - Bureau A02",
        "email": "reclamations@eniad.ma",
        "telephone": "+212 5 36 00 10 02",
        "horaires": "08:30 - 16:30",
        "priorite": 1,
        "keywords": [
            "reclamation", "reclamation administrative", "appel decision",
            "recours", "mediation", "contester decision", "signalement probleme",
            "erreur administrative", "litige administratif",
        ],
        "documents_requis": [
            "Description écrite et détaillée du problème",
            "Pièces justificatives (documents, courriers, captures d'écran)",
            "Copie de la CIN",
            "Formulaire de réclamation (disponible au Bureau A02)",
        ],
        "process": [
            "Tenter d'abord une résolution directe avec le service concerné",
            "Rassembler tous les documents justifiant votre réclamation",
            "Remplir le formulaire de réclamation et le déposer au Bureau A02",
            "Conserver une copie complète de votre dossier",
            "Attendre la prise de contact du Service Réclamations",
            "Recevoir la réponse officielle ou participer à une médiation si nécessaire",
        ],
        "delai_estime": "5 à 10 jours ouvrables",
        "resultat_attendu": "Réponse officielle et résolution du problème soulevé",
    },
}


@tool
def oriente_support_admin(user_message: str, user_id: int = 0) -> str:
    """Classifie le problème rapporté et retourne le service, responsable, actions et processus.

    Retourne une string JSON structurée : {success, key, title, type, service, responsable, actions, process, final}
    """
    try:
        text = (user_message or "").lower()

        # Score matching by keyword occurrences
        scores = {}
        for key, info in ADMIN_SUPPORT_MAP.items():
            score = 0
            for kw in info.get("keywords", []):
                if kw in text:
                    score += 1
            scores[key] = score

        # Choose best match
        best_key = max(scores, key=lambda k: scores[k])
        if scores[best_key] == 0:
            # Fallback par mots simples
            if any(w in text for w in ["carte", "perdu", "perdue", "duplicata"]):
                best_key = "carte_perdue"
            elif any(w in text for w in ["filiere", "filière", "changer filiere", "transfert filiere"]):
                best_key = "changement_filiere"
            elif any(w in text for w in ["attestation", "attestation scolarite"]):
                best_key = "attestation"
            elif any(w in text for w in ["releve", "bulletin"]):
                best_key = "releve_notes"
            elif any(w in text for w in ["note", "notes", "notation", "ma note"]):
                best_key = "probleme_note"
            elif any(w in text for w in ["absent", "absence", "justificatif", "rate examen", "rattrapage"]):
                best_key = "absence_examen"
            elif any(w in text for w in ["pfe", "pfa", "fin d'etude", "memoire", "projet fin", "soutenance"]):
                best_key = "stage_pfa_pfe"
            elif any(w in text for w in ["convention", "signer convention"]):
                best_key = "convention_stage"
            elif any(w in text for w in ["plateforme", "moodle", "ent", "portail"]):
                best_key = "acces_plateforme"
            elif any(w in text for w in ["mot de passe", "password", "mdp", "reinitialisation", "oublie"]):
                best_key = "reinitialisation_mdp"
            elif any(w in text for w in ["wifi", "wi-fi", "internet", "reseau", "connexion", "point d'acces", "se connecter au", "acces wifi"]):
                best_key = "wifi"
            elif any(w in text for w in ["bourse", "aide financiere", "aide sociale", "allocation"]):
                best_key = "bourse"
            elif any(w in text for w in ["evenement", "club", "participer", "hackathon", "conference", "workshop"]):
                best_key = "participation_evenement"
            elif any(w in text for w in ["certificat"]):
                best_key = "certificat"
            elif any(w in text for w in ["diplome", "diplôme", "retrait diplome"]):
                best_key = "retrait_diplome"
            elif any(w in text for w in ["reinscription", "re-inscription", "nouvelle annee", "renouveler"]):
                best_key = "reinscription"
            elif any(w in text for w in ["conge", "suspension", "interrompre", "pause etude"]):
                best_key = "conge_academique"
            elif any(w in text for w in ["equivalence", "equivalent", "valider module"]):
                best_key = "equivalence_module"
            elif any(w in text for w in ["emploi du temps", "edt", "planning cours", "horaire cours"]):
                best_key = "emploi_temps"
            elif any(w in text for w in ["examen", "partiel", "date examen", "calendrier examen"]):
                best_key = "programme_examens"
            elif any(w in text for w in ["bibliotheque", "livre", "emprunter", "mediatheque"]):
                best_key = "bibliotheque"
            elif any(w in text for w in ["frais", "payer", "paiement", "quitus financier"]):
                best_key = "paiement_frais"
            elif any(w in text for w in ["mobilite", "erasmus", "echange international", "etranger"]):
                best_key = "mobilite_internationale"
            elif any(w in text for w in ["reclamation", "plainte", "contester decision", "appel"]):
                best_key = "reclamation_admin"
            elif any(w in text for w in ["stage", "encadrant", "entreprise"]):
                best_key = "convention_stage"
            else:
                return json.dumps({
                    "success": False,
                    "message": (
                        "Je n'ai pas pu identifier précisément votre situation. "
                        "Pouvez-vous préciser votre demande ? Exemples : "
                        "'perte de carte', 'problème WiFi', 'changement de filière', "
                        "'attestation de scolarité', 'relevé de notes', 'stage PFA/PFE', "
                        "'convention de stage', 'problème de note', 'bourse', "
                        "'réinscription', 'bibliothèque', 'frais de scolarité', 'Erasmus'..."
                    )
                }, ensure_ascii=False)

        info = ADMIN_SUPPORT_MAP[best_key]

        # Build final guided message — étapes + contact uniquement
        process = info.get("process", [])
        steps_txt = "\n".join(f"{i}. {s}" for i, s in enumerate(process, 1)) if process else ""

        contact_lines = [f"**{info['service']}**"]
        contact_lines.append(f"• {info['responsable']}")
        if info.get("email"):
            contact_lines.append(f"• {info['email']}")
        if info.get("telephone"):
            contact_lines.append(f"• {info['telephone']}")
        if info.get("bureau"):
            contact_lines.append(f"• {info['bureau']}")
        if info.get("horaires"):
            contact_lines.append(f"• {info['horaires']}")
        contact_block = "\n".join(contact_lines)

        parts = [f"**{info['title']}**"]
        if steps_txt:
            parts.append(f"**Étapes :**\n{steps_txt}")
        parts.append(contact_block)
        final = "\n\n".join(parts)

        return json.dumps({
            "success": True,
            "key": best_key,
            "title": info["title"],
            "type": info["type"],
            "service": info["service"],
            "responsable": info["responsable"],
            "bureau": info.get("bureau", ""),
            "email": info.get("email", ""),
            "telephone": info.get("telephone", ""),
            "priorite": info.get("priorite", 2),
            "documents_requis": info.get("documents_requis", []),
            "process": info.get("process", []),
            "delai_estime": info.get("delai_estime", ""),
            "resultat_attendu": info.get("resultat_attendu", ""),
            "final": final,
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"oriente_support_admin error: {e}")
        return json.dumps({"success": False, "message": str(e)}, ensure_ascii=False)



# ─────────────────────────────────────────────────────────────────────────────
# Tools — actions réelles sur la BD et génération PDF
# ─────────────────────────────────────────────────────────────────────────────

@tool
def recuperer_profil_etudiant(user_id: int) -> str:
    """Recupere les informations completes de l'etudiant depuis la base de donnees: nom, email, filiere, annee, matricule, statut."""
    try:
        from backend.models import User, UserProfile
        db = _db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return f"Aucun etudiant trouve avec l'ID {user_id}."

            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

            info = {
                "id": user.id,
                "nom_complet": user.full_name or user.username,
                "email": user.email,
                "username": user.username,
                "filiere": profile.major if profile else "Non renseignee",
                "annee": profile.year if profile else None,
                "universite": profile.university if profile else "ENIAD",
                "telephone": profile.phone if profile else None,
                "statut": "Actif" if user.is_active else "Inactif",
            }
            return json.dumps(info, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"recuperer_profil_etudiant error: {e}")
        return f"Erreur lors de la recuperation du profil: {e}"


@tool
def generer_document_pdf(
    doc_type: str,
    user_id: int,
    entreprise: str = "",
    adresse_entreprise: str = "",
    telephone: str = "",
    fax: str = "",
    tuteur: str = "",
    poste: str = "",
    date_debut: str = "",
    date_fin: str = "",
) -> str:
    """Genere un document PDF officiel et l'enregistre en base de donnees.

    TYPES AUTORISES (3 uniquement — tout autre type est refuse):
      - 'Attestation de scolarite' : certifie l'inscription de l'etudiant (identite + filiere uniquement)
      - 'Convention de stage'      : accord tripartite ENIAD / etudiant / entreprise (infos stage uniquement)
      - "Reglement de l'ecole"     : reglement interieur officiel ENIAD (document statique)

    Pour 'Convention de stage', fournir: entreprise, adresse_entreprise, telephone, fax, tuteur, poste, date_debut, date_fin.
    Ces champs sont IGNORES pour les autres types de documents.

    INTERDIT: ne jamais passer 'Releve de notes', 'Certificat de stage' ou tout autre type.
    """
    from backend.agents.documents_agent import ALLOWED_DOC_TYPES, resolve_doc_type

    # ── 1. Validate doc_type against the strict whitelist ────────────────────
    try:
        canonical = resolve_doc_type(doc_type)
    except ValueError:
        return json.dumps({
            "success": False,
            "error": (
                f"Type de document '{doc_type}' non autorise. "
                f"Types valides: {', '.join(ALLOWED_DOC_TYPES)}"
            ),
        }, ensure_ascii=False)

    try:
        from backend.models import User, UserProfile, AdminRequest
        from backend.agents.documents_agent import get_documents_agent

        db = _db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return f"Etudiant introuvable (ID: {user_id})."

            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            full_name = user.full_name or user.username or ""
            parts = full_name.split()
            first = user.first_name or (parts[0] if parts else "")
            last  = user.last_name  or (" ".join(parts[1:]) if len(parts) > 1 else "")

            # ── 2. Build per-document data — no cross-module contamination ───
            # Identity fields shared by all documents
            base_data = {
                "full_name":       full_name,
                "first_name":      first,
                "last_name":       last,
                "student_id":      str(user_id),
                "student_card_id": (profile.student_card_id if profile else None) or str(user_id),
                "email":           user.email or "",
                "major":           (profile.major if profile else None) or "Genie Informatique",
                "year":            (profile.year if profile else None) or 3,
                "phone":           (profile.phone if profile else None) or "",
                "cne":             getattr(profile, "cne", None) or "" if profile else "",
                "cin":             getattr(profile, "cin", None) or "" if profile else "",
                "date_naissance":  getattr(profile, "date_naissance", None) or "" if profile else "",
            }

            # Convention de stage: add internship fields only for this type
            if canonical == "Convention de stage":
                base_data.update({
                    "entreprise":         entreprise or "________________",
                    "adresse_entreprise": adresse_entreprise or "________________",
                    "telephone":          telephone or "",
                    "fax":                fax or "",
                    "tuteur":             tuteur or "________________",
                    "poste":              poste or "Stage de fin d'etudes",
                    "date_debut":         date_debut or "________________",
                    "date_fin":           date_fin or "________________",
                })
            # Reglement and Attestation receive no extra fields — their generators
            # are static or identity-only by design.

            doc_id, _ = get_documents_agent().generate(canonical, base_data)

            req_id = str(uuid.uuid4())
            req = AdminRequest(
                id=req_id,
                user_id=user_id,
                request_type=canonical,
                status="validated",
                description=f"Genere par AdminAgent - {canonical}",
                doc_id=doc_id,
            )
            db.add(req)
            db.commit()

            return json.dumps({
                "success": True,
                "doc_id": doc_id,
                "request_id": req_id,
                "doc_type": canonical,
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"generer_document_pdf error: {e}")
        return f"Erreur lors de la generation du document: {e}"


@tool
def verifier_statut_demandes(user_id: int) -> str:
    """Consulte le statut reel de toutes les demandes administratives de l'etudiant depuis la base de donnees."""
    try:
        from backend.models import AdminRequest
        db = _db_session()
        try:
            _LABELS = {
                "pending": "En attente", "in_progress": "En cours",
                "validated": "Validee", "refused": "Refusee",
            }

            requests = (
                db.query(AdminRequest)
                .filter(AdminRequest.user_id == user_id)
                .order_by(AdminRequest.created_at.desc())
                .limit(10)
                .all()
            )

            if not requests:
                return "Aucune demande administrative trouvee pour cet etudiant."

            result = {
                "demandes": [
                    {
                        "id": r.id[:8],
                        "type": r.request_type,
                        "statut": _LABELS.get(r.status, r.status),
                        "date": r.created_at.strftime("%d/%m/%Y"),
                        "doc_disponible": r.doc_id is not None,
                    }
                    for r in requests
                ],
            }
            return json.dumps(result, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"verifier_statut_demandes error: {e}")
        return f"Erreur lors de la consultation: {e}"


@tool
def creer_demande_administrative(user_id: int, type_demande: str, description: str) -> str:
    """Cree une demande administrative formelle en base de donnees (sans PDF immediat).
    Utiliser pour: redoublement, equivalence, transfert, ou toute demande necessitant traitement manuel par le secretariat."""
    try:
        from backend.models import AdminRequest
        db = _db_session()
        try:
            req_id = str(uuid.uuid4())
            req = AdminRequest(
                id=req_id,
                user_id=user_id,
                request_type=type_demande,
                status="pending",
                description=description[:1000],
            )
            db.add(req)
            db.commit()

            return json.dumps({
                "success": True,
                "request_id": req_id[:8],
                "type": type_demande,
                "statut": "En attente",
                "message": (
                    f"Demande '{type_demande}' enregistree avec succes.\n"
                    f"- Reference: {req_id[:8]}\n"
                    "- Traitement: 3 a 5 jours ouvrables."
                ),
            }, ensure_ascii=False)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"creer_demande_administrative error: {e}")
        return f"Erreur lors de la creation de la demande: {e}"


@tool
def rechercher_contact_eniad(requete: str) -> str:
    """Recherche dans la base de connaissances ENIAD : procedures administratives, contacts, services et informations generales.
    Retourne la procedure complete (etapes, documents, delai, contact) pour toute question d'etudiant.
    Utiliser pour: toute question sur les demarches, services, contacts, procedures, evenements, documents, stages, examens, etc."""
    import unicodedata, os, json as _json

    def _norm(s: str) -> str:
        n = unicodedata.normalize("NFKD", s.lower().strip())
        return "".join(c for c in n if not unicodedata.combining(c))

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "contacts_eniad.json")
    try:
        with open(data_path, encoding="utf-8") as f:
            data = _json.load(f)
    except Exception as e:
        return f"Annuaire non disponible: {e}"

    query_norm = _norm(requete)
    query_words = set(query_norm.split())

    def score_keywords(keywords: list) -> int:
        s = 0
        for kw in keywords:
            kw_norm = _norm(kw)
            if kw_norm in query_norm:
                s += 2
            elif any(w in kw_norm for w in query_words if len(w) > 3):
                s += 1
        return s

    # ── 1. Chercher dans les procédures (source prioritaire) ──────────────────
    proc_matches: list[tuple[int, str, dict]] = []
    for key, proc in data.get("procedures", {}).items():
        s = score_keywords(proc.get("keywords", []))
        if s > 0:
            proc_matches.append((s, key, proc))

    if proc_matches:
        proc_matches.sort(key=lambda x: x[0], reverse=True)
        _, _, best = proc_matches[0]

        etapes = best.get("etapes", [])
        parts = [f"**{best.get('titre', '')}**"]

        if etapes:
            steps_txt = "\n".join(f"{i}. {s}" for i, s in enumerate(etapes, 1))
            parts.append(f"**Étapes :**\n{steps_txt}")

        contact_lines = [f"**{best.get('service', '')}**"]
        if best.get("responsable"):
            contact_lines.append(f"• {best['responsable']}")
        if best.get("email"):
            contact_lines.append(f"• {best['email']}")
        if best.get("telephone"):
            contact_lines.append(f"• {best['telephone']}")
        if best.get("bureau"):
            contact_lines.append(f"• {best['bureau']}")
        if best.get("horaires"):
            contact_lines.append(f"• {best['horaires']}")
        parts.append("\n".join(contact_lines))

        return "\n\n".join(parts)

    # ── 2. Chercher dans la direction ─────────────────────────────────────────
    direction = data.get("direction", {})
    if score_keywords(direction.get("keywords", [])) > 0:
        return (
            f"**Direction Générale ENIAD**\n"
            f"• {direction.get('directeur', '')}\n"
            f"• {direction.get('email', '')}\n"
            f"• {direction.get('telephone', '')}\n"
            f"• {direction.get('bureau', '')}"
        )

    # ── 3. Chercher dans les chefs de filière ─────────────────────────────────
    chef_matches: list[tuple[int, dict]] = []
    for entry in data.get("chefs_filiere", []):
        s = score_keywords(entry.get("keywords", []))
        if s > 0:
            chef_matches.append((s, entry))

    if chef_matches:
        chef_matches.sort(key=lambda x: x[0], reverse=True)
        lines = []
        for _, entry in chef_matches[:2]:
            lines.append(
                f"**{entry['filiere']}**\n"
                f"• {entry['responsable']}\n"
                f"• {entry['email']}\n"
                f"• {entry['telephone']}\n"
                f"• {entry['bureau']}"
            )
        return "\n\n".join(lines)

    # ── 4. Chercher dans les services ─────────────────────────────────────────
    svc_matches: list[tuple[int, dict]] = []
    for entry in data.get("services", []):
        s = score_keywords(entry.get("keywords", []))
        if s > 0:
            svc_matches.append((s, entry))

    if svc_matches:
        svc_matches.sort(key=lambda x: x[0], reverse=True)
        _, entry = svc_matches[0]
        lines = [
            f"**{entry['service']}**",
            f"• {entry['responsable']}",
            f"• {entry['email']}",
            f"• {entry['telephone']}",
            f"• {entry['bureau']}",
        ]
        if entry.get("horaires"):
            lines.append(f"• {entry['horaires']}")
        return "\n".join(lines)

    # ── 5. Fallback général ───────────────────────────────────────────────────
    return (
        "**Service Scolarité ENIAD**\n"
        "• scolarite@eniad.ma\n"
        "• +212 5 36 00 10 01\n"
        "• Bloc Administratif - Bureau A01\n"
        "• 08:30 - 16:30 (Lundi - Vendredi)"
    )


@tool
def rechercher_info_eniad(requete: str) -> str:
    """Recherche dans les documents officiels ENIAD (reglement, procedures, calendrier academique, contacts) via la base documentaire RAG."""
    try:
        from backend.services.rag_service import get_rag_service
        rag = get_rag_service()
        if not rag.is_ready:
            return (
                "Base documentaire ENIAD non disponible. "
                "Contactez le secretariat ENIAD directement pour toute information officielle."
            )

        results = rag.query(requete, n_results=4)
        if not results:
            return "Aucune information trouvee dans les documents ENIAD pour cette requete."

        parts = [f"[Source {i+1}] {r.get('content', '')[:500]}" for i, r in enumerate(results)]
        return "\n\n".join(parts)
    except Exception as e:
        logger.warning(f"rechercher_info_eniad error: {e}")
        return f"Recherche documentaire indisponible: {e}"


_TOOLS = [
    oriente_support_admin,
    recuperer_profil_etudiant,
    generer_document_pdf,
    verifier_statut_demandes,
    creer_demande_administrative,
    rechercher_contact_eniad,
    rechercher_info_eniad,
]


# ─────────────────────────────────────────────────────────────────────────────
# Agent Node (ReAct — Reason + Act)
# ─────────────────────────────────────────────────────────────────────────────

async def agent_node(state: AdminAgentState) -> dict:
    user_id = state.get("user_id", 0)
    ctx = state.get("user_context") or {}

    nom = ctx.get("full_name") or ctx.get("username") or "l'etudiant"
    filiere = ctx.get("major") or "filiere non renseignee"
    annee = ctx.get("year") or "annee non renseignee"

    system_prompt = (
        f"Tu es l'Assistant Administratif de SmartStudent — ENIAD Berkane, Maroc.\n"
        f"Tu interagis avec : {nom} | Filière : {filiere} | Année : {annee} | ID : {user_id}.\n\n"

        "══════════════════════════════════════════════════════════════\n"
        "RÔLE PRINCIPAL : GUIDE ADMINISTRATIF (PAS UN CRÉATEUR DE TICKETS)\n"
        "══════════════════════════════════════════════════════════════\n"
        "Quand un étudiant décrit une situation ou un problème (ex : 'j'ai perdu ma carte',\n"
        "'problème WiFi', 'je veux une attestation'), tu dois :\n"
        "  1. Utiliser oriente_support_admin(user_message=...) pour identifier la situation\n"
        "  2. Expliquer la procédure ETAPE PAR ETAPE de façon claire et structurée\n"
        "  3. Lister les documents éventuellement nécessaires\n"
        "  4. Indiquer le service ET la personne responsable à contacter\n"
        "  5. ORIENTER l'étudiant vers l'administration — NE PAS créer de ticket à sa place\n\n"

        "SITUATIONS COUVERTES (25 cas) :\n"
        "  • Perte carte étudiant       → Service Scolarité\n"
        "  • Changement de filière      → Chef de filière + Scolarité\n"
        "  • Attestation de scolarité   → Service Scolarité\n"
        "  • Relevé de notes            → Service Scolarité\n"
        "  • Problème de note           → Enseignant + Chef de filière\n"
        "  • Absence à un examen        → Affaires Estudiantines\n"
        "  • Stage PFA/PFE              → Service Stages\n"
        "  • Convention de stage        → Service Stages\n"
        "  • Accès plateforme           → Service Informatique\n"
        "  • Réinitialisation MDP       → Service Informatique\n"
        "  • Problème WiFi              → Service Informatique\n"
        "  • Bourse                     → Affaires Estudiantines\n"
        "  • Participation événement    → Affaires Estudiantines\n"
        "  • Demande de certificat      → Service Scolarité\n"
        "  • Retrait du diplôme         → Service Scolarité\n"
        "  • Réinscription annuelle     → Service Scolarité\n"
        "  • Congé académique           → Service Scolarité\n"
        "  • Équivalence de module      → Chef de filière + Scolarité\n"
        "  • Emploi du temps            → Secrétariat pédagogique\n"
        "  • Calendrier des examens     → Service Scolarité\n"
        "  • Bibliothèque               → Bibliothèque/Médiathèque\n"
        "  • Paiement des frais         → Service Finances\n"
        "  • Mobilité internationale    → Bureau Relations Internationales\n"
        "  • Réclamation administrative → Service Réclamations\n"
        "  • Contact chefs de filière   → Bureau de filière concerné\n\n"

        "RÈGLE IMPORTANTE — UTILISATION DES OUTILS :\n"
        "  • Pour toute demande administrative/procédurale : oriente_support_admin() EN PREMIER\n"
        "  • Pour contacts, infos sur un service, ou demande non couverte : rechercher_contact_eniad()\n"
        "  • Si oriente_support_admin() ne trouve pas, utiliser rechercher_contact_eniad()\n"
        "  • Toujours donner la procédure COMPLÈTE : étapes + documents + contact + délai\n\n"

        "FORMAT DE RÉPONSE ATTENDU pour chaque situation :\n"
        "  📋 Situation identifiée : <titre>\n"
        "  🏫 Service compétent : <service> | Responsable : <nom>\n"
        "  📄 Documents requis : (liste si applicable)\n"
        "  📍 Démarche à suivre :\n"
        "     1. Étape 1\n"
        "     2. Étape 2\n"
        "     ...\n"
        "  ⏱ Délai estimé : <délai>\n"
        "  ✅ Résultat attendu : <résultat>\n\n"

        "══════════════════════════════════════════════════════════════\n"
        "RÈGLE — PAS DE RÉCLAMATION À LA PLACE DE L'ÉTUDIANT :\n"
        "══════════════════════════════════════════════════════════════\n"
        "Pour les réclamations, expliquer la procédure et orienter vers le Service Réclamations\n"
        "(Bureau A02, reclamations@eniad.ma). Ne pas créer de ticket à la place de l'étudiant.\n\n"

        "OUTILS DISPONIBLES :\n"
        f"0. Guide administratif   -> oriente_support_admin(user_message=...)  ← PRIORITAIRE pour demandes procédurales\n"
        f"1. Annuaire/procédures   -> rechercher_contact_eniad(requete=...)    ← si oriente ne trouve pas ou pour contacts\n"
        f"2. Profil étudiant       -> recuperer_profil_etudiant(user_id={user_id})\n"
        f"3. Générer document PDF  -> generer_document_pdf(doc_type=..., user_id={user_id}, ...)\n"
        f"4. Suivi des demandes    -> verifier_statut_demandes(user_id={user_id})\n"
        f"5. Demande formelle      -> creer_demande_administrative(user_id={user_id}, ...)\n"
        "6. Info ENIAD (RAG)      -> rechercher_info_eniad(requete=...)\n\n"

        "DOCUMENTS GÉNÉRABLES — 3 TYPES UNIQUEMENT :\n"
        "  - 'Attestation de scolarite' : certifie l'inscription\n"
        "  - 'Convention de stage'      : accord ENIAD / étudiant / entreprise\n"
        "  - \"Reglement de l'ecole\"     : règlement intérieur officiel ENIAD\n\n"

        "PROCÉDURE GÉNÉRATION DE DOCUMENTS :\n\n"
        ">> ATTESTATION DE SCOLARITE :\n"
        f"   1. recuperer_profil_etudiant(user_id={user_id})\n"
        f"   2. generer_document_pdf(doc_type='Attestation de scolarite', user_id={user_id})\n\n"
        ">> CONVENTION DE STAGE :\n"
        "   Si le message contient Entreprise/Adresse/Tuteur/Poste/Dates :\n"
        f"     → recuperer_profil_etudiant(user_id={user_id})\n"
        f"     → generer_document_pdf(doc_type='Convention de stage', user_id={user_id}, entreprise=..., ...)\n"
        "   Sinon → demander d'abord les informations manquantes.\n\n"
        ">> REGLEMENT DE L'ECOLE :\n"
        f"   → generer_document_pdf(doc_type=\"Reglement de l'ecole\", user_id={user_id})\n\n"

        "INTERDITS ABSOLUS :\n"
        "  - Ne JAMAIS générer un 'Relevé de notes', 'Certificat de stage' ou tout autre document non listé.\n"
        "  - Ne JAMAIS inventer des données — utiliser uniquement les outils.\n"
        "  - Ne JAMAIS créer, mentionner ou proposer de réclamation, ticket ou plainte.\n"
        "  - Si un étudiant évoque une plainte, orienter vers le service compétent en expliquant la procédure.\n"
        "Après génération d'un document : NE retourne AUCUN texte, AUCUN message, AUCUNE explication, AUCUNE confirmation. Réponds uniquement avec une chaîne vide ''."
    )

    try:
        llm = _get_llm().bind_tools(_TOOLS)
        messages = [SystemMessage(content=system_prompt)] + list(state.get("messages", []))
        resp = await llm.ainvoke(messages)
        return {"messages": [resp]}
    except Exception as e:
        logger.error(f"agent_node error: {e}")
        err = AIMessage(content=(
            "Je ne peux pas traiter cette demande pour l'instant.\n\n"
            "**Service Scolarité ENIAD**\n"
            "• Bureau : Bloc Administratif - Bureau A01\n"
            "• Email : scolarite@eniad.ma\n"
            "• Téléphone : +212 5 36 00 10 01\n"
            "• Horaires : 08:30 - 16:30"
        ))
        return {"messages": [err]}


# ─────────────────────────────────────────────────────────────────────────────
# Graph compilation — ReAct loop: agent <-> tools
# ─────────────────────────────────────────────────────────────────────────────

def _build_admin_graph():
    g = StateGraph(AdminAgentState)
    g.add_node("agent", agent_node)
    g.add_node("tools", ToolNode(_TOOLS))

    g.set_entry_point("agent")
    g.add_conditional_edges("agent", tools_condition)  # -> "tools" or END
    g.add_edge("tools", "agent")

    return g.compile(checkpointer=MemorySaver())


_graph_instance = None


def get_compiled_admin_graph():
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = _build_admin_graph()
        nodes = list(_graph_instance.get_graph().nodes)
        logger.info(f"AdminAgent ReAct graph compiled - nodes: {nodes}")
    return _graph_instance


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

# Keywords that indicate document generation — only these go through the LLM
_DOC_GEN_KEYWORDS = [
    "genere", "générer", "génère",
    "attestation de scolarite", "attestation scolarite",
    "convention de stage",
    "reglement de l'ecole", "reglement ecole",
    "telecharger", "télécharger", "pdf",
]


# ─────────────────────────────────────────────────────────────────────────────
# Intent detection — what does the student actually want?
# ─────────────────────────────────────────────────────────────────────────────

# ── Intent detection: weighted keyword rules ──────────────────────────────────
# Each entry: (intent_type, [keywords], weight)
# Specific multi-word phrases get weight=2; generic single words get weight=1.
_INTENT_RULES: list[tuple[str, list[str], int]] = [
    ("contact", [
        "je veux le contact", "donne moi le contact", "quel est le contact",
        "comment joindre", "comment contacter", "email de", "mail de",
        "numéro de", "numero de", "téléphone de", "telephone de",
        "coordonnées de", "coordonnees de",
    ], 2),
    ("contact", [
        "contact", "email", "mail", "téléphone", "telephone", "tél", "tel",
        "numéro", "numero", "joindre", "contacter", "coordonnées", "coordonnees", "appeler",
    ], 1),
    ("responsible", [
        "nom du responsable", "qui est responsable", "qui s'occupe de",
        "qui gère le", "qui gere le", "qui traite", "qui est le chef de",
        "qui est le directeur", "qui s occupe",
    ], 2),
    ("responsible", [
        "responsable", "qui est", "chef de", "directeur", "encadrant",
    ], 1),
    ("location", [
        "où dois-je aller", "où se trouve", "ou deposer", "ou remettre",
        "où déposer", "ou se rendre", "ou aller deposer", "ou dois-je",
        "où dois-je", "où aller",
    ], 2),
    ("location", [
        "où", "ou aller", "bureau", "localisation", "adresse", "se rendre",
        "déposer", "deposer", "remettre", "aller au", "localiser",
    ], 1),
    ("procedure", [
        "comment faire", "comment obtenir", "comment procéder", "comment proceder",
        "comment demander", "comment avoir", "j'ai perdu", "j ai perdu",
        "que faire si", "que dois-je faire", "quelles sont les étapes",
        "quelles sont les etapes", "comment je peux", "comment puis-je",
        "comment je dois", "quelle est la démarche", "quelle est la demarche",
    ], 2),
    ("procedure", [
        "comment", "procédure", "procedure", "étapes", "etapes",
        "démarche", "demarche", "que faire", "perdu", "perdue",
        "obtenir", "avoir",
    ], 1),
    ("documents", [
        "quels documents faut-il", "quels documents dois-je", "quels sont les documents",
        "liste des documents", "quelles pièces", "quoi apporter", "quoi fournir",
        "faut-il comme document", "quels fichiers", "pièces à fournir",
        "documents à fournir", "dossier à constituer",
    ], 2),
    ("documents", [
        "document", "documents", "pièce", "pieces", "piece", "pièces",
        "fournir", "apporter", "amener", "justificatif", "justificatifs",
    ], 1),
    ("conditions", [
        "quelles sont les conditions", "qui peut faire", "est-ce que je peux",
        "suis-je éligible", "ai-je le droit", "conditions pour",
        "conditions requises", "qui a le droit", "est-ce possible pour",
    ], 2),
    ("conditions", [
        "condition", "conditions", "eligible", "éligible", "requis",
        "prérequis", "prerequis", "droit à", "peut-on", "critères", "criteres",
    ], 1),
    ("delai", [
        "combien de temps", "quel est le délai", "quel est le delai",
        "dans combien de temps", "délai de traitement", "quand vais-je recevoir",
        "quand je vais avoir", "quand est-ce que",
    ], 2),
    ("delai", [
        "délai", "delai", "durée", "duree", "quand", "combien de jours",
        "urgent", "urgence", "rapidement",
    ], 1),
    ("suivi", [
        "suivre ma demande", "où en est ma demande", "statut de ma demande",
        "j'ai déjà déposé", "j ai deja depose", "après avoir déposé",
        "que se passe-t-il après", "vais-je être contacté",
        "j ai soumis", "j'ai soumis", "j'ai envoyé",
    ], 2),
    ("suivi", [
        "suivi", "suivre", "statut", "après", "apres",
        "résultat attendu", "reponse attendue", "déjà fait", "deja fait",
    ], 1),
]


def _detect_intent(text: str) -> str:
    """Detects the primary intent using weighted rule scoring.

    Returns one of: contact, responsible, location, procedure,
    documents, conditions, delai, suivi, general, clarification.
    """
    t = text.lower()
    scores: dict[str, float] = {}
    for intent_type, keywords, weight in _INTENT_RULES:
        for kw in keywords:
            if kw in t:
                scores[intent_type] = scores.get(intent_type, 0) + weight

    if not scores:
        return "clarification" if len(t.split()) <= 4 else "general"

    best = max(scores, key=lambda k: scores[k])
    top_two = sorted(scores.values(), reverse=True)
    # Ambiguous tie at low score → general
    if len(top_two) >= 2 and top_two[0] <= 1 and top_two[0] == top_two[1]:
        return "general"

    return best


def _detect_filiere(text: str) -> str | None:
    """Detects which filière the student is asking about."""
    t = text.lower()
    if "intelligence artificielle" in t or " ia" in t or t.endswith(" ia") or "chef ia" in t or "filiere ia" in t or "filière ia" in t:
        return "Intelligence Artificielle"
    if "génie informatique" in t or "genie informatique" in t or " gi" in t or t.endswith(" gi") or "chef gi" in t or "filiere gi" in t or "filière gi" in t:
        return "Génie Informatique"
    if "robotique" in t or "robot" in t or "chef robotique" in t:
        return "Robotique"
    if "réseaux" in t or "reseaux" in t or " rs" in t or t.endswith(" rs") or "telecoms" in t or "chef reseaux" in t or "chef réseau" in t:
        return "Réseaux et Systèmes"
    return None


def _classify_message_direct(text: str) -> str | None:
    """Pure-Python keyword scoring — no LLM needed. Returns ADMIN_SUPPORT_MAP key or None."""
    t = text.lower()
    scores = {key: sum(1 for kw in info.get("keywords", []) if kw in t)
              for key, info in ADMIN_SUPPORT_MAP.items()}
    best = max(scores, key=lambda k: scores[k])
    if scores[best] > 0:
        return best
    # Simple fallback words covering all situations
    _fb = [
        (["chef filiere", "chef de filiere", "chef ia", "chef gi", "chef robotique", "chef reseaux", "contact chef"], "chef_filiere_contact"),
        (["carte", "perdu", "perdue", "duplicata", "nouvelle carte"],  "carte_perdue"),
        (["filiere", "filière", "changer filiere", "transfert"],        "changement_filiere"),
        (["attestation"],                                               "attestation"),
        (["releve", "bulletin", "mes notes"],                           "releve_notes"),
        (["probleme note", "erreur note", "ma note", "contestation"],  "probleme_note"),
        (["absent", "absence", "justificatif", "rate examen"],         "absence_examen"),
        (["pfe", "pfa", "fin d'etude", "memoire", "soutenance"],       "stage_pfa_pfe"),
        (["convention", "stage"],                                      "convention_stage"),
        (["plateforme", "moodle", "ent", "portail", "acces cours"],    "acces_plateforme"),
        (["mot de passe", "password", "mdp", "reinitialisation", "oublie mot"],  "reinitialisation_mdp"),
        (["wifi", "wi-fi", "internet", "reseau", "connexion", "point d'acces", "point d'accès", "se connecter"], "wifi"),
        (["bourse", "aide financiere", "aide sociale", "soutien financier"],  "bourse"),
        (["evenement", "événement", "club", "participer", "hackathon", "conference"],  "participation_evenement"),
        (["certificat"],                                               "certificat"),
        (["diplome", "diplôme", "retrait diplome"],                    "retrait_diplome"),
        (["reinscription", "renouveler inscription", "nouvelle annee"], "reinscription"),
        (["conge", "suspension etude", "interrompre etude"],           "conge_academique"),
        (["equivalence", "valider module", "reconnaitre module"],      "equivalence_module"),
        (["emploi du temps", "edt", "planning cours"],                 "emploi_temps"),
        (["examen", "partiel", "date examen", "programme examen"],     "programme_examens"),
        (["bibliotheque", "emprunter livre", "pret livre"],            "bibliotheque"),
        (["frais scolarite", "payer scolarite", "quitus financier"],   "paiement_frais"),
        (["erasmus", "mobilite internationale", "echange international"], "mobilite_internationale"),
        (["reclamation", "plainte", "contestation decision"],          "reclamation_admin"),
    ]
    for words, key in _fb:
        if any(w in t for w in words):
            return key
    return None


def _build_smart_response(info: dict, nom: str, intent: str, original_text: str = "") -> str:
    """Retourne uniquement les étapes à suivre + le contact du responsable."""
    title       = info.get("title", "")
    service     = info.get("service", "")
    responsable = info.get("responsable", "")
    bureau      = info.get("bureau", "")
    email       = info.get("email", "")
    telephone   = info.get("telephone", "")
    horaires    = info.get("horaires", "")
    process     = info.get("process", [])
    chefs       = info.get("chefs_filiere", {})

    # Chefs de filière : carte de contact
    if chefs and not process:
        filiere = _detect_filiere(original_text)
        if filiere and filiere in chefs:
            c = chefs[filiere]
            return (
                f"**{filiere}**\n"
                f"• {c['chef']}\n"
                f"• {c.get('email', '')}\n"
                f"• {c.get('telephone', '')}\n"
                f"• {c.get('bureau', '')}"
            )
        lines = []
        for f_name, c in chefs.items():
            lines.append(f"**{f_name}** — {c['chef']} | {c.get('email', '')} | {c.get('telephone', '')} | {c.get('bureau', '')}")
        return "\n".join(lines)

    parts = []

    # Étapes
    if process:
        steps = "\n".join(f"{i}. {s}" for i, s in enumerate(process, 1))
        parts.append(f"**Étapes :**\n{steps}")

    # Contact du responsable
    contact_lines = [f"**{service}**"]
    if responsable:
        contact_lines.append(f"• {responsable}")
    if email:
        contact_lines.append(f"• {email}")
    if telephone:
        contact_lines.append(f"• {telephone}")
    if bureau:
        contact_lines.append(f"• {bureau}")
    if horaires:
        contact_lines.append(f"• {horaires}")
    parts.append("\n".join(contact_lines))

    header = f"**{title}**\n\n" if title else ""
    return header + "\n\n".join(parts)


class AdminAgent:
    def __init__(self):
        self._graph = get_compiled_admin_graph()

    async def process(
        self,
        user_message: str,
        user_id: int,
        user_context: dict,
        conversation_id: str = "default",
    ) -> dict:
        nom = (user_context or {}).get("full_name") or (user_context or {}).get("username") or "étudiant"

        # ── Fast path: pure-Python guide (no LLM, no Groq API calls) ─────────
        # Use direct classification for all support queries. Only document
        # generation requests go through the LLM agent.
        needs_doc_gen = any(kw in user_message.lower() for kw in _DOC_GEN_KEYWORDS)
        if not needs_doc_gen:
            key = _classify_message_direct(user_message)
            if key and key in ADMIN_SUPPORT_MAP:
                intent = _detect_intent(user_message)
                return {
                    "response":   _build_smart_response(ADMIN_SUPPORT_MAP[key], nom, intent, user_message),
                    "doc_id":     None,
                    "request_id": None,
                    "ticket_id":  None,
                }

        # ── Slow path: LangGraph ReAct for document generation ────────────────
        thread_id = f"admin_{conversation_id}"
        initial: AdminAgentState = {
            "messages":     [HumanMessage(content=user_message)],
            "user_id":      user_id,
            "user_context": user_context,
        }
        config = {"configurable": {"thread_id": thread_id}}

        try:
            result = await self._graph.ainvoke(initial, config=config)
        except Exception as e:
            logger.error(f"AdminAgent.process graph error: {e}")
            # Fallback: try direct classification even for doc-gen messages
            key = _classify_message_direct(user_message)
            if key and key in ADMIN_SUPPORT_MAP:
                intent = _detect_intent(user_message)
                return {
                    "response":   _build_smart_response(ADMIN_SUPPORT_MAP[key], nom, intent, user_message),
                    "doc_id":     None,
                    "request_id": None,
                    "ticket_id":  None,
                }
            return {
                "response": "Le service IA est temporairement indisponible. Veuillez reessayer ou contacter le secretariat ENIAD.",
                "doc_id": None,
                "request_id": None,
                "ticket_id": None,
            }

        last_ai = next(
            (m for m in reversed(result.get("messages", [])) if isinstance(m, AIMessage)),
            None,
        )

        # Extract doc/ticket IDs from tool result messages
        doc_id = request_id = ticket_id = None
        for msg in result.get("messages", []):
            content = getattr(msg, "content", "")
            if not isinstance(content, str):
                continue
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    doc_id = doc_id or data.get("doc_id")
                    request_id = request_id or data.get("request_id")
                    ticket_id = ticket_id or data.get("ticket_id")
            except Exception:
                pass

        return {
            "response":   "" if doc_id else (str(last_ai.content) if last_ai else "Une erreur est survenue."),
            "doc_id":     doc_id,
            "request_id": request_id,
            "ticket_id":  ticket_id,
        }


def get_admin_agent() -> AdminAgent:
    return AdminAgent()
