import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';
import '../services/secure_storage_service.dart';

class AuthState {
  final bool isLoading;
  final bool isAuthenticated;
  final User? user;
  final String? error;

  AuthState({
    this.isLoading = false,
    this.isAuthenticated = false,
    this.user,
    this.error,
  });

  AuthState copyWith({
    bool? isLoading,
    bool? isAuthenticated,
    User? user,
    String? error,
  }) {
    return AuthState(
      isLoading: isLoading ?? this.isLoading,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      user: user ?? this.user,
      error: error ?? this.error,
    );
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  final secureStorage = ref.watch(secureStorageServiceProvider);
  return AuthNotifier(apiService: apiService, secureStorage: secureStorage);
});

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService apiService;
  final SecureStorageService secureStorage;

  AuthNotifier({
    required this.apiService,
    required this.secureStorage,
  }) : super(AuthState());

  Future<void> register({
    required String email,
    required String username,
    required String password,
    required String fullName,
  }) async {
    print('📝 AuthNotifier: Starting registration for $email');
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      print('📝 AuthNotifier: Calling apiService.register()');
      final response = await apiService.register(
        email: email,
        username: username,
        password: password,
        fullName: fullName,
      );
      
      print('📝 AuthNotifier: Got response: ${response.keys}');
      print('📝 AuthNotifier: User data: ${response['user']}');

      final user = User.fromJson(response['user']);
      print('📝 AuthNotifier: Parsed user: ${user.email}');
      
      await secureStorage.saveAccessToken(response['access_token']);
      print('📝 AuthNotifier: Saved access token');
      
      if (response['refresh_token'] != null) {
        await secureStorage.saveRefreshToken(response['refresh_token']);
        print('📝 AuthNotifier: Saved refresh token');
      }
      
      await secureStorage.saveUserData(response['user']);
      print('📝 AuthNotifier: Saved user data');

      state = state.copyWith(
        isLoading: false,
        isAuthenticated: true,
        user: user,
      );
      print('✅ AuthNotifier: Registration successful!');
    } catch (e) {
      print('❌ AuthNotifier: Registration failed - $e');
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
      rethrow;
    }
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    print('🔐 AuthNotifier: Starting login for $email');
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      print('🔐 AuthNotifier: Calling apiService.login()');
      final response = await apiService.login(
        email: email,
        password: password,
      );
      
      print('🔐 AuthNotifier: Got response: ${response.keys}');

      final user = User.fromJson(response['user']);
      print('🔐 AuthNotifier: Parsed user: ${user.email}');
      
      await secureStorage.saveAccessToken(response['access_token']);
      if (response['refresh_token'] != null) {
        await secureStorage.saveRefreshToken(response['refresh_token']);
      }
      await secureStorage.saveUserData(response['user']);
      print('🔐 AuthNotifier: Saved credentials');

      state = state.copyWith(
        isLoading: false,
        isAuthenticated: true,
        user: user,
      );
      print('✅ AuthNotifier: Login successful!');
    } catch (e) {
      print('❌ AuthNotifier: Login failed - $e');
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
      rethrow;
    }
  }

  Future<void> logout() async {
    await secureStorage.clearAll();
    state = AuthState();
  }

  Future<void> checkAuthStatus() async {
    state = state.copyWith(isLoading: true);
    
    try {
      final isLoggedIn = await secureStorage.isLoggedIn();
      
      if (isLoggedIn) {
        final userData = await secureStorage.getUserData();
        if (userData != null) {
          final user = User.fromJson(Map<String, dynamic>.from(userData));
          state = state.copyWith(
            isLoading: false,
            isAuthenticated: true,
            user: user,
          );
        }
      } else {
        state = state.copyWith(
          isLoading: false,
          isAuthenticated: false,
        );
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
}
