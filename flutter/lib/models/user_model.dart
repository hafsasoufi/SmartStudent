class User {
  final int id;
  final String email;
  final String username;
  final String fullName;
  final String? firstName;
  final String? lastName;
  final bool isActive;
  final bool isAdmin;
  final DateTime createdAt;

  User({
    required this.id,
    required this.email,
    required this.username,
    required this.fullName,
    this.firstName,
    this.lastName,
    required this.isActive,
    this.isAdmin = false,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      username: json['username'] as String,
      fullName: json['full_name'] as String? ?? '',
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      isActive: json['is_active'] as bool? ?? true,
      isAdmin: json['is_admin'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
      'full_name': fullName,
      'first_name': firstName,
      'last_name': lastName,
      'is_active': isActive,
      'is_admin': isAdmin,
      'created_at': createdAt.toIso8601String(),
    };
  }

  String get displayName => fullName.isNotEmpty ? fullName : username;
}

class UserProfile {
  final int id;
  final int userId;
  final String? bio;
  final String? avatarUrl;
  final String? phone;
  final String? university;
  final String? major;
  final int? year;
  final String? studentCardId;
  final String language;
  final String timezone;

  UserProfile({
    required this.id,
    required this.userId,
    this.bio,
    this.avatarUrl,
    this.phone,
    this.university,
    this.major,
    this.year,
    this.studentCardId,
    this.language = 'en',
    this.timezone = 'UTC',
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'] as int,
      userId: json['user_id'] as int,
      bio: json['bio'] as String?,
      avatarUrl: json['avatar_url'] as String?,
      phone: json['phone'] as String?,
      university: json['university'] as String?,
      major: json['major'] as String?,
      year: json['year'] as int?,
      studentCardId: json['student_card_id'] as String?,
      language: json['language'] as String? ?? 'en',
      timezone: json['timezone'] as String? ?? 'UTC',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'bio': bio,
      'avatar_url': avatarUrl,
      'phone': phone,
      'university': university,
      'major': major,
      'year': year,
      'student_card_id': studentCardId,
      'language': language,
      'timezone': timezone,
    };
  }
}
