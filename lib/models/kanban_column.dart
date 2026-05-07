import 'package:flutter/material.dart';

class KanbanColumn {
  final String userId; // String
  final int boardId;
  final String title;
  final String status;
  final Color color;
  final int position;

  KanbanColumn({
    required this.userId,
    required this.boardId,
    required this.title,
    required this.status,
    required this.color,
    required this.position,
  });

  Map<String, dynamic> toMap() {
    return {
      'userId': userId,
      'boardId': boardId,
      'title': title,
      'status': status,
      'color': color.value,
      'position': position,
    };
  }
}
