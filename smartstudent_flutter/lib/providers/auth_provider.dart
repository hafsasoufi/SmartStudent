import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ApiService());
});

class AuthState {
  final bool isLoading;
  final bool isAuthenticated;
  final User? user;
  final String? error;
  final String? token;

  AuthState({
    this.isLoading = false,
    this.isAuthenticated = false,
    this.user,
    this.error,
    this.token,
  });

  AuthState copyWith({
    bool? isLoading,
    bool? isAuthenticated,
    User? user,
    String? error,
    String? token,
  }) {
    return AuthState(
      isLoading: isLoading ?? this.isLoading,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      user: user ?? this.user,
      error: error,
      token: token ?? this.token,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService _apiService;

  AuthNotifier(this._apiService) : super(AuthState());

  Future<void> register({
    required String email,
    required String password,
    required String fullName,
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await _apiService.register(
        email: email,
        password: password,
        fullName: fullName,
      );

      final token = response['access_token'] as String;
      _apiService.setAuthToken(token);

      state = state.copyWith(
        isLoading: false,
        isAuthenticated: true,
        token: token,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final response = await _apiService.login(
        email: email,
        password: password,
      );

      final token = response['access_token'] as String;
      _apiService.setAuthToken(token);

      final user = User(
        id: response['user']['id'],
        email: response['user']['email'],
        fullName: response['user']['full_name'],
      );

      state = state.copyWith(
        isLoading: false,
        isAuthenticated: true,
        user: user,
        token: token,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  Future<void> fetchProfile() async {
    if (!state.isAuthenticated) return;

    try {
      final response = await _apiService.getUserProfile();
      final user = User(
        id: response['id'],
        email: response['email'],
        fullName: response['full_name'],
        bio: response['bio'],
      );

      state = state.copyWith(user: user);
    } catch (e) {
      print('Error fetching profile: $e');
    }
  }

  Future<void> logout() async {
    _apiService.clearAuthToken();
    state = AuthState();
  }
}
