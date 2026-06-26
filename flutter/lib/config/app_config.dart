class AppConfig {
  static const String appName = 'SmartStudent';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  // Order matters — each URL is tried in sequence until one responds.
  // [0] Current PC WiFi IP  ← Android devices on same WiFi use this
  // [1] Android emulator    ← AVD uses 10.0.2.2 to reach the host
  // [2] USB adb reverse     ← physical device connected via USB (run: adb reverse tcp:8000 tcp:8000)
  // [3] USB adb reverse     ← same, 127.0.0.1 alias
  // [4] Windows hotspot IP  ← phone tethered to PC hotspot
  // [5] Web / desktop       ← browser / desktop app running on same machine
  // [6] Web / desktop       ← same, 127.0.0.1 alias
  static const List<String> apiBaseUrls = [
    'http://192.168.8.135:8000/api',  // [0] PC WiFi IP (current)
    'http://10.0.2.2:8000/api',       // [1] Android emulator
    'http://localhost:8000/api',      // [2] USB adb reverse
    'http://127.0.0.1:8000/api',      // [3] USB adb reverse fallback
    'http://192.168.137.1:8000/api',  // [4] Windows Mobile Hotspot
    'http://localhost:8000/api',      // [5] Web / desktop
    'http://127.0.0.1:8000/api',      // [6] Web / desktop fallback
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
