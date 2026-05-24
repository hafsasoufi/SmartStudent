import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

class SecureStorageService {
  static const String _authBoxName = 'auth_box';
  static const String _userBoxName = 'user_box';
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userDataKey = 'user_data';

  late Box<String> _authBox;
  late Box<dynamic> _userBox;

  Future<void> init() async {
    _authBox = await Hive.openBox<String>(_authBoxName);
    _userBox = await Hive.openBox(_userBoxName);
  }

  // Token management
  Future<void> saveAccessToken(String token) async {
    await _authBox.put(_accessTokenKey, token);
  }

  Future<String?> getAccessToken() async {
    return _authBox.get(_accessTokenKey);
  }

  Future<void> saveRefreshToken(String token) async {
    await _authBox.put(_refreshTokenKey, token);
  }

  Future<String?> getRefreshToken() async {
    return _authBox.get(_refreshTokenKey);
  }

  // User data management
  Future<void> saveUserData(Map<String, dynamic> userData) async {
    await _userBox.put(_userDataKey, userData);
  }

  Future<Map<dynamic, dynamic>?> getUserData() async {
    return _userBox.get(_userDataKey);
  }

  Future<bool> isLoggedIn() async {
    return _authBox.get(_accessTokenKey) != null;
  }

  // Clear all
  Future<void> clearAll() async {
    await _authBox.deleteAll([_accessTokenKey, _refreshTokenKey]);
    await _userBox.delete(_userDataKey);
  }
}

final secureStorageService = SecureStorageService();

final secureStorageServiceProvider = Provider<SecureStorageService>((ref) {
  return secureStorageService;
});
