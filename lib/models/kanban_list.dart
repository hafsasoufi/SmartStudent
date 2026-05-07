import 'package:flutter/material.dart';
import 'package:startuplaunchpad/models/task.dart';

class KanbanList {
  String title;
  String subtitle;
  Color color;
  List<Task> tasks;

  KanbanList({
    required this.title,
    required this.subtitle,
    required this.color,
    required this.tasks,
  });

  void sortByPriority() {
    tasks.sort((a, b) => a.priority.index.compareTo(b.priority.index));
  }
}
