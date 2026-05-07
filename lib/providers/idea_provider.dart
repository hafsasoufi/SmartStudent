import 'package:flutter/material.dart';
import '../services/database_service.dart';
import 'board_provider.dart';

class IdeaProvider extends ChangeNotifier {
  final DBService _dbService = DBService();

  int? _userId;
  List<Map<String, dynamic>> ideas = [];
  Map<String, int> stats = {'Backlog': 0, 'In Progress': 0, 'Done': 0};
  List<String> activityLog = [];

  void setUserId(int? userId) {
    _userId = userId;
    if (userId != null) {
      fetchIdeas();
    } else {
      ideas = [];
      stats = {'Backlog': 0, 'In Progress': 0, 'Done': 0};
      activityLog = [];
      notifyListeners();
    }
  }

  String getUserId() {
    return _userId?.toString() ?? '';
  }

  void _addActivity(String activity) {
    activityLog.insert(0, activity);
    if (activityLog.length > 20) activityLog.removeLast();
  }

  Future<void> fetchIdeas() async {
    if (_userId == null) return;

    ideas = await _dbService.getAllIdeas(_userId!);

    // Debug: Afficher les attachments de chaque idée
    for (var idea in ideas) {
      if (idea['attachments'] != null) {
        print(
          '📎 Idea "${idea['title']}" has attachments: ${idea['attachments']}',
        );
      }
    }

    _addActivity('📋 Récupération de ${ideas.length} idées');
    await fetchStats();
    notifyListeners();
  }

  Future<void> fetchStats() async {
    if (_userId == null) return;
    stats = await _dbService.getStatsByStatus(_userId!);
    notifyListeners();
  }

  List<Map<String, dynamic>> getIdeasByStatus(String status, {int? boardId}) {
    if (boardId != null) {
      return ideas
          .where(
            (idea) => idea['status'] == status && idea['boardId'] == boardId,
          )
          .toList();
    }
    return ideas.where((idea) => idea['status'] == status).toList();
  }

  List<Map<String, dynamic>> getIdeasByBoard(int boardId) {
    return ideas.where((idea) => idea['boardId'] == boardId).toList();
  }

  Future<void> addIdea(Map<String, dynamic> idea, {BoardProvider? boardProvider}) async {
    if (_userId == null) throw Exception('User not authenticated');

    // Passer le userId comme argument séparé
    final ideaId = await _dbService.addIdea(idea, _userId!);
    final title = idea['title'] ?? 'Sans titre';
    _addActivity('✅ Carte ajoutée: $title');
    await fetchIdeas();
    
    // Sync shared boards if needed
    if (boardProvider != null && idea['boardId'] != null) {
      await boardProvider.refreshSharedBoardIfNeeded(idea['boardId'], getIdeasByBoard(idea['boardId']));
      // Also propagate changes if this board is a shared imported board
      await boardProvider.refreshSharedBoardFromSharedUser(idea['boardId'], getIdeasByBoard(idea['boardId']));
    }
    
    print('Idée ajoutée avec succès, ID: $ideaId'); // Debug
  }

  Future<void> updateIdeaStatus(int id, String newStatus, {BoardProvider? boardProvider}) async {
    if (_userId == null) throw Exception('User not authenticated');

    final idea = ideas.firstWhere((i) => i['id'] == id, orElse: () => {});
    final title = idea['title'] ?? 'Carte';
    final boardId = idea['boardId'];

    await _dbService.updateStatus(id, _userId!, newStatus);
    _addActivity('🔄 "$title" déplacée vers $newStatus');
    await fetchIdeas();
    
    // Sync shared boards if needed
    if (boardProvider != null && boardId != null) {
      await boardProvider.refreshSharedBoardIfNeeded(boardId, getIdeasByBoard(boardId));
      await boardProvider.refreshSharedBoardFromSharedUser(boardId, getIdeasByBoard(boardId));
    }
  }

  Future<void> updateIdea(int id, Map<String, dynamic> updates, {BoardProvider? boardProvider}) async {
    if (_userId == null) throw Exception('User not authenticated');

    final idea = ideas.firstWhere((i) => i['id'] == id, orElse: () => {});
    final boardId = idea['boardId'];

    await _dbService.updateIdea(id, _userId!, updates);
    await fetchIdeas();
    
    // Sync shared boards if needed
    if (boardProvider != null && boardId != null) {
      await boardProvider.refreshSharedBoardIfNeeded(boardId, getIdeasByBoard(boardId));
      await boardProvider.refreshSharedBoardFromSharedUser(boardId, getIdeasByBoard(boardId));
    }
  }

  Future<void> deleteIdea(int id, {BoardProvider? boardProvider}) async {
    if (_userId == null) throw Exception('User not authenticated');

    final idea = ideas.firstWhere((i) => i['id'] == id, orElse: () => {});
    final title = idea['title'] ?? 'Carte';
    final boardId = idea['boardId'];

    await _dbService.deleteIdea(id, _userId!);
    _addActivity('🗑️ Carte "$title" supprimée');
    await fetchIdeas();
    
    // Sync shared boards if needed
    if (boardProvider != null && boardId != null) {
      await boardProvider.refreshSharedBoardIfNeeded(boardId, getIdeasByBoard(boardId));
      await boardProvider.refreshSharedBoardFromSharedUser(boardId, getIdeasByBoard(boardId));
    }
  }

  double getProgress() {
    int total = ideas.length;
    if (total == 0) return 0.0;
    int done = ideas.where((idea) => idea['status'] == 'Done').length;
    return done / total;
  }

  // ================= VOTES =================
  Future<void> voteIdea(int id) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.voteIdea(id, _userId!);
    _addActivity('👍 Vote ajouté');
    await fetchIdeas();
  }

  Future<void> unvoteIdea(int id) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.unvoteIdea(id, _userId!);
    _addActivity('👎 Vote retiré');
    await fetchIdeas();
  }

  Future<List<Map<String, dynamic>>> getTopVotedIdeas({int limit = 10}) async {
    if (_userId == null) return [];
    return await _dbService.getTopVotedIdeas(_userId!, limit: limit);
  }

  // ================= FILTRES ET RECHERCHE =================

  /// Rechercher des idées par texte
  Future<List<Map<String, dynamic>>> searchIdeas(String query) async {
    if (_userId == null) return [];
    if (query.isEmpty) return ideas;

    final results = await _dbService.searchIdeas(_userId!, query);
    _addActivity('🔍 Recherche: "$query" (${results.length} résultats)');
    return results;
  }

  /// Filtrer par priorité
  Future<List<Map<String, dynamic>>> filterByPriority(int priority) async {
    if (_userId == null) return [];
    final results = await _dbService.getIdeasByPriority(_userId!, priority);
    _addActivity('📊 Filtré par priorité ${_getPriorityLabel(priority)}');
    return results;
  }

  /// Filtrer par catégorie
  Future<List<Map<String, dynamic>>> filterByCategory(String category) async {
    if (_userId == null) return [];
    final results = await _dbService.getIdeasByCategory(_userId!, category);
    _addActivity('🏷️ Filtré par catégorie: $category');
    return results;
  }

  /// Obtenir statistiques par catégorie
  Future<Map<String, int>> getStatsByCategory() async {
    if (_userId == null) return {};
    return await _dbService.getStatsByCategory(_userId!);
  }

  /// Obtenir statistiques par priorité
  Future<Map<String, int>> getStatsByPriority() async {
    if (_userId == null) return {};
    return await _dbService.getStatsByPriority(_userId!);
  }

  /// Obtenir l'activité récente
  Future<List<Map<String, dynamic>>> getRecentActivity({int days = 7}) async {
    if (_userId == null) return [];
    return await _dbService.getRecentActivity(_userId!, days: days);
  }

  /// Calculer le pourcentage d'avancement par catégorie
  Map<String, double> getCategoryProgress() {
    if (ideas.isEmpty) return {};

    Map<String, int> total = {};
    Map<String, int> done = {};

    for (var idea in ideas) {
      String category = idea['category']?.toString() ?? 'other';
      total[category] = (total[category] ?? 0) + 1;

      if (idea['status'] == 'Done') {
        done[category] = (done[category] ?? 0) + 1;
      }
    }

    Map<String, double> progress = {};
    for (var category in total.keys) {
      progress[category] = (done[category] ?? 0) / total[category]!;
    }

    return progress;
  }

  String _getPriorityLabel(int priority) {
    switch (priority) {
      case 2:
        return 'Haute';
      case 1:
        return 'Moyenne';
      case 0:
      default:
        return 'Basse';
    }
  }
}
