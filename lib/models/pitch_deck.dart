enum PitchSlideType { title, problem, solution, market, business, traction, team, closing }

class PitchSlide {
  final PitchSlideType type;
  final String title;
  final String content;
  final List<String> bullets;

  PitchSlide({
    required this.type,
    required this.title,
    required this.content,
    this.bullets = const [],
  });

  Map<String, dynamic> toMap() {
    return {
      'type': type.name,
      'title': title,
      'content': content,
      'bullets': bullets.join('|||'),
    };
  }

  factory PitchSlide.fromMap(Map<String, dynamic> map) {
    return PitchSlide(
      type: PitchSlideType.values.firstWhere(
        (e) => e.name == map['type'],
        orElse: () => PitchSlideType.title,
      ),
      title: map['title'] ?? '',
      content: map['content'] ?? '',
      bullets: (map['bullets'] as String?)?.split('|||') ?? [],
    );
  }
}

class PitchDeck {
  int? id;
  int? ideaId;
  String userId;
  String title;
  String subtitle;
  String description;
  List<PitchSlide> slides;
  DateTime createdAt;
  DateTime? updatedAt;
  List<String> targetAudience;
  int duration; // in minutes

  PitchDeck({
    this.id,
    this.ideaId,
    required this.userId,
    required this.title,
    required this.subtitle,
    required this.description,
    List<PitchSlide>? slides,
    DateTime? createdAt,
    this.updatedAt,
    this.targetAudience = const [],
    this.duration = 5,
  })  : slides = slides ?? [],
        createdAt = createdAt ?? DateTime.now();

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'ideaId': ideaId,
      'userId': userId,
      'title': title,
      'subtitle': subtitle,
      'description': description,
      'slides': slides.map((s) => s.toMap()).toList(),
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt?.toIso8601String(),
      'targetAudience': targetAudience.join(','),
      'duration': duration,
    };
  }

  factory PitchDeck.fromMap(Map<String, dynamic> map) {
    return PitchDeck(
      id: map['id'],
      ideaId: map['ideaId'],
      userId: map['userId'] ?? '',
      title: map['title'] ?? '',
      subtitle: map['subtitle'] ?? '',
      description: map['description'] ?? '',
      slides: map['slides'] != null
          ? List<PitchSlide>.from(
              (map['slides'] as List).map((s) => PitchSlide.fromMap(s as Map<String, dynamic>)),
            )
          : [],
      createdAt: map['createdAt'] != null
          ? DateTime.parse(map['createdAt'] as String)
          : DateTime.now(),
      updatedAt: map['updatedAt'] != null ? DateTime.parse(map['updatedAt'] as String) : null,
      targetAudience: (map['targetAudience'] as String?)?.split(',') ?? [],
      duration: map['duration'] as int? ?? 5,
    );
  }
}
