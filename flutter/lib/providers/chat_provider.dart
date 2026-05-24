import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/message_model.dart';
import '../services/api_service.dart';

class ChatState {
  final List<ChatMessage> messages;
  final bool isLoading;
  final String? error;
  final String conversationId;
  final String? currentAgent;

  ChatState({
    this.messages = const [],
    this.isLoading = false,
    this.error,
    required this.conversationId,
    this.currentAgent,
  });

  ChatState copyWith({
    List<ChatMessage>? messages,
    bool? isLoading,
    String? error,
    String? conversationId,
    String? currentAgent,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      conversationId: conversationId ?? this.conversationId,
      currentAgent: currentAgent ?? this.currentAgent,
    );
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return ChatNotifier(apiService: apiService);
});

class ChatNotifier extends StateNotifier<ChatState> {
  final ApiService apiService;

  ChatNotifier({required this.apiService})
      : super(ChatState(conversationId: DateTime.now().millisecondsSinceEpoch.toString()));

  Future<void> sendMessage(String message) async {
    // Add user message to state immediately
    final userMessage = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: message,
      sender: "user",
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMessage],
      isLoading: true,
      error: null,
    );

    try {
      final response = await apiService.sendMessage(
        message: message,
        conversationId: state.conversationId,
      );

      final assistantMessage = ChatMessage(
        id: response['conversation_id'] ?? DateTime.now().millisecondsSinceEpoch.toString(),
        content: response['response'] ?? 'No response',
        sender: "assistant",
        timestamp: DateTime.now(),
        agent: response['agent'],
        metadata: response['metadata'] as Map<String, dynamic>?,
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

  void clearMessages() {
    state = ChatState(
      conversationId: DateTime.now().millisecondsSinceEpoch.toString(),
    );
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}
