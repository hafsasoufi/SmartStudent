# Pitch Deck Mode - Architecture Visuelle

## 🏗️ Architecture d'Application

```
┌─────────────────────────────────────────────────────────────┐
│                       MAIN APPLICATION                       │
│                    (SmartShop/Yarebi)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   MultiProvider Setup                        │
├─────────────────────────────────────────────────────────────┤
│ • AuthProvider                                               │
│ • IdeaProvider                                               │
│ • BoardProvider                                              │
│ • ThemeProvider                                              │
│ • PitchDeckProvider ✨ (NEW)                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   MainLayout (Navigation)                    │
├─────────────────────────────────────────────────────────────┤
│ BottomNavigationBar (5 Tabs):                               │
│ ├─ Dashboard (0)                                             │
│ ├─ Kanban (1)                                               │
│ ├─ Roadmap (2)                                              │
│ ├─ Statistics (3)                                           │
│ └─ Pitch Deck ✨ (4)                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Pitch Deck Navigation Flow

```
┌──────────────────────────────┐
│  PitchDeckScreen             │
│  (MainLayout case 4)         │
└──────────┬───────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────────────────────┐  ┌──────────────────────┐
│  Generate Tab           │  │  My Decks Tab        │
├─────────────────────────┤  ├──────────────────────┤
│ • List All Ideas        │  │ • List All Pitches   │
│ • Show Generate Button  │  │ • View/Edit Options  │
│ • Click to Generate     │  │ • Delete Option      │
└──────────┬──────────────┘  └──────────┬───────────┘
           │                             │
           └─────────────┬───────────────┘
                         │
                         ▼
        ┌──────────────────────────────┐
        │ PitchDeckViewerScreen        │
        ├──────────────────────────────┤
        │ • PageView for slides        │
        │ • Navigation controls        │
        │ • Progress indicator         │
        │ • Edit buttons               │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │ PitchSlideWidget             │
        ├──────────────────────────────┤
        │ • View Mode (professional)   │
        │ • Edit Mode (editable)       │
        │ • Save changes in real-time  │
        └──────────────────────────────┘
```

---

## 📊 Data Flow Architecture

```
USER ACTION
│
├─ Selects Idea from List
│  └─ Triggers: PitchDeckScreen._generateAndViewPitch()
│
▼
┌─────────────────────────────────┐
│ PitchDeckProvider.generatePitchDeck()
└──────────┬──────────────────────┘
           │
           ├─ Create PitchDeck instance
           │
           ├─ Call _generateSlides()
           │  │
           │  ├─ Slide 1: Title
           │  ├─ Slide 2: Problem (_generateProblemStatement)
           │  ├─ Slide 3: Solution (from description)
           │  ├─ Slide 4: Market (_generateMarketOpportunity)
           │  ├─ Slide 5: Business (_generateBusinessModel)
           │  ├─ Slide 6: Traction (template)
           │  ├─ Slide 7: Team (template)
           │  └─ Slide 8: Closing (template)
           │
           ├─ Add to _pitchDecks list
           ├─ Set _currentPitchDeck
           └─ notifyListeners()
                │
                ▼
        ┌──────────────────┐
        │ UI Rebuilds      │
        │ PitchDeckViewer  │
        └──────────────────┘
                │
                ▼
        USER VIEWS SLIDES
        (Navigate with Previous/Next)
                │
                ├─ Option 1: Edit a slide
                │  └─ Click edit icon
                │     └─ Toggle PitchSlideWidget to Edit Mode
                │        └─ Modify content/bullets
                │           └─ Save changes
                │              └─ PitchDeckProvider.updateSlide()
                │                 └─ notifyListeners()
                │                    └─ UI Updates
                │
                └─ Option 2: View all decks
                   └─ Tab to "My Decks"
                      └─ List all created pitches
                         └─ Select one to view/edit again
```

---

## 🗂️ Directory Structure

```
lib/
│
├── models/
│   └── pitch_deck.dart
│       ├── class PitchDeck
│       ├── class PitchSlide
│       └── enum PitchSlideType
│
├── providers/
│   ├── pitch_deck_provider.dart
│   │   └── class PitchDeckProvider (ChangeNotifier)
│   │       ├── generatePitchDeck()
│   │       ├── updateSlide()
│   │       ├── addCustomSlide()
│   │       ├── removeSlide()
│   │       └── [other methods...]
│   │
│   └── idea_provider.dart (modified)
│       └── + getUserId() method
│
├── screens/
│   ├── pitch_deck_screen.dart
│   │   ├── class PitchDeckScreen (StatefulWidget)
│   │   │   ├── _buildGenerateTab()
│   │   │   └── _buildMyDecksTab()
│   │   │
│   │   └── class PitchDeckViewerScreen (StatefulWidget)
│   │       └── Build slide viewer with PageView
│   │
│   └── [other screens...]
│
├── widgets/
│   ├── pitch_slide_widget.dart
│   │   └── class PitchSlideWidget (StatefulWidget)
│   │       ├── _buildViewMode()
│   │       └── _buildEditMode()
│   │
│   ├── main_layout.dart (modified)
│   │   └── case 4: PitchDeckScreen
│   │
│   └── [other widgets...]
│
└── main.dart (modified)
    └── + PitchDeckProvider in MultiProvider
```

---

## 🎯 Component Interaction Diagram

```
                    PitchDeckScreen
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Generate Tab    My Decks Tab      Tab Controller
   (ListView)      (ListView)         (TabBar)
        │                │
        │                └──────────────┐
        │                               │
        ▼                               ▼
  IdeaProvider                  PitchDeckProvider
  (all ideas)              (all pitch decks)
        │                               │
        │                               │
        └───────────────┬───────────────┘
                        │
                        ▼
            PitchDeckViewerScreen
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   PageView       Navigation       Progress
  (slides)        Controls          Bar
        │               │
        └─────────┬─────┘
                  │
                  ▼
          PitchSlideWidget
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
    View Mode           Edit Mode
   (display)        (TextFields)
        │                    │
        │                    └──────────┐
        │                               │
        └─────────────┬─────────────────┘
                      │
                      ▼
          onEdit Callback
                      │
                      ▼
       PitchDeckProvider.updateSlide()
                      │
                      ▼
                notifyListeners()
                      │
                      ▼
                  UI Rebuilds
```

---

## 🔐 State Management Flow

```
PitchDeckProvider (ChangeNotifier)
│
├─ _pitchDecks: List<PitchDeck>
│  └─ All pitch decks created by user
│
├─ _currentPitchDeck: PitchDeck?
│  └─ Currently viewing/editing
│
└─ Public Methods:
   │
   ├─ generatePitchDeck()
   │  ├─ Create new PitchDeck
   │  ├─ Generate 8 slides
   │  ├─ Add to _pitchDecks
   │  └─ notifyListeners() → Rebuild
   │
   ├─ updateSlide(index, slide)
   │  ├─ Modify slide at index
   │  └─ notifyListeners() → Rebuild
   │
   ├─ selectPitchDeck(deck)
   │  ├─ Set _currentPitchDeck
   │  └─ notifyListeners() → Rebuild
   │
   ├─ deletePitchDeck(index)
   │  ├─ Remove from _pitchDecks
   │  └─ notifyListeners() → Rebuild
   │
   └─ [Other getters/methods...]
```

---

## 🎨 UI Component Hierarchy

```
PitchDeckScreen
│
├─ AppBar
│  └─ TabBar (Generate | My Decks)
│
└─ TabBarView
   │
   ├─ Generate Tab (Tab 0)
   │  ├─ Header Card (teal gradient)
   │  ├─ "Available Ideas" Text
   │  └─ ListView of ideas
   │     └─ IdeaCard (repeating)
   │        ├─ Leading Icon
   │        ├─ Title
   │        ├─ Description
   │        └─ "Generate" Button
   │
   └─ My Decks Tab (Tab 1)
      └─ ListView of pitches
         └─ DeckCard (repeating)
            ├─ Leading Icon
            ├─ Title
            ├─ Info (slides count, date)
            └─ Popup Menu

PitchDeckViewerScreen
│
├─ AppBar
│  └─ Share button
│
├─ Progress Section
│  ├─ "Slide X of Y" text
│  └─ Progress bar
│
├─ PageView
│  └─ PitchSlideWidget (repeating)
│     ├─ View Mode (default)
│     │  ├─ Badge (Slide #)
│     │  ├─ Title (large)
│     │  ├─ Content (formatted)
│     │  ├─ Bullets (numbered)
│     │  └─ Edit button
│     │
│     └─ Edit Mode (when edit clicked)
│        ├─ Title bar with close
│        ├─ Content TextEdit
│        ├─ Bullet TextEdits
│        └─ Save button
│
└─ Navigation Controls
   ├─ Previous button
   └─ Next button
```

---

## 🔄 Complete User Journey

```
START
  │
  ▼
┌─────────────────────────┐
│ User Opens App          │
│ Views Dashboard/Kanban  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Tap "Pitch Deck" Tab    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Generate Tab (default)  │
│ Shows all ideas         │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Select Idea → Click     │
│ "Generate"              │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ System generates:       │
│ • 8 slides             │
│ • Smart content        │
│ • Professional format  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Pitch Viewer Opens      │
│ Shows Slide 1           │
└──────────┬──────────────┘
           │
    ┌──────┴────────────────────┐
    │                           │
    ▼                           ▼
┌─────────────┐        ┌──────────────────┐
│ Navigate    │        │ Edit Slides      │
│ slides with │        │ • Click edit btn │
│ Prev/Next   │        │ • Modify content │
│             │        │ • Save changes   │
└──────┬──────┘        └──────┬───────────┘
       │                      │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ View "My Decks" Tab  │
       │ See all pitches      │
       └──────────┬───────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
    ┌──────────┐      ┌──────────┐
    │ Select   │      │ Delete   │
    │ View     │      │ Old      │
    │ Again    │      │ Pitches  │
    └──────────┘      └──────────┘
         │                 │
         └────────┬────────┘
                  │
                  ▼
              SUCCESS
```

---

## 📱 Responsive Design

```
DESKTOP (Wide Screen)
┌────────────────────────────────────┐
│ AppBar with large icons             │
├────────────────────────────────────┤
│  Slide content full width           │
│  ┌──────────────────────────────┐   │
│  │                              │   │
│  │   Slide Title (Large)        │   │
│  │                              │   │
│  │   Content Text               │   │
│  │                              │   │
│  │   • Bullet 1                 │   │
│  │   • Bullet 2                 │   │
│  │   • Bullet 3                 │   │
│  │                              │   │
│  └──────────────────────────────┘   │
├────────────────────────────────────┤
│ [Previous] [Progress] [Next]        │
└────────────────────────────────────┘

TABLET (Medium Screen)
┌──────────────────────────┐
│ AppBar                    │
├──────────────────────────┤
│  Slide content            │
│  (slightly smaller)       │
├──────────────────────────┤
│ Navigation buttons        │
└──────────────────────────┘

MOBILE (Small Screen)
┌──────────────┐
│ AppBar       │
├──────────────┤
│ Progress     │
│ Slide        │
│ content      │
│ (compact)    │
├──────────────┤
│ Navigation   │
└──────────────┘
```

---

## 🎯 Integration Points

```
Other Components          PitchDeck Mode
─────────────────         ──────────────
Dashboard        ──────►  Generate Ideas List
  ↓                       (from IdeaProvider)
Ideas List       ◄──────  Navigation Flow
  ↓
Kanban Board     ──────►  (Future: Quick Generate)
  ↓
Theme Provider   ◄──────  Dark Mode Support
  ↓
Auth Provider    ◄──────  User ID
  ↓
ID Provider      ────────► Idea Details
```

---

## 🏁 Summary

La architecture Pitch Deck est :
- ✅ **Modulaire** : Composants indépendants et réutilisables
- ✅ **Scalable** : Facile d'ajouter de nouvelles fonctionnalités
- ✅ **Maintenable** : Code bien organisé et documenté
- ✅ **Performant** : Provider pattern pour state management efficace
- ✅ **User-Friendly** : UX intuitive et réactive
