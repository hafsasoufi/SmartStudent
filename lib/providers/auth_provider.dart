import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AuthProvider extends ChangeNotifier {
  Map<String, dynamic>? _user; // l'utilisateur connecté
  int? _userId;
  String? _userName;
  String? _userEmail;

  bool get isAuthenticated => _user != null;
  Map<String, dynamic>? get user => _user;
  int? get userId => _userId;
  String? get userName => _userName;
  String? get userEmail => _userEmail;

  // ================= LOGIN =================
  Future<void> login(String email, String password) async {
    final result = await ApiService().login(email, password);

    if (result['status']) {
      _user = result['user'];
      _userId = _user!['id'] as int;
      _userName = _user!['name'];
      _userEmail = _user!['email'];
      notifyListeners();
    } else {
      throw Exception(result['message']);
    }
  }

  // ================= REGISTER =================
  Future<void> register(String email, String password, String name) async {
    final result = await ApiService().register(email, password, name);

    if (result['status']) {
      _user = result['user'];
      _userId = _user!['id'] as int;
      _userName = _user!['name'];
      _userEmail = _user!['email'];
      notifyListeners();
    } else {
      throw Exception(result['message']);
    }
  }

  // ================= LOGOUT =================
  void logout() {
    _user = null;
    _userId = null;
    _userName = null;
    _userEmail = null;
    notifyListeners();
  }
}
