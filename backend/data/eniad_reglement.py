"""
Documents officiels ENIAD — Règlement Intérieur + Convention de Stage
Source: Règlement Intérieur ENIAD Berkane (6 pages, 31 articles)
        Convention de Stage ENIAD (2 pages, 12 articles)
Données structurées en chunks sémantiques pour indexation RAG ChromaDB.
"""

ENIAD_OFFICIAL_DOCUMENTS = [

    # ─── RÈGLEMENT INTÉRIEUR ─────────────────────────────────────────────────

    {
        "id": "ri_acces_formation_statut",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 1 à 3",
        "title": "Accès à l'école, durée de formation et statut d'élève ingénieur",
        "content": """
ACCÈS À L'ÉCOLE (Article 1) :
L'ENIAD est un établissement à accès régulé. L'accès aux études des classes préparatoires et
du cycle ingénieur est organisé par voie de concours.

DURÉE ET CONTENU DE LA FORMATION (Article 2) :
Les études à l'ENIAD durent 5 années (10 semestres), réparties en deux cycles :
- Cycle préparatoire (CP) : 2 années (4 semestres, S1 à S4)
- Cycle ingénieur d'état (CI) : 3 années (6 semestres, S5 à S10), incluant le Projet de Fin
  d'Études (PFE) réalisé durant tout le 6ème semestre (S10).

STATUT D'ÉLÈVE INGÉNIEUR (Article 3) :
- Est considéré élève de l'ENIAD toute personne ayant réussi un concours d'accès et régulièrement inscrite.
- Les droits et obligations sont précisés dans les articles 69 à 76 de la loi 01.00.
- Un élève perd son statut dès qu'il est exclu ou a obtenu son diplôme.
- En s'inscrivant à l'ENIAD, l'élève accepte les principes pédagogiques et le règlement intérieur.
"""
    },

    {
        "id": "ri_inscription_filieres",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 4 et 5",
        "title": "Inscription, réinscription et choix des filières",
        "content": """
INSCRIPTION ET RÉINSCRIPTION (Article 4) :
- L'inscription et la réinscription sont annuelles, effectuées dans les délais fixés par le Directeur.
- Inscription en 1ère année : ouverte aux titulaires du baccalauréat de l'enseignement secondaire.
- Inscription en 3ème année : ouverte aux titulaires du DUT/DEUST, DEUG ou licence (Pro/fondamentale/Sciences et techniques).
- Après inscription, une carte d'élève ingénieur est délivrée (pièce d'identité dans l'établissement, moyen d'authentification aux examens).
- Un élève s'inscrit dans une seule filière d'ingénierie.
- L'élève peut se réinscrire une fois à un module non validé. Une dérogation pour une 2ème et dernière réinscription peut être accordée par le directeur.

CHOIX DES FILIÈRES DU CYCLE INGÉNIEUR (Article 5) :
- Le choix des spécialités est arrêté à la fin de la 2ème année du cycle préparatoire.
- Répartition selon les vœux des élèves, leur classement (notes du cycle préparatoire) et la capacité d'accueil de chaque filière.
- Le choix des options au niveau d'une filière est arrêté par l'équipe pédagogique de la filière.
Filières disponibles : IA (Intelligence Artificielle), GINF (Génie Informatique), IRSI (Réseaux et Sécurité), ROC (Robotique et Objets Connectés).
"""
    },

    {
        "id": "ri_assiduite_presence",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Article 6",
        "title": "Assiduité et présence obligatoire aux cours",
        "content": """
ASSIDUITÉ ET PRÉSENCE (Article 6) :
- La présence aux cours magistraux, Travaux Dirigés (TD), Travaux Pratiques (TP), ateliers,
  séminaires, visites, contrôles et examens est OBLIGATOIRE.
- L'absence est gérée par les filières et prise en compte lors des délibérations de fin d'année.
- Toute absence doit être justifiée dans un délai de 48 heures auprès de l'enseignant responsable
  et du service de scolarité.
- Seule la commission pédagogique de la filière valide la justification.
- Tout élève exclu d'une séance pour indiscipline est compté absent.
- Les élèves doivent respecter les emplois du temps.
- L'accès aux locaux en dehors des horaires prévus nécessite une autorisation.
"""
    },

    {
        "id": "ri_absences_motifs_justifications",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 7 et 7Bis",
        "title": "Retards, absences et motifs de justification acceptés",
        "content": """
RETARDS ET ABSENCES (Article 7) :
- Tout retard risque d'entraîner une exclusion de la séance (absence non justifiée).
- Toute absence est relevée par l'enseignant sur une feuille d'absence.
- Absence non justifiée à un TP : peut empêcher la validation du module en session ordinaire. La séance ne peut être rattrapée.
- Absence justifiée à un TP : non pénalisante, mais ne peut être rattrapée.
- Plus d'1 séance de TP manquée OU plus de 2 séances de Cours/TD d'un même module : compromet la validation du module.
- Absences excessives (même justifiées) : le Conseil de l'Établissement prend des mesures.
- Délai de justification : 48 heures maximum auprès du secrétariat, du directeur adjoint, des coordonnateurs de filière et de l'enseignant.

MOTIFS D'ABSENCE ACCEPTÉS ET JUSTIFICATIONS REQUISES (Article 7Bis) :
| Motif | Justification requise |
|---|---|
| Maladie ou accident | Certificat médical selon l'imprimé de l'école |
| Hospitalisation | Attestation d'hospitalisation selon imprimé de l'école |
| Convocation administrative (Police, Consulat, entretien de stage, activité socioculturelle) | Copie certifiée conforme de la convocation |
| Stage autorisé par l'école | Copie convention de stage + attestation de stage + autorisation du coordinateur de filière |
| Décès d'un proche (parents, grands-parents, frères/sœurs, enfants) | Copie certifiée conforme de l'attestation du décès |
| État de santé avec absences répétitives dépassant 30 absences (15 jours) | Dossier médical détaillé signé par entité médicale reconnue |
"""
    },

    {
        "id": "ri_sanctions_absences",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Article 8",
        "title": "Sanctions pour absences non justifiées",
        "content": """
SANCTIONS AUX ABSENCES (Article 8) :

Sanctions cumulées sur PLUSIEURS MODULES lors d'un semestre :
- 3 absences → Avertissement (copie transmise à l'élève)
- 5 absences → Blâme (copie transmise aux parents)
- 7 absences → Conseil de discipline (décision sur durée d'exclusion)

Sanctions cumulées sur UN SEUL MODULE :
- 3 absences à un élément de module → Annulation de l'élément
- 5 absences à un module → Annulation du module

Règle générale :
- Cumul d'absences justifiées + non justifiées ≥ 15% du volume horaire du semestre → Annulation de la session de rattrapage.
- L'avertissement est formulé par les enseignants en présence des responsables de module, de la filière et de l'élève.
- Le PV d'avertissement est établi en 3 exemplaires (élève, filière, administration).
- IMPORTANT : Toutes les sanctions sont prises en compte par les jurys de délibérations ET pour l'octroi de recommandations (stages, bourses).
"""
    },

    {
        "id": "ri_examens_obligations",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Article 9",
        "title": "Obligations relatives aux contrôles et examens",
        "content": """
CONTRÔLES ET EXAMENS — OBLIGATIONS (Article 9) :
- La présence à tous les contrôles et examens est OBLIGATOIRE.
- Absent avec justificatif à la session ordinaire → droit uniquement à la session de rattrapage.
- Absent sans justificatif à un contrôle de la session ordinaire → peut demander une dérogation
  exceptionnelle pour le rattrapage, étudiée par la direction après avis de la commission pédagogique.
"""
    },

    {
        "id": "ri_evaluation_connaissances",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Article 10",
        "title": "Évaluation des connaissances — modalités",
        "content": """
ÉVALUATION DES CONNAISSANCES (Article 10) :
- L'évaluation s'effectue sous forme de contrôle continu : examens, tests, devoirs, exposés, rapports de stages.
- Un examen final peut être organisé en plus du contrôle continu si besoin.
- Les examens de TP sont pratiques (toute autre forme est exceptionnelle et justifiée).
- Minimum 2 contrôles écrits par élément de module ou module : 1 à mi-session + 1 en fin de session.
- Les évaluations écrites ne peuvent avoir lieu qu'en présence du ou des enseignants responsables.
- Les notes des épreuves écrites peuvent donner lieu à une vérification (pas une discussion).
  Délai de demande : 2 jours ouvrables suivant la publication des résultats, par écrit au secrétariat du Directeur Adjoint.
- L'élève doit assumer la note recalculée après vérification.
- Les notes orales ou pratiques ne peuvent donner lieu à une vérification.
"""
    },

    {
        "id": "ri_admission_module_notes",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Article 11",
        "title": "Admission du module — Notes minimales, notes éliminatoires et conditions de passage",
        "content": """
ADMISSION DU MODULE ET CONDITIONS DE PASSAGE (Article 11) :

Note minimale de validation d'un module :
- Cycle Préparatoire (CP) : 10/20
- Cycle Ingénieur (CI) : 12/20

Note éliminatoire (en dessous → non admis même si moyenne suffisante) :
- CP et CI : strictement inférieur à 7/20

Conditions d'admission à l'année :
- Moyenne générale ≥ 10/20 (CP) ou ≥ 12/20 (CI)
- ET avoir validé :
  * CP : 12 modules sur 14 (12/14)
  * CI Tronc commun (3ème année) : 12 modules sur 14 (12/14)
  * CI 4ème et 5ème année : 10 modules sur 14 (10/14)

Si les conditions ne sont pas satisfaites :
- Le chef d'établissement peut accorder une ANNÉE DE RÉSERVE après délibération du jury.
- L'année de réserve n'est autorisée qu'UNE SEULE FOIS par cycle.
- L'élève non admis est convoqué à un contrôle de rattrapage.
"""
    },

    {
        "id": "ri_calendrier_examens_convocation",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 12 et 13",
        "title": "Calendrier des examens, convocation et accès aux salles",
        "content": """
CALENDRIER ET CONVOCATION (Article 12) :
- Le calendrier des contrôles est établi par le directeur adjoint chargé de la pédagogie en concertation avec les coordonnateurs de filières.
- Les élèves doivent être informés au moins UNE SEMAINE avant les examens.
- Organisation en deux sessions :
  * Session normale : date communiquée au plus tard 1 semaine avant, par voie d'affichage.
  * Session de rattrapage : au moins 1 semaine après proclamation des résultats de la session normale.
  * Un élève n'a droit qu'à UN SEUL rattrapage par module.

ACCÈS AUX SALLES D'EXAMEN (Article 13) :
- Les élèves doivent consulter les plannings et leurs places à l'avance.
- Se présenter 10 MINUTES AVANT le début des épreuves avec la carte d'élève ingénieur (ou CIN).
- En cas de retard inférieur au tiers de la durée de l'épreuve : accès autorisé si aucun élève n'a quitté la salle.
- Les retardataires n'ont AUCUN temps supplémentaire pendant l'épreuve.
"""
    },

    {
        "id": "ri_devoirs_fraude_examen",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 14, 15 et 16",
        "title": "Obligations pendant l'épreuve, sortie de salle et fraude aux examens",
        "content": """
DEVOIRS PENDANT L'ÉPREUVE (Article 14) :
L'élève doit :
- Inscrire nom, prénom, code Apogée sur la copie et signer la feuille de présence.
- Composer seul et personnellement.
- Respecter le bon déroulement, ne pas troubler l'épreuve.
- Remettre obligatoirement la copie avant de quitter la salle.
- Déposer sacs et objets encombrants à l'entrée ou en bout de rangée.

Il est INTERDIT pendant les examens :
- Communiquer entre candidats ou avec l'extérieur.
- Utiliser ou conserver des documents/matériels non autorisés.
- Utiliser téléphones portables, tablettes ou tout appareil électronique non autorisé (doivent être laissés à l'extérieur).

SORTIE DE SALLE (Article 15) :
- Aucun candidat ne peut quitter la salle avant la moitié de la durée de la composition.
- Sortie temporaire : uniquement avec approbation du responsable et accompagné d'un surveillant.
  La copie est remise au surveillant (heure de sortie et retour inscrites).
- Infraction → note zéro, pas de rattrapage possible.

FRAUDE AUX EXAMENS (Article 16) :
- Tout non-respect des consignes des articles 14 et 15 constitue une fraude.
- Tentative ou fraude constatée → convocation devant le conseil de discipline.
- Plagiat dans les activités hors établissement (PFE, projets, devoirs) → mêmes sanctions.
- La direction peut engager des poursuites disciplinaires ou judiciaires.
"""
    },

    {
        "id": "ri_comportement_discipline",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 17 à 21",
        "title": "Comportement, discipline, respect du patrimoine et utilisation des locaux",
        "content": """
LIBERTÉ D'OPINION (Article 17) :
L'enseignement implique objectivité et tolérance. Toute forme de propagande politique,
philosophique ou religieuse est incompatible avec l'enseignement.

MANQUEMENT À LA DISCIPLINE (Article 18) :
Tout manquement (indiscipline, manque de respect, dégradation...) fait l'objet de rapports officiels
dans un délai de 48 heures. Le Conseil d'Établissement réuni en Conseil de Discipline étudie les rapports
et entérine les sanctions.

CONDUITE ET COMPORTEMENT (Article 19) :
Les élèves doivent respecter tous les personnels (pédagogiques, administratifs, techniques).
Tout manquement au respect ou acte inconvenant est sévèrement sanctionné.

RESPECT DU PATRIMOINE (Article 20) :
- Maintenir les bâtiments (cours, TD, TP, laboratoires, toilettes) en bon état et propres.
- Prendre soin du matériel ; toute dégradation est sanctionnée et remboursée.
- Respecter les livres de la bibliothèque (ouvrage abîmé → remboursement + suspension de consultation).
- Les supports de cours sont la propriété de l'enseignant. Ils ne peuvent pas être mis en libre accès sur Internet.

UTILISATION DES LOCAUX (Article 21) :
- Conditions définies et contrôlées par le Directeur.
- Personnes étrangères à l'école : autorisation explicite de la Direction requise.
- Toute dégradation des locaux entraîne une procédure disciplinaire.
"""
    },

    {
        "id": "ri_dispositions_generales",
        "category": "reglement",
        "source": "Règlement Intérieur ENIAD — Articles 22 à 31",
        "title": "Dispositions générales — interdictions, tenue, assurance, engagement",
        "content": """
DISPOSITIONS GÉNÉRALES :

Article 22 — Appareils électroniques et photographie :
Strictement interdit de prendre des photos/vidéos dans les salles de cours, TD, TP ou réunions sans autorisation.
Photos sans consentement ou mise en ligne de photos d'examens/élèves/enseignants → exclusion systématique
+ confiscation de l'appareil + poursuites judiciaires.

Article 23 — Tenue vestimentaire :
Les élèves doivent avoir une tenue correcte. Les tenues excentriques ou attirant l'attention sont interdites.

Article 24 — Bizutage :
Le bizutage est strictement interdit.

Article 25 — Interdiction de fumer :
L'interdiction de fumer est générale et absolue dans tous les locaux de l'école.

Article 26 — Produits illicites :
Toute utilisation ou détention de cigarette électronique, stupéfiants, alcool, psychotropes → sanction
disciplinaire majeure + poursuite judiciaire.

Article 27 — Réunions et activités :
Toute réunion, assemblée ou activité doit faire l'objet d'une autorisation écrite préalable auprès de la direction.

Article 28 — Assurance obligatoire :
Une police d'assurance annuelle est obligatoire pour l'inscription ou la réinscription à l'école.

Article 29 — Interlocuteurs de l'administration :
Les étudiants majeurs sont les seuls interlocuteurs de l'administration et des équipes pédagogiques
(les parents ou amis ne peuvent pas intervenir à leur place).

Articles 30-31 — Modifications et approbation :
Le conseil d'établissement est seul habilité à modifier le règlement. Le présent règlement est établi
et approuvé par le conseil d'établissement de l'ENIAD Berkane.
"""
    },

    # ─── CONVENTION DE STAGE ─────────────────────────────────────────────────

    {
        "id": "convention_stage_presentation",
        "category": "stage",
        "source": "Convention de Stage ENIAD — Introduction",
        "title": "Convention de Stage ENIAD — Présentation et parties",
        "content": """
CONVENTION DE STAGE ENIAD :
La convention de stage règle les rapports entre l'Organisme/Entreprise d'accueil et l'ENIAD.

ÉCOLE :
- École Nationale de l'Intelligence Artificielle et du Digital de Berkane (ENIAD)
- Adresse : Km 1, P6008, Sidi Slimane Echcharaa, 63300 Berkane
- Site Web : www.eniad.ump.ma | Email : eniad@ump.ac.ma
- Représentée par : M. KHALID JAAFAR

OBJECTIF :
Permettre à l'étudiant d'entrer en contact direct avec le milieu professionnel et de mettre en
application les connaissances théoriques acquises au cours de son cursus.

CHAMP D'APPLICATION :
Pour l'obtention du diplôme d'Ingénieur d'État, en vue d'un stage dans une entité professionnelle.
Ce stage est prévu par le règlement de l'ENIAD ; l'élève ingénieur est considéré comme ayant
donné son consentement en s'inscrivant à l'école.

Pour télécharger la convention officielle :
https://eniad.ump.ma/storage/files/1/Convention de stage/68234cd5a6293.pdf
"""
    },

    {
        "id": "convention_stage_duree_objectifs",
        "category": "stage",
        "source": "Convention de Stage ENIAD — Articles 1 à 3",
        "title": "Convention de Stage — Durée, objectifs et programme",
        "content": """
DURÉE DU STAGE (Article 1) :
- La durée du stage est fixée entre les parties (dates de début et fin précisées dans la convention).
- Les horaires sont ceux de l'administration de l'entreprise.
- L'élève stagiaire peut être autorisé à retourner à l'ENIAD pendant le stage pour certains cours
  ou conférences (date portée à la connaissance du directeur avant le commencement du stage).

OBJECTIFS DU STAGE (Article 2) :
Le stage a pour but :
1. Permettre à l'élève de rentrer en contact avec le milieu professionnel.
2. Tester ses possibilités d'adaptation personnelle.
3. Mettre en pratique les connaissances acquises à l'école.
4. Se préparer à une des épreuves du diplôme.

PROGRAMME DU STAGE (Article 3) :
Le programme est établi par les personnes chargées de l'encadrement, en tenant compte :
- Du programme et de la spécialité de l'élève.
- De la disponibilité des moyens humains et matériels de l'établissement d'accueil.
L'entreprise se réserve le droit de réorienter l'apprentissage selon les qualifications du stagiaire.
"""
    },

    {
        "id": "convention_stage_obligations_droits",
        "category": "stage",
        "source": "Convention de Stage ENIAD — Articles 4 à 8",
        "title": "Convention de Stage — Obligations, assurance, discipline et absences",
        "content": """
ASSURANCE RESPONSABILITÉ CIVILE (Article 4) :
L'étudiant doit souscrire à une assurance responsabilité civile personnelle pour couvrir tous
les risques pendant le stage. L'établissement (ENIAD) ne peut être tenu responsable des dommages
causés à des tiers ou subis par l'étudiant.

STATUT PENDANT LE STAGE (Article 5) :
Le stagiaire demeure élève ingénieur pendant toute la durée de son séjour dans l'entreprise.

DISCIPLINE DANS L'ENTREPRISE (Article 6) :
Le stagiaire est soumis à la discipline de l'entreprise (visites médicales, horaires de travail).
En cas de manquement grave, l'entreprise peut mettre fin au stage après avoir prévenu le service
des stages de l'ENIAD.

INTERRUPTION DU STAGE (Article 7) :
Le stagiaire ne peut interrompre son stage sous peine d'en perdre le bénéfice.

ABSENCES PENDANT LE STAGE (Article 8) :
En cas d'absence, le stagiaire doit aviser dans les 24 heures ouvrables les responsables de stage
de l'entreprise ET de l'ENIAD. En cas de difficulté ou d'accident, le responsable de stage prend
contact avec le service des stages de l'ENIAD le plus rapidement possible.
"""
    },

    {
        "id": "convention_stage_salaire_attestation_rapport",
        "category": "stage",
        "source": "Convention de Stage ENIAD — Articles 9 à 12",
        "title": "Convention de Stage — Statut salarial, attestation de stage et rapport",
        "content": """
SALAIRE ET INDEMNITÉ (Article 9) :
L'élève ingénieur de l'ENIAD ne peut prétendre à aucun salaire pendant le stage.
Toutefois, une indemnité de stage et/ou une gratification en fin de stage peuvent être versées
par l'entreprise (montant fixé librement par le chef d'entreprise).

CONTRAT DE TRAVAIL (Article 10) :
Le stagiaire n'est lié par aucun contrat de travail avec l'entreprise d'accueil.

ATTESTATION DE FIN DE STAGE (Article 11) :
À la fin du stage, l'entreprise délivre au stagiaire une attestation précisant la nature et la
durée du stage.

RAPPORT DE STAGE (Article 12) :
À son retour à l'ENIAD, l'élève est tenu de remettre un rapport de stage.

SIGNATURES REQUISES SUR LA CONVENTION :
- Le Chef d'Entreprise (avec mention "Lu et approuvé")
- Pour l'Établissement de Formation (ENIAD — M. KHALID JAAFAR)
- L'Élève Stagiaire (avec mention "Lu et approuvé")
"""
    },
]
