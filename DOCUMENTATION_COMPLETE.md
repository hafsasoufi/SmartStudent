# 🚀 Startup Launchpad - Application de Gestion de Projet

Une application Flutter complète pour gérer et organiser vos idées de startup, avec Kanban, roadmap, statistiques et bien plus.

## 📋 Fonctionnalités Implémentées

### ✅ 1. Gestion des Idées

Chaque idée contient :
- **Titre** - Le nom de l'idée
- **Description** - Détails complets de l'idée
- **Priorité** - Haute / Moyenne / Basse (avec couleurs distinctives)
- **Catégorie** - Produit, Marketing, Business, Tech, Design, Ventes, Autre
- **Date de création** - Automatiquement enregistrée
- **Date d'échéance** - Optionnelle
- **Tags** - Pour une organisation personnalisée
- **Votes** - Système de vote intégré
- **Pièces jointes** - Support d'images et PDF

#### Fonctionnalités disponibles :
- ➕ Ajouter une idée
- ✏️ Modifier une idée
- 🗑️ Supprimer une idée
- 🔍 Recherche textuelle dans titre, description et tags
- 🎯 Filtrer par priorité (Haute/Moyenne/Basse)
- 🏷️ Filtrer par catégorie
- 📊 Trier par date, priorité ou votes

**Fichier principal** : [`lib/screens/ideas_management_screen.dart`](lib/screens/ideas_management_screen.dart)

---

### ✅ 2. Kanban Board (Obligatoire)

Interface Kanban avec **3 colonnes par défaut** :
1. **Backlog** - Idées à évaluer
2. **In Progress** - En développement
3. **Done** - Terminé

#### Actions disponibles :
- 🎯 Glisser-déposer les idées entre colonnes
- 🔄 Déplacer avec boutons directionnels
- 📊 Tri automatique par priorité
- 📈 Compteurs en temps réel (ex: "5 idées en cours")
- ➕ Ajouter des colonnes personnalisées
- 🎨 Colonnes avec couleurs personnalisables

#### Interface UI :
- 🎨 Cartes colorées selon priorité (Rouge/Orange/Vert)
- 🏷️ Icônes et badges visuels par catégorie
- ✨ Animations fluides lors du déplacement
- 📱 Interface responsive

**Fichier principal** : [`lib/pages/kanban_page_dynamic.dart`](lib/pages/kanban_page_dynamic.dart)

---

### ✅ 3. Roadmap Visuelle

Section dédiée affichant :
- 🎯 **Objectifs du trimestre** - Vue Q1/Q2/Q3/Q4
- 🚀 **Fonctionnalités majeures** - Idées haute priorité
- 📅 **Échéances** - Timeline interactive
- 📊 **Progression** - Par barre et cercle de pourcentage
- ⚠️ **Alertes** - Tâches en retard surlignées

#### Dynamique :
- 🔗 Liée aux idées du Kanban
- 🔄 Mise à jour automatique en temps réel
- 📈 Suivi de progression par catégorie

**Fichier principal** : [`lib/screens/roadmap_screen.dart`](lib/screens/roadmap_screen.dart)

---

### ✅ 4. Statistiques Projet

Graphiques et visualisations avec **fl_chart** :

#### Graphiques disponibles :
1. **📊 Répartition par Statut** - Camembert (Backlog/In Progress/Done)
2. **📈 Idées par Catégorie** - Graphique en barres
3. **🎯 Distribution des Priorités** - Camembert (Haute/Moyenne/Basse)
4. **📉 Avancement Global** - Cercle de progression avec pourcentage
5. **📋 Activité Récente** - Liste des dernières actions

#### Cartes récapitulatives :
- 💡 Total d'idées
- 📦 Idées en backlog
- 🔄 Idées en cours
- ✅ Idées terminées

**Fichier principal** : [`lib/screens/statistics_screen.dart`](lib/screens/statistics_screen.dart)

---

### ✅ 5. Notifications Internes

Système de notifications intelligentes :

#### Exemples de notifications :
- 🔴 "3 tâches en priorité haute dans le backlog"
- 🎉 "Félicitations ! Vous avez terminé 80% de vos objectifs"
- ⏰ "3 échéances dans les 7 prochains jours"
- ⚠️ "5 tâches en retard"
- 🔄 "7 idées en cours - pensez à en terminer quelques-unes"

#### Affichage :
- Widget notification dans le dashboard
- SnackBar contextuelle
- Notifications inline dans les pages

**Fichier principal** : [`lib/widgets/notification_widget.dart`](lib/widgets/notification_widget.dart)

---

### ✅ 6. Stockage SQLite

**Base de données** : `kanban.db`

#### Tables principales :

##### Table `ideas` :
```sql
CREATE TABLE ideas(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT,
  priority INTEGER,
  category TEXT,              -- NOUVEAU
  tags TEXT,
  dueDate TEXT,
  attachments TEXT,
  votes INTEGER DEFAULT 0,
  boardId INTEGER NOT NULL,
  userId TEXT NOT NULL,
  createdAt TEXT,
  updatedAt TEXT,
  FOREIGN KEY (boardId) REFERENCES boards(id) ON DELETE CASCADE
)
```

##### Table `boards` :
```sql
CREATE TABLE boards(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  createdAt TEXT,
  userId TEXT NOT NULL
)
```

##### Table `kanban_columns` :
```sql
CREATE TABLE kanban_columns(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  color INTEGER,
  position INTEGER,
  boardId INTEGER NOT NULL,
  userId TEXT NOT NULL,
  FOREIGN KEY (boardId) REFERENCES boards(id) ON DELETE CASCADE
)
```

##### Table `users` :
```sql
CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT UNIQUE,
  password TEXT
)
```

#### Requêtes implémentées :
- ➕ Ajout / édition / suppression d'idées
- 🔄 Tri par priorité
- 🏷️ Regroupement par catégorie
- 📊 Mise à jour du statut
- 🔍 Recherche textuelle
- 📈 Statistiques par statut, catégorie, priorité
- 📅 Filtrage par date
- 👍 Gestion des votes

**Fichiers principaux** :
- [`lib/services/database_service.dart`](lib/services/database_service.dart)
- [`lib/db/database_helper.dart`](lib/db/database_helper.dart)

---

## 🎁 Fonctionnalités BONUS

### ✅ A. Système de Vote
- 👍 Vote/Dévote sur les idées
- 📊 Top idées les plus votées
- 📈 Tri par nombre de votes

### ✅ B. Pièces Jointes
- 📎 Ajout d'images (PNG, JPG, JPEG)
- 📄 Support de PDF
- 🗑️ Suppression de pièces jointes

### 🚧 C. Export/Import JSON (À implémenter)
Permettre de partager son plan avec d'autres utilisateurs.

### 🚧 D. Mode "Pitch Deck" (À implémenter)
Générer automatiquement un mini pitch basé sur les idées.

### 🚧 E. Timeline Animée Avancée (Partiellement implémenté)
Frise chronologique interactive dans la roadmap.

---

## 🛠️ Architecture Technique

### Structure du Projet
```
lib/
├── config/
│   └── auth_config.dart
├── db/
│   └── database_helper.dart
├── models/
│   ├── idea.dart              ✅ MODIFIÉ (ajout catégorie)
│   ├── board.dart
│   ├── kanban_column.dart
│   ├── kanban_list.dart
│   ├── task.dart
│   └── user_model.dart
├── pages/
│   └── kanban_page_dynamic.dart
├── providers/
│   ├── auth_provider.dart
│   ├── board_provider.dart
│   ├── idea_provider.dart     ✅ MODIFIÉ (ajout filtres)
│   └── theme_provider.dart
├── screens/
│   ├── ideas_management_screen.dart  ✅ NOUVEAU
│   ├── statistics_screen.dart
│   └── roadmap_screen.dart
├── services/
│   └── database_service.dart   ✅ MODIFIÉ (ajout requêtes)
├── widgets/
│   ├── add_idea_dialog.dart    ✅ MODIFIÉ (ajout catégorie)
│   ├── notification_widget.dart ✅ NOUVEAU
│   └── dynamic_kanban_column.dart
└── main.dart
```

### Technologies Utilisées

#### Dépendances principales :
- **flutter** - Framework UI
- **sqflite** ^2.3.3 - Base de données SQLite
- **provider** ^6.1.1 - State management
- **fl_chart** ^1.1.1 - Graphiques et visualisations
- **intl** ^0.19.0 - Internationalisation et formats de date
- **google_fonts** ^6.1.0 - Polices personnalisées
- **file_picker** ^10.3.8 - Sélection de fichiers
- **path_provider** ^2.1.1 - Accès aux chemins système
- **shared_preferences** ^2.5.4 - Stockage de préférences

### State Management
Le projet utilise **Provider** pour la gestion d'état :
- `IdeaProvider` - Gestion des idées
- `BoardProvider` - Gestion des tableaux Kanban
- `AuthProvider` - Authentification utilisateur
- `ThemeProvider` - Thème de l'application

### Persistence
- **SQLite** pour le stockage local
- Support hors-ligne complet
- Migration automatique de la base de données

---

## 🚀 Installation et Lancement

### Prérequis
- Flutter SDK ^3.9.2
- Dart SDK inclus avec Flutter
- Android Studio / VS Code

### Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd startuplaunchpad
```

2. **Installer les dépendances**
```bash
flutter pub get
```

3. **Lancer l'application**
```bash
# Sur émulateur/simulateur
flutter run

# Sur appareil physique
flutter run -d <device-id>

# Pour le web
flutter run -d chrome
```

### Build pour production

```bash
# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

---

## 📱 Utilisation

### 1. Connexion/Inscription
- Créez un compte ou connectez-vous
- Les données sont isolées par utilisateur

### 2. Créer des idées
- Cliquez sur le bouton "+" 
- Remplissez les informations (titre obligatoire)
- Choisissez priorité et catégorie
- Ajoutez une date d'échéance si nécessaire

### 3. Gérer le Kanban
- Glissez-déposez les idées entre colonnes
- Utilisez les boutons pour déplacer
- Créez des colonnes personnalisées

### 4. Consulter les statistiques
- Accédez à l'écran Statistiques
- Visualisez les graphiques
- Suivez votre progression

### 5. Planifier avec la Roadmap
- Ouvrez la Roadmap
- Consultez les échéances
- Suivez les objectifs trimestriels

---

## 🎨 Personnalisation

### Thèmes
Le projet supporte le mode clair et sombre via `ThemeProvider`.

### Couleurs
Les couleurs sont définies selon :
- **Rouge** - Priorité haute / Retard
- **Orange** - Priorité moyenne / En cours
- **Vert** - Priorité basse / Terminé
- **Bleu** - Tech / Information
- **Violet** - Marketing
- **Rose** - Design

### Catégories personnalisées
Modifiez `IdeaCategory` dans [`lib/models/idea.dart`](lib/models/idea.dart) pour ajouter des catégories.

---

## 🐛 Débogage

### Réinitialiser la base de données
```dart
await DBService().resetDatabase();
```

### Vérifier les logs
```bash
flutter logs
```

### Debug mode
Lancez avec :
```bash
flutter run --debug
```

---

## 📝 Contraintes Respectées

✅ **Flutter obligatoire** - Application 100% Flutter  
✅ **Persistance SQLite + services** - `database_service.dart` et `sqflite`  
✅ **Interface Kanban fluide** - Drag & drop + animations  
✅ **State management** - Provider utilisé partout  
✅ **Application hors-ligne** - Fonctionne sans connexion  
✅ **Code organisé** - Structure models/providers/views/services  

---

## 🔮 Améliorations Futures

- [ ] Export/Import JSON des projets
- [ ] Mode Pitch Deck automatique
- [ ] Synchronisation cloud
- [ ] Notifications push
- [ ] Collaboration multi-utilisateurs
- [ ] Statistiques avancées avec IA
- [ ] Timeline animée complète
- [ ] Support tablettes avec layout adaptatif
- [ ] Mode présentation full-screen
- [ ] Intégration avec calendrier

---

## 👥 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation Flutter : https://flutter.dev
- Consultez la documentation Provider : https://pub.dev/packages/provider

---

## 🙏 Remerciements

- Flutter Team pour l'excellent framework
- Provider package pour la gestion d'état
- FL Chart pour les graphiques
- SQLite pour la persistence
- Toute la communauté Flutter

---

**Version** : 1.0.0  
**Dernière mise à jour** : Décembre 2024  
**Statut** : ✅ Production Ready
