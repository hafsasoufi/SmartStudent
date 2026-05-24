import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/home/home_screen.dart';
import '../screens/chat/chat_screen.dart';
import '../screens/modules/admin_screen.dart';
import '../screens/modules/planning_screen.dart';
import '../screens/modules/exams_screen.dart';
import '../screens/modules/orientation_screen.dart';
import '../screens/modules/campus_screen.dart';
import '../screens/modules/wellbeing_screen.dart';

class AppRoutes {
  static final GlobalKey<NavigatorState> rootNavigatorKey =
      GlobalKey<NavigatorState>();

  static final GoRouter router = GoRouter(
    navigatorKey: rootNavigatorKey,
    initialLocation: '/login',
    routes: [
      // Auth Routes
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),

      // Main Routes
      GoRoute(
        path: '/home',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),

      // Chat Route
      GoRoute(
        path: '/chat',
        name: 'chat',
        builder: (context, state) => const ChatScreen(),
      ),

      // Module Routes
      GoRoute(
        path: '/admin',
        name: 'admin',
        builder: (context, state) => const AdminScreen(),
      ),
      GoRoute(
        path: '/planning',
        name: 'planning',
        builder: (context, state) => const PlanningScreen(),
      ),
      GoRoute(
        path: '/exams',
        name: 'exams',
        builder: (context, state) => const ExamsScreen(),
      ),
      GoRoute(
        path: '/orientation',
        name: 'orientation',
        builder: (context, state) => const OrientationScreen(),
      ),
      GoRoute(
        path: '/campus',
        name: 'campus',
        builder: (context, state) => const CampusScreen(),
      ),
      GoRoute(
        path: '/wellbeing',
        name: 'wellbeing',
        builder: (context, state) => const WellbeingScreen(),
      ),
    ],
    redirect: (context, state) {
      // Handle auth redirect
      final isLoggedIn = context.read(authProvider).isAuthenticated;
      final isLoggingIn = state.path == '/login' || state.path == '/register';

      if (!isLoggedIn && !isLoggingIn) {
        return '/login';
      }

      if (isLoggedIn && isLoggingIn) {
        return '/home';
      }

      return null;
    },
  );
}
