# 📚 Index des Fichiers - Startup Launchpad

## 📖 Documentation (Lisez en premier !)

| Fichier | Description | Priorité |
|---------|-------------|----------|
| [SYNTHESE_FINALE.md](SYNTHESE_FINALE.md) | 🏆 Vue d'ensemble complète du projet | ⭐⭐⭐⭐⭐ |
| [GUIDE_RAPIDE.md](GUIDE_RAPIDE.md) | 🚀 Démarrage rapide et utilisation | ⭐⭐⭐⭐⭐ |
| [DOCUMENTATION_COMPLETE.md](DOCUMENTATION_COMPLETE.md) | 📖 Documentation technique complète | ⭐⭐⭐⭐ |
| [GUIDE_TEST.md](GUIDE_TEST.md) | 🧪 Scénarios de test détaillés | ⭐⭐⭐⭐ |
| [RECAP_MODIFICATIONS.md](RECAP_MODIFICATIONS.md) | 📝 Récapitulatif de toutes les modifications | ⭐⭐⭐ |
| [COMMANDES_UTILES.md](COMMANDES_UTILES.md) | ⚡ Toutes les commandes Flutter utiles | ⭐⭐⭐ |

---

## 🏗️ Structure du Projet

### Configuration Racine

| Fichier | Description |
|---------|-------------|
| `pubspec.yaml` | Configuration du projet et dépendances |
| `analysis_options.yaml` | Configuration du linter Dart |
| `README.md` | README original du projet |

---

## 📱 Code Source Principal

### Modèles (Models)

| Fichier | Description | Modifié |
|---------|-------------|---------|
| `lib/models/idea.dart` | Modèle Idea avec catégorie et votes | ✅ OUI |
| `lib/models/board.dart` | Modèle Board (tableau Kanban) | ❌ NON |
| `lib/models/kanban_column.dart` | Modèle KanbanColumn | ❌ NON |
| `lib/models/kanban_list.dart` | Modèle KanbanList | ❌ NON |
| `lib/models/task.dart` | Modèle Task | ❌ NON |
| `lib/models/user_model.dart` | Modèle User | ❌ NON |
| `lib/models/checklist_item.dart` | Modèle ChecklistItem | ❌ NON |

**Modifications importantes :**
- ✅ `idea.dart` : Ajout de `IdeaCategory`, `category`, `votes`, `updatedAt`

---

### Services

| Fichier | Description | Modifié |
|---------|-------------|---------|
| `lib/services/database_service.dart` | Service SQLite principal | ✅ OUI |
| `lib/db/database_helper.dart` | Helper base de données | ❌ NON |

**Modifications importantes :**
- ✅ `database_service.dart` : 
  - Ajout colonne `category` dans table `ideas`
  - Ajout méthodes de filtrage (searchIdeas, getIdeasByPriority, etc.)
  - Ajout méthodes de statistiques par catégorie/priorité
  - Ajout getRecentActivity()

---

### Providers (State Management)

| Fichier | Description | Modifié |
|---------|-------------|---------|
| `lib/providers/idea_provider.dart` | Provider pour idées | ✅ OUI |
| `lib/providers/board_provider.dart` | Provider pour boards | ❌ NON |
| `lib/providers/auth_provider.dart` | Provider authentification | ❌ NON |
| `lib/providers/theme_provider.dart` | Provider thème | ❌ NON |

**Modifications importantes :**
- ✅ `idea_provider.dart` :
  - Ajout searchIdeas()
  - Ajout filterByPriority()
  - Ajout filterByCategory()
  - Ajout getStatsByCategory()
  - Ajout getStatsByPriority()
  - Ajout getRecentActivity()
  - Ajout getCategoryProgress()

---

### Écrans (Screens)

| Fichier | Description | Créé/Modifié |
|---------|-------------|--------------|
| `lib/screens/ideas_management_screen.dart` | Page gestion des idées avec filtres | 🆕 NOUVEAU |
| `lib/screens/statistics_screen.dart` | Page statistiques avec graphiques | ❌ EXISTANT |
| `lib/screens/roadmap_screen.dart` | Page roadmap visuelle | ❌ EXISTANT |
| `lib/screens/...` | Autres écrans existants | ❌ EXISTANTS |

**Nouveaux écrans :**
- 🆕 `ideas_management_screen.dart` : 
  - Interface complète de gestion des idées
  - Recherche textuelle en temps réel
  - Filtres par priorité et catégorie
  - Tri par date/priorité/votes
  - Affichage sous forme de cartes colorées
  - Vote sur idées
  - Suppression d'idées

---

### Pages

| Fichier | Description | Modifié |
|---------|-------------|---------|
| `lib/pages/kanban_page_dynamic.dart` | Page Kanban dynamique | ❌ NON |

---

### Widgets

| Fichier | Description | Créé/Modifié |
|---------|-------------|--------------|
| `lib/widgets/add_idea_dialog.dart` | Dialog ajout/édition idée | ✅ MODIFIÉ |
| `lib/widgets/notification_widget.dart` | Widget de notifications | 🆕 NOUVEAU |
| `lib/widgets/dynamic_kanban_column.dart` | Colonne Kanban dynamique | ❌ EXISTANT |
| `lib/widgets/...` | Autres widgets existants | ❌ EXISTANTS |

**Modifications importantes :**
- ✅ `add_idea_dialog.dart` :
  - Ajout sélecteur de catégorie avec icônes
  - Liste _categories avec 7 catégories
  - Inclusion de la catégorie lors de la création

**Nouveaux widgets :**
- 🆕 `notification_widget.dart` :
  - NotificationWidget principal
  - InlineNotification pour notifications inline
  - NotificationService pour gestion des notifications
  - Génération automatique de notifications intelligentes

---

### Configuration

| Fichier | Description |
|---------|-------------|
| `lib/config/auth_config.dart` | Configuration authentification |

---

## 🎨 Assets et Resources

### Android
- `android/app/src/main/AndroidManifest.xml`
- `android/app/build.gradle.kts`
- `android/build.gradle.kts`

### iOS
- `ios/Runner/Info.plist`
- `ios/Runner/AppDelegate.swift`

### Web
- `web/index.html`
- `web/manifest.json`

### Windows
- `windows/runner/`

### macOS
- `macos/Runner/`

### Linux
- `linux/runner/`

---

## 🧪 Tests

| Fichier | Description |
|---------|-------------|
| `test/widget_test.dart` | Tests de widgets (à compléter) |

---

## 📊 Fichiers Générés (Build)

| Dossier | Description | À ignorer |
|---------|-------------|-----------|
| `build/` | Fichiers de build compilés | ✅ |
| `.dart_tool/` | Outils Dart | ✅ |
| `.idea/` | Configuration IDE | ✅ |
| `.vscode/` | Configuration VS Code | ✅ |

---

## 🔑 Fichiers Clés par Fonctionnalité

### Gestion des Idées
1. `lib/models/idea.dart` - Modèle avec catégorie
2. `lib/screens/ideas_management_screen.dart` - Interface utilisateur
3. `lib/widgets/add_idea_dialog.dart` - Formulaire de création
4. `lib/providers/idea_provider.dart` - Logique métier
5. `lib/services/database_service.dart` - Persistance

### Kanban Board
1. `lib/pages/kanban_page_dynamic.dart` - Interface Kanban
2. `lib/widgets/dynamic_kanban_column.dart` - Colonnes
3. `lib/models/kanban_column.dart` - Modèle colonne

### Statistiques
1. `lib/screens/statistics_screen.dart` - Graphiques
2. `lib/providers/idea_provider.dart` - Calculs stats
3. `lib/services/database_service.dart` - Requêtes stats

### Roadmap
1. `lib/screens/roadmap_screen.dart` - Interface roadmap
2. `lib/providers/idea_provider.dart` - Données

### Notifications
1. `lib/widgets/notification_widget.dart` - Tout le système

### Base de Données
1. `lib/services/database_service.dart` - Service principal
2. `lib/db/database_helper.dart` - Helper

---

## 📈 Flux de Données

```
User Interface (Screens/Pages)
       ↓
   Providers (State Management)
       ↓
   Services (Business Logic)
       ↓
   Database (SQLite)
```

### Exemple : Créer une Idée
1. User → `add_idea_dialog.dart` (remplit le formulaire)
2. Dialog → `idea_provider.dart` (appelle addIdea())
3. Provider → `database_service.dart` (appelle addIdea())
4. Service → SQLite (INSERT INTO ideas)
5. Service → Provider (confirme succès)
6. Provider → UI (notifyListeners())
7. UI → User (affiche la nouvelle idée)

---

## 🔍 Trouver un Fichier

### Par Fonctionnalité

**Besoin de modifier les catégories ?**
→ `lib/models/idea.dart` (enum IdeaCategory)

**Besoin d'ajouter un filtre ?**
→ `lib/screens/ideas_management_screen.dart` (méthode _getFilteredIdeas)

**Besoin de changer le schéma de la base ?**
→ `lib/services/database_service.dart` (méthode _onCreate)

**Besoin d'ajouter un graphique ?**
→ `lib/screens/statistics_screen.dart`

**Besoin de modifier les notifications ?**
→ `lib/widgets/notification_widget.dart` (méthode _generateNotifications)

**Besoin de modifier le Kanban ?**
→ `lib/pages/kanban_page_dynamic.dart`

---

## 📦 Dépendances Importantes

| Package | Version | Usage |
|---------|---------|-------|
| provider | ^6.1.1 | State management |
| sqflite | ^2.3.3 | Base de données SQLite |
| fl_chart | ^1.1.1 | Graphiques statistiques |
| intl | ^0.19.0 | Formats dates/nombres |
| file_picker | ^10.3.8 | Sélection fichiers |
| path_provider | ^2.1.1 | Chemins système |
| shared_preferences | ^2.5.4 | Préférences stockées |
| google_fonts | ^6.1.0 | Polices personnalisées |

---

## 🎯 Parcours Recommandé pour Comprendre le Code

### Pour un Débutant
1. Lire [GUIDE_RAPIDE.md](GUIDE_RAPIDE.md)
2. Regarder `lib/main.dart`
3. Explorer `lib/models/idea.dart`
4. Lire `lib/screens/ideas_management_screen.dart`
5. Comprendre `lib/providers/idea_provider.dart`

### Pour un Développeur
1. Lire [DOCUMENTATION_COMPLETE.md](DOCUMENTATION_COMPLETE.md)
2. Analyser l'architecture dans `lib/`
3. Étudier `lib/services/database_service.dart`
4. Examiner les providers
5. Tester avec [GUIDE_TEST.md](GUIDE_TEST.md)

### Pour un Reviewer
1. Lire [SYNTHESE_FINALE.md](SYNTHESE_FINALE.md)
2. Consulter [RECAP_MODIFICATIONS.md](RECAP_MODIFICATIONS.md)
3. Vérifier les fichiers modifiés marqués ✅
4. Tester les fonctionnalités principales
5. Valider avec [GUIDE_TEST.md](GUIDE_TEST.md)

---

## 🚀 Quick Start

### Pour Lancer l'App
```bash
# 1. Lire
GUIDE_RAPIDE.md

# 2. Installer
flutter pub get

# 3. Lancer
flutter run
```

### Pour Comprendre le Code
```bash
# 1. Lire
DOCUMENTATION_COMPLETE.md

# 2. Explorer
lib/models/idea.dart
lib/screens/ideas_management_screen.dart
lib/providers/idea_provider.dart
```

### Pour Tester
```bash
# 1. Lire
GUIDE_TEST.md

# 2. Tester chaque scénario
```

---

## 📞 Aide Contextuelle

### "Je veux ajouter une fonctionnalité"
1. Lire [DOCUMENTATION_COMPLETE.md](DOCUMENTATION_COMPLETE.md) - Section Architecture
2. Identifier le fichier à modifier dans cet index
3. Consulter les providers et services correspondants

### "J'ai un bug"
1. Consulter [COMMANDES_UTILES.md](COMMANDES_UTILES.md) - Section Débogage
2. Vérifier les logs avec `flutter logs`
3. Analyser avec `flutter analyze`

### "Je veux comprendre une fonctionnalité"
1. Trouver le fichier dans cet index
2. Lire les commentaires dans le code
3. Consulter [DOCUMENTATION_COMPLETE.md](DOCUMENTATION_COMPLETE.md)

---

## ✅ Checklist Fichiers Importants

### Avant de Modifier le Code
- [ ] Lire la documentation correspondante
- [ ] Comprendre le flux de données
- [ ] Vérifier les dépendances

### Avant de Commiter
- [ ] `flutter analyze` sans erreur
- [ ] `flutter format lib/` exécuté
- [ ] Tests passent (si existants)
- [ ] Documentation mise à jour si nécessaire

---

## 🎓 Ressources d'Apprentissage

### Documentation Officielle
- Flutter : https://flutter.dev/docs
- Provider : https://pub.dev/packages/provider
- SQLite : https://pub.dev/packages/sqflite
- FL Chart : https://pub.dev/packages/fl_chart

### Dans le Projet
- [DOCUMENTATION_COMPLETE.md](DOCUMENTATION_COMPLETE.md) - Tout sur l'app
- [GUIDE_RAPIDE.md](GUIDE_RAPIDE.md) - Utilisation pratique
- [GUIDE_TEST.md](GUIDE_TEST.md) - Scénarios de test
- [COMMANDES_UTILES.md](COMMANDES_UTILES.md) - Commandes Flutter

---

**Version :** 1.0.0  
**Dernière mise à jour :** 28 Décembre 2024

**Navigation facilitée dans le projet ! 📚**
