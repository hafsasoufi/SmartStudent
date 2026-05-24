import 'package:flutter/material.dart';

class NotificationModel {
  final String id;
  final String title;
  final String message;
  final NotificationType type;
  final DateTime createdAt;
  bool isRead;

  NotificationModel({
    required this.id,
    required this.title,
    required this.message,
    required this.type,
    required this.createdAt,
    this.isRead = false,
  });
}

enum NotificationType {
  deadline('Deadline', Colors.orange),
  exam('Exam', Colors.red),
  event('Event', Colors.blue),
  message('Message', Colors.green),
  achievement('Achievement', Colors.purple),
  system('System', Colors.grey);

  final String label;
  final Color color;

  const NotificationType(this.label, this.color);
}

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();

  final List<NotificationModel> _notifications = [];

  NotificationService._internal();

  factory NotificationService() {
    return _instance;
  }

  List<NotificationModel> get notifications => _notifications;

  List<NotificationModel> get unreadNotifications =>
      _notifications.where((n) => !n.isRead).toList();

  void addNotification({
    required String title,
    required String message,
    required NotificationType type,
  }) {
    final notification = NotificationModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: title,
      message: message,
      type: type,
      createdAt: DateTime.now(),
    );
    _notifications.insert(0, notification);
  }

  void markAsRead(String notificationId) {
    final index = _notifications.indexWhere((n) => n.id == notificationId);
    if (index != -1) {
      _notifications[index].isRead = true;
    }
  }

  void markAllAsRead() {
    for (var notification in _notifications) {
      notification.isRead = true;
    }
  }

  void removeNotification(String notificationId) {
    _notifications.removeWhere((n) => n.id == notificationId);
  }

  void clearAll() {
    _notifications.clear();
  }

  // Simulated incoming notifications
  void simulateNotifications() {
    Future.delayed(const Duration(seconds: 3), () {
      addNotification(
        title: 'Math Assignment Due',
        message: 'Your Math 101 assignment is due in 3 days',
        type: NotificationType.deadline,
      );
    });

    Future.delayed(const Duration(seconds: 6), () {
      addNotification(
        title: 'New Study Group',
        message: 'Join the Calculus II study group meeting today at 4 PM',
        type: NotificationType.event,
      );
    });

    Future.delayed(const Duration(seconds: 9), () {
      addNotification(
        title: 'Achievement Unlocked',
        message: 'You\'ve completed 10 practice quizzes!',
        type: NotificationType.achievement,
      );
    });
  }
}
