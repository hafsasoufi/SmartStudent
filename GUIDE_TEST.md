# 🧪 Guide de Test - Startup Launchpad

## 🚀 Lancement Rapide

### 1. Installation des Dépendances
```bash
flutter pub get
```

### 2. Vérification de l'Installation
```bash
flutter doctor
```

### 3. Lancement de l'Application

#### Sur Émulateur/Simulateur
```bash
flutter run
```

#### Sur Appareil Physique
```bash
# Lister les appareils connectés
flutter devices

# Lancer sur un appareil spécifique
flutter run -d <device-id>
```

#### Sur Chrome (Web)
```bash
flutter run -d chrome
```

#### Sur Windows
```bash
flutter run -d windows
```

---

## ✅ Scénarios de Test

### Test 1 : Création d'une Idée Complète

1. **Lancer l'application**
2. **Se connecter** ou créer un compte
3. **Cliquer sur le bouton ➕** dans l'interface
4. **Remplir le formulaire :**
   - Titre : "Lancer le MVP"
   - Description : "Développer la version minimale viable"
   - Priorité : Haute
   - Catégorie : Produit
   - Date d'échéance : Dans 30 jours
   - Tags : "urgent, mvp, v1"
5. **Cliquer sur "Créer"**
6. **Vérifier** que l'idée apparaît dans le Kanban (colonne Backlog)

**✅ Résultat attendu :** Idée créée avec succès, visible dans Backlog avec badge rouge (haute priorité)

---

### Test 2 : Filtrage par Catégorie

1. **Aller dans "Gestion des Idées"** (menu navigation)
2. **Créer 3 idées** :
   - Idée 1 : Catégorie "Produit"
   - Idée 2 : Catégorie "Marketing"
   - Idée 3 : Catégorie "Tech"
3. **Cliquer sur le filtre "Catégorie"**
4. **Sélectionner "Produit"**
5. **Vérifier** que seule l'idée "Produit" s'affiche

**✅ Résultat attendu :** Filtrage fonctionne, affiche uniquement les idées de la catégorie sélectionnée

---

### Test 3 : Recherche Textuelle

1. **Dans "Gestion des Idées"**
2. **Taper "MVP"** dans la barre de recherche
3. **Vérifier** que seules les idées contenant "MVP" s'affichent

**✅ Résultat attendu :** Recherche en temps réel fonctionne correctement

---

### Test 4 : Kanban Drag & Drop

1. **Aller dans le Kanban Board**
2. **Glisser une idée** de "Backlog" vers "In Progress"
3. **Vérifier** que le statut change
4. **Vérifier** que le compteur se met à jour
5. **Glisser vers "Done"**

**✅ Résultat attendu :** Glisser-déposer fluide, compteurs mis à jour, statut changé en base de données

---

### Test 5 : Statistiques

1. **Créer au moins 10 idées** avec différentes catégories et priorités
2. **Aller dans "Statistiques"**
3. **Vérifier les graphiques :**
   - Camembert par statut
   - Barres par catégorie
   - Camembert par priorité
   - Cercle de progression

**✅ Résultat attendu :** Tous les graphiques s'affichent correctement avec les bonnes données

---

### Test 6 : Roadmap

1. **Créer des idées** avec dates d'échéance :
   - Idée 1 : Échéance dans 5 jours
   - Idée 2 : Échéance dans 15 jours
   - Idée 3 : Échéance passée (hier)
2. **Aller dans "Roadmap"**
3. **Vérifier :**
   - Vue du trimestre en cours
   - Timeline des fonctionnalités
   - Échéances importantes
   - Idée en retard affichée en rouge

**✅ Résultat attendu :** Roadmap affiche correctement les échéances avec les bonnes couleurs d'alerte

---

### Test 7 : Notifications

1. **Créer 3 idées** en priorité haute dans le Backlog
2. **Créer une idée** avec échéance dans 2 jours
3. **Regarder le widget de notifications** sur le dashboard
4. **Vérifier les alertes :**
   - "3 tâches en priorité haute dans le backlog"
   - "1 échéance dans les 7 prochains jours"

**✅ Résultat attendu :** Notifications s'affichent automatiquement avec les bonnes informations

---

### Test 8 : Système de Vote

1. **Créer plusieurs idées**
2. **Cliquer sur le bouton 👍** d'une idée
3. **Vérifier** que le compteur augmente
4. **Trier par votes** dans "Gestion des Idées"
5. **Vérifier** que l'idée votée apparaît en premier

**✅ Résultat attendu :** Système de vote fonctionne, tri correct

---

### Test 9 : Pièces Jointes

1. **Créer une nouvelle idée**
2. **Cliquer sur "Ajouter des fichiers"**
3. **Sélectionner** une image PNG ou un PDF
4. **Vérifier** que le fichier apparaît dans la liste
5. **Créer l'idée**
6. **Consulter les détails** de l'idée

**✅ Résultat attendu :** Fichiers attachés correctement à l'idée

---

### Test 10 : Persistance des Données

1. **Créer 5 idées** avec différentes informations
2. **Fermer complètement l'application**
3. **Relancer l'application**
4. **Se reconnecter**
5. **Vérifier** que toutes les idées sont présentes

**✅ Résultat attendu :** Toutes les données sont sauvegardées et restaurées correctement (SQLite)

---

## 🐛 Tests de Robustesse

### Test 11 : Gestion des Erreurs

**Cas 1 : Création sans titre**
1. Essayer de créer une idée sans titre
2. **Vérifier** qu'un message d'erreur s'affiche

**Cas 2 : Recherche vide**
1. Rechercher un terme inexistant
2. **Vérifier** qu'un message "Aucune idée trouvée" s'affiche

**Cas 3 : Suppression**
1. Supprimer une idée
2. **Vérifier** qu'elle disparaît du Kanban et des statistiques

**✅ Résultat attendu :** Gestion d'erreurs propre avec messages appropriés

---

### Test 12 : Performance

1. **Créer 50+ idées**
2. **Tester** :
   - Rapidité du filtrage
   - Fluidité du drag & drop
   - Temps de chargement des statistiques
   - Navigation entre pages

**✅ Résultat attendu :** Application reste fluide même avec beaucoup de données

---

## 📱 Tests Multi-Plateforme

### Android
```bash
flutter build apk --debug
flutter install
```

### iOS (Mac uniquement)
```bash
flutter build ios --debug
```

### Web
```bash
flutter build web
cd build/web
python -m http.server 8000
# Ouvrir http://localhost:8000
```

### Windows
```bash
flutter build windows
.\build\windows\runner\Release\startuplaunchpad.exe
```

---

## 🔍 Commandes de Débogage

### Voir les Logs
```bash
flutter logs
```

### Analyser le Code
```bash
flutter analyze
```

### Formater le Code
```bash
flutter format lib/
```

### Nettoyer le Build
```bash
flutter clean
flutter pub get
```

### Inspecter la Base de Données (Debug)
Sur Android :
```bash
adb shell
cd /data/data/com.example.startuplaunchpad/databases/
sqlite3 kanban.db
.tables
SELECT * FROM ideas;
.quit
```

---

## 📊 Checklist Complète de Test

### Fonctionnalités de Base
- [ ] Inscription/Connexion
- [ ] Création d'idée
- [ ] Modification d'idée
- [ ] Suppression d'idée
- [ ] Navigation entre pages

### Gestion des Idées
- [ ] Recherche textuelle
- [ ] Filtre par priorité
- [ ] Filtre par catégorie
- [ ] Tri par date
- [ ] Tri par priorité
- [ ] Tri par votes
- [ ] Affichage des détails
- [ ] Vote sur idée

### Kanban Board
- [ ] Affichage des 3 colonnes par défaut
- [ ] Glisser-déposer entre colonnes
- [ ] Déplacement avec boutons
- [ ] Compteurs en temps réel
- [ ] Création de colonne personnalisée
- [ ] Suppression de colonne
- [ ] Couleurs personnalisables

### Roadmap
- [ ] Vue du trimestre
- [ ] Objectifs prioritaires
- [ ] Timeline des fonctionnalités
- [ ] Échéances importantes
- [ ] Indicateurs visuels (couleurs)
- [ ] Détection des retards

### Statistiques
- [ ] Graphique par statut
- [ ] Graphique par catégorie
- [ ] Graphique par priorité
- [ ] Cercle de progression
- [ ] Cartes résumé
- [ ] Activité récente

### Notifications
- [ ] Alertes priorité haute
- [ ] Messages de progression
- [ ] Alertes échéances
- [ ] Alertes retards
- [ ] Suggestions catégories

### Persistance
- [ ] Sauvegarde automatique
- [ ] Restauration après fermeture
- [ ] Migration de base de données
- [ ] Isolation par utilisateur

---

## 🎯 Critères de Réussite

Une fonctionnalité est validée si :
- ✅ Pas d'erreurs dans la console
- ✅ Interface réactive et fluide
- ✅ Données persistantes
- ✅ Comportement conforme aux attentes
- ✅ Messages d'erreur appropriés le cas échéant

---

## 📝 Rapport de Test (Modèle)

```markdown
## Test du [Date]

### Environnement
- OS : Windows/Mac/Linux
- Flutter version : [version]
- Device : [nom de l'appareil]

### Tests Effectués
1. [Nom du test] - ✅ Réussi / ❌ Échoué
2. [Nom du test] - ✅ Réussi / ❌ Échoué
3. ...

### Bugs Trouvés
1. [Description du bug]
   - Sévérité : Critique/Haute/Moyenne/Basse
   - Reproduction : [étapes]

### Améliorations Suggérées
1. [Description]
2. [Description]

### Conclusion
[Statut global : Prêt pour production / Nécessite corrections]
```

---

## 🚀 Déploiement

### Avant le Déploiement
- [ ] Tous les tests passent
- [ ] Pas d'erreurs d'analyse (`flutter analyze`)
- [ ] Code formaté (`flutter format`)
- [ ] Documentation à jour
- [ ] Version bump dans pubspec.yaml

### Commandes de Build
```bash
# Android Release
flutter build apk --release
flutter build appbundle --release

# iOS Release
flutter build ios --release

# Web Release
flutter build web --release

# Windows Release
flutter build windows --release
```

---

**Version du guide :** 1.0.0  
**Dernière mise à jour :** 28 Décembre 2024

**Bon test ! 🧪**
