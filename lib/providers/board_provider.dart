import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:async';
import '../services/database_service.dart';

class BoardProvider extends ChangeNotifier {
  final DBService _dbService = DBService();

  int? _userId;
  List<Map<String, dynamic>> boards = [];
  int? _selectedBoardId;
  List<Map<String, dynamic>> columns = [];
  Timer? _sharedPollingTimer;
  final Map<int, String> _ownerJsonCache = {};

  int? get selectedBoardId => _selectedBoardId;

  void setUserId(int? userId) {
    _userId = userId;
    if (userId != null) {
      fetchBoards();
      // Start polling for shared board updates for this user
      // Note: caller should call startSharedBoardsPolling(email, userId) after login
    } else {
      boards = [];
      columns = [];
      _selectedBoardId = null;
      notifyListeners();
    }
  }

  /// Démarrer le polling des tableaux partagés (appelé après login)
  void startSharedBoardsPolling(String email, int userId, {Duration interval = const Duration(seconds: 10)}) {
    stopSharedBoardsPolling();
    _sharedPollingTimer = Timer.periodic(interval, (_) async {
      await _checkForSharedUpdates(email, userId);
    });
  }

  /// Arrêter le polling
  void stopSharedBoardsPolling() {
    _sharedPollingTimer?.cancel();
    _sharedPollingTimer = null;
  }

  Future<void> _checkForSharedUpdates(String email, int userId) async {
    if (_userId == null) return;
    try {
      final db = DBService();
      final sharedList = await db.getSharedBoardsForEmail(email);
      for (var row in sharedList) {
        final ownerBoardId = row['board_id'] as int? ?? 0;
        final ownerJson = row['board_json'] as String? ?? '';

        // Find mapping to our local imported board
        final syncRows = await db.getSharedBoardSyncByOwnerBoardIdAndEmail(ownerBoardId, email);
        if (syncRows.isEmpty) continue;
        final sharedUserBoardId = syncRows.first['shared_user_board_id'] as int? ?? 0;
        if (sharedUserBoardId == 0) continue;

        // Compare cached owner json to detect changes
        final previous = _ownerJsonCache[ownerBoardId];
        if (previous == ownerJson) continue; // no change

        // Update local imported board with ownerJson
        final updated = await db.updateImportedBoard(sharedUserBoardId, ownerJson, userId);
        if (updated > 0) {
          _ownerJsonCache[ownerBoardId] = ownerJson;
          await fetchBoards();
          await fetchColumns();
        }
      }
    } catch (e) {
      print('Error checking shared updates: $e');
    }
  }

  Future<void> fetchBoards() async {
    if (_userId == null) return;
    boards = await _dbService.getAllBoards(_userId!);
    _selectedBoardId ??= boards.isNotEmpty ? boards.first['id'] : null;
    notifyListeners();
  }

  Future<void> addBoard(Map<String, dynamic> board) async {
    if (_userId == null) throw Exception('User not authenticated');
    final id = await _dbService.addBoard(board, _userId!);
    _selectedBoardId = id;

    // Créer les colonnes par défaut
    await _createDefaultColumns(id);

    await fetchBoards();
    await fetchColumns();
  }

  Future<void> _createDefaultColumns(int boardId) async {
    if (_userId == null) return;

    // Colonnes par défaut pour un tableau Kanban
    final defaultColumns = [
      {
        'boardId': boardId,
        'title': 'Backlog',
        'status': 'Backlog',
        'color': 0xFF9E9E9E, // Grey
        'position': 0,
      },
      {
        'boardId': boardId,
        'title': 'In Progress',
        'status': 'In Progress',
        'color': 0xFF2196F3, // Blue
        'position': 1,
      },
      {
        'boardId': boardId,
        'title': 'Done',
        'status': 'Done',
        'color': 0xFF4CAF50, // Green
        'position': 2,
      },
    ];

    for (var column in defaultColumns) {
      await _dbService.addColumn(column, _userId!);
    }
  }

  Future<void> updateBoard(int id, Map<String, dynamic> updates) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.updateBoard(id, _userId!, updates);
    await fetchBoards();
  }

  Future<void> deleteBoard(int id) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.deleteBoard(id, _userId!);
    await fetchBoards();
    _selectedBoardId = boards.isNotEmpty ? boards.first['id'] : null;
    await fetchColumns();
  }

  void selectBoard(int boardId) {
    _selectedBoardId = boardId;
    fetchColumns();
    notifyListeners();
  }

  Future<void> fetchColumns() async {
    if (_userId == null || _selectedBoardId == null) {
      columns = [];
      notifyListeners();
      return;
    }
    columns = await _dbService.getColumnsByBoard(_selectedBoardId!, _userId!);
    notifyListeners();
  }

  Future<void> addColumn(Map<String, dynamic> column) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.addColumn(column, _userId!);
    await fetchColumns();
  }

  Future<void> updateColumn(int id, Map<String, dynamic> updates) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.updateColumn(id, _userId!, updates);
    await fetchColumns();
  }

  Future<void> deleteColumn(int id) async {
    if (_userId == null) throw Exception('User not authenticated');
    await _dbService.deleteColumn(id, _userId!);
    await fetchColumns();
  }

  /// Mettre à jour le JSON partagé après une modification (appelé après ajouter/modifier/supprimer une idée ou colonne)
  Future<void> refreshSharedBoardIfNeeded(int boardId, List<Map<String, dynamic>> ideas) async {
    if (_userId == null) return;
    try {
      // Récupérer le board courant
      final board = boards.firstWhere(
        (b) => b['id'] == boardId,
        orElse: () => <String, dynamic>{},
      );

      if (board.isEmpty) return;

      // Récupérer les colonnes pour ce board
      final boardColumns = await _dbService.getColumnsByBoard(boardId, _userId!);

      // Reconstruire le payload JSON
      final payload = {
        'board': board,
        'columns': boardColumns,
        'ideas': ideas,
      };

      final boardJson = jsonEncode(payload);

      // Récupérer les entrées shared_board_sync pour ce board
      final syncEntries = await _dbService.getSharedBoardSyncByOwner(
        boardId,
        _userId!.toString(),
      );

      // Mettre à jour le JSON dans shared_boards pour chaque utilisateur avec lequel c'est partagé
      for (var syncEntry in syncEntries) {
        final sharedUserEmail = syncEntry['shared_user_email'] as String?;
        if (sharedUserEmail != null && sharedUserEmail.isNotEmpty) {
          // Récupérer l'entrée shared_boards existante
          final existingShared = await _dbService.getSharedBoardsForEmail(sharedUserEmail);
          if (existingShared.isNotEmpty) {
            // Mettre à jour la première entrée trouvée
            final sharedId = existingShared.first['id'];
            final db = await _dbService.database;
            await db.update(
              'shared_boards',
              {'board_json': boardJson},
              where: 'id = ?',
              whereArgs: [sharedId],
            );
          }
        }
      }
    } catch (e) {
      print('Error refreshing shared board: $e');
    }
  }

  /// Si le board local (le destinataire) est une copie partagée, propager ses changements
  /// vers l'entrée `shared_boards` de l'owner pour que l'owner voie les modifications.
  Future<void> refreshSharedBoardFromSharedUser(int sharedBoardId, List<Map<String, dynamic>> ideas) async {
    if (_userId == null) return;
    try {
      final syncEntries = await _dbService.getSharedBoardSyncBySharedUserBoardId(sharedBoardId);
      if (syncEntries.isEmpty) return;

      // Pour chaque mapping, mettre à jour l'entrée shared_boards correspondante
      for (var syncEntry in syncEntries) {
        final ownerBoardId = syncEntry['owner_board_id'] as int? ?? 0;
        final ownerUserIdStr = syncEntry['owner_user_id']?.toString() ?? '';
        final sharedUserEmail = syncEntry['shared_user_email'] as String? ?? '';

        // Récupérer la représentation 'board' originale depuis shared_boards (owner side)
        final db = await _dbService.database;
        final ownerSharedRows = await db.query(
          'shared_boards',
          where: 'board_id = ? AND shared_with = ?',
          whereArgs: [ownerBoardId, sharedUserEmail],
        );
        if (ownerSharedRows.isEmpty) continue;

        Map<String, dynamic> boardMeta = {};
        try {
          final existingJson = ownerSharedRows.first['board_json'] as String? ?? '';
          final dec = jsonDecode(existingJson) as Map<String, dynamic>?;
          if (dec != null && dec['board'] != null) boardMeta = dec['board'] as Map<String, dynamic>;
        } catch (_) {}

        // Récupérer les colonnes locales pour sharedBoardId
        final localColumns = await _dbService.getColumnsByBoard(sharedBoardId, _userId!);

        final payload = {
          'board': boardMeta,
          'columns': localColumns,
          'ideas': ideas,
        };

        final boardJson = jsonEncode(payload);

        // Mettre à jour l'entrée shared_boards appartenant à l'owner
        await db.update(
          'shared_boards',
          {'board_json': boardJson},
          where: 'board_id = ? AND shared_with = ?',
          whereArgs: [ownerBoardId, sharedUserEmail],
        );

        // Appliquer également les changements directement sur le board de l'owner
        // afin que l'owner voie les modifications dans son interface.
        try {
          if (ownerUserIdStr.isNotEmpty) {
            final ownerUserId = int.tryParse(ownerUserIdStr);
            if (ownerUserId != null) {
              final updated = await _dbService.updateImportedBoard(ownerBoardId, boardJson, ownerUserId);
              if (updated > 0) {
                // Si la session courante est celle de l'owner, rafraîchir l'UI
                if (_userId != null && _userId == ownerUserId) {
                  await fetchBoards();
                  await fetchColumns();
                }
              }
            }
          }
        } catch (e) {
          print('Error applying shared-user changes to owner board: $e');
        }
      }
    } catch (e) {
      print('Error propagating shared-user changes: $e');
    }
  }
}
