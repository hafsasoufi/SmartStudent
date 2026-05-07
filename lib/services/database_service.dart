import 'dart:convert';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DBService {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    final path = join(await getDatabasesPath(), 'kanban.db');
    return await openDatabase(
      path,
      version: 7, // Augmenter la version pour forcer la migration
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
    );
  }

  Future _onUpgrade(Database db, int oldVersion, int newVersion) async {
    print('Upgrading database from version $oldVersion to $newVersion');

    // Assurer l'existence de la table users
    await db.execute('''
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
      )
    ''');

    // Si version très ancienne, recréer tout
    if (oldVersion < 3) {
      print('Old version detected, dropping and recreating tables');
      await db.execute('DROP TABLE IF EXISTS ideas');
      await db.execute('DROP TABLE IF EXISTS kanban_columns');
      await db.execute('DROP TABLE IF EXISTS columns');
      await db.execute('DROP TABLE IF EXISTS boards');
      await _onCreate(db, newVersion);
      return;
    }

    // Migrations progressives pour versions plus récentes
    if (oldVersion < 4) {
      print(
        'Migrating to version 4: adding category, attachments, updatedAt, votes',
      );
      // Ajouter les colonnes manquantes une par une
      try {
        await db.execute(
          'ALTER TABLE ideas ADD COLUMN category TEXT DEFAULT "other"',
        );
        print('Added category column');
      } catch (e) {
        print('Category column already exists or error: $e');
      }

      try {
        await db.execute('ALTER TABLE ideas ADD COLUMN attachments TEXT');
        print('Added attachments column');
      } catch (e) {
        print('Attachments column already exists or error: $e');
      }

      try {
        await db.execute('ALTER TABLE ideas ADD COLUMN updatedAt TEXT');
        print('Added updatedAt column');
      } catch (e) {
        print('UpdatedAt column already exists or error: $e');
      }

      try {
        await db.execute(
          'ALTER TABLE ideas ADD COLUMN votes INTEGER DEFAULT 0',
        );
        print('Added votes column');
      } catch (e) {
        print('Votes column already exists or error: $e');
      }
    }

    // Ajouter la table shared_boards pour le partage de tableaux
    if (oldVersion < 5) {
      try {
        await db.execute('''
          CREATE TABLE IF NOT EXISTS shared_boards(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INTEGER,
            board_json TEXT NOT NULL,
            shared_with TEXT NOT NULL,
            createdAt TEXT
          )
        ''');
        print('Created shared_boards table');
      } catch (e) {
        print('Error creating shared_boards table: $e');
      }
    }

    // Table pour synchronisation des tableaux partagés (v6)
    if (oldVersion < 6) {
      try {
        await db.execute('''
          CREATE TABLE IF NOT EXISTS shared_board_sync(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_board_id INTEGER,
            owner_user_id TEXT,
            shared_user_email TEXT,
            shared_user_board_id INTEGER,
            createdAt TEXT
          )
        ''');
        print('Created shared_board_sync table');
      } catch (e) {
        print('Error creating shared_board_sync table: $e');
      }
    }

    // Table pour les pitch decks (v7)
    if (oldVersion < 7) {
      try {
        await db.execute('''
          CREATE TABLE IF NOT EXISTS pitch_decks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_id INTEGER,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            subtitle TEXT,
            description TEXT,
            slides TEXT NOT NULL,
            duration INTEGER DEFAULT 5,
            target_audience TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT
          )
        ''');
        print('Created pitch_decks table');
      } catch (e) {
        print('Error creating pitch_decks table: $e');
      }
    }
  }

  Future _onCreate(Database db, int version) async {
    // Créer la table users ici pour garantir une initialisation cohérente
    await db.execute('''
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
      )
    ''');

    await db.execute('''
      CREATE TABLE boards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        createdAt TEXT,
        userId TEXT NOT NULL
      )
    ''');

    await db.execute('''
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
    ''');

    await db.execute('''
      CREATE TABLE ideas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT,
        priority INTEGER,
        category TEXT,
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
    ''');

      // Table pour les tableaux partagés
      await db.execute('''
        CREATE TABLE IF NOT EXISTS shared_boards(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          board_id INTEGER,
          board_json TEXT NOT NULL,
          shared_with TEXT NOT NULL,
          createdAt TEXT
        )
      ''');

      // Table pour tracker la synchronisation entre tableaux partagés
      await db.execute('''
        CREATE TABLE IF NOT EXISTS shared_board_sync(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          owner_board_id INTEGER,
          owner_user_id TEXT,
          shared_user_email TEXT,
          shared_user_board_id INTEGER,
          createdAt TEXT
        )
      ''');

      // Table pour les pitch decks
      await db.execute('''
        CREATE TABLE IF NOT EXISTS pitch_decks(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          idea_id INTEGER,
          user_id TEXT NOT NULL,
          title TEXT NOT NULL,
          subtitle TEXT,
          description TEXT,
          slides TEXT NOT NULL,
          duration INTEGER DEFAULT 5,
          target_audience TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT
        )
      ''');
  }

  // Méthode pour réinitialiser la base de données
  Future<void> resetDatabase() async {
    final path = join(await getDatabasesPath(), 'kanban.db');
    await deleteDatabase(path);
    _database = null;
    await database; // Recréer la base
  }

  // ================= BOARDS =================
  Future<int> addBoard(Map<String, dynamic> board, int userId) async {
    final db = await database;
    try {
      // S'assurer que userId est une string
      board['userId'] = userId.toString();
      board['createdAt'] = DateTime.now().toIso8601String();

      print('Adding board: $board'); // Debug
      final id = await db.insert('boards', board);
      print('Board added with id: $id'); // Debug
      return id;
    } catch (e) {
      print('Error adding board: $e');
      rethrow;
    }
  }

  Future<List<Map<String, dynamic>>> getAllBoards(int userId) async {
    final db = await database;
    try {
      final result = await db.query(
        'boards',
        where: 'userId = ?',
        whereArgs: [userId.toString()],
        orderBy: 'createdAt DESC',
      );
      print('Fetched ${result.length} boards for user $userId'); // Debug
      return result;
    } catch (e) {
      print('Error fetching boards: $e');
      return [];
    }
  }

  Future<int> updateBoard(
    int id,
    int userId,
    Map<String, dynamic> updates,
  ) async {
    final db = await database;
    try {
      return await db.update(
        'boards',
        updates,
        where: 'id = ? AND userId = ?',
        whereArgs: [id, userId.toString()],
      );
    } catch (e) {
      print('Error updating board: $e');
      rethrow;
    }
  }

  Future<int> deleteBoard(int id, int userId) async {
    final db = await database;
    try {
      await db.delete(
        'kanban_columns',
        where: 'boardId = ? AND userId = ?',
        whereArgs: [id, userId.toString()],
      );
      await db.delete(
        'ideas',
        where: 'boardId = ? AND userId = ?',
        whereArgs: [id, userId.toString()],
      );
      return await db.delete(
        'boards',
        where: 'id = ? AND userId = ?',
        whereArgs: [id, userId.toString()],
      );
    } catch (e) {
      print('Error deleting board: $e');
      rethrow;
    }
  }

  // ================= COLUMNS =================
  Future<int> addColumn(Map<String, dynamic> column, int userId) async {
    final db = await database;
    column['userId'] = userId.toString();
    return await db.insert('kanban_columns', column);
  }

  Future<List<Map<String, dynamic>>> getColumnsByBoard(
    int boardId,
    int userId,
  ) async {
    final db = await database;
    return await db.query(
      'kanban_columns',
      where: 'boardId = ? AND userId = ?',
      whereArgs: [boardId, userId.toString()],
      orderBy: 'position ASC',
    );
  }

  Future<int> updateColumn(
    int id,
    int userId,
    Map<String, dynamic> updates,
  ) async {
    final db = await database;
    return await db.update(
      'kanban_columns',
      updates,
      where: 'id = ? AND userId = ?',
      whereArgs: [id, userId.toString()],
    );
  }

  Future<int> deleteColumn(int id, int userId) async {
    final db = await database;
    return await db.delete(
      'kanban_columns',
      where: 'id = ? AND userId = ?',
      whereArgs: [id, userId.toString()],
    );
  }

  // ================= IDEAS =================
  Future<int> addIdea(Map<String, dynamic> idea, int userId) async {
    final db = await database;
    idea['userId'] = userId.toString();
    idea['createdAt'] = DateTime.now().toIso8601String();
    idea['status'] ??= 'Backlog';

    print('=== Attempting to insert idea ===');
    print('Idea data: $idea');

    try {
      final id = await db.insert('ideas', idea);
      print('Idea inserted successfully with ID: $id');
      return id;
    } catch (e) {
      print('ERROR inserting idea: $e');
      print('Idea data that failed: $idea');
      rethrow;
    }
  }

  // ================= SHARED BOARDS =================
  Future<int> addSharedBoard(int boardId, String boardJson, String sharedWith) async {
    final db = await database;
    final entry = {
      'board_id': boardId,
      'board_json': boardJson,
      'shared_with': sharedWith,
      'createdAt': DateTime.now().toIso8601String(),
    };
    return await db.insert('shared_boards', entry);
  }

  Future<List<Map<String, dynamic>>> getSharedBoardsForEmail(String email) async {
    final db = await database;
    return await db.query(
      'shared_boards',
      where: 'shared_with = ?',
      whereArgs: [email],
      orderBy: 'createdAt DESC',
    );
  }

  /// Enregistrer le lien de synchronisation entre un tableau partagé et les utilisateurs
  Future<int> addSharedBoardSync(
    int ownerBoardId,
    String ownerUserId,
    String sharedUserEmail,
    int sharedUserBoardId,
  ) async {
    final db = await database;
    final entry = {
      'owner_board_id': ownerBoardId,
      'owner_user_id': ownerUserId,
      'shared_user_email': sharedUserEmail,
      'shared_user_board_id': sharedUserBoardId,
      'createdAt': DateTime.now().toIso8601String(),
    };
    return await db.insert('shared_board_sync', entry);
  }

  /// Enregistrer l'id du tableau importé pour un utilisateur partagé
  Future<int> setSharedUserBoardId(int ownerBoardId, String sharedUserEmail, int sharedUserBoardId) async {
    final db = await database;
    try {
      return await db.update(
        'shared_board_sync',
        {'shared_user_board_id': sharedUserBoardId},
        where: 'owner_board_id = ? AND shared_user_email = ?',
        whereArgs: [ownerBoardId, sharedUserEmail],
      );
    } catch (e) {
      print('Error setting shared_user_board_id: $e');
      return 0;
    }
  }

  /// Retourne la/les ligne(s) de sync pour un ownerBoardId et un email partagé
  Future<List<Map<String, dynamic>>> getSharedBoardSyncByOwnerBoardIdAndEmail(
    int ownerBoardId,
    String sharedUserEmail,
  ) async {
    final db = await database;
    return await db.query(
      'shared_board_sync',
      where: 'owner_board_id = ? AND shared_user_email = ?',
      whereArgs: [ownerBoardId, sharedUserEmail],
    );
  }

  /// Retourne la/les ligne(s) de sync pour un shared_user_board_id (recherche inverse)
  Future<List<Map<String, dynamic>>> getSharedBoardSyncBySharedUserBoardId(
    int sharedBoardId,
  ) async {
    final db = await database;
    return await db.query(
      'shared_board_sync',
      where: 'shared_user_board_id = ?',
      whereArgs: [sharedBoardId],
    );
  }

  /// Mettre à jour un board importé déjà existant (supprime ses colonnes/ideas et remplace par celles du JSON)
  Future<int> updateImportedBoard(int existingBoardId, String boardJson, int userId) async {
    final db = await database;
    Map<String, dynamic> payload;
    try {
      final dynamic json = jsonDecode(boardJson);
      if (json is Map<String, dynamic>) {
        payload = json;
      } else {
        return -1;
      }
    } catch (e) {
      print('Error decoding shared board json for update: $e');
      return -1;
    }

    final columns = (payload['columns'] as List<dynamic>?) ?? [];
    final ideas = (payload['ideas'] as List<dynamic>?) ?? [];

    try {
      // Remove existing columns and ideas for that board and user
      await db.delete(
        'kanban_columns',
        where: 'boardId = ? AND userId = ?',
        whereArgs: [existingBoardId, userId.toString()],
      );
      await db.delete(
        'ideas',
        where: 'boardId = ? AND userId = ?',
        whereArgs: [existingBoardId, userId.toString()],
      );

      // Insert columns
      for (var c in columns) {
        try {
          final original = Map<String, dynamic>.from(c as Map);
          original.remove('id');
          original.remove('boardId');
          original.remove('userId');
          final col = <String, dynamic>{
            'title': original['title'] ?? 'Column',
            'status': original['status'] ?? 'Backlog',
            'color': original['color'] ?? 0xFF9E9E9E,
            'position': original['position'] ?? 0,
            'boardId': existingBoardId,
            'userId': userId.toString(),
          };
          await db.insert('kanban_columns', col);
        } catch (e) {
          print('Error inserting column during updateImportedBoard: $e');
        }
      }

      // Insert ideas
      for (var it in ideas) {
        try {
          final original = Map<String, dynamic>.from(it as Map);
          original.remove('id');
          original.remove('boardId');
          original.remove('userId');
          final idea = <String, dynamic>{
            'title': original['title'] ?? 'Idea',
            'description': original['description'],
            'status': original['status'] ?? 'Backlog',
            'priority': original['priority'] ?? 0,
            'category': original['category'],
            'tags': original['tags'],
            'dueDate': original['dueDate'],
            'attachments': original['attachments'],
            'votes': original['votes'] ?? 0,
            'boardId': existingBoardId,
            'userId': userId.toString(),
            'createdAt': original['createdAt'] ?? DateTime.now().toIso8601String(),
            'updatedAt': original['updatedAt'],
          };
          await db.insert('ideas', idea);
        } catch (e) {
          print('Error inserting idea during updateImportedBoard: $e');
        }
      }

      return existingBoardId;
    } catch (e) {
      print('Error updating imported board: $e');
      return -1;
    }
  }

  /// Obtenir les tableaux qui doivent être synchronisés avec un utilisateur
  /// (tableaux que l'utilisateur possède et qui sont partagés avec d'autres)
  Future<List<Map<String, dynamic>>> getSharedBoardSyncByOwner(
    int ownerBoardId,
    String ownerUserId,
  ) async {
    final db = await database;
    return await db.query(
      'shared_board_sync',
      where: 'owner_board_id = ? AND owner_user_id = ?',
      whereArgs: [ownerBoardId, ownerUserId],
    );
  }

  /// Importer un tableau partagé pour un utilisateur local (`userId`).
  /// Le `boardJson` doit contenir la structure: { "board": {...}, "columns": [...], "ideas": [...] }
  Future<int> importSharedBoardForUser(String boardJson, int userId) async {
    final db = await database;
    Map<String, dynamic> payload;
    try {
      final dynamic json = jsonDecode(boardJson);
      if (json is Map<String, dynamic>) {
        payload = json;
      } else {
        print('❌ Invalid JSON structure: not a map');
        return -1;
      }
    } catch (e) {
      print('❌ Error decoding shared board json: $e');
      return -1;
    }

    final boardMap = payload['board'] as Map<String, dynamic>?;
    final columns = (payload['columns'] as List<dynamic>?) ?? [];
    final ideas = (payload['ideas'] as List<dynamic>?) ?? [];

    print('📥 IMPORTING: Board=${boardMap?['name']}, Columns=${columns.length}, Ideas=${ideas.length}');
    print('   Columns: ${columns.map((c) => (c as Map)['title']).toList()}');
    print('   Ideas: ${ideas.map((i) => (i as Map)['title']).toList()}');

    if (boardMap == null) {
      print('❌ No board data in payload');
      return -1;
    }

    // Insert board
    final boardEntry = {
      'name': boardMap['name'] ?? 'Imported Board',
      'createdAt': DateTime.now().toIso8601String(),
      'userId': userId.toString(),
    };
    final newBoardId = await db.insert('boards', boardEntry);
    print('✅ Board inserted with ID=$newBoardId');

    // Insert columns (sanitize incoming maps to avoid id/user/board collisions)
    print('   Inserting ${columns.length} columns...');
    for (var c in columns) {
      try {
        final original = Map<String, dynamic>.from(c as Map);
        // Remove owner-specific keys that could conflict
        original.remove('id');
        original.remove('boardId');
        original.remove('userId');

        // Ensure required fields exist
        final col = <String, dynamic>{
          'title': original['title'] ?? 'Column',
          'status': original['status'] ?? 'Backlog',
          'color': original['color'] ?? 0xFF9E9E9E,
          'position': original['position'] ?? 0,
          'boardId': newBoardId,
          'userId': userId.toString(),
        };

        await db.insert('kanban_columns', col);
        print('      ✓ Column: ${col['title']}');
      } catch (e) {
        print('      ❌ Error inserting column: $e');
      }
    }

    // Insert ideas/cards (sanitize maps similarly)
    print('   Inserting ${ideas.length} ideas...');
    for (var it in ideas) {
      try {
        final original = Map<String, dynamic>.from(it as Map);
        original.remove('id');
        original.remove('boardId');
        original.remove('userId');

        final idea = <String, dynamic>{
          'title': original['title'] ?? 'Idea',
          'description': original['description'],
          'status': original['status'] ?? 'Backlog',
          'priority': original['priority'] ?? 0,
          'category': original['category'],
          'tags': original['tags'],
          'dueDate': original['dueDate'],
          'attachments': original['attachments'],
          'votes': original['votes'] ?? 0,
          'boardId': newBoardId,
          'userId': userId.toString(),
          'createdAt': original['createdAt'] ?? DateTime.now().toIso8601String(),
          'updatedAt': original['updatedAt'],
        };

        await db.insert('ideas', idea);
        print('      ✓ Idea: ${idea['title']} (${idea['status']})');
      } catch (e) {
        print('      ❌ Error inserting idea: $e');
      }
    }

    print('✅ IMPORT COMPLETE: Board=$newBoardId with ${columns.length} columns and ${ideas.length} ideas');
    return newBoardId;
  }

  Future<List<Map<String, dynamic>>> getAllIdeas(int userId) async {
    final db = await database;
    return await db.query(
      'ideas',
      where: 'userId = ?',
      whereArgs: [userId.toString()],
    );
  }

  /// Récupérer les idées d'un board pour un utilisateur
  Future<List<Map<String, dynamic>>> getIdeasByBoard(int userId, int boardId) async {
    final db = await database;
    return await db.query(
      'ideas',
      where: 'userId = ? AND boardId = ?',
      whereArgs: [userId.toString(), boardId],
      orderBy: 'createdAt DESC',
    );
  }

  Future<int> updateIdea(
    int id,
    int userId,
    Map<String, dynamic> updates,
  ) async {
    final db = await database;
    // Mettre à jour la date de modification
    updates['updatedAt'] = DateTime.now().toIso8601String();
    return await db.update(
      'ideas',
      updates,
      where: 'id = ? AND userId = ?',
      whereArgs: [id, userId.toString()],
    );
  }

  Future<int> deleteIdea(int id, int userId) async {
    final db = await database;
    return await db.delete(
      'ideas',
      where: 'id = ? AND userId = ?',
      whereArgs: [id, userId.toString()],
    );
  }

  // ================= STATISTIQUES =================
  Future<Map<String, int>> getStatsByStatus(int userId) async {
    final db = await database;
    final ideas = await db.query(
      'ideas',
      where: 'userId = ?',
      whereArgs: [userId.toString()],
    );

    Map<String, int> stats = {'Backlog': 0, 'In Progress': 0, 'Done': 0};

    for (var idea in ideas) {
      String status = idea['status']?.toString() ?? 'Backlog';
      stats[status] = (stats[status] ?? 0) + 1;
    }

    return stats;
  }

  Future<int> updateStatus(int id, int userId, String status) async {
    return updateIdea(id, userId, {'status': status});
  }

  // ================= VOTES =================
  Future<int> voteIdea(int id, int userId) async {
    final db = await database;
    final idea = await db.query(
      'ideas',
      where: 'id = ?',
      whereArgs: [id],
    );

    if (idea.isEmpty) return 0;

    final currentVotes = (idea.first['votes'] as int?) ?? 0;
    return await db.update(
      'ideas',
      {'votes': currentVotes + 1},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<int> unvoteIdea(int id, int userId) async {
    final db = await database;
    final idea = await db.query(
      'ideas',
      where: 'id = ?',
      whereArgs: [id],
    );

    if (idea.isEmpty) return 0;

    final currentVotes = (idea.first['votes'] as int?) ?? 0;
    if (currentVotes > 0) {
      return await db.update(
        'ideas',
        {'votes': currentVotes - 1},
        where: 'id = ?',
        whereArgs: [id],
      );
    }
    return 0;
  }

  Future<List<Map<String, dynamic>>> getTopVotedIdeas(
    int userId, {
    int limit = 10,
  }) async {
    final db = await database;
    return await db.query(
      'ideas',
      where: 'userId = ?',
      whereArgs: [userId.toString()],
      orderBy: 'votes DESC, createdAt DESC',
      limit: limit,
    );
  }

  // ================= FILTRES ET RECHERCHE =================

  /// Recherche textuelle dans les idées
  Future<List<Map<String, dynamic>>> searchIdeas(
    int userId,
    String query,
  ) async {
    final db = await database;
    final searchQuery = '%$query%';
    return await db.query(
      'ideas',
      where:
          'userId = ? AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)',
      whereArgs: [userId.toString(), searchQuery, searchQuery, searchQuery],
      orderBy: 'createdAt DESC',
    );
  }

  /// Filtrer les idées par priorité
  Future<List<Map<String, dynamic>>> getIdeasByPriority(
    int userId,
    int priority,
  ) async {
    final db = await database;
    return await db.query(
      'ideas',
      where: 'userId = ? AND priority = ?',
      whereArgs: [userId.toString(), priority],
      orderBy: 'createdAt DESC',
    );
  }

  /// Filtrer les idées par catégorie
  Future<List<Map<String, dynamic>>> getIdeasByCategory(
    int userId,
    String category,
  ) async {
    final db = await database;
    return await db.query(
      'ideas',
      where: 'userId = ? AND category = ?',
      whereArgs: [userId.toString(), category],
      orderBy: 'createdAt DESC',
    );
  }

  /// Filtrer les idées par statut
  Future<List<Map<String, dynamic>>> getIdeasByStatus(
    int userId,
    String status,
  ) async {
    final db = await database;
    return await db.query(
      'ideas',
      where: 'userId = ? AND status = ?',
      whereArgs: [userId.toString(), status],
      orderBy: 'priority DESC, createdAt DESC',
    );
  }

  /// Obtenir des statistiques par catégorie
  Future<Map<String, int>> getStatsByCategory(int userId) async {
    final db = await database;
    final ideas = await db.query(
      'ideas',
      where: 'userId = ?',
      whereArgs: [userId.toString()],
    );

    Map<String, int> stats = {};
    for (var idea in ideas) {
      String category = idea['category']?.toString() ?? 'other';
      stats[category] = (stats[category] ?? 0) + 1;
    }
    return stats;
  }

  /// Obtenir des statistiques par priorité
  Future<Map<String, int>> getStatsByPriority(int userId) async {
    final db = await database;
    final ideas = await db.query(
      'ideas',
      where: 'userId = ?',
      whereArgs: [userId.toString()],
    );

    Map<String, int> stats = {'0': 0, '1': 0, '2': 0}; // low, medium, high
    for (var idea in ideas) {
      String priority = idea['priority']?.toString() ?? '0';
      stats[priority] = (stats[priority] ?? 0) + 1;
    }
    return stats;
  }

  /// Obtenir l'activité récente (idées modifiées récemment)
  Future<List<Map<String, dynamic>>> getRecentActivity(
    int userId, {
    int days = 7,
  }) async {
    final db = await database;
    final cutoffDate = DateTime.now()
        .subtract(Duration(days: days))
        .toIso8601String();

    return await db.query(
      'ideas',
      where: 'userId = ? AND (createdAt >= ? OR updatedAt >= ?)',
      whereArgs: [userId.toString(), cutoffDate, cutoffDate],
      orderBy: 'COALESCE(updatedAt, createdAt) DESC',
      limit: 20,
    );
  }

  // ===================== PITCH DECK METHODS =====================

  /// Ajouter un pitch deck
  Future<int> addPitchDeck(Map<String, dynamic> pitchDeck) async {
    final db = await database;
    return await db.insert('pitch_decks', {
      'idea_id': pitchDeck['ideaId'],
      'user_id': pitchDeck['userId'],
      'title': pitchDeck['title'],
      'subtitle': pitchDeck['subtitle'],
      'description': pitchDeck['description'],
      'slides': pitchDeck['slides'], // JSON string
      'duration': pitchDeck['duration'] ?? 5,
      'target_audience': pitchDeck['targetAudience'],
      'created_at': pitchDeck['createdAt'],
      'updated_at': pitchDeck['updatedAt'],
    });
  }

  /// Obtenir tous les pitch decks d'un utilisateur
  Future<List<Map<String, dynamic>>> getPitchDecksByUser(String userId) async {
    final db = await database;
    return await db.query(
      'pitch_decks',
      where: 'user_id = ?',
      whereArgs: [userId],
      orderBy: 'created_at DESC',
    );
  }

  /// Obtenir les pitch decks d'une idée
  Future<List<Map<String, dynamic>>> getPitchDecksByIdea(int ideaId) async {
    final db = await database;
    return await db.query(
      'pitch_decks',
      where: 'idea_id = ?',
      whereArgs: [ideaId],
      orderBy: 'created_at DESC',
    );
  }

  /// Mettre à jour un pitch deck
  Future<int> updatePitchDeck(int id, Map<String, dynamic> updates) async {
    final db = await database;
    return await db.update(
      'pitch_decks',
      {
        'title': updates['title'],
        'subtitle': updates['subtitle'],
        'description': updates['description'],
        'slides': updates['slides'],
        'duration': updates['duration'],
        'target_audience': updates['targetAudience'],
        'updated_at': updates['updatedAt'],
      },
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  /// Supprimer un pitch deck
  Future<int> deletePitchDeck(int id) async {
    final db = await database;
    return await db.delete(
      'pitch_decks',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  /// Obtenir un pitch deck par ID
  Future<Map<String, dynamic>?> getPitchDeckById(int id) async {
    final db = await database;
    final results = await db.query(
      'pitch_decks',
      where: 'id = ?',
      whereArgs: [id],
    );
    return results.isNotEmpty ? results.first : null;
  }
}
