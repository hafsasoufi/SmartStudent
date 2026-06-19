# -*- coding: utf-8 -*-
# =============================================================================
# CONVENTION DE STAGE — Base de données pour chatbot/assistant ENIAD
# Source : convention_de_stage.pdf
# Format : liste de dicts { id, category, title, content }
# =============================================================================

KNOWLEDGE_BASE = [

    # ── Présentation générale ─────────────────────────────────────────────────

    {
        "id": "stage_001",
        "category": "general",
        "title": "Objet de la convention de stage",
        "content": (
            "La convention de stage règle les rapports entre l'organisme ou l'entreprise d'accueil "
            "et l'École Nationale de l'Intelligence Artificielle et du Digital de Berkane (ENIAD).\n\n"
            "Coordonnées de l'ENIAD :\n"
            "- Adresse : Km 1, P6008, Sidi Slimane Echcharaa, 63300 Berkane\n"
            "- Site Web : www.eniad.ump.ma\n"
            "- E-mail : eniad@ump.ac.ma\n"
            "- Représentée par : M. KHALID JAAFAR\n\n"
            "Ce stage est prévu dans le cadre de l'obtention du diplôme d'Ingénieur d'État. "
            "En s'inscrivant, l'élève ingénieur est considéré comme ayant donné son consentement "
            "aux clauses de la présente convention."
        ),
    },
    {
        "id": "stage_002",
        "category": "general",
        "title": "Objectifs du stage",
        "content": (
            "Le stage a pour objectifs :\n"
            "- Permettre à l'élève d'entrer en contact direct avec le milieu professionnel.\n"
            "- Tester ses capacités d'adaptation personnelle.\n"
            "- Mettre en pratique les connaissances théoriques acquises à l'école.\n"
            "- Le préparer à l'une des épreuves du diplôme d'Ingénieur d'État."
        ),
    },

    # ── Articles de la convention ─────────────────────────────────────────────

    {
        "id": "stage_003",
        "category": "convention",
        "title": "Article 1 — Durée et horaires du stage",
        "content": (
            "La durée du stage est fixée contractuellement (dates de début et de fin à renseigner "
            "dans la convention).\n"
            "Les horaires sont ceux de l'administration de l'entreprise d'accueil.\n\n"
            "Toutefois, l'élève stagiaire peut être autorisé à retourner à l'ENIAD pendant la durée "
            "du stage pour suivre certains cours ou assister à des conférences, à condition que "
            "les dates soient portées à la connaissance du directeur de l'ENIAD avant le début du stage."
        ),
    },
    {
        "id": "stage_004",
        "category": "convention",
        "title": "Article 2 — But du stage",
        "content": (
            "Le stage a pour but :\n"
            "- De permettre à l'élève de rentrer en contact avec le milieu professionnel.\n"
            "- De tester ses possibilités d'adaptation personnelle.\n"
            "- De mettre en pratique les connaissances acquises à l'école.\n"
            "- De lui donner l'opportunité de se préparer à l'une des épreuves du diplôme "
            "préparé par son établissement."
        ),
    },
    {
        "id": "stage_005",
        "category": "convention",
        "title": "Article 3 — Programme du stage",
        "content": (
            "Le programme du stage est établi par le ou les encadrant(s) de l'entreprise d'accueil, "
            "en tenant compte du programme de formation, de la spécialité de l'élève "
            "et des moyens humains et matériels disponibles.\n"
            "L'entreprise se réserve le droit de réorienter l'apprentissage en fonction "
            "des qualifications du stagiaire et du rythme de ses activités professionnelles."
        ),
    },
    {
        "id": "stage_006",
        "category": "convention",
        "title": "Article 4 — Assurance et responsabilité civile",
        "content": (
            "L'étudiant certifie qu'il souscrira à une assurance responsabilité civile personnelle "
            "afin de couvrir tous les risques pouvant survenir pendant la durée de son stage.\n"
            "L'ENIAD ne pourra être tenu responsable :\n"
            "- Des dommages causés à des tiers par le stagiaire.\n"
            "- Des dommages subis par l'étudiant durant son stage."
        ),
    },
    {
        "id": "stage_007",
        "category": "convention",
        "title": "Article 5 — Statut pendant le stage",
        "content": (
            "Le stagiaire demeure élève ingénieur pendant toute la durée de son séjour dans l'entreprise."
        ),
    },
    {
        "id": "stage_008",
        "category": "convention",
        "title": "Article 6 — Discipline en entreprise",
        "content": (
            "Le stagiaire est soumis à la discipline de l'entreprise d'accueil, notamment en ce qui "
            "concerne les visites médicales et les horaires de travail.\n\n"
            "En cas de manquement à la discipline, l'entreprise peut mettre fin au stage après "
            "en avoir prévenu le service des stages de l'ENIAD.\n"
            "L'entreprise doit s'assurer, avant le départ du stagiaire, "
            "que l'avertissement est bien parvenu à son destinataire."
        ),
    },
    {
        "id": "stage_009",
        "category": "convention",
        "title": "Article 7 — Interruption du stage",
        "content": (
            "Le stagiaire ne peut pas interrompre son stage sous peine d'en perdre le bénéfice."
        ),
    },
    {
        "id": "stage_010",
        "category": "convention",
        "title": "Article 8 — Absence pendant le stage",
        "content": (
            "En cas d'absence, le stagiaire doit aviser dans les 24 heures ouvrables :\n"
            "- Le responsable de stage de l'entreprise d'accueil.\n"
            "- Le service des stages de l'ENIAD.\n\n"
            "En cas de difficulté ou d'accident, le responsable de stage est tenu de prendre contact "
            "le plus rapidement possible avec le service des stages de l'ENIAD."
        ),
    },
    {
        "id": "stage_011",
        "category": "convention",
        "title": "Article 9 — Rémunération du stagiaire",
        "content": (
            "L'élève ingénieur de l'ENIAD ne peut prétendre à aucun salaire durant son stage.\n"
            "Toutefois, une indemnité de stage et/ou une gratification de fin de stage peuvent "
            "lui être versées par le chef d'entreprise, qui en fixe librement le montant."
        ),
    },
    {
        "id": "stage_012",
        "category": "convention",
        "title": "Article 10 — Absence de contrat de travail",
        "content": (
            "Le stagiaire n'est lié par aucun contrat de travail avec l'entreprise d'accueil."
        ),
    },
    {
        "id": "stage_013",
        "category": "convention",
        "title": "Article 11 — Attestation de stage",
        "content": (
            "À la fin du stage, l'entreprise délivre au stagiaire une attestation "
            "précisant la nature et la durée du stage."
        ),
    },
    {
        "id": "stage_014",
        "category": "convention",
        "title": "Article 12 — Rapport de stage",
        "content": (
            "À son retour à l'ENIAD, l'élève est tenu de remettre un rapport de stage."
        ),
    },

    # ── Signataires & Champs à renseigner ────────────────────────────────────

    {
        "id": "stage_015",
        "category": "procedure",
        "title": "Signataires de la convention",
        "content": (
            "La convention doit être signée (Lu et approuvé) par trois parties :\n"
            "- Le Chef d'Entreprise (entreprise d'accueil)\n"
            "- Le représentant de l'ENIAD (M. KHALID JAAFAR)\n"
            "- L'élève stagiaire\n\n"
            "La convention est établie à Berkane, avec la date de signature."
        ),
    },
    {
        "id": "stage_016",
        "category": "procedure",
        "title": "Informations à renseigner dans la convention",
        "content": (
            "Côté entreprise :\n"
            "- Nom de l'entreprise\n"
            "- Adresse complète\n"
            "- Numéro de téléphone et fax\n\n"
            "Côté élève :\n"
            "- Spécialité (filière)\n"
            "- Nom et prénom de l'élève ingénieur\n"
            "- Année du cycle ingénieur\n\n"
            "Côté stage :\n"
            "- Date de début du stage\n"
            "- Date de fin du stage"
        ),
    },
]

# -----------------------------------------------------------------------------
# RESSOURCE PDF SOURCE
# -----------------------------------------------------------------------------

PDF_RESOURCES = [
    {
        "id": "pdf_001",
        "label": "Convention de stage ENIAD",
        "filename": "convention_de_stage.pdf",
        "description": (
            "Convention officielle (12 articles) encadrant les stages en entreprise "
            "pour les élèves ingénieurs de l'ENIAD."
        ),
    },
]

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------

def search(query: str) -> list:
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
