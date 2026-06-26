# -*- coding: utf-8 -*-
"""
events_clubs_data.py

Données structurées : ÉVÉNEMENTS et CLUBS de l'ENIADB (École Nationale de
l'Intelligence Artificielle et du Digital - Berkane).

Format identique à la base de connaissances existante :
- une liste de dictionnaires avec les clés : id, category, title, content
- une liste séparée PDF_RESOURCES pour référencer les documents source

Source des événements : activite.pdf (12 affiches officielles, clubs AEI-ENIADB).
"""

# ---------------------------------------------------------------------------
# ÉVÉNEMENTS
# ---------------------------------------------------------------------------

EVENTS = [
    {
        "id": "evt_001",
        "category": "evenement",
        "title": "Movie Night Halloween - Club NURLIA",
        "content": """Club organisateur : NURLIA (Data Science & AI)
Date : 31 octobre
Heure : 18h00
Durée : 2 heures
Description : Soirée cinéma sur le thème d'Halloween. Au programme : un film
d'horreur, pop-corn et boissons, et des photos "spooky" avec masques.
Tarif : entrée à 20 DH
Dress code : noir, rouge et orange""",
    },
    {
        "id": "evt_002",
        "category": "evenement",
        "title": "Sortie nature / randonnée - Programme du jour (25 octobre 2025)",
        "content": """Date : 25 octobre 2025
Programme de la journée :
- 09h30 : Départ de Berkane (rassemblement du groupe, départ en bus, ambiance
  conviviale durant le trajet)
- 10h00 : Petit-déjeuner à la grotte "Magharat Lh'mam" (préparation du thé,
  distribution du petit-déjeuner, temps libre pour profiter du paysage et
  prendre des photos)
- 11h00 : Visite & découverte (randonnée vers Tafoughat, visite de l'enclos
  des mouflons, direction Zegzel, exploration des paysages et de la grotte
  "Magharat Ljamal")
- 14h00 : Déjeuner & convivialité (pause repas collective dans la nature)
- 15h00 : Activités ludiques (petits jeux d'équipe et activités récréatives
  dans la nature)
- 17h30 : Retour à Berkane (fin de la sortie)""",
    },
    {
        "id": "evt_003",
        "category": "evenement",
        "title": "Kick Off Party - AEI ENIADB",
        "content": """Club organisateur : AEI (Association des Étudiants Ingénieurs ENIADB)
Date : dimanche 02 novembre
Heure : début à 15h00
Lieu : Coin de la Ruche
Description : Fête de lancement (Kick Off Party) avec animation DJ et
karaoké. Crêpe et boisson offertes (free crêpe + drink). 15% de réduction
sur le menu.
Tarif : 55 DH
Places limitées : 50 places
Contact / réservation : 06 28 27 78 47 - 06 41 34 29 75""",
    },
    {
        "id": "evt_004",
        "category": "evenement",
        "title": "Battle of Minds - Tournoi d'échecs rapide",
        "content": """Clubs / partenaires organisateurs : AEI ENIADB, LINX (Power Energy Drink),
Jamiyat Al Liimoun Lichatranj (club d'échecs de Berkane)
Date : jeudi 02 avril
Heure : 12h30
Lieu : Buvette ENIAD
Description : Compétition "Battle of Minds" - tournoi d'échecs rapide,
20 minutes par partie, en élimination directe.
Inscription : du 31 au 1er mars, via lien de formulaire
Places limitées : 60 joueurs""",
    },
    {
        "id": "evt_005",
        "category": "evenement",
        "title": "Windows Pentesting - Active Directory Attacks - Club SECORA",
        "content": """Club organisateur : SECORA Club (cybersécurité)
Intervenant : Abdellatif TAZARANI
Date : samedi 28 février
Heure : 13h00 (1:00 PM)
Lieu : Salle BR6
Description : Atelier/conférence de pentesting Windows portant sur les
attaques Active Directory.""",
    },
    {
        "id": "evt_006",
        "category": "evenement",
        "title": "Qoffa El Khir - Panier de la solidarité (2ème édition) - Club Al Ataa",
        "content": """Club organisateur : Al Ataa, en partenariat avec l'ENIADB
Description : Campagne caritative "Qoffa El Khir" (panier du bien), 2ème
édition. Collecte de paniers solidaires (panier de Ramadan : huile,
conserves, denrées de base) au profit des personnes dans le besoin.
Pour contribuer financièrement :
- RIB : 007 575 0008115000302990 60
- Téléphone : 06 24 21 95 39""",
    },
    {
        "id": "evt_007",
        "category": "evenement",
        "title": "Programme Ingénieur 360° - Journée AEI / CSN Agency / Alpha Connect",
        "content": """Clubs / partenaires organisateurs : AEI ENIADB, CSN Agency, Alpha Connect
(Coworking - Business Center)
Description : Journée "Ingénieur 360°" consacrée à l'employabilité et au
développement professionnel.
Programme de la journée :
- 09h30 - 10h00 : Accueil & inscription
- 10h00 - 10h30 : Cérémonie d'ouverture (hymne national, mot du directeur,
  mot du président AEI)
- 10h30 - 11h15 : Conférence 1 (à distance) - M. Ayoubi Amine : "Réussir son
  entretien dans le marché du travail marocain"
- 11h20 - 12h00 : Conférence 2 (présentiel) - M. Oumri Mohamed : "Les
  compétences IA dans l'industrie automobile"
- 12h00 - 13h00 : Simulation d'entretien (jury : Oumri Mohamed, El Rhali
  Hicham ; candidats : 2 ou 3 étudiants)
- 13h00 - 14h00 : Pause café
- 14h00 - 15h30 : Workshops simultanés (Salle 1 - M. El Rhali Hicham : "Job
  attitude" ; Salle 2 : atelier technique)
- 15h30 - 16h00 : Clôture (remerciements et fin de l'événement)""",
    },
    {
        "id": "evt_008",
        "category": "evenement",
        "title": "Leo's Gala - Club LEO ENIADB Berkane",
        "content": """Club organisateur : LEO Club ENIADB Berkane
Date : samedi 13 décembre
Horaires : 12h00 - 20h00 (transport inclus)
Lieu : Salle des Fêtes Benisnassen
Description : Gala annuel avec performance spéciale Dekka Merrakchiya,
Aissawa, et DJ Reggada Oujda. Repas (poulet rôti), dessert, thé et gâteaux.
Tenue traditionnelle obligatoire.
Tarifs : interne 150 DH | AG présents 130 DH | externe 180 DH
Réservation : 06 84 37 77 71 - 06 95 32 76 26""",
    },
    {
        "id": "evt_009",
        "category": "evenement",
        "title": "Forum de l'Entreprise - 1ère édition (AEI ENIADB x CIH Bank)",
        "content": """Clubs / partenaires organisateurs : AEI ENIADB, ENIADB, CIH Bank
Thème : "L'IA et le recrutement"
Dates : 14 et 15 novembre
Description : 1ère édition du Forum de l'Entreprise - ENIAD, plateforme
d'échanges favorisant la connexion entre les entreprises innovantes et les
talents de demain, à l'heure où le numérique transforme l'ensemble des
secteurs.
Contact : contact@eniadb.site - 0700-511866
Lieu : Sidi Slimane, Berkane""",
    },
    {
        "id": "evt_010",
        "category": "evenement",
        "title": "Tech Connect - Jour 2 (Club GI ENSAO x ENIAD Innoverse)",
        "content": """Clubs / partenaires organisateurs : Club GI ENSAO (@club_gi_ensao), ENIAD
Innoverse (@eniad.innoverse)
Thème : "Future Opportunities and Challenges"
Date : 02 novembre 2025, à partir de 9h30
Description : Deuxième journée de l'événement Tech Connect, articulée
autour de trois volets : conférence, ateliers et compétition.""",
    },
    {
        "id": "evt_011",
        "category": "evenement",
        "title": "Formation aux Premiers Secours Essentiels - Club Al Ataa x ASPIVOT",
        "content": """Clubs / partenaires organisateurs : Al Ataa, ASPIVOT, en partenariat avec
l'ENIADB
Date : samedi 01 novembre 2025
Heure : 15h00 - 17h30
Description : Formation certifiée et ouverte à tous sur les premiers
secours essentiels. Programme :
- Introduction aux premiers secours
- Protéger, Alerter, Secourir
- Évaluation de la victime
- Réanimation cardio-pulmonaire (RCP)
- Situations d'urgence courantes
- Exercices pratiques
Contact : +212 691-006540 - Instagram : alataa.eniadb""",
    },
    {
        "id": "evt_012",
        "category": "evenement",
        "title": "ENIAD CTF (Capture The Flag) - Club SECORA",
        "content": """Club organisateur : SECORA Club (cybersécurité)
Description : Compétition de cybersécurité de type Capture The Flag (CTF).
Programme :
- 09h00 : début des ateliers/workshops préparatoires (lieu : Salle de
  Soutenance)
- 12h30 : pause café
- Les participants doivent arriver 30 minutes avant le début du CTF
- 14h00 : début officiel du CTF
- Lieu du CTF : salles AE5 & AE6
Consigne : apporter son ordinateur portable et son chargeur
Slogan : "Break / Hack / Win\"""",
    },
]

# ---------------------------------------------------------------------------
# CLUBS
# ---------------------------------------------------------------------------

CLUBS = [
    {
        "id": "club_001",
        "category": "club",
        "title": "Club SECORA - Cybersécurité",
        "content": """Le club SECORA, spécialisé en cybersécurité, a pour mission de sensibiliser
les étudiants aux enjeux de la sécurité informatique et de la protection
des données. Il s'intéresse aux menaces numériques modernes, aux techniques
de défense, ainsi qu'à la mise en place de bonnes pratiques pour sécuriser
les systèmes informatiques. À travers des ateliers pratiques, des
simulations d'attaques et des formations, SECORA prépare les étudiants à
faire face aux défis de la sécurité dans un monde de plus en plus connecté.""",
    },
    {
        "id": "club_002",
        "category": "club",
        "title": "Club ENNOVERS - Génie Informatique",
        "content": """Le club ENNOVERS, orienté vers le Génie Informatique (GI), se concentre
sur le développement logiciel, la programmation et les technologies
informatiques avancées. Il encourage les membres à travailler sur des
projets concrets en développement web, mobile et systèmes, tout en
renforçant leurs compétences en algorithmique, architecture logicielle et
gestion de projets informatiques.""",
    },
    {
        "id": "club_003",
        "category": "club",
        "title": "Club NURLIA - Intelligence Artificielle",
        "content": """Le club NURLIA, dédié à l'Intelligence Artificielle (IA), explore les
domaines du machine learning, du data science et de l'analyse de données.
Il vise à initier les étudiants aux techniques modernes d'IA, telles que
les réseaux de neurones, le traitement des données et la création de
modèles intelligents capables de résoudre des problèmes réels. NURLIA
favorise également la recherche et l'expérimentation à travers des projets
innovants.""",
    },
    {
        "id": "club_004",
        "category": "club",
        "title": "Club RIOT - Robotique",
        "content": """Le club RIOT, spécialisé en robotique, s'intéresse à la conception, la
programmation et la réalisation de systèmes robotiques. Il permet aux
étudiants de travailler sur des projets matériels et logiciels combinés,
incluant l'électronique, les capteurs, les microcontrôleurs et
l'automatisation. RIOT développe l'esprit d'ingénierie et la créativité à
travers des prototypes et des défis techniques.""",
    },
    {
        "id": "club_005",
        "category": "club",
        "title": "Club Al Ataa - Social et humanitaire",
        "content": """Le club Al Ataa est un club à vocation sociale et humanitaire, axé sur la
solidarité et l'entraide. Il organise des actions communautaires telles que
l'aide aux personnes dans le besoin, les projets de rénovation, les
distributions solidaires et les initiatives éducatives. Son objectif
principal est de promouvoir les valeurs humaines et l'engagement citoyen
chez les étudiants.""",
    },
    {
        "id": "club_006",
        "category": "club",
        "title": "Club Enactus - Entrepreneuriat social",
        "content": """Enactus est un club d'entrepreneuriat social qui encourage les étudiants à
développer des projets ayant un impact positif sur la société. Il combine
innovation, esprit entrepreneurial et responsabilité sociale afin de créer
des solutions durables aux problèmes communautaires.""",
    },
    {
        "id": "club_007",
        "category": "club",
        "title": "Écosystème des clubs ENIADB - Vue d'ensemble",
        "content": """L'ensemble des clubs SECORA, ENNOVERS, NURLIA, RIOT, Al Ataa et Enactus
constitue un écosystème étudiant dynamique et complémentaire, encadré par
l'AEI (Association des Étudiants Ingénieurs ENIADB), visant à développer à
la fois les compétences techniques, l'innovation et l'engagement social des
étudiants. Ensemble, ces clubs forment une plateforme complète où se
rencontrent la technologie, l'innovation et l'engagement social, permettant
aux étudiants de se former, d'expérimenter et de contribuer activement au
développement de leur environnement académique et sociétal.""",
    },
]

# ---------------------------------------------------------------------------
# RESSOURCES PDF
# ---------------------------------------------------------------------------

PDF_RESOURCES = [
    {
        "id": "pdf_001",
        "title": "Affiches officielles des événements ENIADB",
        "filename": "activite.pdf",
        "description": "Recueil de 12 affiches officielles d'événements organisés par "
        "l'AEI et les clubs de l'ENIADB (NURLIA, SECORA, Al Ataa, LEO, etc.) "
        "entre 2025 et 2026.",
    },
]

# ---------------------------------------------------------------------------
# Liste combinée
# ---------------------------------------------------------------------------

ALL_ENTRIES = EVENTS + CLUBS

if __name__ == "__main__":
    print(f"{len(EVENTS)} événements et {len(CLUBS)} clubs chargés "
          f"({len(ALL_ENTRIES)} entrées au total).")
