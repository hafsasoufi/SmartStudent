class AppConfig {
  static const String appName = 'SmartStudent';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  // The client tries several common local endpoints until one works.
  static const List<String> apiBaseUrls = [
    'http://localhost:8000/api',      // [0] USB (adb reverse) — PRIORITAIRE
    'http://127.0.0.1:8000/api',      // [1] USB (adb reverse) — fallback
    'http://192.168.3.19:8000/api',   // [2] PC WiFi IP (réseau actuel)
    'http://192.168.137.1:8000/api',  // [3] PC hotspot IP (Windows Mobile Hotspot)
    'http://172.20.10.2:8000/api',    // [4] PC IP (hotspot network)
    'http://192.168.8.135:8000/api',  // [5] PC WiFi IP (home/office network)
    'http://10.0.2.2:8000/api',       // [6] Android emulator
    'http://10.30.29.176:8000/api',   // [7] PC IP (old university WiFi)
  ];
  static const String apiTimeout = '30'; // seconds per URL attempt
  
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
