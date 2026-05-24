import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'config/app_config.dart';
import 'config/app_theme.dart';
import 'routes/app_routes.dart';
import 'services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase and notifications
  await NotificationService.initialize();
  
  runApp(
    const ProviderScope(
      child: SmartStudentApp(),
    ),
  );
}

class SmartStudentApp extends StatefulWidget {
  const SmartStudentApp({Key? key}) : super(key: key);

  @override
  State<SmartStudentApp> createState() => _SmartStudentAppState();
}

class _SmartStudentAppState extends State<SmartStudentApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'SmartStudent',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routerConfig: AppRoutes.router,
      debugShowCheckedModeBanner: false,
    );
  }
}
