import 'dart:convert';

/// The five specialized agents the orchestrator can route a message to.
enum SmartAgent {
  administration('Administration'),
  planning('Planning'),
  exams('Exams'),
  orientation('Orientation'),
  campus('Campus');

  const SmartAgent(this.label);

  /// Canonical label as used in the orchestrator JSON contract.
  final String label;

  static SmartAgent fromLabel(String value) {
    final normalized = value.trim().toLowerCase();
    for (final agent in SmartAgent.values) {
      if (agent.label.toLowerCase() == normalized) return agent;
    }
    // Closest-match fallback keeps the contract deterministic.
    return SmartAgent.administration;
  }
}

/// Result of the orchestrator: the strict JSON contract
/// `{agent, reason, query_type}`.
class AgentRoute {
  const AgentRoute({
    required this.agent,
    required this.reason,
    required this.queryType,
  });

  final SmartAgent agent;
  final String reason;
  final String queryType;

  Map<String, dynamic> toJson() => {
    'agent': agent.label,
    'reason': reason,
    'query_type': queryType,
  };

  /// Pretty JSON string matching the orchestrator output format.
  String toPrettyJson() =>
      const JsonEncoder.withIndent('  ').convert(toJson());

  /// Parses a (possibly fenced) JSON string returned by an LLM.
  static AgentRoute fromJsonString(String raw) {
    final cleaned = _stripCodeFences(raw);
    final start = cleaned.indexOf('{');
    final end = cleaned.lastIndexOf('}');
    if (start == -1 || end == -1 || end <= start) {
      throw const FormatException('No JSON object found in orchestrator output');
    }
    final decoded =
        jsonDecode(cleaned.substring(start, end + 1)) as Map<String, dynamic>;
    return AgentRoute(
      agent: SmartAgent.fromLabel((decoded['agent'] ?? '').toString()),
      reason: (decoded['reason'] ?? '').toString(),
      queryType: (decoded['query_type'] ?? '').toString(),
    );
  }

  static String _stripCodeFences(String input) {
    var text = input.trim();
    if (text.startsWith('```')) {
      final firstNewline = text.indexOf('\n');
      if (firstNewline != -1) text = text.substring(firstNewline + 1);
      if (text.endsWith('```')) {
        text = text.substring(0, text.length - 3);
      }
    }
    return text.trim();
  }
}
