class Board {
  final String userId; // String, correspond à user.email
  final String name;

  Board({required this.userId, required this.name});

  Map<String, dynamic> toMap() {
    return {'userId': userId, 'name': name};
  }
}
