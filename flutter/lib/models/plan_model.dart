class Plan {
  final int id;
  final int userId;
  final String title;
  final String? description;
  final String category;
  final DateTime dueDate;
  final int priority;
  final String status;
  final DateTime createdAt;

  Plan({
    required this.id,
    required this.userId,
    required this.title,
    this.description,
    required this.category,
    required this.dueDate,
    required this.priority,
    required this.status,
    required this.createdAt,
  });

  bool get isCompleted => status == 'completed';

  int get daysLeft => dueDate.difference(DateTime.now()).inDays;

  bool get isUrgent => daysLeft <= 2 && !isCompleted;

  factory Plan.fromJson(Map<String, dynamic> json) {
    return Plan(
      id: json['id'] as int,
      userId: json['user_id'] as int,
      title: json['title'] as String,
      description: json['description'] as String?,
      category: json['category'] as String? ?? 'study',
      dueDate: DateTime.parse(json['due_date'] as String),
      priority: json['priority'] as int? ?? 1,
      status: json['status'] as String? ?? 'pending',
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'user_id': userId,
        'title': title,
        'description': description,
        'category': category,
        'due_date': dueDate.toIso8601String(),
        'priority': priority,
        'status': status,
        'created_at': createdAt.toIso8601String(),
      };

  Plan copyWith({String? status}) => Plan(
        id: id,
        userId: userId,
        title: title,
        description: description,
        category: category,
        dueDate: dueDate,
        priority: priority,
        status: status ?? this.status,
        createdAt: createdAt,
      );
}
