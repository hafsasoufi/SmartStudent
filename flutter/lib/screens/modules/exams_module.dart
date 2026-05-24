import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/exam_model.dart';
import '../../providers/exams_provider.dart';
import '../../theme/app_theme.dart';

class ExamsModule extends ConsumerStatefulWidget {
  const ExamsModule({Key? key}) : super(key: key);

  @override
  ConsumerState<ExamsModule> createState() => _ExamsModuleState();
}

class _ExamsModuleState extends ConsumerState<ExamsModule> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      ref.read(examsProvider.notifier).loadHistory();
      ref.read(examsProvider.notifier).loadStats();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Examens & Quiz'), elevation: 0),
      body: DefaultTabController(
        length: 3,
        child: Column(
          children: [
            const TabBar(tabs: [
              Tab(icon: Icon(Icons.quiz), text: 'Nouveau quiz'),
              Tab(icon: Icon(Icons.trending_up), text: 'Stats'),
              Tab(icon: Icon(Icons.history), text: 'Historique'),
            ]),
            Expanded(
              child: TabBarView(children: [
                _GenerateQuizTab(),
                _StatsTab(),
                _HistoryTab(),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Onglet Générer un quiz ───────────────────────────────────────────────────
class _GenerateQuizTab extends ConsumerStatefulWidget {
  @override
  ConsumerState<_GenerateQuizTab> createState() => _GenerateQuizTabState();
}

class _GenerateQuizTabState extends ConsumerState<_GenerateQuizTab> {
  final _subjectCtrl = TextEditingController();
  int _numQuestions = 5;
  String _difficulty = 'medium';

  static const _subjects = [
    'Algorithmique', 'Machine Learning', 'Bases de données',
    'Réseaux informatiques', 'Mathématiques', 'Programmation Python',
    'Intelligence Artificielle', 'Systèmes d\'exploitation',
  ];

  static const _difficulties = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile',
  };

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(examsProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Header
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [AppTheme.primaryColor, AppTheme.accentColor],
            ),
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Row(children: [
            Icon(Icons.auto_awesome, color: Colors.white, size: 28),
            SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Quiz Génératif IA',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.bold)),
                Text('L\'IA génère des questions personnalisées pour toi',
                    style: TextStyle(color: Colors.white70, fontSize: 12)),
              ]),
            ),
          ]),
        ),
        const SizedBox(height: 24),

        // Sujet
        const Text('Sujet', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 8),
        TextField(
          controller: _subjectCtrl,
          decoration: const InputDecoration(
            hintText: 'Ex : Arbres binaires, Réseaux de neurones...',
            border: OutlineInputBorder(),
            prefixIcon: Icon(Icons.book),
          ),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 4,
          children: _subjects
              .map((s) => ActionChip(
                    label: Text(s, style: const TextStyle(fontSize: 11)),
                    onPressed: () => _subjectCtrl.text = s,
                  ))
              .toList(),
        ),
        const SizedBox(height: 20),

        // Nombre de questions
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          const Text('Nombre de questions',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
          Text('$_numQuestions',
              style: TextStyle(
                  color: AppTheme.primaryColor,
                  fontWeight: FontWeight.bold,
                  fontSize: 18)),
        ]),
        Slider(
          value: _numQuestions.toDouble(),
          min: 3,
          max: 10,
          divisions: 7,
          label: '$_numQuestions questions',
          onChanged: (v) => setState(() => _numQuestions = v.round()),
        ),
        const SizedBox(height: 16),

        // Difficulté
        const Text('Difficulté',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 8),
        SegmentedButton<String>(
          segments: _difficulties.entries
              .map((e) => ButtonSegment(value: e.key, label: Text(e.value)))
              .toList(),
          selected: {_difficulty},
          onSelectionChanged: (s) => setState(() => _difficulty = s.first),
        ),
        const SizedBox(height: 28),

        // Bouton générer
        SizedBox(
          width: double.infinity,
          height: 52,
          child: ElevatedButton.icon(
            onPressed: state.isGenerating ? null : _generateQuiz,
            icon: state.isGenerating
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                        strokeWidth: 2, color: Colors.white))
                : const Icon(Icons.play_arrow),
            label: Text(
              state.isGenerating ? 'Génération en cours...' : 'Générer le quiz',
              style: const TextStyle(fontSize: 16),
            ),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
            ),
          ),
        ),

        if (state.error != null) ...[
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.red.shade50,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.red.shade200),
            ),
            child: Row(children: [
              const Icon(Icons.error_outline, color: Colors.red),
              const SizedBox(width: 8),
              Expanded(
                child: Text(state.error!,
                    style: const TextStyle(color: Colors.red, fontSize: 12)),
              ),
            ]),
          ),
        ],
      ]),
    );
  }

  Future<void> _generateQuiz() async {
    final subject = _subjectCtrl.text.trim();
    if (subject.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Veuillez saisir un sujet')),
      );
      return;
    }
    final exam = await ref.read(examsProvider.notifier).generateQuiz(
          subject: subject,
          numQuestions: _numQuestions,
          difficulty: _difficulty,
        );
    if (exam != null && mounted) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => QuizScreen(exam: exam)),
      );
    }
  }
}

// ── Onglet Stats ─────────────────────────────────────────────────────────────
class _StatsTab extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final stats = ref.watch(examsProvider).stats;
    final history = ref.watch(examsProvider).history;
    final completed = history.where((e) => e.status == 'completed').toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Statistiques principales
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          childAspectRatio: 1.6,
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
          children: [
            _StatCard(
              title: 'Moyenne',
              value: '${stats.averageScore.toStringAsFixed(0)}%',
              icon: Icons.trending_up,
              color: stats.averageScore >= 70 ? Colors.green : Colors.orange,
            ),
            _StatCard(
              title: 'Quiz effectués',
              value: '${stats.completedExams}',
              icon: Icons.quiz,
              color: AppTheme.primaryColor,
            ),
            _StatCard(
              title: 'Total quiz',
              value: '${stats.totalExams}',
              icon: Icons.list_alt,
              color: AppTheme.secondaryColor,
            ),
            _StatCard(
              title: 'Progression',
              value: stats.totalExams > 0
                  ? '${(stats.completedExams / stats.totalExams * 100).toStringAsFixed(0)}%'
                  : '0%',
              icon: Icons.donut_large,
              color: Colors.teal,
            ),
          ],
        ),
        if (completed.isNotEmpty) ...[
          const SizedBox(height: 20),
          const Text('Derniers résultats',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
          const SizedBox(height: 10),
          ...completed.take(5).map((e) => _ResultTile(exam: e)),
        ],
        if (completed.isEmpty) ...[
          const SizedBox(height: 40),
          const Center(
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Icon(Icons.quiz_outlined, size: 64, color: Colors.grey),
              SizedBox(height: 12),
              Text('Aucun quiz terminé encore.',
                  style: TextStyle(color: Colors.grey)),
              Text('Va dans "Nouveau quiz" pour commencer !',
                  style: TextStyle(color: Colors.grey, fontSize: 12)),
            ]),
          ),
        ],
      ]),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _StatCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Icon(icon, color: color, size: 22),
        const Spacer(),
        Text(value,
            style: TextStyle(
                fontSize: 22, fontWeight: FontWeight.bold, color: color)),
        Text(title,
            style: TextStyle(fontSize: 11, color: Colors.grey[600])),
      ]),
    );
  }
}

class _ResultTile extends StatelessWidget {
  final ExamRecord exam;
  const _ResultTile({required this.exam});

  @override
  Widget build(BuildContext context) {
    final pct = exam.percentage;
    final color = pct >= 80
        ? Colors.green
        : pct >= 60
            ? Colors.orange
            : Colors.red;
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        title: Text(exam.title,
            style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(exam.subject),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          decoration: BoxDecoration(
            color: color.withOpacity(0.15),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Text('${pct.toStringAsFixed(0)}%',
              style: TextStyle(color: color, fontWeight: FontWeight.bold)),
        ),
      ),
    );
  }
}

// ── Onglet Historique ────────────────────────────────────────────────────────
class _HistoryTab extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(examsProvider);

    if (state.isLoading) return const Center(child: CircularProgressIndicator());

    if (state.history.isEmpty) {
      return const Center(
        child: Text('Aucun quiz dans l\'historique.'),
      );
    }

    return RefreshIndicator(
      onRefresh: () => ref.read(examsProvider.notifier).loadHistory(),
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: state.history.length,
        itemBuilder: (_, i) {
          final exam = state.history[i];
          final pct = exam.percentage;
          final statusColor = exam.status == 'completed'
              ? (pct >= 60 ? Colors.green : Colors.red)
              : Colors.orange;
          final statusLabel = exam.status == 'completed'
              ? '${pct.toStringAsFixed(0)}%'
              : exam.status == 'in_progress'
                  ? 'En cours'
                  : 'Non commencé';

          return Card(
            margin: const EdgeInsets.only(bottom: 10),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: statusColor.withOpacity(0.15),
                child: Icon(Icons.quiz, color: statusColor),
              ),
              title: Text(exam.title,
                  style: const TextStyle(fontWeight: FontWeight.w600)),
              subtitle: Text(
                  '${exam.subject} • ${exam.questions.length} questions'),
              trailing: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: statusColor.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(statusLabel,
                          style: TextStyle(
                              color: statusColor,
                              fontSize: 12,
                              fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '${exam.createdAt.day}/${exam.createdAt.month}',
                      style: TextStyle(fontSize: 11, color: Colors.grey[500]),
                    ),
                  ]),
              onTap: exam.status != 'completed'
                  ? () => Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => QuizScreen(exam: exam)),
                      )
                  : null,
            ),
          );
        },
      ),
    );
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// Écran Quiz interactif
// ══════════════════════════════════════════════════════════════════════════════
class QuizScreen extends ConsumerStatefulWidget {
  final ExamRecord exam;
  const QuizScreen({Key? key, required this.exam}) : super(key: key);

  @override
  ConsumerState<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends ConsumerState<QuizScreen> {
  late List<String?> _answers;
  int _currentIndex = 0;
  bool _submitted = false;
  Map<String, dynamic>? _result;

  @override
  void initState() {
    super.initState();
    _answers = List.filled(widget.exam.questions.length, null);
  }

  @override
  Widget build(BuildContext context) {
    if (_submitted && _result != null) return _buildResultScreen();

    final questions = widget.exam.questions;
    if (questions.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('Quiz')),
        body: const Center(child: Text('Aucune question disponible.')),
      );
    }

    final q = questions[_currentIndex];
    final total = questions.length;

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.exam.subject),
        elevation: 0,
        actions: [
          Center(
            child: Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Text('${_currentIndex + 1}/$total',
                  style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Barre de progression
          LinearProgressIndicator(
            value: (_currentIndex + 1) / total,
            backgroundColor: Colors.grey[200],
            color: AppTheme.primaryColor,
            minHeight: 6,
          ),

          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Numéro de question
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppTheme.primaryColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text('Question ${_currentIndex + 1}',
                          style: TextStyle(
                              color: AppTheme.primaryColor,
                              fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 16),

                    // Question
                    Text(q.question,
                        style: const TextStyle(
                            fontSize: 17, fontWeight: FontWeight.w600)),
                    const SizedBox(height: 24),

                    // Options
                    ...q.options.map((opt) {
                      final selected = _answers[_currentIndex] == opt;
                      return GestureDetector(
                        onTap: () => setState(
                            () => _answers[_currentIndex] = opt),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          margin: const EdgeInsets.only(bottom: 10),
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: selected
                                ? AppTheme.primaryColor.withOpacity(0.12)
                                : Colors.white,
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(
                              color: selected
                                  ? AppTheme.primaryColor
                                  : Colors.grey.shade300,
                              width: selected ? 2 : 1,
                            ),
                          ),
                          child: Row(children: [
                            Icon(
                              selected
                                  ? Icons.radio_button_checked
                                  : Icons.radio_button_off,
                              color: selected
                                  ? AppTheme.primaryColor
                                  : Colors.grey,
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                                child: Text(opt,
                                    style: TextStyle(
                                        fontWeight: selected
                                            ? FontWeight.w600
                                            : FontWeight.normal))),
                          ]),
                        ),
                      );
                    }),
                  ]),
            ),
          ),

          // Navigation
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(children: [
              if (_currentIndex > 0)
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () =>
                        setState(() => _currentIndex--),
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Précédent'),
                  ),
                ),
              if (_currentIndex > 0) const SizedBox(width: 12),
              Expanded(
                child: _currentIndex < total - 1
                    ? ElevatedButton.icon(
                        onPressed: _answers[_currentIndex] != null
                            ? () => setState(() => _currentIndex++)
                            : null,
                        icon: const Icon(Icons.arrow_forward),
                        label: const Text('Suivant'),
                        style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.primaryColor,
                            foregroundColor: Colors.white),
                      )
                    : ElevatedButton.icon(
                        onPressed: _answers.every((a) => a != null)
                            ? _submitQuiz
                            : null,
                        icon: const Icon(Icons.check),
                        label: const Text('Terminer'),
                        style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white),
                      ),
              ),
            ]),
          ),
        ],
      ),
    );
  }

  Future<void> _submitQuiz() async {
    final result = await ref.read(examsProvider.notifier).submitQuiz(
          examId: widget.exam.id,
          answers: _answers,
        );
    if (mounted) {
      setState(() {
        _submitted = true;
        _result = result ?? {'score': 0, 'total': widget.exam.questions.length};
      });
    }
  }

  Widget _buildResultScreen() {
    final score = _result!['score'] as int? ?? 0;
    final total = _result!['total'] as int? ?? widget.exam.questions.length;
    final pct = total > 0 ? score / total * 100 : 0;
    final color = pct >= 80
        ? Colors.green
        : pct >= 60
            ? Colors.orange
            : Colors.red;
    final emoji = pct >= 80 ? '🎉' : pct >= 60 ? '👍' : '💪';
    final message = pct >= 80
        ? 'Excellent travail !'
        : pct >= 60
            ? 'Bon résultat, continue !'
            : 'Continue de t\'entraîner !';

    final feedbackList = (_result!['feedback'] as List?)?.cast<Map<String, dynamic>>() ?? [];

    return Scaffold(
      appBar: AppBar(title: const Text('Résultat'), elevation: 0),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(children: [
          // Score summary
          Text(emoji, style: const TextStyle(fontSize: 56)),
          const SizedBox(height: 8),
          Text(message,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: color.withOpacity(0.3)),
            ),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              Text('${pct.toStringAsFixed(0)}%',
                  style: TextStyle(
                      fontSize: 44, fontWeight: FontWeight.bold, color: color)),
              const SizedBox(width: 16),
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('$score / $total',
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const Text('questions correctes',
                    style: TextStyle(fontSize: 12, color: Colors.grey)),
              ]),
            ]),
          ),
          const SizedBox(height: 24),

          // Per-question feedback
          if (feedbackList.isNotEmpty) ...[
            const Align(
              alignment: Alignment.centerLeft,
              child: Text('Correction détaillée',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(height: 10),
            ...feedbackList.asMap().entries.map((entry) {
              final i = entry.key;
              final fb = entry.value;
              final isCorrect = fb['is_correct'] as bool? ?? false;
              final fbColor = isCorrect ? Colors.green : Colors.red;
              return Card(
                margin: const EdgeInsets.only(bottom: 10),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                  side: BorderSide(color: fbColor.withOpacity(0.3)),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Row(children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: fbColor.withOpacity(0.12),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text('Q${i + 1}',
                            style: TextStyle(color: fbColor, fontWeight: FontWeight.bold, fontSize: 12)),
                      ),
                      const SizedBox(width: 8),
                      Icon(isCorrect ? Icons.check_circle : Icons.cancel,
                          color: fbColor, size: 18),
                      const SizedBox(width: 4),
                      Text(isCorrect ? 'Correct' : 'Incorrect',
                          style: TextStyle(color: fbColor, fontWeight: FontWeight.w600, fontSize: 13)),
                    ]),
                    const SizedBox(height: 8),
                    Text(fb['question'] as String? ?? '',
                        style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                    const SizedBox(height: 6),
                    if (!isCorrect) ...[
                      _FeedbackRow(
                          label: 'Ta réponse',
                          value: fb['user_answer'] as String? ?? '',
                          color: Colors.red),
                      const SizedBox(height: 4),
                      _FeedbackRow(
                          label: 'Bonne réponse',
                          value: fb['correct_answer'] as String? ?? '',
                          color: Colors.green),
                    ] else
                      _FeedbackRow(
                          label: 'Réponse',
                          value: fb['correct_answer'] as String? ?? '',
                          color: Colors.green),
                    if (fb['explanation'] != null && (fb['explanation'] as String).isNotEmpty) ...[
                      const SizedBox(height: 6),
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.blue.withOpacity(0.06),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          const Icon(Icons.lightbulb_outline, size: 14, color: Colors.blue),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(fb['explanation'] as String,
                                style: const TextStyle(fontSize: 12, color: Colors.black87)),
                          ),
                        ]),
                      ),
                    ],
                  ]),
                ),
              );
            }),
            const SizedBox(height: 8),
          ],

          ElevatedButton.icon(
            onPressed: () => Navigator.popUntil(context, (r) => r.isFirst),
            icon: const Icon(Icons.home),
            label: const Text('Retour à l\'accueil'),
            style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryColor,
                foregroundColor: Colors.white,
                minimumSize: const Size(200, 48)),
          ),
          const SizedBox(height: 16),
        ]),
      ),
    );
  }
}

class _FeedbackRow extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  const _FeedbackRow({required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text('$label : ',
          style: TextStyle(fontSize: 12, color: color, fontWeight: FontWeight.w600)),
      Expanded(
        child: Text(value, style: const TextStyle(fontSize: 12)),
      ),
    ]);
  }
}
