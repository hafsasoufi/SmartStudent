import 'package:flutter/material.dart';

enum Priority { high, medium, low }

class Task {
  String title;
  Priority priority;

  Task({required this.title, required this.priority});

  Color get color {
    switch (priority) {
      case Priority.high:
        return Colors.red;
      case Priority.medium:
        return Colors.orange;
      case Priority.low:
        return Colors.green;
    }
  }

  IconData get icon {
    switch (priority) {
      case Priority.high:
        return Icons.priority_high;
      case Priority.medium:
        return Icons.trending_up;
      case Priority.low:
        return Icons.low_priority;
    }
  }

  String get label {
    switch (priority) {
      case Priority.high:
        return 'HIGH';
      case Priority.medium:
        return 'MED';
      case Priority.low:
        return 'LOW';
    }
  }
}
