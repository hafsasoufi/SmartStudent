import 'package:firebase_messaging/firebase_messaging.dart';

class NotificationService {
  static final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;

  static Future<void> initialize() async {
    try {
      // Request permission
      final settings = await _firebaseMessaging.requestPermission(
        alert: true,
        announcement: false,
        badge: true,
        carPlay: false,
        criticalAlert: false,
        provisional: false,
        sound: true,
      );

      if (settings.authorizationStatus == AuthorizationStatus.authorized) {
        // Get token
        final token = await _firebaseMessaging.getToken();
        print('[Notifications] FCM Token: $token');

        // Handle foreground messages
        FirebaseMessaging.onMessage.listen((message) {
          _handleMessage(message);
        });

        // Handle background messages
        FirebaseMessaging.onMessageOpenedApp.listen((message) {
          _handleMessage(message);
        });
      }
    } catch (e) {
      print('[Notifications] Error initializing: $e');
    }
  }

  static void _handleMessage(RemoteMessage message) {
    print('[Notifications] Message received: ${message.messageId}');
    print('[Notifications] Title: ${message.notification?.title}');
    print('[Notifications] Body: ${message.notification?.body}');
  }

  static Future<String?> getToken() async {
    return await _firebaseMessaging.getToken();
  }
}
