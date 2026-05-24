class Message {
  final int id;
  final int userId;
  final String content;
  final String sender; // "user" or "assistant"
  final String messageType; // "text", "image", "document"
  final Map<String, dynamic>? metadata;
  final DateTime createdAt;

  Message({
    required this.id,
    required this.userId,
    required this.content,
    required this.sender,
    required this.messageType,
    this.metadata,
    required this.createdAt,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'] as int,
      userId: json['user_id'] as int,
      content: json['content'] as String,
      sender: json['sender'] as String,
      messageType: json['message_type'] as String? ?? 'text',
      metadata: json['metadata'] as Map<String, dynamic>?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'content': content,
      'sender': sender,
      'message_type': messageType,
      'metadata': metadata,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

class ChatMessage {
  final String id;
  final String content;
  final String sender; // "user" or "assistant"
  final DateTime timestamp;
  final String? agent;
  final Map<String, dynamic>? metadata;

  ChatMessage({
    required this.id,
    required this.content,
    required this.sender,
    required this.timestamp,
    this.agent,
    this.metadata,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'] as String,
      content: json['content'] as String,
      sender: json['sender'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      agent: json['agent'] as String?,
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'content': content,
      'sender': sender,
      'timestamp': timestamp.toIso8601String(),
      'agent': agent,
      'metadata': metadata,
    };
  }
}
