# -*- coding: utf-8 -*-
"""
Procédures administratives ENIAD — base de connaissances RAG.
Source : site officiel eniad.ump.ma + règlement intérieur.
"""

ENIAD_ADMIN_PROCEDURES = [
    {
        "id": "demande_attestation_scolarite",
        "category": "admin",
        "title": "Demande d'attestation de scolarité",
        "content": """Procédure pour obtenir une attestation de scolarité à l'ENIAD :

Étape 1 : Faire la demande auprès du service de la scolarité (sur place ou par email à eniad@ump.ac.ma).
Étape 2 : Préciser le motif de la demande (bourse, visa, CAF, banque, etc.) si requis par le formulaire.
Étape 3 : Récupérer le document signé et cacheté auprès de la scolarité.

Délai de délivrance : generalement quelques jours ouvrés (à confirmer avec la scolarité).
Pièces à fournir : carte d'étudiant ou numéro d'apogée, parfois une pièce d'identité.
Contact : eniad@ump.ac.ma | Téléphone : +212 536

À savoir : certains usages (bourse, CNOPS/AMO) peuvent nécessiter un nombre d'exemplaires précis — le demander en une seule fois pour éviter les allers-retours.""",
    },
    {
        "id": "demande_releve_de_notes",
        "category": "admin",
        "title": "Demande de relevé de notes",
        "content": """Procédure pour obtenir un relevé de notes officiel à l'ENIAD :

Étape 1 : Attendre la délibération du jury pour le semestre concerné (voir calendrier académique).
Étape 2 : Faire la demande auprès de la scolarité, en précisant le semestre ou l'année concernée.
Étape 3 : Le relevé est édité avec les notes officielles et signé par l'administration.

Délai : disponible après délibération (environ 2-3 semaines après les examens), puis délai d'édition à confirmer.
À noter : les résultats provisoires sont consultables en ligne sur https://eniad.ump.ma/fr/resultats avant l'édition du relevé papier officiel.
En cas d'erreur ou de contestation de note, s'adresser au chef de filière ou à l'administration avant de demander le relevé définitif.""",
    },
    {
        "id": "procedure_reinscription",
        "category": "admin",
        "title": "Réinscription annuelle",
        "content": """Procédure de réinscription à l'ENIAD (passage à l'année supérieure ou redoublement) :

Étape 1 : Vérifier les résultats de délibération annuelle (publiés après la session de rattrapage, généralement fin juin/juillet).
Étape 2 : Réinscription en ligne ou auprès de la scolarité selon les modalités communiquées par l'école pour l'année en cours.
Étape 3 : Fournir les pièces demandées (résultats, pièce d'identité, photos, etc. — liste précisée par la scolarité).
Étape 4 : Régler les frais de scolarité éventuels et récupérer la nouvelle carte d'étudiant.

Délai : campagne de réinscription généralement entre les délibérations annuelles et la rentrée de septembre (dates précises communiquées par affichage/site officiel).
Contact : eniad@ump.ac.ma""",
    },
    {
        "id": "procedure_stage",
        "category": "admin",
        "title": "Démarches administratives pour un stage",
        "content": """Procédure administrative pour effectuer un stage (été ou PFA) :

Étape 1 : Trouver une entreprise d'accueil (le CIOVE peut aider à l'orientation et la recherche).
Étape 2 : Télécharger la convention de stage officielle sur https://eniad.ump.ma/fr/documents-de-stage
Étape 3 : Faire remplir et signer la convention par l'entreprise (responsable du stage côté entreprise).
Étape 4 : Faire signer/valider la convention par l'école (scolarité ou responsable de filière) avant le début du stage.
Étape 5 : Effectuer le stage (durée minimale 4 à 8 semaines selon le type de stage).
Étape 6 : Rédiger et déposer le rapport de stage selon les consignes données par l'encadrant pédagogique.

Documents : https://eniad.ump.ma/fr/documents-de-stage
Important : la convention doit être signée par toutes les parties AVANT le démarrage effectif du stage.""",
    },
    {
        "id": "procedure_redoublement",
        "category": "admin",
        "title": "Procédure en cas de redoublement",
        "content": """Procédure administrative liée au redoublement à l'ENIAD :

Étape 1 : Le redoublement est décidé lors de la délibération annuelle du jury pédagogique, sur la base des résultats aux semestres et aux rattrapages.
Étape 2 : L'étudiant concerné est informé du résultat (affichage et/ou consultation en ligne sur https://eniad.ump.ma/fr/resultats).
Étape 3 : En cas de redoublement, l'étudiant doit procéder à la réinscription administrative pour la même année selon les modalités fixées par l'école.
Étape 4 : Pour toute contestation, s'adresser au chef de filière ou à l'administration pédagogique dans les délais communiqués après la délibération.

Conditions de passage et de redoublement : régies par le règlement intérieur de l'école.
Référence : https://eniad.ump.ma/fr/reglement-interieur-de-lecole""",
    },
    {
        "id": "procedure_bourse",
        "category": "admin",
        "title": "Demande de bourse d'études",
        "content": """Procédure pour demander une bourse d'études à l'ENIAD :

Étape 1 : Vérifier les conditions d'éligibilité (résultats académiques, situation sociale) — voir https://eniad.ump.ma/fr/bourses
Étape 2 : Constituer le dossier de demande (pièces justificatives sociales/financières, résultats académiques, etc. — liste précise communiquée lors de l'ouverture de la campagne).
Étape 3 : Déposer le dossier auprès du service compétent (scolarité ou service des affaires estudiantines) dans les délais de la campagne annuelle.
Étape 4 : Suivre la décision d'attribution communiquée par l'administration.

Délai : campagnes généralement ouvertes en début d'année universitaire (dates précises annoncées chaque année par l'école).
Plus d'infos : https://eniad.ump.ma/fr/bourses""",
    },
]
