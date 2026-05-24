import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/message_model.dart';
import '../services/api_service.dart';

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  return ChatNotifier(ApiService());
});

class ChatState {
  final List<Message> messages;
  final bool isLoading;
  final String? error;
  final String? currentAgent;

  ChatState({
    this.messages = const [],
    this.isLoading = false,
    this.error,
    this.currentAgent,
  });

  ChatState copyWith({
    List<Message>? messages,
    bool? isLoading,
    String? error,
    String? currentAgent,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      currentAgent: currentAgent ?? this.currentAgent,
    );
  }
}

class ChatNotifier extends StateNotifier<ChatState> {
  final ApiService _apiService;

  ChatNotifier(this._apiService) : super(ChatState());

  Future<void> sendMessage(String messageText) async {
    if (messageText.isEmpty) return;

    // Add user message
    final userMessage = Message(
      id: DateTime.now().toString(),
      content: messageText,
      sender: 'user',
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMessage],
      isLoading: true,
      error: null,
    );

    try {
      final response = await _apiService.sendMessage(
        message: messageText,
        conversationId: null,
      );

      final assistantMessage = Message(
        id: response['id'],
        content: response['response'],
        sender: 'assistant',
        timestamp: DateTime.now(),
        agent: response['agent'],
      );

      state = state.copyWith(
        messages: [...state.messages, assistantMessage],
        isLoading: false,
        currentAgent: response['agent'],
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  void clearError() {
    state = state.copyWith(error: null);
  }

  void clearMessages() {
    state = state.copyWith(messages: []);
  }
}
