# Documentation des Widgets Dynamiques de l'Application KANFLOW

## 🎯 Vue d'ensemble

Tous les widgets de l'application sont maintenant **DYNAMIQUES** et réagissent aux changements d'état en temps réel grâce à l'architecture Provider.

## ✨ NOUVEAUTÉS - Widgets Dynamiques Ajoutés

### 🔔 Système de Notifications en Temps Réel
**Emplacement :** AppBar (MainLayout)

**Fonctionnalités :**
- ✅ Badge dynamique avec compteur de notifications
- ✅ Affichage du nombre de tâches en retard
- ✅ Affichage du nombre de tâches haute priorité
- ✅ Badge avec "9+" si plus de 9 notifications
- ✅ Couleur rouge pour attirer l'attention
- ✅ Navigation vers NotificationPage au clic

**Mise à jour :** En temps réel via `Consumer<IdeaProvider>`

### 📊 QuickStatsWidget - Statistiques en Temps Réel
**Emplacement :** DashboardScreen (en haut)

**Fonctionnalités :**
- ✅ Vue d'ensemble complète en temps réel
- ✅ Badge "En direct" avec indicateur vert pulsant
- ✅ Grille de 4 cartes statistiques :
  - Total des tâches
  - Tâches en cours
  - Tâches terminées
  - Backlog
- ✅ Barre de progression globale avec pourcentage
- ✅ Alertes dynamiques :
  - Priorité haute (rouge)
  - En retard (orange)
  - À venir dans 3 jours (ambre)
- ✅ Affichage du nombre de tableaux actifs
- ✅ Chip avec le nom du tableau sélectionné

**Mise à jour :** Consumer2<IdeaProvider, BoardProvider> - Mise à jour automatique

### 📈 Drawer Enrichi avec Statistiques
**Emplacement :** Drawer (MainLayout)

**Nouvelles fonctionnalités :**
- ✅ Section statistiques en temps réel :
  - Total des tâches
  - Tâches en cours
  - Tâches terminées
- ✅ Barre de progression avec pourcentage
- ✅ Design avec couleurs primaires du thème
- ✅ Widget helper `_buildStatRow` pour l'affichage

**Mise à jour :** Consumer3<BoardProvider, AuthProvider, IdeaProvider>

### 🔴 NotificationPage Intégrée
**Emplacement :** Accessible via bouton dans AppBar

**Fonctionnalités :**
- ✅ Affichage des tâches haute priorité
- ✅ Affichage du taux de complétion
- ✅ Journal d'activité récente
- ✅ Filtrage par tableau si sélectionné
- ✅ Design avec cartes colorées (rouge/vert)

## 📱 Structure de l'Application

### 1. **MainLayout** (`lib/widgets/main_layout.dart`)
Le layout principal enrichi :
- **AppBar** dynamique avec :
  - ✅ Badge de notifications (nouveau)
  - ✅ Toggle de thème
- **BottomNavigationBar** pour la navigation
- **Drawer** avec statistiques en temps réel (amélioré)
- Navigation dynamique entre Dashboard, Kanban et Roadmap

**Fonctionnalités dynamiques :**
- ✅ Création de tableaux en temps réel
- ✅ Sélection de tableaux avec mise à jour automatique
- ✅ Renommage de tableaux avec menu PopupMenu
- ✅ Suppression de tableaux avec menu PopupMenu
- ✅ Toggle thème clair/sombre
- ✅ Affichage dynamique de l'utilisateur connecté
- ✅ Déconnexion avec redirection
- ✅ **Statistiques en temps réel dans le Drawer**
- ✅ **Notifications dynamiques dans l'AppBar**

### 2. **DashboardScreen** (`lib/screens/dashboard_screen.dart`)
Écran de tableau de bord avec statistiques en temps réel :
- ✅ **QuickStatsWidget en haut** (nouveau)
- ✅ Compteur total de tâches
- ✅ Statistiques par statut (Backlog, In Progress, Done)
- ✅ Tâches en retard
- ✅ Tâches haute priorité
- ✅ Activité récente
- ✅ Graphiques de progression
- ✅ Mise à jour automatique lors de changements

### 3. **KanbanPageDynamic** (`lib/pages/kanban_page_dynamic.dart`)
Vue Kanban complètement dynamique :
- ✅ Colonnes dynamiques créées à partir de la base de données
- ✅ Ajout de nouvelles colonnes en temps réel
- ✅ Renommage de colonnes
- ✅ Suppression de colonnes
- ✅ Recherche de cartes en temps réel
- ✅ Filtrage par tags, priorité, date
- ✅ Drag & Drop entre colonnes
- ✅ Mise à jour de statut automatique

### 4. **DynamicKanbanColumn** (`lib/widgets/dynamic_kanban_column.dart`)
Colonne Kanban avec toutes les fonctionnalités :
- ✅ Affichage dynamique des cartes par statut
- ✅ Drag & Drop des cartes
- ✅ Badges de priorité (Haute/Moyenne/Basse)
- ✅ Indicateurs de date d'échéance
- ✅ Tags colorés
- ✅ Édition de cartes
- ✅ Suppression de cartes
- ✅ Compteur de cartes
- ✅ Actions contextuelles (modifier colonne, supprimer)

### 5. **AddIdeaDialog** (`lib/widgets/add_idea_dialog.dart`)
Dialogue dynamique pour créer des cartes :
- ✅ Formulaire complet avec validation
- ✅ Sélection de priorité (chips interactifs)
- ✅ Sélection de statut (dropdown)
- ✅ Date picker pour échéance
- ✅ Tags multiples
- ✅ Description riche
- ✅ Validation en temps réel
- ✅ Feedback visuel (SnackBar)

### 6. **RoadmapScreen** (`lib/screens/roadmap_screen.dart`)
Vue roadmap avec progression :
- ✅ Barre de progression globale
- ✅ Statistiques par statut
- ✅ Liste des tâches en retard (alertes)
- ✅ Tâches haute priorité
- ✅ Vue chronologique
- ✅ Mise à jour en temps réel

### 7. **NotificationPage** (`lib/screens/notification_page.dart`) - NOUVEAU
Page de notifications dédiée :
- ✅ Alertes pour tâches haute priorité
- ✅ Indicateur de complétion
- ✅ Journal d'activité
- ✅ Filtrage par tableau
- ✅ Design avec cartes colorées

### 8. **QuickStatsWidget** (`lib/widgets/quick_stats_widget.dart`) - NOUVEAU
Widget de statistiques rapides :
- ✅ Grille de 4 cartes de statistiques
- ✅ Barre de progression
- ✅ Alertes (priorité, retard, à venir)
- ✅ Info tableaux actifs
- ✅ Badge "En direct"

## 🔄 Providers (Gestion d'État)

### 1. **AuthProvider** (`lib/providers/auth_provider.dart`)
Gestion de l'authentification :
- ✅ Connexion/Inscription
- ✅ Stockage du token
- ✅ Informations utilisateur (nom, email, ID)
- ✅ Déconnexion
- ✅ Vérification d'authentification

### 2. **BoardProvider** (`lib/providers/board_provider.dart`)
Gestion des tableaux :
- ✅ Liste des tableaux par utilisateur
- ✅ Tableau sélectionné
- ✅ CRUD complet (Create, Read, Update, Delete)
- ✅ Colonnes dynamiques par tableau
- ✅ Synchronisation avec la base de données

### 3. **IdeaProvider** (`lib/providers/idea_provider.dart`)
Gestion des cartes/idées :
- ✅ Liste des cartes par tableau
- ✅ CRUD complet
- ✅ Changement de statut
- ✅ Filtrage et recherche
- ✅ Mise à jour de priorité
- ✅ Gestion des dates d'échéance
- ✅ **Journal d'activité** (utilisé par NotificationPage)

### 4. **ThemeProvider** (`lib/providers/theme_provider.dart`)
Gestion du thème :
- ✅ Toggle dark/light mode
- ✅ Persistance du choix
- ✅ Application globale

## 💾 Base de Données

### DatabaseHelper (`lib/db/database_helper.dart`)
SQLite local avec tables :
- `users` - Utilisateurs
- `boards` - Tableaux
- `kanban_columns` - Colonnes personnalisées
- `ideas` - Cartes/Tâches

Toutes les opérations sont asynchrones et mettent à jour l'UI automatiquement.

## 🎨 Widgets UI Dynamiques

### Composants Réutilisables :
- **Cards animées** - Toutes les cartes réagissent aux interactions
- **Dialogs modaux** - Formulaires interactifs
- **Drag & Drop** - Réorganisation fluide
- **Search Bar** - Filtrage en temps réel
- **Chips** - Tags et priorités interactifs
- **Date Pickers** - Sélection de dates
- **Progress Bars** - Barres de progression animées
- **Badges** - Indicateurs de statut et notifications
- **PopupMenus** - Menus contextuels
- **Stack avec Badge** - Notifications avec compteur (nouveau)

## 🔄 Flux de Données Dynamiques

```
User Action → Provider → Database → Provider.notifyListeners() → UI Update
```

### Exemple : Créer une carte
1. Utilisateur remplit le formulaire `AddIdeaDialog`
2. `IdeaProvider.addIdea()` est appelé
3. Carte insérée dans SQLite via `DatabaseHelper`
4. `notifyListeners()` déclenché
5. Tous les widgets qui écoutent `IdeaProvider` se mettent à jour :
   - `KanbanPageDynamic` affiche la nouvelle carte
   - `DashboardScreen` met à jour les statistiques
   - **`QuickStatsWidget` actualise les compteurs**
   - **Badge de notifications dans AppBar se met à jour**
   - **Drawer affiche les nouvelles stats**
   - `RoadmapScreen` actualise la progression

## ✅ Fonctionnalités Temps Réel

### Tout est dynamique et réactif :
- ✅ Ajout/modification/suppression de tableaux
- ✅ Ajout/modification/suppression de colonnes
- ✅ Ajout/modification/suppression de cartes
- ✅ Drag & Drop avec mise à jour de statut
- ✅ Recherche et filtrage
- ✅ **Statistiques en temps réel** (QuickStatsWidget)
- ✅ **Notifications dynamiques avec badge**
- ✅ **Statistiques dans le Drawer**
- ✅ Notifications visuelles (SnackBars)
- ✅ Toggle thème sans redémarrage
- ✅ Navigation fluide entre écrans
- ✅ Gestion des états vides (empty states)
- ✅ Validation de formulaires

## 🚀 Comment Tester

1. **Lancer l'application** :
   ```bash
   flutter run -d 9EHNW20825005405
   ```

2. **Créer un compte** ou se connecter

3. **Tester les nouvelles fonctionnalités dynamiques** :
   - **Badge de notifications** → Créer une tâche haute priorité, le badge s'affiche automatiquement
   - **QuickStatsWidget** → Visible en haut du Dashboard, se met à jour en temps réel
   - **Drawer avec stats** → Ouvrir le drawer pour voir les statistiques
   - Créer un tableau → Apparaît immédiatement dans le drawer
   - Créer des colonnes → S'affichent dans le Kanban
   - Ajouter des cartes → **Toutes les stats se mettent à jour instantanément**
   - Drag & Drop une carte → Statut change, stats se mettent à jour
   - Marquer une tâche comme terminée → Barre de progression s'anime
   - **Cliquer sur le badge de notifications** → Ouvre la NotificationPage
   - Basculer le thème → Application entière change
   - Rechercher → Résultats en temps réel

## 📊 Architecture

```
main.dart
  ├─ MultiProvider (AuthProvider, BoardProvider, IdeaProvider, ThemeProvider)
  │   └─ MaterialApp
  │       └─ AuthWrapper
  │           ├─ AuthScreen (si non connecté)
  │           └─ MainLayout (si connecté)
  │               ├─ AppBar (dynamique + Badge Notifications) ★ NOUVEAU
  │               ├─ BottomNavigationBar (navigation)
  │               ├─ Drawer (tableaux, profil + Stats) ★ AMÉLIORÉ
  │               └─ Pages dynamiques :
  │                   ├─ DashboardScreen
  │                   │   └─ QuickStatsWidget ★ NOUVEAU
  │                   ├─ KanbanPageDynamic (drag & drop)
  │                   ├─ RoadmapScreen (progression)
  │                   └─ NotificationPage ★ NOUVEAU (via AppBar)
```

## 🎯 Résumé des Améliorations

### Avant :
- Navigation basique
- Statistiques statiques
- Pas de notifications visibles
- Drawer simple

### Maintenant :
- ✅ **Badge de notifications dynamique** dans l'AppBar
- ✅ **QuickStatsWidget** avec statistiques en temps réel
- ✅ **Drawer enrichi** avec statistiques et progression
- ✅ **NotificationPage** dédiée
- ✅ **Tous les widgets** connectés aux providers
- ✅ **Mise à jour instantanée** de toute l'UI
- ✅ **Indicateurs visuels** (badges, barres de progression)
- ✅ **Architecture complètement réactive**

**Tous les widgets de votre application KANFLOW sont maintenant 100% DYNAMIQUES** et réagissent en temps réel aux actions de l'utilisateur. L'architecture Provider assure une séparation claire entre la logique métier et l'interface, permettant des mises à jour fluides et performantes de l'UI.

**Aucun widget n'est statique** - tout est réactif, connecté et se met à jour automatiquement !


## 📱 Structure de l'Application

### 1. **MainLayout** (`lib/widgets/main_layout.dart`)
Le layout principal qui contient :
- **AppBar** dynamique avec toggle de thème
- **BottomNavigationBar** pour la navigation entre les écrans
- **Drawer** pour la gestion des tableaux et du profil utilisateur
- Navigation dynamique entre Dashboard, Kanban et Roadmap

**Fonctionnalités dynamiques :**
- ✅ Création de tableaux en temps réel
- ✅ Sélection de tableaux avec mise à jour automatique
- ✅ Renommage de tableaux
- ✅ Suppression de tableaux
- ✅ Toggle thème clair/sombre
- ✅ Affichage dynamique de l'utilisateur connecté
- ✅ Déconnexion avec redirection

### 2. **DashboardScreen** (`lib/screens/dashboard_screen.dart`)
Écran de tableau de bord avec statistiques en temps réel :
- ✅ Compteur total de tâches
- ✅ Statistiques par statut (Backlog, In Progress, Done)
- ✅ Tâches en retard
- ✅ Tâches haute priorité
- ✅ Activité récente
- ✅ Graphiques de progression
- ✅ Mise à jour automatique lors de changements

### 3. **KanbanPageDynamic** (`lib/pages/kanban_page_dynamic.dart`)
Vue Kanban complètement dynamique :
- ✅ Colonnes dynamiques créées à partir de la base de données
- ✅ Ajout de nouvelles colonnes en temps réel
- ✅ Renommage de colonnes
- ✅ Suppression de colonnes
- ✅ Recherche de cartes en temps réel
- ✅ Filtrage par tags, priorité, date
- ✅ Drag & Drop entre colonnes
- ✅ Mise à jour de statut automatique

### 4. **DynamicKanbanColumn** (`lib/widgets/dynamic_kanban_column.dart`)
Colonne Kanban avec toutes les fonctionnalités :
- ✅ Affichage dynamique des cartes par statut
- ✅ Drag & Drop des cartes
- ✅ Badges de priorité (Haute/Moyenne/Basse)
- ✅ Indicateurs de date d'échéance
- ✅ Tags colorés
- ✅ Édition de cartes
- ✅ Suppression de cartes
- ✅ Compteur de cartes
- ✅ Actions contextuelles (modifier colonne, supprimer)

### 5. **AddIdeaDialog** (`lib/widgets/add_idea_dialog.dart`)
Dialogue dynamique pour créer des cartes :
- ✅ Formulaire complet avec validation
- ✅ Sélection de priorité (chips interactifs)
- ✅ Sélection de statut (dropdown)
- ✅ Date picker pour échéance
- ✅ Tags multiples
- ✅ Description riche
- ✅ Validation en temps réel
- ✅ Feedback visuel (SnackBar)

### 6. **RoadmapScreen** (`lib/screens/roadmap_screen.dart`)
Vue roadmap avec progression :
- ✅ Barre de progression globale
- ✅ Statistiques par statut
- ✅ Liste des tâches en retard (alertes)
- ✅ Tâches haute priorité
- ✅ Vue chronologique
- ✅ Mise à jour en temps réel

## 🔄 Providers (Gestion d'État)

### 1. **AuthProvider** (`lib/providers/auth_provider.dart`)
Gestion de l'authentification :
- ✅ Connexion/Inscription
- ✅ Stockage du token
- ✅ Informations utilisateur (nom, email, ID)
- ✅ Déconnexion
- ✅ Vérification d'authentification

### 2. **BoardProvider** (`lib/providers/board_provider.dart`)
Gestion des tableaux :
- ✅ Liste des tableaux par utilisateur
- ✅ Tableau sélectionné
- ✅ CRUD complet (Create, Read, Update, Delete)
- ✅ Colonnes dynamiques par tableau
- ✅ Synchronisation avec la base de données

### 3. **IdeaProvider** (`lib/providers/idea_provider.dart`)
Gestion des cartes/idées :
- ✅ Liste des cartes par tableau
- ✅ CRUD complet
- ✅ Changement de statut
- ✅ Filtrage et recherche
- ✅ Mise à jour de priorité
- ✅ Gestion des dates d'échéance

### 4. **ThemeProvider** (`lib/providers/theme_provider.dart`)
Gestion du thème :
- ✅ Toggle dark/light mode
- ✅ Persistance du choix
- ✅ Application globale

## 💾 Base de Données

### DatabaseHelper (`lib/db/database_helper.dart`)
SQLite local avec tables :
- `users` - Utilisateurs
- `boards` - Tableaux
- `kanban_columns` - Colonnes personnalisées
- `ideas` - Cartes/Tâches

Toutes les opérations sont asynchrones et mettent à jour l'UI automatiquement.

## 🎨 Widgets UI Dynamiques

### Composants Réutilisables :
- **Cards animées** - Toutes les cartes réagissent aux interactions
- **Dialogs modaux** - Formulaires interactifs
- **Drag & Drop** - Réorganisation fluide
- **Search Bar** - Filtrage en temps réel
- **Chips** - Tags et priorités interactifs
- **Date Pickers** - Sélection de dates
- **Progress Bars** - Barres de progression animées
- **Badges** - Indicateurs de statut
- **PopupMenus** - Menus contextuels

## 🔄 Flux de Données Dynamiques

```
User Action → Provider → Database → Provider.notifyListeners() → UI Update
```

### Exemple : Créer une carte
1. Utilisateur remplit le formulaire `AddIdeaDialog`
2. `IdeaProvider.addIdea()` est appelé
3. Carte insérée dans SQLite via `DatabaseHelper`
4. `notifyListeners()` déclenché
5. Tous les widgets qui écoutent `IdeaProvider` se mettent à jour :
   - `KanbanPageDynamic` affiche la nouvelle carte
   - `DashboardScreen` met à jour les statistiques
   - `RoadmapScreen` actualise la progression

## ✅ Fonctionnalités Temps Réel

### Tout est dynamique et réactif :
- ✅ Ajout/modification/suppression de tableaux
- ✅ Ajout/modification/suppression de colonnes
- ✅ Ajout/modification/suppression de cartes
- ✅ Drag & Drop avec mise à jour de statut
- ✅ Recherche et filtrage
- ✅ Statistiques en temps réel
- ✅ Notifications visuelles (SnackBars)
- ✅ Toggle thème sans redémarrage
- ✅ Navigation fluide entre écrans
- ✅ Gestion des états vides (empty states)
- ✅ Validation de formulaires

## 🚀 Comment Tester

1. **Lancer l'application** :
   ```bash
   flutter run -d windows
   ```

2. **Créer un compte** ou se connecter

3. **Tester les fonctionnalités dynamiques** :
   - Créer un tableau → Apparaît immédiatement dans le drawer
   - Créer des colonnes → S'affichent dans le Kanban
   - Ajouter des cartes → Mises à jour en temps réel
   - Drag & Drop une carte → Statut change automatiquement
   - Basculer le thème → Application entière change
   - Rechercher → Résultats en temps réel

## 📊 Architecture

```
main.dart
  ├─ MultiProvider (AuthProvider, BoardProvider, IdeaProvider, ThemeProvider)
  │   └─ MaterialApp
  │       └─ AuthWrapper
  │           ├─ AuthScreen (si non connecté)
  │           └─ MainLayout (si connecté)
  │               ├─ AppBar (dynamique)
  │               ├─ BottomNavigationBar (navigation)
  │               ├─ Drawer (tableaux, profil)
  │               └─ Pages dynamiques :
  │                   ├─ DashboardScreen (statistiques)
  │                   ├─ KanbanPageDynamic (drag & drop)
  │                   └─ RoadmapScreen (progression)
```

## 🎯 Résumé

**Tous les widgets de votre application KANFLOW sont maintenant DYNAMIQUES** et réagissent en temps réel aux actions de l'utilisateur. L'architecture Provider assure une séparation claire entre la logique métier et l'interface, permettant des mises à jour fluides et performantes de l'UI.

**Aucun widget n'est statique** - tout est réactif et connecté à la base de données !
