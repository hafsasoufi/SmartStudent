class Event {
  final int id;
  final String title;
  final String? description;
  final String eventType;
  final DateTime startDate;
  final DateTime? endDate;
  final String? location;
  final bool isPublic;
  final DateTime createdAt;

  Event({
    required this.id,
    required this.title,
    this.description,
    required this.eventType,
    required this.startDate,
    this.endDate,
    this.location,
    required this.isPublic,
    required this.createdAt,
  });

  factory Event.fromJson(Map<String, dynamic> json) {
    return Event(
      id: json['id'] as int,
      title: json['title'] as String,
      description: json['description'] as String?,
      eventType: json['event_type'] as String? ?? 'event',
      startDate: DateTime.parse(json['start_date'] as String),
      endDate: json['end_date'] != null
          ? DateTime.parse(json['end_date'] as String)
          : null,
      location: json['location'] as String?,
      isPublic: json['is_public'] as bool? ?? true,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'description': description,
        'event_type': eventType,
        'start_date': startDate.toIso8601String(),
        'end_date': endDate?.toIso8601String(),
        'location': location,
        'is_public': isPublic,
        'created_at': createdAt.toIso8601String(),
      };
}
