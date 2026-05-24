class User {
  final String id;
  final String email;
  final String fullName;
  final String? bio;
  final String? avatar;
  final DateTime? createdAt;

  User({
    required this.id,
    required this.email,
    required this.fullName,
    this.bio,
    this.avatar,
    this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      fullName: json['full_name'],
      bio: json['bio'],
      avatar: json['avatar'],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'full_name': fullName,
    'bio': bio,
    'avatar': avatar,
    'created_at': createdAt?.toIso8601String(),
  };
}
