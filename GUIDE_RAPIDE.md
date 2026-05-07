# 🚀 Guide de Démarrage Rapide - Startup Launchpad

## Installation Express

```bash
# 1. Installer les dépendances
flutter pub get

# 2. Lancer l'application
flutter run
```

## 🎯 Fonctionnalités Principales

### 1️⃣ Gestion des Idées

**Créer une idée :**
1. Cliquez sur le bouton ➕ 
2. Remplissez :
   - **Titre** (obligatoire)
   - **Description**
   - **Priorité** : Haute/Moyenne/Basse
   - **Catégorie** : Produit/Marketing/Business/Tech/Design/Ventes/Autre
   - **Date d'échéance** (optionnel)
   - **Tags** (optionnel)

**Filtrer les idées :**
- 🔍 Barre de recherche pour chercher dans titre/description
- 🎯 Filtre par priorité
- 🏷️ Filtre par catégorie
- 📊 Tri par date/priorité/votes

**Accès :** Menu → "Gestion des Idées"

---

### 2️⃣ Kanban Board

**Colonnes par défaut :**
- **Backlog** - Idées à évaluer
- **In Progress** - En développement  
- **Done** - Terminé

**Actions :**
- 🎯 Glisser-déposer les cartes entre colonnes
- ➡️ Boutons de déplacement rapide
- ➕ Créer des colonnes personnalisées
- 🎨 Personnaliser les couleurs

**Cartes colorées selon priorité :**
- 🔴 Rouge = Haute priorité
- 🟠 Orange = Moyenne priorité
- 🟢 Vert = Basse priorité

**Accès :** Menu → "Kanban Board"

---

### 3️⃣ Roadmap Visuelle

**Vue d'ensemble :**
- 📅 Objectifs du trimestre en cours (Q1/Q2/Q3/Q4)
- 📊 Progression globale en pourcentage
- 🎯 Objectifs prioritaires listés
- 📅 Timeline des fonctionnalités avec échéances
- ⏰ Échéances importantes à venir

**Indicateurs :**
- ✅ Vert = Terminé
- 🔵 Bleu = Dans les temps
- 🟠 Orange = Proche de l'échéance
- 🔴 Rouge = En retard

**Accès :** Menu → "Roadmap"

---

### 4️⃣ Statistiques

**Graphiques disponibles :**
1. **Camembert Statuts** - Répartition Backlog/In Progress/Done
2. **Barres Catégories** - Nombre d'idées par catégorie
3. **Camembert Priorités** - Distribution des priorités
4. **Cercle Progression** - Avancement global en %
5. **Activité Récente** - Liste des dernières actions

**Cartes résumé :**
- 💡 Total d'idées
- 📦 En backlog
- 🔄 En cours
- ✅ Terminées

**Accès :** Menu → "Statistiques"

---

### 5️⃣ Notifications

Le système vous alerte sur :
- 🔴 Tâches haute priorité en attente
- 🎉 Progression importante (> 80%)
- ⏰ Échéances dans les 7 jours
- ⚠️ Tâches en retard
- 📊 Idées sans catégorie

**Affichage :** Widget sur le dashboard et notifications inline

---

## ⚡ Raccourcis et Astuces

### Gestion Rapide
- **Double-clic** sur une carte → Détails
- **Glisser-déposer** → Changer de statut
- **Vote** → Clic sur 👍

### Organisation
- Utilisez les **tags** pour filtrer facilement
- Assignez une **catégorie** à chaque idée
- Définissez des **dates d'échéance** pour la roadmap
- Votez pour prioriser les idées importantes

### Productivité
- Consultez les **statistiques** régulièrement
- Utilisez la **roadmap** pour planifier
- Suivez les **notifications** pour ne rien manquer
- Filtrez par **priorité haute** pour les urgences

---

## 🎨 Personnalisation

### Créer une Colonne Kanban
1. Sur la page Kanban
2. Cliquez sur "Ajouter une colonne"
3. Entrez le titre et le statut
4. Choisissez une couleur
5. Validez

### Modifier une Idée
1. Cliquez sur l'idée
2. Modifier les champs souhaités
3. Sauvegardez

### Supprimer une Idée
1. Ouvrez les détails de l'idée
2. Cliquez sur "Supprimer"
3. Confirmez

---

## 📊 Structure de Base de Données

Vos données sont stockées localement dans SQLite :

**Tables :**
- `ideas` - Toutes vos idées
- `boards` - Vos tableaux Kanban
- `kanban_columns` - Colonnes personnalisées
- `users` - Comptes utilisateurs

**Emplacement :** Stockage local de l'appareil  
**Sauvegarde :** Automatique à chaque modification

---

## 🐛 Résolution de Problèmes

### L'application ne démarre pas
```bash
flutter clean
flutter pub get
flutter run
```

### Les données ne se sauvent pas
- Vérifiez que vous êtes connecté
- Redémarrez l'application

### Erreur de base de données
- L'application créera automatiquement les tables manquantes
- En cas de problème persistant, supprimez et réinstallez

### Performance lente
- Supprimez les idées anciennes et terminées
- Limitez le nombre de pièces jointes

---

## 📱 Utilisation Multi-Plateforme

### Android
- Installation APK directe
- Google Play Store (si publié)

### iOS  
- TestFlight (beta)
- App Store (si publié)

### Web
```bash
flutter run -d chrome
```
Accès via navigateur

### Desktop (Windows/Mac/Linux)
```bash
flutter run -d windows
flutter run -d macos
flutter run -d linux
```

---

## 🔐 Sécurité & Confidentialité

- ✅ Données stockées localement
- ✅ Pas de collecte de données
- ✅ Isolation par utilisateur
- ✅ Mot de passe hashé
- ✅ Fonctionne hors ligne

---

## 📈 Conseils d'Organisation

### Pour une Startup
1. **Produit** - Fonctionnalités à développer
2. **Marketing** - Campagnes et stratégies
3. **Business** - Partenariats et modèle économique
4. **Tech** - Infrastructure et optimisations

### Pour un Projet Personnel
1. Créez un board par projet
2. Utilisez les tags pour les contextes (@home, @work)
3. Définissez des échéances réalistes
4. Consultez la roadmap chaque semaine

### Pour une Équipe
1. Votez pour prioriser ensemble
2. Commentez dans les descriptions
3. Utilisez les catégories pour les responsabilités
4. Suivez les statistiques collectivement

---

## 🎓 Tutoriel Vidéo (À venir)

- Installation et configuration
- Création de la première idée
- Utilisation du Kanban
- Analyse des statistiques
- Planification avec la roadmap

---

## ✅ Checklist Première Utilisation

- [ ] Créer un compte
- [ ] Ajouter 3-5 idées
- [ ] Assigner des catégories
- [ ] Définir les priorités
- [ ] Ajouter quelques dates d'échéance
- [ ] Tester le Kanban (glisser-déposer)
- [ ] Consulter les statistiques
- [ ] Vérifier la roadmap
- [ ] Voter sur une idée
- [ ] Créer une colonne personnalisée

---

## 🚀 Prochaines Étapes

Une fois familiarisé avec l'application :
1. Explorez les filtres avancés
2. Créez des colonnes personnalisées
3. Utilisez les pièces jointes pour documenter
4. Consultez régulièrement les notifications
5. Analysez vos statistiques pour optimiser

---

## 💡 Besoin d'Aide ?

- 📖 Consultez la [Documentation Complète](DOCUMENTATION_COMPLETE.md)
- 🐛 Signalez un bug sur GitHub Issues
- 💬 Posez vos questions dans les Discussions
- 📧 Contact : [votre-email]

---

**Version** : 1.0.0  
**Dernière mise à jour** : Décembre 2024

**Bon lancement ! 🚀**
