import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/app_config.dart';
import 'secure_storage_service.dart';

// Watched by the root widget to force-logout on token expiry
final sessionExpiredNotifier = ValueNotifier<bool>(false);

class ApiService {
  final Dio dio;
  final SecureStorageService secureStorage;
  final List<String> _baseUrls;
  int _activeBaseUrlIndex = 0;

  ApiService({required this.dio, required this.secureStorage})
      : _baseUrls = _determineApiBaseUrls() {
    _initializeDio();
  }

  static List<String> _determineApiBaseUrls() {
    if (kIsWeb) {
      return [
        AppConfig.apiBaseUrls[5], // localhost for web
        AppConfig.apiBaseUrls[6], // 127.0.0.1 fallback
      ];
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return [
          AppConfig.apiBaseUrls[0], // PC WiFi IP — physical device on same WiFi
          AppConfig.apiBaseUrls[1], // Android emulator (10.0.2.2)
          AppConfig.apiBaseUrls[2], // USB adb reverse (localhost)
          AppConfig.apiBaseUrls[3], // USB adb reverse (127.0.0.1)
          AppConfig.apiBaseUrls[4], // Windows hotspot
        ];
      case TargetPlatform.iOS:
        return [
          AppConfig.apiBaseUrls[0], // PC WiFi IP
          AppConfig.apiBaseUrls[2], // localhost
          AppConfig.apiBaseUrls[3], // 127.0.0.1
        ];
      case TargetPlatform.windows:
      case TargetPlatform.linux:
      case TargetPlatform.macOS:
        return [
          AppConfig.apiBaseUrls[5], // localhost
          AppConfig.apiBaseUrls[6], // 127.0.0.1
          AppConfig.apiBaseUrls[0], // PC WiFi IP fallback
        ];
      default:
        return AppConfig.apiBaseUrls;
    }
  }

  String get _activeBaseUrl => _baseUrls[_activeBaseUrlIndex];

  void _initializeDio() {
    dio.options.baseUrl = _activeBaseUrl;
    dio.options.connectTimeout = Duration(seconds: int.parse(AppConfig.apiTimeout));
    dio.options.receiveTimeout = Duration(seconds: int.parse(AppConfig.apiTimeout));
    
    // Clear interceptors to avoid duplicates
    dio.interceptors.clear();
    
    // Add request interceptor for auth token
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await secureStorage.getAccessToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          options.headers['Content-Type'] = 'application/json';
          print('ApiService: Request to ${options.baseUrl}${options.path}');
          return handler.next(options);
        },
        onError: (error, handler) async {
          print('ApiService: Interceptor error - status: ${error.response?.statusCode}, message: ${error.message}');
          if (error.response?.statusCode == 401 &&
              !(error.requestOptions.path.contains('/auth/'))) {
            try {
              final refreshToken = await secureStorage.getRefreshToken();
              if (refreshToken != null) {
                final refreshDio = Dio();
                refreshDio.options.baseUrl = dio.options.baseUrl;
                final refreshResp = await refreshDio.post(
                  '/auth/refresh',
                  data: {'refresh_token': refreshToken},
                );
                final newToken = refreshResp.data['access_token'] as String;
                await secureStorage.saveAccessToken(newToken);
                final retryOptions = error.requestOptions;
                retryOptions.headers['Authorization'] = 'Bearer $newToken';
                final retryResp = await dio.fetch(retryOptions);
                return handler.resolve(retryResp);
              }
            } catch (_) {}
            await secureStorage.clearAll();
            sessionExpiredNotifier.value = true;
          }
          return handler.next(error);
        },
      ),
    );
  }

  Future<T> _performRequestWithFallback<T>(Future<T> Function() request) async {
    DioException? lastException;
    print('🔄 ApiService: Starting fallback mechanism with ${_baseUrls.length} URLs');
    
    for (var i = 0; i < _baseUrls.length; i++) {
      _activeBaseUrlIndex = i;
      dio.options.baseUrl = _baseUrls[i];
      print('🌐 ApiService: Attempt ${i + 1}/${_baseUrls.length} - Trying ${_baseUrls[i]}');

      try {
        print('🔗 ApiService: Executing request with baseUrl: ${dio.options.baseUrl}');
        final result = await request();
        print('✅ ApiService: SUCCESS with ${_baseUrls[i]}');
        return result;
      } on DioException catch (e) {
        print('❌ ApiService: Failed with ${_baseUrls[i]}');
        print('   Error Type: ${e.type}');
        print('   Error Message: ${e.message}');
        print('   Status Code: ${e.response?.statusCode}');
        print('   Response: ${e.response?.data}');
        
        lastException = e;
        
        if (e.response != null) {
          print('⚠️ ApiService: Server responded with status ${e.response?.statusCode}, stopping fallback');
          rethrow;
        }
        
        if (i == _baseUrls.length - 1) {
          print('💥 ApiService: All URLs exhausted, throwing exception');
          rethrow;
        }
        
        print('➡️ ApiService: Trying next URL...');
      }
    }

    throw lastException ?? Exception('No available API base URL');
  }

  // Auth endpoints
  Future<Map<String, dynamic>> register({
    required String email,
    required String username,
    required String password,
    required String fullName,
    String? firstName,
    String? lastName,
    String? studentCardId,
    String? fieldOfStudy,
    int? academicYear,
  }) async {
    try {
      print('📝 ApiService.register: Building request payload');
      final payload = {
        'email': email,
        'username': username,
        'password': password,
        'full_name': fullName,
        if (firstName != null && firstName.isNotEmpty) 'first_name': firstName,
        if (lastName  != null && lastName.isNotEmpty)  'last_name': lastName,
        if (studentCardId != null && studentCardId.isNotEmpty) 'student_card_id': studentCardId,
        if (fieldOfStudy  != null && fieldOfStudy.isNotEmpty)  'field_of_study': fieldOfStudy,
        if (academicYear  != null) 'academic_year': academicYear,
      };
      print('📝 ApiService.register: Payload = $payload');
      
      final response = await _performRequestWithFallback(
        () => dio.post(
          '/auth/register',
          data: payload,
        ),
      );
      
      print('📝 ApiService.register: Got response type: ${response.runtimeType}');
      print('📝 ApiService.register: Response statusCode: ${response.statusCode}');
      print('📝 ApiService.register: Response data type: ${response.data.runtimeType}');
      print('📝 ApiService.register: Response keys: ${(response.data as Map).keys}');
      
      final result = response.data as Map<String, dynamic>;
      print('✅ ApiService.register: Returning ${result.keys}');
      return result;
    } on DioException catch (e) {
      print('❌ ApiService.register: DioException caught');
      throw _handleError(e);
    } catch (e) {
      print('❌ ApiService.register: Unexpected error: $e (${e.runtimeType})');
      rethrow;
    }
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      print('🔐 ApiService.login: Building request payload');
      final payload = {
        'email': email,
        'password': password,
      };
      print('🔐 ApiService.login: Payload = $payload');
      
      final response = await _performRequestWithFallback(
        () => dio.post(
          '/auth/login',
          data: payload,
        ),
      );
      
      print('🔐 ApiService.login: Got response type: ${response.runtimeType}');
      print('🔐 ApiService.login: Response statusCode: ${response.statusCode}');
      
      final result = response.data as Map<String, dynamic>;
      print('✅ ApiService.login: Returning ${result.keys}');
      return result;
    } on DioException catch (e) {
      print('❌ ApiService.login: DioException caught');
      throw _handleError(e);
    } catch (e) {
      print('❌ ApiService.login: Unexpected error: $e (${e.runtimeType})');
      rethrow;
    }
  }

  // User endpoints
  Future<Map<String, dynamic>> getUserProfile() async {
    try {
      final response = await _performRequestWithFallback(
        () => dio.get('/user/profile'),
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateUserProfile({
    required Map<String, dynamic> data,
  }) async {
    try {
      final response = await _performRequestWithFallback(
        () => dio.put('/user/profile', data: data),
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Chat endpoints
  Future<Map<String, dynamic>> sendMessage({
    required String message,
    String? conversationId,
  }) async {
    try {
      final response = await _performRequestWithFallback(
        () => dio.post(
          '/chat',
          data: {
            'message': message,
            'conversation_id': conversationId,
          },
        ),
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // ── Planning endpoints ────────────────────────────────────────────────────
  Future<dynamic> getTasks() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/planning/tasks'));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<dynamic> createTask({
    required String title,
    required String category,
    required DateTime dueDate,
    String? description,
    int priority = 1,
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post('/planning/tasks', data: {
        'title': title,
        'category': category,
        'due_date': dueDate.toIso8601String(),
        'description': description,
        'priority': priority,
      }));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<void> updateTask({required int taskId, String? status, int? priority}) async {
    try {
      await _performRequestWithFallback(() => dio.put('/planning/tasks/$taskId', data: {
        if (status != null) 'status': status,
        if (priority != null) 'priority': priority,
      }));
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<void> deleteTask(int taskId) async {
    try {
      await _performRequestWithFallback(() => dio.delete('/planning/tasks/$taskId'));
    } on DioException catch (e) { throw _handleError(e); }
  }

  // ── Campus / Events endpoints ─────────────────────────────────────────────
  Future<dynamic> getEvents() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/campus/events'));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  // ── Exams endpoints ───────────────────────────────────────────────────────
  Future<dynamic> getExamHistory() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/exams/history'));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<dynamic> getExamStats() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/exams/stats'));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<dynamic> generateExam({
    required String subject,
    int numQuestions = 5,
    String difficulty = 'medium',
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post('/exams/generate', data: {
        'subject': subject,
        'num_questions': numQuestions,
        'difficulty': difficulty,
      }));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<dynamic> submitExam({required int examId, required List<String?> answers}) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post('/exams/$examId/submit', data: {
        'exam_id': examId,
        'answers': answers,
      }));
      return r.data;
    } on DioException catch (e) { throw _handleError(e); }
  }

  // ── Admin Agent endpoints ─────────────────────────────────────────────────
  Future<Map<String, dynamic>> askAdminAgent({
    required String question,
    String? conversationId,
  }) async {
    // LangGraph ReAct agent needs up to 90s (LLM + tools + LLM again)
    const _agentTimeout = Duration(seconds: 90);
    try {
      final r = await _performRequestWithFallback(() => dio.post('/admin/ask',
        data: {
          'question': question,
          if (conversationId != null) 'conversation_id': conversationId,
        },
        options: Options(
          receiveTimeout: _agentTimeout,
          sendTimeout: _agentTimeout,
        ),
      ));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> getAttestationPrefill() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/admin/attestation/prefill'));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> generateAttestation({
    Map<String, dynamic> extraFields = const {},
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post(
        '/admin/attestation/generate',
        data: {'extra_fields': extraFields},
      ));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> createAdminRequest({
    required String requestType,
    String? description,
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post('/admin/requests', data: {
        'request_type': requestType,
        if (description != null) 'description': description,
      }));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<List<dynamic>> getAdminRequests() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/admin/requests'));
      return r.data as List<dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  // ── Modules & Course PDF endpoints ───────────────────────────────────────

  Future<Map<String, dynamic>> getModules({String? semestre}) async {
    try {
      final params = semestre != null ? {'semestre': semestre} : null;
      final r = await _performRequestWithFallback(
        () => dio.get('/user/modules', queryParameters: params),
      );
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> uploadCoursePdf({
    required String matiere,
    required String titre,
    required List<int> bytes,
    required String filename,
  }) async {
    try {
      final formData = FormData.fromMap({
        'matiere': matiere,
        'titre': titre,
        'file': MultipartFile.fromBytes(bytes, filename: filename),
      });
      final r = await _performRequestWithFallback(
        () => dio.post('/exams/courses/upload', data: formData,
            options: Options(
              contentType: 'multipart/form-data',
              receiveTimeout: const Duration(seconds: 60),
            )),
      );
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<List<dynamic>> getCourses() async {
    try {
      final r = await _performRequestWithFallback(() => dio.get('/exams/courses'));
      return r.data as List<dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<void> deleteCourse(int docId) async {
    try {
      await _performRequestWithFallback(() => dio.delete('/exams/courses/$docId'));
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> askCoursePdf({
    required int docId,
    required String question,
    String type = 'question',
  }) async {
    try {
      final r = await _performRequestWithFallback(
        () => dio.post('/exams/courses/$docId/ask',
            data: {'question': question, 'type': type},
            options: Options(receiveTimeout: const Duration(seconds: 90))),
      );
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> getOfficialSchedule({String? filiere, String? semestre}) async {
    try {
      final queryParams = <String, dynamic>{};
      if (filiere != null && filiere.isNotEmpty) queryParams['filiere'] = filiere;
      if (semestre != null && semestre.isNotEmpty) queryParams['semestre'] = semestre;
      final r = await _performRequestWithFallback(
        () => dio.get('/exams/official-schedule', queryParameters: queryParams),
      );
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  // ── Documents endpoints ───────────────────────────────────────────────────
  Future<Map<String, dynamic>> generateDocument({
    required String docType,
    String? description,
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post('/documents/generate', data: {
        'doc_type': docType,
        if (description != null && description.isNotEmpty) 'description': description,
      }));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> generateRecommendations({
    required String prenom,
    required String nom,
    String? cne,
    required String filiere,
    required String annee,
    required String typeDemande,
    required String description,
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post(
        '/recommendations/generate',
        data: {
          'prenom': prenom,
          'nom': nom,
          if (cne != null && cne.isNotEmpty) 'cne': cne,
          'filiere': filiere,
          'annee': annee,
          'type_demande': typeDemande,
          'description': description,
        },
        options: Options(receiveTimeout: const Duration(seconds: 60)),
      ));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<List<int>> downloadDocumentBytes(String docId) async {
    try {
      final r = await _performRequestWithFallback(() => dio.get(
        '/documents/download/$docId',
        options: Options(responseType: ResponseType.bytes),
      ));
      return (r.data as List).cast<int>();
    } on DioException catch (e) { throw _handleError(e); }
  }

  // ── Orientation endpoints ─────────────────────────────────────────────────
  Future<Map<String, dynamic>> analyzeCv({
    required List<int> fileBytes,
    required String filename,
    String? posteCible,
  }) async {
    try {
      final formData = FormData.fromMap({
        'cv_file': MultipartFile.fromBytes(fileBytes, filename: filename),
        if (posteCible != null && posteCible.isNotEmpty) 'poste_cible': posteCible,
      });
      final r = await _performRequestWithFallback(() => dio.post(
        '/orientation/analyze-cv',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
          receiveTimeout: const Duration(seconds: 90),
          sendTimeout: const Duration(seconds: 60),
        ),
      ));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> generateLm({
    required String poste,
    required String entreprise,
    String typeLm = 'startup',
    String? competences,
    String? projets,
  }) async {
    try {
      final r = await _performRequestWithFallback(() => dio.post(
        '/orientation/generate-lm',
        data: {
          'poste': poste,
          'entreprise': entreprise,
          'type_lm': typeLm,
          if (competences != null && competences.isNotEmpty) 'competences': competences,
          if (projets != null && projets.isNotEmpty) 'projets': projets,
        },
        options: Options(receiveTimeout: const Duration(seconds: 90)),
      ));
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  Future<Map<String, dynamic>> getStages({String? filiere, String? typeStage}) async {
    try {
      final params = <String, dynamic>{};
      if (filiere != null && filiere.isNotEmpty) params['filiere'] = filiere;
      if (typeStage != null && typeStage.isNotEmpty) params['type_stage'] = typeStage;
      final r = await _performRequestWithFallback(
        () => dio.get('/orientation/stages', queryParameters: params),
      );
      return r.data as Map<String, dynamic>;
    } on DioException catch (e) { throw _handleError(e); }
  }

  // Error handling
  String _handleError(DioException error) {
    print('🚨 ApiService: Error Handler Called');
    print('   Type: ${error.type}');
    print('   Message: ${error.message}');
    print('   Has Response: ${error.response != null}');
    
    if (error.response != null) {
      final data = error.response?.data;
      String errorMsg;
      if (data is Map) {
        errorMsg = data['detail']?.toString() ?? data['error']?.toString() ?? 'An error occurred';
      } else {
        errorMsg = data?.toString() ?? 'An error occurred';
      }
      print('   Server Error: $errorMsg');
      return errorMsg;
    } else if (error.type == DioExceptionType.connectionTimeout) {
      print('   -> Connection Timeout');
      return 'Connection timeout - Check your network connection';
    } else if (error.type == DioExceptionType.receiveTimeout) {
      print('   -> Receive Timeout');
      return 'Request timeout - Server took too long to respond';
    } else {
      print('   -> Network Error (${error.type})');
      return 'Network error. Tried ${dio.options.baseUrl}. If you run on Android emulator, use 10.0.2.2; for Genymotion use 10.0.3.2; for a physical device use your PC IP on port 8000. Also verify the backend is running and reachable.';
    }
  }

  // Diagnostic method to test which URLs are reachable
  Future<void> diagnoseConnectivity() async {
    print('\n🔍 === CONNECTIVITY DIAGNOSTIC ===');
    print('📍 Testing ${_baseUrls.length} URLs:');
    
    for (var i = 0; i < _baseUrls.length; i++) {
      final url = _baseUrls[i];
      print('\n🔗 [$i+1] Testing: $url');
      
      try {
        final testDio = Dio();
        testDio.options.connectTimeout = Duration(seconds: 10);
        testDio.options.receiveTimeout = Duration(seconds: 10);
        
        final diagnosticsUrl = Uri.parse(url).resolve('/docs').toString();
        final response = await testDio.get(diagnosticsUrl, // Simple endpoint to test
          options: Options(
            validateStatus: (status) => true, // Accept any status
          ),
        );
        
        print('   ✅ Reachable! Status: ${response.statusCode}');
      } catch (e) {
        print('   ❌ Not reachable: $e');
      }
    }
    
    print('\n=== END DIAGNOSTIC ===\n');
  }
}

// Riverpod provider
final dioProvider = Provider((ref) {
  return Dio();
});

final apiServiceProvider = Provider((ref) {
  final dio = ref.watch(dioProvider);
  final secureStorage = ref.watch(secureStorageServiceProvider);
  return ApiService(dio: dio, secureStorage: secureStorage);
});
