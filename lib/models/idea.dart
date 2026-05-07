enum IdeaPriority { low, medium, high }

enum IdeaStatus { backlog, inProgress, done }

enum IdeaCategory { product, marketing, business, tech, design, sales, other }

class Idea {
  int? id;
  String userId;
  int boardId;
  String title;
  String description;
  IdeaPriority priority;
  IdeaCategory category;
  String status; // Changed to String for flexibility
  DateTime createdAt;
  DateTime? updatedAt;
  DateTime? dueDate;
  List<String> tags;
  int votes;

  Idea({
    this.id,
    required this.userId,
    this.boardId = 1,
    required this.title,
    required this.description,
    required this.priority,
    this.category = IdeaCategory.other,
    this.status = 'Backlog',
    DateTime? createdAt,
    this.updatedAt,
    this.dueDate,
    List<String>? tags,
    this.votes = 0,
  }) : createdAt = createdAt ?? DateTime.now(),
       tags = tags ?? [];

  // Convertir en Map pour SQLite
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'userId': userId,
      'boardId': boardId,
      'title': title,
      'description': description,
      'priority': priority.index,
      'category': category.name,
      'status': status,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt?.toIso8601String(),
      'dueDate': dueDate?.toIso8601String(),
      'tags': tags.join(','),
      'votes': votes,
    };
  }

  // Créer à partir d'un Map
  factory Idea.fromMap(Map<String, dynamic> map) {
    IdeaCategory category;
    if (map['category'] != null) {
      try {
        category = IdeaCategory.values.firstWhere(
          (e) => e.name == map['category'],
          orElse: () => IdeaCategory.other,
        );
      } catch (_) {
        category = IdeaCategory.other;
      }
    } else {
      category = IdeaCategory.other;
    }

    return Idea(
      id: map['id'] as int?,
      userId: map['userId'] as String? ?? '',
      boardId: map['boardId'] as int? ?? 1,
      title: map['title'] as String? ?? '',
      description: map['description'] as String? ?? '',
      priority: IdeaPriority.values[map['priority'] as int? ?? 0],
      category: category,
      status: map['status'] as String? ?? 'Backlog',
      createdAt: map['createdAt'] != null
          ? DateTime.parse(map['createdAt'] as String)
          : DateTime.now(),
      updatedAt: map['updatedAt'] != null
          ? DateTime.parse(map['updatedAt'] as String)
          : null,
      dueDate: map['dueDate'] != null
          ? DateTime.parse(map['dueDate'] as String)
          : null,
      tags: map['tags'] != null && (map['tags'] as String).isNotEmpty
          ? (map['tags'] as String).split(',')
          : [],
      votes: map['votes'] as int? ?? 0,
    );
  }

  bool get isOverdue =>
      dueDate != null && dueDate!.isBefore(DateTime.now()) && status != 'Done';

  // Helpers pour obtenir les labels en français
  String get priorityLabel {
    switch (priority) {
      case IdeaPriority.high:
        return 'Haute';
      case IdeaPriority.medium:
        return 'Moyenne';
      case IdeaPriority.low:
        return 'Basse';
    }
  }

  String get categoryLabel {
    switch (category) {
      case IdeaCategory.product:
        return 'Produit';
      case IdeaCategory.marketing:
        return 'Marketing';
      case IdeaCategory.business:
        return 'Business';
      case IdeaCategory.tech:
        return 'Tech';
      case IdeaCategory.design:
        return 'Design';
      case IdeaCategory.sales:
        return 'Ventes';
      case IdeaCategory.other:
        return 'Autre';
    }
  }

  @override
  String toString() {
    return 'Idea(id: $id, boardId: $boardId, title: $title, description: $description, priority: $priority, category: $category, status: $status, createdAt: $createdAt, updatedAt: $updatedAt, dueDate: $dueDate, tags: $tags, votes: $votes)';
  }
}
