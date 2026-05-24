class Message {
  final String id;
  final String content;
  final String sender;
  final DateTime timestamp;
  final String? agent;
  final String? type;

  Message({
    required this.id,
    required this.content,
    required this.sender,
    required this.timestamp,
    this.agent,
    this.type = 'text',
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      content: json['content'],
      sender: json['sender'],
      timestamp: DateTime.parse(json['timestamp']),
      agent: json['agent'],
      type: json['type'] ?? 'text',
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'content': content,
    'sender': sender,
    'timestamp': timestamp.toIso8601String(),
    'agent': agent,
    'type': type,
  };
}
