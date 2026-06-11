class AppConfig {
  static const String appName = 'SmartStudent';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  // The client tries several common local endpoints until one works.
  static const List<String> apiBaseUrls = [
    'http://localhost:8000/api',      // USB (adb reverse) — PRIORITAIRE
    'http://127.0.0.1:8000/api',      // USB (adb reverse) — fallback
    'http://192.168.1.106:8000/api',  // PC WiFi (réseau actuel)
    'http://172.20.10.2:8000/api',    // PC IP (hotspot network)
    'http://192.168.8.135:8000/api',  // PC WiFi IP (home/office network)
    'http://192.168.137.1:8000/api',  // PC hotspot IP (Windows Mobile Hotspot)
    'http://10.0.2.2:8000/api',       // Android emulator
    'http://10.30.29.176:8000/api',   // PC IP (old university WiFi)
  ];
  static const String apiTimeout = '15'; // seconds per URL attempt (regular endpoints)
  
  // Feature Flags
  static const bool enableOfflineMode = true;
  static const bool enablePushNotifications = true;
  static const bool enableAnalytics = true;
  
  // App Settings
  static const int maxRetries = 3;
  static const int cacheDurationMinutes = 60;
  
  // Supported Languages
  static const Map<String, String> supportedLanguages = {
    'en': 'English',
    'fr': 'Français',
    'ar': 'العربية',
  };
  
  static const String defaultLanguage = 'en';
}
