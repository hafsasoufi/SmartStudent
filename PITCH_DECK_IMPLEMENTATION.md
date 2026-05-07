# Pitch Deck Mode - Implementation Guide

## 📁 Structure des Fichiers

```
lib/
├── models/
│   └── pitch_deck.dart              # Modèles PitchDeck et PitchSlide
├── providers/
│   └── pitch_deck_provider.dart     # État global des pitch decks
├── screens/
│   └── pitch_deck_screen.dart       # Écrans du mode Pitch Deck
├── widgets/
│   └── pitch_slide_widget.dart      # Widget de slide réutilisable
└── widgets/
    └── main_layout.dart             # Intégration dans la navigation

Documentation/
├── PITCH_DECK_MODE.md               # Documentation complète
└── PITCH_DECK_QUICKSTART.md         # Guide rapide
```

---

## 🔧 Composants Clés

### 1. PitchDeck Model (`lib/models/pitch_deck.dart`)

#### Classes
- **PitchDeck** : Représente une présentation complète
  - id, ideaId, userId
  - title, subtitle, description
  - List<PitchSlide> slides
  - createdAt, updatedAt
  - targetAudience, duration

- **PitchSlide** : Représente une slide individuelle
  - type (PitchSlideType enum)
  - title, content
  - List<String> bullets

#### Enums
```dart
enum PitchSlideType { 
  title, problem, solution, market, 
  business, traction, team, closing 
}
```

#### Méthodes
- `toMap()` / `fromMap()` : Sérialisation/Désérialisation
- `PitchSlide.fromMap()` : Construction depuis données

---

### 2. PitchDeckProvider (`lib/providers/pitch_deck_provider.dart`)

#### État
```dart
List<PitchDeck> _pitchDecks    // Tous les pitches de l'utilisateur
PitchDeck? _currentPitchDeck   // Pitch en cours de visualisation
```

#### Principales Méthodes

##### Génération
```dart
PitchDeck generatePitchDeck({
  required String title,
  required String description,
  required String category,
  int? ideaId,
  required String userId,
})
```
Génère automatiquement un pitch deck complet avec 8 slides.

##### Gestion des Slides
```dart
void updateSlide(int slideIndex, PitchSlide slide)
void addCustomSlide(PitchSlide slide)
void removeSlide(int slideIndex)
```

##### Gestion des Pitches
```dart
void selectPitchDeck(PitchDeck deck)
void deletePitchDeck(int index)
List<PitchDeck> getPitchDecksByIdea(int ideaId)
List<PitchDeck> getPitchDecksByUser(String userId)
void clearSelection()
```

#### Génération Intelligente
Le système génère automatiquement des slides intelligentes basées sur :
- Titre de l'idée → Slide titre et subtitle
- Description → Contenu des slides solution/business
- Catégorie → Contexte d'industrie
- Format → 8 slides optimisées pour un pitch professionnel

---

### 3. PitchDeckScreen (`lib/screens/pitch_deck_screen.dart`)

#### Composants

##### PitchDeckScreen (StatefulWidget)
Écran principal avec deux onglets :
1. **Generate Tab** : Liste des idées avec bouton "Generate"
2. **My Decks Tab** : Liste de tous les pitches créés

**Fonctionnalités** :
- Affichage des idées disponibles
- Génération rapide avec un clic
- Gestion de l'historique des pitches
- Suppression de pitches

##### PitchDeckViewerScreen (StatefulWidget)
Visionneuse de pitch deck avec :
- PageView pour navigation slide-by-slide
- Contrôles Précédent/Suivant
- Indicateur de progression
- Bouton de partage (futur)
- Édition en ligne de chaque slide

---

### 4. PitchSlideWidget (`lib/widgets/pitch_slide_widget.dart`)

#### Modes
1. **View Mode** : Affichage formaté avec design professionnel
2. **Edit Mode** : Édition du contenu et des points clés

#### Design
- Gradient teal pour l'identité visuelle
- Slide number badge
- Formatage hiérarchique (titre > contenu > points)
- Numérotation intelligente des points clés
- Responsive et Dark Mode compatible

#### Interaction
```dart
PitchSlideWidget(
  slideIndex: 0,
  title: "Slide Title",
  content: "Main content",
  bullets: ["Point 1", "Point 2"],
  isEditable: true,
  onEdit: (content, bullets) {
    // Callback de modification
  }
)
```

---

## 🔄 Flux de Données

```
User selects Idea
    ↓
PitchDeckScreen._generateAndViewPitch()
    ↓
PitchDeckProvider.generatePitchDeck()
    ├─ Create PitchDeck instance
    ├─ Call _generateSlides()
    │   ├─ Create 8 PitchSlide objects
    │   ├─ Populate with intelligent content
    │   └─ Return List<PitchSlide>
    ├─ Add to _pitchDecks list
    ├─ Set _currentPitchDeck
    └─ notifyListeners()
    ↓
Navigate to PitchDeckViewerScreen
    ↓
Display slides with PageView
    ↓
User edits slide
    ↓
PitchSlideWidget.onEdit() callback
    ↓
PitchDeckProvider.updateSlide()
    ├─ Update slide in _currentPitchDeck
    └─ notifyListeners()
    ↓
UI rebuilds with updated content
```

---

## 🎯 Génération Intelligente de Contenu

### Processus de Génération

```dart
_generateSlides(title, description, category)
  ├─ Slide 1: Title
  │   └─ _generateSubtitle()
  ├─ Slide 2: Problem
  │   └─ _generateProblemStatement()
  ├─ Slide 3: Solution
  │   └─ description utilisateur
  ├─ Slide 4: Market
  │   └─ _generateMarketOpportunity()
  ├─ Slide 5: Business
  │   └─ _generateBusinessModel()
  ├─ Slide 6: Traction
  │   └─ Template statique
  ├─ Slide 7: Team
  │   └─ Template statique
  └─ Slide 8: Closing
      └─ Template dynamique
```

### Méthodes de Génération

```dart
String _generateSubtitle(String title)
// Crée un subtitle accrocheur

String _generateProblemStatement(String description, String category)
// Formule un problème pertinent au secteur

String _generateMarketOpportunity(String category)
// Évalue le potentiel du marché

String _generateBusinessModel(String category)
// Propose un modèle d'affaires adapté
```

---

## 🔌 Intégration dans l'Écosystème

### MainLayout Integration
```dart
// Ajout au switch de navigation
case 4:
  return const PitchDeckScreen();

// Ajout au BottomNavigationBar
const BottomNavigationBarItem(
  icon: Icon(Icons.auto_awesome),
  label: 'Pitch Deck',
)

// Import dans main_layout.dart
import '../screens/pitch_deck_screen.dart';
```

### Provider Integration
```dart
// Ajout dans main.dart
MultiProvider(
  providers: [
    // ... autres providers
    ChangeNotifierProvider(create: (_) => PitchDeckProvider()),
  ],
)
```

### IdeaProvider Integration
```dart
// Nouvelle méthode pour obtenir l'ID utilisateur
String getUserId() {
  return _userId?.toString() ?? '';
}
```

---

## 🎨 Thème et Styling

### Couleurs Principales
- Primary: Colors.teal
- Gradient: teal.shade300 → teal.shade700
- Secondary: Colors.purple (pour les decks)

### Typographie
- Font Family: Poppins
- Headlines: headlineSmall, headlineMedium
- Body: bodyLarge, bodyMedium

### Spacing
- Card margin: EdgeInsets.all(16)
- Internal padding: EdgeInsets.all(24)
- Between elements: SizedBox(height: 16/24)

---

## 📊 Données Persistantes (Futur)

### Stockage Local
À implémenter avec SQLite :
```sql
CREATE TABLE pitch_decks (
  id INTEGER PRIMARY KEY,
  idea_id INTEGER,
  user_id STRING,
  title STRING,
  subtitle STRING,
  description TEXT,
  slides JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Synchronisation Cloud
À implémenter avec Firebase/Backend :
- Sauvegarde automatique
- Partage entre appareils
- Collaboration temps réel

---

## 🚀 Performance

### Optimisations Actuelles
- Provider pour state management efficace
- PageView pour navigation fluide
- Lazy loading des slides
- Limited re-rendering avec Consumer

### Optimisations Futures
- Caching des pitch decks
- Lazy loading du contenu
- Pagination des listes
- Image compression
- Video thumbnail generation

---

## 🧪 Tests

### Tests Unitaires à Implémenter
```dart
test('generatePitchDeck creates 8 slides', () {
  // Test que 8 slides sont générées
});

test('updateSlide modifies content correctly', () {
  // Test que les modifications sont sauvegardées
});

test('getPitchDecksByUser returns correct decks', () {
  // Test le filtrage par utilisateur
});
```

### Tests d'Intégration
```dart
testWidgets('User can generate and view pitch', (WidgetTester tester) {
  // Workflow complet
});
```

---

## 🐛 Debugging

### Logs Utiles
```dart
// Dans PitchDeckProvider
print('Generated ${slides.length} slides');
print('Current deck: ${_currentPitchDeck?.title}');

// Dans PitchDeckScreen
print('Generating pitch for idea: $title');
print('Navigation to viewer');
```

### État du Provider
```dart
// Vérifier l'état
final provider = context.read<PitchDeckProvider>();
print(provider.pitchDecks.length); // Nombre de decks
print(provider.currentPitchDeck?.slides.length); // Nombre de slides
```

---

## 📚 Références

- [Dart Documentation](https://dart.dev)
- [Flutter Provider Pattern](https://pub.dev/packages/provider)
- [Material Design 3](https://m3.material.io/)
- [Pitch Deck Best Practices](https://www.pitchdeckhunt.com/)

---

## ✅ Checklist d'Implémentation

- [x] Modèles (PitchDeck, PitchSlide)
- [x] Provider (PitchDeckProvider)
- [x] Écran de génération
- [x] Visionneuse de pitches
- [x] Widget de slide avec édition
- [x] Intégration dans MainLayout
- [x] Support du Dark Mode
- [x] Responsive design
- [ ] Persistance SQLite
- [ ] Export PDF
- [ ] Export PowerPoint
- [ ] Partage via lien
- [ ] Collaboration temps réel
- [ ] Analytics

---

## 🔮 Roadmap Futur

**Phase 1** (Actuelle)
- ✅ Génération automatique
- ✅ Édition basique
- ✅ Gestion des pitches

**Phase 2** (Prochaine)
- 🔜 Export PDF/PowerPoint
- 🔜 Partage via lien
- 🔜 Templates personnalisés

**Phase 3** (À explorer)
- 🔮 AI-powered content generation
- 🔮 Prédiction de performance
- 🔮 Collaboration temps réel
- 🔮 Analytics avancées
