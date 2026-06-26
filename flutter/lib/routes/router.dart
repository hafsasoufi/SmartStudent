import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../providers/auth_provider.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/home/home_screen.dart';
import '../screens/chat/chat_screen.dart';
import '../screens/chat/recommendations_screen.dart';
import '../screens/modules/admin_module.dart';
import '../screens/modules/planning_module.dart';
import '../screens/modules/exams_module.dart';
import '../screens/modules/orientation_module.dart';
import '../screens/modules/campus_module.dart';
import '../screens/modules/wellbeing_module.dart';
import '../screens/profile/profile_screen.dart';
import '../screens/notifications_screen.dart';
import '../screens/settings_screen.dart';
import '../screens/admin/admin_dashboard_screen.dart';

class AuthNotifier extends ChangeNotifier {
  AuthNotifier(this.ref) {
    ref.listen(authProvider, (previous, next) {
      notifyListeners();
    });
  }
  
  final Ref ref;
}

final authNotifierProvider = Provider<AuthNotifier>((ref) {
  return AuthNotifier(ref);
});

final appRouterProvider = Provider<GoRouter>((ref) {
  final authNotifier = ref.watch(authNotifierProvider);

  return GoRouter(
    initialLocation: '/login',
    refreshListenable: authNotifier,
    redirect: (context, state) {
      final auth = ref.read(authProvider);
      final isAuthenticated = auth.isAuthenticated;
      final isLoggingIn = state.matchedLocation == '/login' || 
                          state.matchedLocation == '/register';

      if (!isAuthenticated && !isLoggingIn) {
        return '/login';
      }

      if (isAuthenticated && isLoggingIn) {
        return '/home';
      }

      return null;
    },
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
      GoRoute(
        path: '/chat',
        name: 'chat',
        builder: (context, state) => const ChatScreen(),
      ),
      GoRoute(
        path: '/home-chat',
        name: 'home-chat',
        builder: (context, state) => const ChatScreen(forceAgent: 'home'),
      ),
      GoRoute(
        path: '/recommendations',
        name: 'recommendations',
        builder: (context, state) => const RecommendationsScreen(),
      ),

      // Module Routes
      GoRoute(
        path: '/admin',
        name: 'admin',
        builder: (context, state) => const AdminModule(),
      ),
      GoRoute(
        path: '/planning',
        name: 'planning',
        builder: (context, state) => const PlanningModule(),
      ),
      GoRoute(
        path: '/exams',
        name: 'exams',
        builder: (context, state) => const ExamsModule(),
      ),
      GoRoute(
        path: '/orientation',
        name: 'orientation',
        builder: (context, state) => const OrientationModule(),
      ),
      GoRoute(
        path: '/campus',
        name: 'campus',
        builder: (context, state) => const CampusModule(),
      ),
      GoRoute(
        path: '/wellbeing',
        name: 'wellbeing',
        builder: (context, state) => const WellbeingModule(),
      ),

      // Profile Routes
      GoRoute(
        path: '/profile',
        name: 'profile',
        builder: (context, state) => const ProfileScreen(),
      ),

      // Notifications Route
      GoRoute(
        path: '/notifications',
        name: 'notifications',
        builder: (context, state) => const NotificationsScreen(),
      ),

      // Settings Route
      GoRoute(
        path: '/settings',
        name: 'settings',
        builder: (context, state) => const SettingsScreen(),
      ),

      // Admin Dashboard Route
      GoRoute(
        path: '/admin-dashboard',
        name: 'admin-dashboard',
        builder: (context, state) => const AdminDashboardScreen(),
      ),
    ],
  );
});
