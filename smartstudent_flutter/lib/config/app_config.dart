class AppConfig {
  static const String appName = 'SmartStudent';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  static const String apiBaseUrl = 'http://localhost:8000/api';
  static const String apiTimeout = '30';
  
  // Firebase Configuration
  static const String firebaseProjectId = 'smartstudent-ai';
  
  // Languages
  static const List<String> supportedLanguages = ['en', 'fr', 'ar'];
  static const String defaultLanguage = 'en';
  
  // Feature Flags
  static const bool enableAnalytics = true;
  static const bool enableCrashReporting = true;
}
