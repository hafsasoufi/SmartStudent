import 'database_service.dart';

class ApiService {
  final DBService _db = DBService();

  // ================= REGISTER =================
  Future<Map<String, dynamic>> register(
    String email,
    String password,
    String name,
  ) async {
    try {
      final db = await _db.database;

      // check email
      final exists = await db.query(
        'users',
        where: 'email = ?',
        whereArgs: [email],
      );

      if (exists.isNotEmpty) {
        return {'status': false, 'message': 'Email déjà utilisé'};
      }

      final id = await db.insert('users', {
        'name': name,
        'email': email,
        'password': password,
      });

      return {
        'status': true,
        'user': {'id': id, 'name': name, 'email': email},
      };
    } catch (e) {
      return {'status': false, 'message': 'Erreur API locale: $e'};
    }
  }

  // ================= LOGIN =================
  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final db = await _db.database;

      final result = await db.query(
        'users',
        where: 'email = ? AND password = ?',
        whereArgs: [email, password],
      );

      if (result.isNotEmpty) {
        return {'status': true, 'user': result.first};
      } else {
        return {'status': false, 'message': 'Email ou mot de passe incorrect'};
      }
    } catch (e) {
      return {'status': false, 'message': 'Erreur API locale: $e'};
    }
  }
}
