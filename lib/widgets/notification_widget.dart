import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';

class NotificationWidget extends StatelessWidget {
  const NotificationWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<IdeaProvider>(
      builder: (context, provider, child) {
        final notifications = _generateNotifications(provider);

        if (notifications.isEmpty) {
          return const SizedBox.shrink();
        }

        return Card(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          color: Colors.blue[50],
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(
                      Icons.notifications_active,
                      color: Colors.blue[700],
                      size: 20,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Notifications',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue[900],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                ...notifications.map(
                  (notif) => _buildNotificationItem(
                    notif['icon'] as IconData,
                    notif['message'] as String,
                    notif['color'] as Color,
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  List<Map<String, dynamic>> _generateNotifications(IdeaProvider provider) {
    final notifications = <Map<String, dynamic>>[];

    // Notification pour les tâches haute priorité dans le backlog
    final highPriorityBacklog = provider.ideas
        .where((idea) => idea['priority'] == 2 && idea['status'] == 'Backlog')
        .length;

    if (highPriorityBacklog > 0) {
      notifications.add({
        'icon': Icons.priority_high,
        'message':
            '$highPriorityBacklog tâche${highPriorityBacklog > 1 ? 's' : ''} en priorité haute dans le backlog',
        'color': Colors.red,
      });
    }

    // Notification pour le pourcentage d'avancement
    final progress = provider.getProgress();
    final progressPercent = (progress * 100).toInt();

    if (progressPercent >= 80) {
      notifications.add({
        'icon': Icons.celebration,
        'message':
            'Félicitations ! Vous avez terminé $progressPercent% de vos objectifs',
        'color': Colors.green,
      });
    } else if (progressPercent >= 50) {
      notifications.add({
        'icon': Icons.trending_up,
        'message':
            'Bon travail ! $progressPercent% de vos objectifs sont atteints',
        'color': Colors.orange,
      });
    }

    // Notification pour les idées en cours
    final inProgressCount = provider.ideas
        .where((idea) => idea['status'] == 'In Progress')
        .length;

    if (inProgressCount > 5) {
      notifications.add({
        'icon': Icons.warning,
        'message':
            'Vous avez $inProgressCount idées en cours. Pensez à en terminer quelques-unes !',
        'color': Colors.orange,
      });
    }

    // Notification pour les échéances proches
    final now = DateTime.now();
    final upcomingDeadlines = provider.ideas.where((idea) {
      if (idea['dueDate'] == null || idea['status'] == 'Done') return false;

      try {
        final dueDate = DateTime.parse(idea['dueDate'] as String);
        final daysUntil = dueDate.difference(now).inDays;
        return daysUntil >= 0 && daysUntil <= 7;
      } catch (e) {
        return false;
      }
    }).length;

    if (upcomingDeadlines > 0) {
      notifications.add({
        'icon': Icons.access_time,
        'message':
            '$upcomingDeadlines échéance${upcomingDeadlines > 1 ? 's' : ''} dans les 7 prochains jours',
        'color': Colors.red,
      });
    }

    // Notification pour les idées en retard
    final overdueIdeas = provider.ideas.where((idea) {
      if (idea['dueDate'] == null || idea['status'] == 'Done') return false;

      try {
        final dueDate = DateTime.parse(idea['dueDate'] as String);
        return dueDate.isBefore(now);
      } catch (e) {
        return false;
      }
    }).length;

    if (overdueIdeas > 0) {
      notifications.add({
        'icon': Icons.error,
        'message':
            '⚠️ $overdueIdeas tâche${overdueIdeas > 1 ? 's' : ''} en retard !',
        'color': Colors.red[700]!,
      });
    }

    // Notification pour encourager l'utilisation des catégories
    final ideasWithoutCategory = provider.ideas
        .where(
          (idea) => idea['category'] == null || idea['category'] == 'other',
        )
        .length;

    if (ideasWithoutCategory > 5) {
      notifications.add({
        'icon': Icons.label,
        'message':
            '$ideasWithoutCategory idées sans catégorie définie. Organisez-les !',
        'color': Colors.blue,
      });
    }

    return notifications;
  }

  Widget _buildNotificationItem(IconData icon, String message, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 16),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              message,
              style: TextStyle(fontSize: 12, color: Colors.grey[800]),
            ),
          ),
        ],
      ),
    );
  }
}

/// Widget pour afficher une notification inline dans la page
class InlineNotification extends StatelessWidget {
  final String message;
  final IconData icon;
  final Color backgroundColor;
  final Color textColor;
  final VoidCallback? onDismiss;

  const InlineNotification({
    super.key,
    required this.message,
    this.icon = Icons.info,
    this.backgroundColor = Colors.blue,
    this.textColor = Colors.white,
    this.onDismiss,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: backgroundColor.withOpacity(0.1),
        border: Border.all(color: backgroundColor),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Icon(icon, color: backgroundColor),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message,
              style: TextStyle(
                color: backgroundColor,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          if (onDismiss != null)
            IconButton(
              icon: Icon(Icons.close, color: backgroundColor),
              onPressed: onDismiss,
              iconSize: 20,
            ),
        ],
      ),
    );
  }
}

/// Service pour gérer les notifications
class NotificationService {
  /// Vérifie et retourne les notifications à afficher
  static List<String> checkNotifications(IdeaProvider provider) {
    final notifications = <String>[];
    final now = DateTime.now();

    // Tâches haute priorité
    final highPriorityCount = provider.ideas
        .where((idea) => idea['priority'] == 2 && idea['status'] != 'Done')
        .length;

    if (highPriorityCount > 0) {
      notifications.add(
        '🔴 $highPriorityCount tâche${highPriorityCount > 1 ? 's' : ''} haute priorité en attente',
      );
    }

    // Progression
    final progress = provider.getProgress();
    final progressPercent = (progress * 100).toInt();

    if (progressPercent >= 80) {
      notifications.add(
        '🎉 Excellent ! $progressPercent% de vos objectifs atteints !',
      );
    } else if (progressPercent == 100) {
      notifications.add(
        '🏆 Félicitations ! Tous vos objectifs sont atteints !',
      );
    }

    // Échéances proches
    final upcomingDeadlines = provider.ideas.where((idea) {
      if (idea['dueDate'] == null || idea['status'] == 'Done') return false;
      try {
        final dueDate = DateTime.parse(idea['dueDate'] as String);
        final daysUntil = dueDate.difference(now).inDays;
        return daysUntil >= 0 && daysUntil <= 3;
      } catch (e) {
        return false;
      }
    }).length;

    if (upcomingDeadlines > 0) {
      notifications.add(
        '⏰ $upcomingDeadlines échéance${upcomingDeadlines > 1 ? 's' : ''} dans 3 jours',
      );
    }

    // Idées en retard
    final overdueCount = provider.ideas.where((idea) {
      if (idea['dueDate'] == null || idea['status'] == 'Done') return false;
      try {
        final dueDate = DateTime.parse(idea['dueDate'] as String);
        return dueDate.isBefore(now);
      } catch (e) {
        return false;
      }
    }).length;

    if (overdueCount > 0) {
      notifications.add(
        '⚠️ $overdueCount tâche${overdueCount > 1 ? 's' : ''} en retard !',
      );
    }

    return notifications;
  }

  /// Affiche une snackbar avec notification
  static void showNotification(
    BuildContext context,
    String message, {
    Color backgroundColor = Colors.blue,
    Duration duration = const Duration(seconds: 4),
  }) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.notifications, color: Colors.white),
            const SizedBox(width: 8),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: backgroundColor,
        duration: duration,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }
}
