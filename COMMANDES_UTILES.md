# ⚡ Commandes Utiles - Startup Launchpad

## 🚀 Installation et Lancement

### Installation Initiale
```bash
# Installer les dépendances
flutter pub get

# Vérifier l'installation Flutter
flutter doctor

# Vérifier qu'il n'y a pas d'erreurs
flutter analyze
```

### Lancement Rapide
```bash
# Lancer sur émulateur/appareil par défaut
flutter run

# Lancer en mode debug avec hot reload
flutter run --debug

# Lancer en mode release (optimisé)
flutter run --release
```

### Lancement sur Plateformes Spécifiques
```bash
# Android
flutter run -d <android-device-id>

# iOS (Mac uniquement)
flutter run -d <ios-device-id>

# Chrome (Web)
flutter run -d chrome

# Edge (Web)
flutter run -d edge

# Windows Desktop
flutter run -d windows

# macOS Desktop
flutter run -d macos

# Linux Desktop
flutter run -d linux
```

---

## 📱 Gestion des Appareils

```bash
# Lister tous les appareils connectés
flutter devices

# Lister les émulateurs disponibles
flutter emulators

# Lancer un émulateur
flutter emulators --launch <emulator-id>
```

---

## 🔨 Build et Compilation

### Android
```bash
# APK Debug
flutter build apk --debug

# APK Release
flutter build apk --release

# APK Split per ABI (plus petit)
flutter build apk --split-per-abi

# App Bundle (pour Google Play)
flutter build appbundle --release

# Installer l'APK
flutter install
```

### iOS (Mac uniquement)
```bash
# Build iOS
flutter build ios --release

# Build avec configuration spécifique
flutter build ios --release --flavor production
```

### Web
```bash
# Build Web
flutter build web

# Build Web avec optimisations
flutter build web --release

# Servir localement (pour tester)
cd build/web
python -m http.server 8000
# Ouvrir http://localhost:8000
```

### Desktop

#### Windows
```bash
# Build Windows
flutter build windows --release

# Lancer l'exécutable
.\build\windows\runner\Release\startuplaunchpad.exe
```

#### macOS
```bash
# Build macOS
flutter build macos --release

# Lancer l'application
open build/macos/Build/Products/Release/startuplaunchpad.app
```

#### Linux
```bash
# Build Linux
flutter build linux --release

# Lancer l'exécutable
./build/linux/release/bundle/startuplaunchpad
```

---

## 🧹 Nettoyage et Maintenance

```bash
# Nettoyer les builds
flutter clean

# Nettoyer et réinstaller les dépendances
flutter clean && flutter pub get

# Mettre à jour les dépendances
flutter pub upgrade

# Mettre à jour Flutter
flutter upgrade

# Vérifier les versions
flutter --version
dart --version
```

---

## 🐛 Débogage et Logs

```bash
# Voir les logs en temps réel
flutter logs

# Logs pour un appareil spécifique
flutter logs -d <device-id>

# Analyser le code (linter)
flutter analyze

# Analyser avec détails
flutter analyze --verbose

# Formater le code
flutter format lib/

# Formater avec --set-exit-if-changed (pour CI)
flutter format --set-exit-if-changed lib/
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
flutter test

# Lancer un fichier de test spécifique
flutter test test/widget_test.dart

# Tests avec couverture
flutter test --coverage

# Voir le rapport de couverture
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

## 📦 Gestion des Dépendances

```bash
# Ajouter une dépendance
flutter pub add <package_name>

# Ajouter une dépendance de développement
flutter pub add --dev <package_name>

# Retirer une dépendance
flutter pub remove <package_name>

# Lister les dépendances obsolètes
flutter pub outdated

# Mettre à jour toutes les dépendances
flutter pub upgrade

# Mettre à jour vers les dernières versions majeures
flutter pub upgrade --major-versions

# Récupérer les dépendances sans les mettre à jour
flutter pub get
```

---

## 🔍 Inspection et Profiling

```bash
# Ouvrir DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Profiler les performances
flutter run --profile

# Tracer les performances
flutter run --trace-startup

# Mesurer la taille de l'APK
flutter build apk --analyze-size
flutter build appbundle --analyze-size

# Mesurer la taille de l'app iOS
flutter build ios --analyze-size
```

---

## 📊 Analyse de Code

```bash
# Analyse statique
flutter analyze

# Rechercher des dépendances inutilisées
flutter pub deps

# Voir l'arbre des dépendances
flutter pub deps --style=tree

# Vérifier la sécurité des dépendances
flutter pub audit
```

---

## 🗄️ Base de Données SQLite

### Android
```bash
# Se connecter via ADB
adb shell

# Naviguer vers la base
cd /data/data/com.example.startuplaunchpad/databases/

# Ouvrir SQLite
sqlite3 kanban.db

# Commandes SQLite utiles
.tables                    # Lister les tables
.schema ideas             # Voir le schéma d'une table
SELECT * FROM ideas;      # Voir toutes les idées
SELECT * FROM ideas WHERE category='product';  # Filtrer
.quit                     # Quitter
```

### Extraire la base pour analyse
```bash
# Android
adb pull /data/data/com.example.startuplaunchpad/databases/kanban.db ./

# Analyser localement
sqlite3 kanban.db
```

---

## 🌐 Web Spécifique

```bash
# Lancer sur Chrome avec hot reload
flutter run -d chrome

# Build pour production
flutter build web --release

# Build avec web renderer spécifique
flutter build web --web-renderer canvaskit  # Meilleure performance
flutter build web --web-renderer html       # Plus compatible

# Servir localement
cd build/web
python3 -m http.server 8080
```

---

## 📱 Android Spécifique

```bash
# Lister les appareils Android
adb devices

# Installer l'APK manuellement
adb install build/app/outputs/flutter-apk/app-release.apk

# Désinstaller l'app
adb uninstall com.example.startuplaunchpad

# Voir les logs Android
adb logcat | grep flutter

# Nettoyer les logs
adb logcat -c

# Capturer un screenshot
adb shell screencap /sdcard/screen.png
adb pull /sdcard/screen.png
```

---

## 🍎 iOS Spécifique (Mac uniquement)

```bash
# Ouvrir le projet iOS dans Xcode
open ios/Runner.xcworkspace

# Lister les simulateurs
xcrun simctl list devices

# Démarrer un simulateur
xcrun simctl boot "iPhone 14 Pro"

# Installer sur simulateur
flutter install -d <simulator-id>

# Nettoyer le build iOS
cd ios
pod deintegrate
pod install
cd ..
flutter clean
```

---

## 🎨 Génération d'Assets

```bash
# Générer les icônes (si vous utilisez flutter_launcher_icons)
flutter pub run flutter_launcher_icons:main

# Générer le splash screen (si vous utilisez flutter_native_splash)
flutter pub run flutter_native_splash:create
```

---

## 📝 Scripts Personnalisés

### Script de Build Complet (bash/PowerShell)

#### PowerShell (Windows)
```powershell
# build-all.ps1
flutter clean
flutter pub get
flutter analyze
flutter test
flutter build apk --release
flutter build windows --release
Write-Host "Build terminé !"
```

#### Bash (Mac/Linux)
```bash
# build-all.sh
#!/bin/bash
flutter clean
flutter pub get
flutter analyze
flutter test
flutter build apk --release
echo "Build terminé !"
```

---

## 🚀 Déploiement

### Google Play Store
```bash
# 1. Build App Bundle
flutter build appbundle --release

# 2. Le fichier est dans:
# build/app/outputs/bundle/release/app-release.aab

# 3. Télécharger sur Google Play Console
```

### Apple App Store
```bash
# 1. Build pour iOS
flutter build ios --release

# 2. Ouvrir dans Xcode
open ios/Runner.xcworkspace

# 3. Archive et upload via Xcode
```

### Web Hosting
```bash
# 1. Build Web
flutter build web --release

# 2. Déployer build/web/ sur votre hébergeur
# Firebase Hosting
firebase deploy --only hosting

# Netlify
netlify deploy --prod --dir=build/web

# Vercel
vercel --prod build/web
```

---

## 🔧 Dépannage Rapide

### Problème de Build
```bash
flutter clean
flutter pub get
flutter pub upgrade
flutter doctor
```

### Problème de Dépendances
```bash
rm pubspec.lock
flutter pub get
```

### Problème Android
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
```

### Problème iOS
```bash
cd ios
pod deintegrate
pod install
cd ..
flutter clean
flutter pub get
```

### Réinitialiser Flutter
```bash
flutter channel stable
flutter upgrade --force
flutter doctor
```

---

## 📚 Documentation

```bash
# Générer la documentation du code
dart doc .

# Ouvrir la documentation
open doc/api/index.html
```

---

## 🎯 Commandes de Développement Quotidiennes

```bash
# Matin - Démarrer le dev
flutter pub get
flutter run

# Pendant le dev - Vérifier le code
flutter analyze
flutter format lib/

# Avant commit - Tests
flutter test
flutter analyze

# Fin de journée - Build test
flutter build apk --debug
```

---

## 💡 Astuces

### Hot Reload vs Hot Restart
```
Hot Reload : r       (dans le terminal)
Hot Restart : R      (dans le terminal)
Quit : q             (dans le terminal)
```

### DevTools
```bash
# Dans le terminal après flutter run, taper 'v' pour ouvrir DevTools
v
```

### Performance Overlay
```bash
# Afficher l'overlay de performance
flutter run --profile
# Dans l'app : Appuyer sur 'P'
```

---

## 🔐 Variables d'Environnement

```bash
# Définir le SDK Flutter
export FLUTTER_SDK=/path/to/flutter
export PATH=$PATH:$FLUTTER_SDK/bin

# Définir le SDK Android
export ANDROID_SDK_ROOT=/path/to/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
```

---

## 📊 CI/CD Commandes

### GitHub Actions
```yaml
# .github/workflows/build.yml
- run: flutter pub get
- run: flutter analyze
- run: flutter test
- run: flutter build apk --release
```

### GitLab CI
```yaml
# .gitlab-ci.yml
script:
  - flutter pub get
  - flutter analyze
  - flutter test
  - flutter build apk --release
```

---

**Version :** 1.0.0  
**Dernière mise à jour :** 28 Décembre 2024

**Commandes essentielles pour le développement Flutter !** ⚡
