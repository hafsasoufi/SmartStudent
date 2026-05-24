import 'package:dio/dio.dart';
import '../config/app_config.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  late final Dio _dio;
  String? _authToken;

  factory ApiService() {
    return _instance;
  }

  ApiService._internal() {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConfig.apiBaseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        contentType: Headers.jsonContentType,
      ),
    );

    // Add interceptors
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          if (_authToken != null) {
            options.headers['Authorization'] = 'Bearer $_authToken';
          }
          return handler.next(options);
        },
        onError: (error, handler) {
          return handler.next(error);
        },
      ),
    );
  }

  void setAuthToken(String token) {
    _authToken = token;
  }

  void clearAuthToken() {
    _authToken = null;
  }

  // Auth endpoints
  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String fullName,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/register',
        data: {
          'email': email,
          'password': password,
          'full_name': fullName,
        },
      );
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  // User endpoints
  Future<Map<String, dynamic>> getUserProfile() async {
    try {
      final response = await _dio.get('/user/profile');
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<Map<String, dynamic>> updateProfile({
    required String fullName,
    String? bio,
    String? avatar,
  }) async {
    try {
      final response = await _dio.put(
        '/user/profile',
        data: {
          'full_name': fullName,
          if (bio != null) 'bio': bio,
          if (avatar != null) 'avatar': avatar,
        },
      );
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  // Chat endpoints
  Future<Map<String, dynamic>> sendMessage({
    required String message,
    String? conversationId,
  }) async {
    try {
      final response = await _dio.post(
        '/chat',
        data: {
          'message': message,
          'conversation_id': conversationId,
        },
      );
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  // Planning endpoints
  Future<List<dynamic>> getDeadlines() async {
    try {
      final response = await _dio.get('/planning/deadlines');
      return response.data['deadlines'] ?? [];
    } catch (e) {
      rethrow;
    }
  }

  // Exams endpoints
  Future<List<dynamic>> getQuizzes() async {
    try {
      final response = await _dio.get('/exams/quizzes');
      return response.data['quizzes'] ?? [];
    } catch (e) {
      rethrow;
    }
  }

  // Events endpoints
  Future<List<dynamic>> getEvents() async {
    try {
      final response = await _dio.get('/campus/events');
      return response.data['events'] ?? [];
    } catch (e) {
      rethrow;
    }
  }
}
