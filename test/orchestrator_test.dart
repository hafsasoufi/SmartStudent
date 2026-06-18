import 'package:flutter_test/flutter_test.dart';

import 'package:startuplaunchpad/models/agent_route.dart';
import 'package:startuplaunchpad/services/orchestrator_service.dart';

void main() {
  final orchestrator = OrchestratorService();

  group('deterministic classifier', () {
    test('routes administrative requests to Administration', () {
      expect(
        orchestrator.classify('Comment obtenir une attestation de scolarité ?')
            .agent,
        SmartAgent.administration,
      );
    });

    test('routes scheduling messages to Planning', () {
      expect(
        orchestrator
            .classify('Aide-moi à planifier mes révisions avant la deadline')
            .agent,
        SmartAgent.planning,
      );
    });

    test('routes quiz/exam messages to Exams', () {
      expect(
        orchestrator.classify('Génère un quiz pour réviser mon examen').agent,
        SmartAgent.exams,
      );
    });

    test('routes internship/career messages to Orientation', () {
      expect(
        orchestrator.classify('Je cherche un stage en data science').agent,
        SmartAgent.orientation,
      );
    });

    test('routes events/clubs messages to Campus', () {
      expect(
        orchestrator.classify('Quels clubs étudiants et événements ce mois ?')
            .agent,
        SmartAgent.campus,
      );
    });

    test('is deterministic for identical input', () {
      final a = orchestrator.classify('emploi du temps');
      final b = orchestrator.classify('emploi du temps');
      expect(a.toJson(), b.toJson());
    });
  });

  group('AgentRoute JSON contract', () {
    test('parses fenced LLM JSON output', () {
      const raw = '''
```json
{
  "agent": "Exams",
  "reason": "User wants a quiz",
  "query_type": "quiz_generation"
}
```''';
      final route = AgentRoute.fromJsonString(raw);
      expect(route.agent, SmartAgent.exams);
      expect(route.queryType, 'quiz_generation');
    });

    test('serializes with the strict keys', () {
      const route = AgentRoute(
        agent: SmartAgent.campus,
        reason: 'r',
        queryType: 'campus_activity',
      );
      expect(route.toJson().keys.toList(), ['agent', 'reason', 'query_type']);
      expect(route.toJson()['agent'], 'Campus');
    });
  });
}
