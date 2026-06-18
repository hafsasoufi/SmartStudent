import 'package:flutter/material.dart';

import '../models/agent_route.dart';
import '../services/orchestrator_service.dart';

/// Chat screen backed by the SmartStudent Orchestrator. The student types a
/// message and the orchestrator returns which agent should handle it as strict
/// JSON `{agent, reason, query_type}`.
class AssistantScreen extends StatefulWidget {
  const AssistantScreen({super.key});

  @override
  State<AssistantScreen> createState() => _AssistantScreenState();
}

class _ChatMessage {
  _ChatMessage.user(this.text)
    : isUser = true,
      route = null,
      source = null;

  _ChatMessage.assistant(this.route, this.source)
    : isUser = false,
      text = '';

  final bool isUser;
  final String text;
  final AgentRoute? route;
  final RouteSource? source;
}

class _AssistantScreenState extends State<AssistantScreen> {
  final OrchestratorService _orchestrator = OrchestratorService();
  final TextEditingController _inputController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<_ChatMessage> _messages = [];

  bool _sending = false;
  bool _hasKey = false;

  @override
  void initState() {
    super.initState();
    _refreshKeyStatus();
  }

  @override
  void dispose() {
    _inputController.dispose();
    _scrollController.dispose();
    _orchestrator.dispose();
    super.dispose();
  }

  Future<void> _refreshKeyStatus() async {
    final hasKey = await _orchestrator.hasApiKey();
    if (mounted) setState(() => _hasKey = hasKey);
  }

  Future<void> _send() async {
    final text = _inputController.text.trim();
    if (text.isEmpty || _sending) return;

    setState(() {
      _messages.add(_ChatMessage.user(text));
      _sending = true;
      _inputController.clear();
    });
    _scrollToBottom();

    final result = await _orchestrator.route(text);

    if (!mounted) return;
    setState(() {
      _messages.add(_ChatMessage.assistant(result.route, result.source));
      _sending = false;
    });
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_scrollController.hasClients) return;
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 250),
        curve: Curves.easeOut,
      );
    });
  }

  Future<void> _openKeyDialog() async {
    final controller = TextEditingController();
    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Clé OpenAI'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Renseignez une clé OpenAI pour activer le routage par '
              'modèle. Sans clé, un routage local par mots-clés est utilisé.',
            ),
            const SizedBox(height: 12),
            TextField(
              controller: controller,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'sk-...',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Annuler'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Enregistrer'),
          ),
        ],
      ),
    );

    if (saved == true) {
      await _orchestrator.setApiKey(controller.text);
      await _refreshKeyStatus();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Assistant SmartStudent'),
        actions: [
          IconButton(
            tooltip: _hasKey
                ? 'Routage IA (OpenAI) actif'
                : 'Configurer la clé OpenAI',
            icon: Icon(
              _hasKey ? Icons.auto_awesome : Icons.key_outlined,
              color: _hasKey ? theme.colorScheme.primary : null,
            ),
            onPressed: _openKeyDialog,
          ),
        ],
      ),
      body: Column(
        children: [
          _ModeBanner(hasKey: _hasKey),
          Expanded(
            child: _messages.isEmpty
                ? const _EmptyState()
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) =>
                        _MessageBubble(message: _messages[index]),
                  ),
          ),
          if (_sending) const LinearProgressIndicator(minHeight: 2),
          _Composer(
            controller: _inputController,
            enabled: !_sending,
            onSend: _send,
          ),
        ],
      ),
    );
  }
}

class _ModeBanner extends StatelessWidget {
  const _ModeBanner({required this.hasKey});

  final bool hasKey;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final color = hasKey ? theme.colorScheme.primary : Colors.orange;
    return Container(
      width: double.infinity,
      color: color.withOpacity(0.10),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          Icon(hasKey ? Icons.auto_awesome : Icons.offline_bolt, size: 16,
              color: color),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              hasKey
                  ? 'Routage par modèle OpenAI (gpt-4o-mini)'
                  : 'Routage local par mots-clés — ajoutez une clé OpenAI pour '
                        'le routage par modèle',
              style: theme.textTheme.bodySmall?.copyWith(color: color),
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    const examples = [
      'Comment obtenir une attestation de scolarité ?',
      'Aide-moi à planifier mes révisions avant les deadlines',
      'Génère un quiz pour réviser les bases de données',
      'Je cherche un stage en data science',
      'Quels clubs étudiants sont disponibles ce semestre ?',
    ];
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.school_rounded, size: 56,
                color: theme.colorScheme.primary),
            const SizedBox(height: 16),
            Text(
              'Posez une question',
              style: theme.textTheme.titleLarge
                  ?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              "L'orchestrateur choisit l'agent le plus pertinent pour votre "
              'message.',
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 24),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              alignment: WrapAlignment.center,
              children: [
                for (final example in examples)
                  Chip(
                    label: Text(example),
                    backgroundColor:
                        theme.colorScheme.primary.withOpacity(0.08),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  const _MessageBubble({required this.message});

  final _ChatMessage message;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    if (message.isUser) {
      return Align(
        alignment: Alignment.centerRight,
        child: Container(
          margin: const EdgeInsets.only(bottom: 12, left: 48),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: BoxDecoration(
            color: theme.colorScheme.primary,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Text(
            message.text,
            style: const TextStyle(color: Colors.white),
          ),
        ),
      );
    }

    final route = message.route!;
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12, right: 48),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: theme.colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(_agentIcon(route.agent), size: 18,
                    color: theme.colorScheme.primary),
                const SizedBox(width: 8),
                Text(
                  '${route.agent.label} Agent',
                  style: theme.textTheme.titleSmall
                      ?.copyWith(fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                _SourceTag(source: message.source!),
              ],
            ),
            const SizedBox(height: 8),
            Text(route.reason, style: theme.textTheme.bodyMedium),
            const SizedBox(height: 12),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: theme.colorScheme.surface,
                borderRadius: BorderRadius.circular(10),
              ),
              child: SelectableText(
                route.toPrettyJson(),
                style: theme.textTheme.bodySmall?.copyWith(
                  fontFamily: 'monospace',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData _agentIcon(SmartAgent agent) => switch (agent) {
    SmartAgent.administration => Icons.description_rounded,
    SmartAgent.planning => Icons.calendar_month_rounded,
    SmartAgent.exams => Icons.quiz_rounded,
    SmartAgent.orientation => Icons.work_outline_rounded,
    SmartAgent.campus => Icons.groups_rounded,
  };
}

class _SourceTag extends StatelessWidget {
  const _SourceTag({required this.source});

  final RouteSource source;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isLlm = source == RouteSource.llm;
    final label = isLlm ? 'OpenAI' : 'local';
    final color = isLlm ? theme.colorScheme.primary : Colors.orange;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        label,
        style: theme.textTheme.labelSmall?.copyWith(color: color),
      ),
    );
  }
}

class _Composer extends StatelessWidget {
  const _Composer({
    required this.controller,
    required this.enabled,
    required this.onSend,
  });

  final TextEditingController controller;
  final bool enabled;
  final VoidCallback onSend;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SafeArea(
      top: false,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: controller,
                enabled: enabled,
                minLines: 1,
                maxLines: 4,
                textInputAction: TextInputAction.send,
                onSubmitted: (_) => onSend(),
                decoration: InputDecoration(
                  hintText: 'Écrivez votre message…',
                  filled: true,
                  fillColor: theme.colorScheme.surfaceContainerHighest,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24),
                    borderSide: BorderSide.none,
                  ),
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 10,
                  ),
                ),
              ),
            ),
            const SizedBox(width: 8),
            FloatingActionButton(
              heroTag: 'assistantSend',
              elevation: 0,
              onPressed: enabled ? onSend : null,
              child: const Icon(Icons.send_rounded),
            ),
          ],
        ),
      ),
    );
  }
}
