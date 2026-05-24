import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';

// Per-module chat state (keyed by module name)
class _ModuleChatState {
  final List<_Msg> messages;
  final bool isLoading;

  const _ModuleChatState({this.messages = const [], this.isLoading = false});

  _ModuleChatState copyWith({List<_Msg>? messages, bool? isLoading}) =>
      _ModuleChatState(
        messages: messages ?? this.messages,
        isLoading: isLoading ?? this.isLoading,
      );
}

class _Msg {
  final String content;
  final bool isUser;
  final String? agentName;
  _Msg({required this.content, required this.isUser, this.agentName});
}

class _ModuleChatNotifier extends StateNotifier<_ModuleChatState> {
  final ApiService _api;
  final String _conversationId;

  _ModuleChatNotifier(this._api, String module)
      : _conversationId = '${module}_${DateTime.now().millisecondsSinceEpoch}',
        super(const _ModuleChatState());

  Future<void> send(String text) async {
    state = state.copyWith(
      messages: [...state.messages, _Msg(content: text, isUser: true)],
      isLoading: true,
    );
    try {
      final resp = await _api.sendMessage(
        message: text,
        conversationId: _conversationId,
      );
      final answer = resp['response'] as String? ?? '…';
      final agentName = resp['agent_name'] as String?;
      state = state.copyWith(
        messages: [...state.messages, _Msg(content: answer, isUser: false, agentName: agentName)],
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        messages: [
          ...state.messages,
          _Msg(content: 'Erreur : $e', isUser: false),
        ],
        isLoading: false,
      );
    }
  }
}

final _moduleChatProvider = StateNotifierProvider.family<
    _ModuleChatNotifier, _ModuleChatState, String>((ref, module) {
  return _ModuleChatNotifier(ref.watch(apiServiceProvider), module);
});

/// Embedded AI chat for a specific module.
/// [module]      : unique key — "orientation", "campus", "wellbeing"
/// [agentLabel]  : display name shown in the header chip
/// [suggestions] : quick-tap suggestion buttons
class ModuleAgentChat extends ConsumerStatefulWidget {
  final String module;
  final String agentLabel;
  final List<String> suggestions;
  final String placeholder;

  const ModuleAgentChat({
    Key? key,
    required this.module,
    required this.agentLabel,
    this.suggestions = const [],
    this.placeholder = 'Posez votre question…',
  }) : super(key: key);

  @override
  ConsumerState<ModuleAgentChat> createState() => _ModuleAgentChatState();
}

class _ModuleAgentChatState extends ConsumerState<ModuleAgentChat> {
  final _ctrl = TextEditingController();
  final _scroll = ScrollController();

  void _send([String? text]) {
    final msg = text ?? _ctrl.text.trim();
    if (msg.isEmpty) return;
    _ctrl.clear();
    ref.read(_moduleChatProvider(widget.module).notifier).send(msg);
    Future.delayed(const Duration(milliseconds: 150), () {
      if (_scroll.hasClients) {
        _scroll.animateTo(
          _scroll.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _ctrl.dispose();
    _scroll.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(_moduleChatProvider(widget.module));

    return Column(children: [
      // Agent header
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        color: AppTheme.primaryColor.withOpacity(0.08),
        child: Row(children: [
          CircleAvatar(
            radius: 16,
            backgroundColor: AppTheme.primaryColor.withOpacity(0.2),
            child: Icon(Icons.smart_toy, size: 18, color: AppTheme.primaryColor),
          ),
          const SizedBox(width: 10),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(widget.agentLabel,
                style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: AppTheme.primaryColor,
                    fontSize: 13)),
            const Text('Propulsé par Groq · Llama 3.3',
                style: TextStyle(fontSize: 11, color: Colors.grey)),
          ]),
        ]),
      ),

      // Messages
      Expanded(
        child: state.messages.isEmpty
            ? _EmptyState(agentLabel: widget.agentLabel)
            : ListView.builder(
                controller: _scroll,
                padding: const EdgeInsets.all(12),
                itemCount: state.messages.length + (state.isLoading ? 1 : 0),
                itemBuilder: (_, i) {
                  if (i == state.messages.length) return _TypingBubble();
                  final m = state.messages[i];
                  return _Bubble(msg: m);
                },
              ),
      ),

      // Suggestions
      if (widget.suggestions.isNotEmpty && state.messages.isEmpty)
        SizedBox(
          height: 40,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 12),
            children: widget.suggestions
                .map((s) => Padding(
                      padding: const EdgeInsets.only(right: 8),
                      child: ActionChip(
                        label: Text(s, style: const TextStyle(fontSize: 12)),
                        onPressed: () => _send(s),
                      ),
                    ))
                .toList(),
          ),
        ),

      // Input bar
      Container(
        padding: const EdgeInsets.fromLTRB(12, 8, 8, 12),
        decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4, offset: const Offset(0, -1))],
        ),
        child: Row(children: [
          Expanded(
            child: TextField(
              controller: _ctrl,
              decoration: InputDecoration(
                hintText: widget.placeholder,
                hintStyle: const TextStyle(fontSize: 14),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(24)),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                isDense: true,
              ),
              onSubmitted: (_) => _send(),
            ),
          ),
          const SizedBox(width: 8),
          FloatingActionButton.small(
            onPressed: state.isLoading ? null : _send,
            backgroundColor: AppTheme.primaryColor,
            child: Icon(
              state.isLoading ? Icons.hourglass_empty : Icons.send,
              size: 18,
              color: Colors.white,
            ),
          ),
        ]),
      ),
    ]);
  }
}

class _Bubble extends StatelessWidget {
  final _Msg msg;
  const _Bubble({required this.msg});

  @override
  Widget build(BuildContext context) {
    final isUser = msg.isUser;
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (!isUser)
            CircleAvatar(
              radius: 14,
              backgroundColor: AppTheme.primaryColor.withOpacity(0.15),
              child: Icon(Icons.smart_toy, size: 14, color: AppTheme.primaryColor),
            ),
          if (!isUser) const SizedBox(width: 6),
          Flexible(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: isUser
                    ? AppTheme.primaryColor
                    : Theme.of(context).cardColor,
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(16),
                  topRight: const Radius.circular(16),
                  bottomLeft: Radius.circular(isUser ? 16 : 4),
                  bottomRight: Radius.circular(isUser ? 4 : 16),
                ),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 4)],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (!isUser && msg.agentName != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text(msg.agentName!,
                          style: TextStyle(
                              fontSize: 10,
                              color: AppTheme.primaryColor,
                              fontWeight: FontWeight.bold)),
                    ),
                  Text(
                    msg.content,
                    style: TextStyle(
                      fontSize: 14,
                      color: isUser ? Colors.white : null,
                    ),
                  ),
                ],
              ),
            ),
          ),
          if (isUser) const SizedBox(width: 6),
          if (isUser)
            CircleAvatar(
              radius: 14,
              backgroundColor: Colors.grey.shade200,
              child: const Icon(Icons.person, size: 14, color: Colors.grey),
            ),
        ],
      ),
    );
  }
}

class _TypingBubble extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CircleAvatar(
          radius: 14,
          backgroundColor: AppTheme.primaryColor.withOpacity(0.15),
          child: Icon(Icons.smart_toy, size: 14, color: AppTheme.primaryColor),
        ),
        const SizedBox(width: 6),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            borderRadius: BorderRadius.circular(16),
          ),
          child: const SizedBox(
            width: 40,
            height: 16,
            child: _DotsIndicator(),
          ),
        ),
      ],
    );
  }
}

class _DotsIndicator extends StatefulWidget {
  const _DotsIndicator();

  @override
  State<_DotsIndicator> createState() => _DotsIndicatorState();
}

class _DotsIndicatorState extends State<_DotsIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _anim;

  @override
  void initState() {
    super.initState();
    _anim = AnimationController(vsync: this, duration: const Duration(milliseconds: 900))
      ..repeat();
  }

  @override
  void dispose() {
    _anim.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _anim,
      builder: (_, __) {
        return Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: List.generate(3, (i) {
            final offset = ((_anim.value * 3 - i) % 1.0).clamp(0.0, 1.0);
            final scale = 0.6 + 0.4 * (1 - (offset - 0.5).abs() * 2).clamp(0.0, 1.0);
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 2),
              child: Transform.scale(
                scale: scale,
                child: Container(
                  width: 7,
                  height: 7,
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor.withOpacity(0.6),
                    shape: BoxShape.circle,
                  ),
                ),
              ),
            );
          }),
        );
      },
    );
  }
}

class _EmptyState extends StatelessWidget {
  final String agentLabel;
  const _EmptyState({required this.agentLabel});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.chat_bubble_outline, size: 56, color: Colors.grey.shade300),
          const SizedBox(height: 12),
          Text('Parlez à $agentLabel',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 6),
          Text(
            'Posez vos questions ou utilisez les suggestions ci-dessous.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 13, color: Colors.grey.shade600),
          ),
        ]),
      ),
    );
  }
}
