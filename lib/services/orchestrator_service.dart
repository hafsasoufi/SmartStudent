import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../models/agent_route.dart';

/// Where a routing decision came from.
enum RouteSource { llm, local }

/// A routing decision plus metadata about how it was produced.
class OrchestratorResult {
  const OrchestratorResult({required this.route, required this.source});

  final AgentRoute route;
  final RouteSource source;
}

/// Orchestrator AI of the SmartStudent assistant.
///
/// Analyzes a student message and decides which specialized agent should
/// handle it. When an OpenAI API key is available the decision is made by the
/// model using [systemPrompt]; otherwise a deterministic keyword classifier is
/// used so the feature keeps working offline.
class OrchestratorService {
  OrchestratorService({http.Client? client})
    : _client = client ?? http.Client();

  final http.Client _client;

  static const String _prefsKey = 'openai_api_key';
  static const String _model = 'gpt-4o-mini';
  static const String _endpoint =
      'https://api.openai.com/v1/chat/completions';

  /// System prompt that defines the orchestrator behavior. Kept verbatim so
  /// the LLM contract stays consistent and deterministic.
  static const String systemPrompt = '''
You are the Orchestrator AI of a university assistant system called SmartStudent.

Your job is to analyze the user message and decide which specialized agent should handle it.

You have 5 agents:

1. Administration Agent:
- FAQs (university questions, rules, procedures)
- administrative requests
- document explanations

2. Planning Agent:
- schedules and timetables
- deadlines
- study planning
- reminders

3. Exams Agent:
- quiz generation
- exam preparation
- revision support
- performance tracking

4. Orientation Agent:
- career guidance
- internship search advice
- skills analysis
- job recommendations

5. Campus Agent:
- university events
- clubs
- student activities

---

TASK:
For each user message:
1. Understand the user intent
2. Choose the MOST relevant agent
3. Return ONLY a valid JSON response

---

OUTPUT FORMAT (STRICT):
{
  "agent": "Administration | Planning | Exams | Orientation | Campus",
  "reason": "short explanation of why this agent was chosen",
  "query_type": "short intent label"
}

---

RULES:
- Do NOT answer the user question
- Only select ONE agent
- If the message is unclear, choose the closest matching agent
- Always respond in valid JSON only (no extra text)
- Be consistent and deterministic''';

  /// Persisted API key set from the app, falling back to a compile-time
  /// `--dart-define=OPENAI_API_KEY=...` value.
  static const String _compileTimeKey = String.fromEnvironment(
    'OPENAI_API_KEY',
  );

  Future<String?> getApiKey() async {
    final prefs = await SharedPreferences.getInstance();
    final stored = prefs.getString(_prefsKey);
    if (stored != null && stored.trim().isNotEmpty) return stored.trim();
    if (_compileTimeKey.trim().isNotEmpty) return _compileTimeKey.trim();
    return null;
  }

  Future<void> setApiKey(String key) async {
    final prefs = await SharedPreferences.getInstance();
    if (key.trim().isEmpty) {
      await prefs.remove(_prefsKey);
    } else {
      await prefs.setString(_prefsKey, key.trim());
    }
  }

  Future<bool> hasApiKey() async => (await getApiKey()) != null;

  /// Routes [message] to the most relevant agent.
  ///
  /// Tries the LLM first when a key is configured, and transparently falls
  /// back to the deterministic classifier on any error.
  Future<OrchestratorResult> route(String message) async {
    final key = await getApiKey();
    if (key != null) {
      try {
        final route = await _routeWithLlm(message, key);
        return OrchestratorResult(route: route, source: RouteSource.llm);
      } catch (_) {
        // Fall through to deterministic routing on any failure.
      }
    }
    return OrchestratorResult(
      route: classify(message),
      source: RouteSource.local,
    );
  }

  Future<AgentRoute> _routeWithLlm(String message, String apiKey) async {
    final response = await _client.post(
      Uri.parse(_endpoint),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $apiKey',
      },
      body: jsonEncode({
        'model': _model,
        'temperature': 0,
        'response_format': {'type': 'json_object'},
        'messages': [
          {'role': 'system', 'content': systemPrompt},
          {'role': 'user', 'content': message},
        ],
      }),
    );

    if (response.statusCode != 200) {
      throw http.ClientException(
        'OpenAI error ${response.statusCode}: ${response.body}',
      );
    }

    final decoded = jsonDecode(response.body) as Map<String, dynamic>;
    final content =
        (decoded['choices'] as List).first['message']['content'] as String;
    return AgentRoute.fromJsonString(content);
  }

  /// Deterministic keyword-based classifier mirroring the agent definitions.
  /// Used as an offline fallback; identical input always yields identical
  /// output.
  AgentRoute classify(String message) {
    final text = message.toLowerCase();

    final scores = <SmartAgent, int>{
      for (final agent in SmartAgent.values) agent: 0,
    };

    void score(SmartAgent agent, List<String> keywords) {
      for (final keyword in keywords) {
        if (text.contains(keyword)) scores[agent] = scores[agent]! + 1;
      }
    }

    score(SmartAgent.administration, _administrationKeywords);
    score(SmartAgent.planning, _planningKeywords);
    score(SmartAgent.exams, _examsKeywords);
    score(SmartAgent.orientation, _orientationKeywords);
    score(SmartAgent.campus, _campusKeywords);

    var best = SmartAgent.administration;
    var bestScore = 0;
    for (final entry in scores.entries) {
      if (entry.value > bestScore) {
        best = entry.key;
        bestScore = entry.value;
      }
    }

    final reason = bestScore == 0
        ? 'No strong keyword match; defaulting to the closest agent for '
              'general university help.'
        : 'Message matched ${_describe(best)} keywords.';
    final queryType = bestScore == 0 ? 'general_inquiry' : _queryType(best);

    return AgentRoute(agent: best, reason: reason, queryType: queryType);
  }

  String _describe(SmartAgent agent) => switch (agent) {
    SmartAgent.administration => 'administrative / FAQ',
    SmartAgent.planning => 'scheduling / planning',
    SmartAgent.exams => 'exam / revision',
    SmartAgent.orientation => 'career / orientation',
    SmartAgent.campus => 'campus life',
  };

  String _queryType(SmartAgent agent) => switch (agent) {
    SmartAgent.administration => 'administrative_request',
    SmartAgent.planning => 'planning_request',
    SmartAgent.exams => 'exam_preparation',
    SmartAgent.orientation => 'career_guidance',
    SmartAgent.campus => 'campus_activity',
  };

  static const List<String> _administrationKeywords = [
    'faq',
    'document',
    'certificate',
    'attestation',
    'inscription',
    'enroll',
    'registration',
    'procedure',
    'rule',
    'règle',
    'admin',
    'scolarité',
    'transcript',
    'relevé',
    'diploma',
    'diplôme',
    'tuition',
    'frais',
    'demande',
    'request',
    'form',
    'formulaire',
  ];

  static const List<String> _planningKeywords = [
    'schedule',
    'timetable',
    'emploi du temps',
    'deadline',
    'échéance',
    'planning',
    'plan',
    'reminder',
    'rappel',
    'calendar',
    'calendrier',
    'organize',
    'organiser',
    'due',
    'agenda',
    'study plan',
  ];

  static const List<String> _examsKeywords = [
    'exam',
    'examen',
    'quiz',
    'test',
    'revision',
    'révision',
    'revise',
    'réviser',
    'study for',
    'mock',
    'practice',
    'grade',
    'note',
    'score',
    'performance',
    'qcm',
    'midterm',
    'final',
  ];

  static const List<String> _orientationKeywords = [
    'career',
    'carrière',
    'internship',
    'stage',
    'job',
    'emploi',
    'cv',
    'resume',
    'cover letter',
    'lettre de motivation',
    'skill',
    'compétence',
    'recruit',
    'recrutement',
    'orientation',
    'profession',
    'metier',
    'métier',
    'linkedin',
  ];

  static const List<String> _campusKeywords = [
    'event',
    'événement',
    'evenement',
    'club',
    'activity',
    'activité',
    'association',
    'party',
    'fête',
    'festival',
    'sport',
    'volunteer',
    'bénévolat',
    'meetup',
    'campus',
    'student life',
    'vie étudiante',
  ];

  void dispose() => _client.close();
}
