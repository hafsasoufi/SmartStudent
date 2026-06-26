import 'package:file_picker/file_picker.dart';
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

class _ExamsModuleState extends ConsumerState<ExamsModule>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
    Future.microtask(() {
      // loadModules automatically syncs the Planning tab via loadOfficialSchedule
      ref.read(examsProvider.notifier).loadModules();
      ref.read(examsProvider.notifier).loadCourses();
      ref.read(examsProvider.notifier).loadHistory();
      ref.read(examsProvider.notifier).loadStats();
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Examens & Révision'),
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabAlignment: TabAlignment.start,
          tabs: const [
            Tab(icon: Icon(Icons.menu_book, size: 18), text: 'Modules'),
            Tab(icon: Icon(Icons.picture_as_pdf, size: 18), text: 'Assistant PDF'),
            Tab(icon: Icon(Icons.event_note, size: 18), text: 'Planning'),
            Tab(icon: Icon(Icons.trending_up, size: 18), text: 'Stats'),
            Tab(icon: Icon(Icons.history, size: 18), text: 'Historique'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _ModulesTab(onGoToQuiz: () => _tabController.animateTo(3)),
          const _PdfAssistantTab(),
          const _OfficialScheduleTab(),
          const _StatsTab(),
          const _HistoryTab(),
        ],
      ),
    );
  }
}

/// Returns the pair [Sn, Sn+1] for a given semester string, e.g. 'S7' → ['S7','S8'].
List<String> _semesterPair(String semestre) {
  final n = int.tryParse(semestre.replaceAll('S', ''));
  if (n == null || n <= 0) return semestre.isEmpty ? [] : [semestre];
  final impair = n.isOdd ? n : n - 1;
  return ['S$impair', 'S${impair + 1}'];
}

// ══════════════════════════════════════════════════════════════════════════════
// Tab 0 — Mes Modules
// ══════════════════════════════════════════════════════════════════════════════

class _ModulesTab extends ConsumerWidget {
  final VoidCallback onGoToQuiz;
  const _ModulesTab({required this.onGoToQuiz});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(examsProvider);

    if (state.isLoadingModules) {
      return const Center(child: CircularProgressIndicator());
    }

    if (state.modules.isEmpty) {
      return _ModulesEmpty(
        filiere: state.filiere,
        semestre: state.semestre,
        onChangeSemestre: (sem) =>
            ref.read(examsProvider.notifier).loadModules(semestre: sem),
      );
    }

    return RefreshIndicator(
      onRefresh: () => ref.read(examsProvider.notifier).loadModules(),
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: _FiliereHeader(
              filiere: state.filiere,
              semestre: state.semestre,
              session: state.session,
              niveau: state.niveau,
              totalExamens: state.totalExamens,
              onChangeSemestre: (sem) =>
                  ref.read(examsProvider.notifier).loadModules(semestre: sem),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 24),
            sliver: SliverList(
              delegate: SliverChildBuilderDelegate(
                (ctx, i) => _ModuleCard(module: state.modules[i], index: i),
                childCount: state.modules.length,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ModulesEmpty extends StatelessWidget {
  final String filiere;
  final String semestre;
  final void Function(String) onChangeSemestre;
  const _ModulesEmpty(
      {required this.filiere,
      required this.semestre,
      required this.onChangeSemestre});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        const SizedBox(height: 32),
        Icon(Icons.school_outlined, size: 64, color: Colors.grey[400]),
        const SizedBox(height: 16),
        Text(
          filiere.isEmpty
              ? 'Filière non renseignée'
              : 'Aucun examen trouvé pour\n"$filiere"',
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 15, color: Colors.grey),
        ),
        const SizedBox(height: 8),
        const Text(
          'Cette filière n\'est pas couverte par le planning officiel de cette session.',
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.grey, fontSize: 12),
        ),
        const SizedBox(height: 24),
        const Text('Essayez un autre semestre :',
            style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
        const SizedBox(height: 12),
        Wrap(
          spacing: 10,
          children: _semesterPair(semestre).map((s) => OutlinedButton(
            onPressed: () => onChangeSemestre(s),
            style: OutlinedButton.styleFrom(
              side: BorderSide(
                  color: s == semestre
                      ? AppTheme.primaryColor
                      : Colors.grey.shade300),
              foregroundColor:
                  s == semestre ? AppTheme.primaryColor : Colors.grey,
            ),
            child: Text(s),
          )).toList(),
        ),
      ]),
    );
  }
}

class _FiliereHeader extends StatelessWidget {
  final String filiere;
  final String semestre;
  final String session;
  final int niveau;
  final int totalExamens;
  final void Function(String) onChangeSemestre;

  const _FiliereHeader({
    required this.filiere,
    required this.semestre,
    required this.session,
    required this.niveau,
    required this.totalExamens,
    required this.onChangeSemestre,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [AppTheme.primaryColor, AppTheme.accentColor],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.school, color: Colors.white, size: 24),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(filiere,
                  style: const TextStyle(
                      color: Colors.white,
                      fontSize: 15,
                      fontWeight: FontWeight.bold)),
              if (session.isNotEmpty)
                Text(session,
                    style: const TextStyle(
                        color: Colors.white70, fontSize: 11)),
            ]),
          ),
          // Semestre badge
          if (semestre.isNotEmpty)
            Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.25),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(semestre,
                  style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 13)),
            ),
        ]),
        const SizedBox(height: 12),
        // Exam count pill
        Row(children: [
          Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: Colors.red.withOpacity(0.85),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              const Icon(Icons.event_busy, color: Colors.white, size: 14),
              const SizedBox(width: 5),
              Text(
                '$totalExamens examen${totalExamens > 1 ? 's' : ''} programmé${totalExamens > 1 ? 's' : ''}',
                style: const TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.bold),
              ),
            ]),
          ),
          const SizedBox(width: 10),
          // Quick semestre switcher
          ..._semestres(semestre).map((s) => Padding(
            padding: const EdgeInsets.only(right: 6),
            child: GestureDetector(
              onTap: () => onChangeSemestre(s),
              child: Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: s == semestre
                      ? Colors.white
                      : Colors.white.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  s,
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    color: s == semestre
                        ? AppTheme.primaryColor
                        : Colors.white,
                  ),
                ),
              ),
            ),
          )),
        ]),
      ]),
    );
  }

  List<String> _semestres(String current) => _semesterPair(current);
}

class _ModuleCard extends ConsumerWidget {
  final ModuleItem module;
  final int index;
  const _ModuleCard({required this.module, required this.index});

  static const _colors = [
    Color(0xFF6C63FF),
    Color(0xFF0052A5),
    Color(0xFF00897B),
    Color(0xFFE64A19),
    Color(0xFF7B1FA2),
    Color(0xFF1976D2),
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final color = _colors[index % _colors.length];
    final hasExam = module.hasExam;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: hasExam ? 3 : 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: hasExam
            ? const BorderSide(color: Color(0xFFE53935), width: 1.5)
            : BorderSide.none,
      ),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Top row: icon + name + quiz button
          Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Container(
              width: 42,
              height: 42,
              decoration: BoxDecoration(
                color: color.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(Icons.auto_stories, color: color, size: 22),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                Text(module.nom,
                    style: const TextStyle(
                        fontWeight: FontWeight.w600, fontSize: 13.5)),
                const SizedBox(height: 4),
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 7, vertical: 2),
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(module.code,
                      style: TextStyle(
                          fontSize: 10,
                          color: color,
                          fontWeight: FontWeight.w600)),
                ),
              ]),
            ),
            const SizedBox(width: 8),
            ElevatedButton.icon(
              onPressed: hasExam ? () => _showQuizSheet(context, ref) : null,
              icon: const Icon(Icons.quiz, size: 15),
              label: const Text('Réviser', style: TextStyle(fontSize: 12)),
              style: ElevatedButton.styleFrom(
                backgroundColor: hasExam ? const Color(0xFFE53935) : Colors.grey,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8)),
              ),
            ),
          ]),

          // Exam slot banner (only when hasExam)
          if (hasExam && module.examJour != null) ...[
            const SizedBox(height: 10),
            Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
              decoration: BoxDecoration(
                color: Colors.red.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.red.shade200),
              ),
              child: Row(children: [
                const Icon(Icons.event, size: 14, color: Colors.red),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    '${module.examJour}  •  ${module.examCreneau}  •  ${module.examSalle}',
                    style: const TextStyle(
                        color: Colors.red,
                        fontSize: 11,
                        fontWeight: FontWeight.w600),
                  ),
                ),
              ]),
            ),
          ],
        ]),
      ),
    );
  }

  void _showQuizSheet(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (_) => _QuizConfigSheet(module: module, ref: ref),
    );
  }
}

// ── Quiz config bottom sheet ─────────────────────────────────────────────────

class _QuizConfigSheet extends StatefulWidget {
  final ModuleItem module;
  final WidgetRef ref;
  const _QuizConfigSheet({required this.module, required this.ref});

  @override
  State<_QuizConfigSheet> createState() => _QuizConfigSheetState();
}

class _QuizConfigSheetState extends State<_QuizConfigSheet> {
  int _nbQuestions = 5;
  String _difficulty = 'medium';

  static const _difficulties = {
    'easy': 'Facile',
    'medium': 'Moyen',
    'hard': 'Difficile',
  };

  @override
  Widget build(BuildContext context) {
    final isGenerating = widget.ref.watch(examsProvider).isGenerating;

    return Padding(
      padding: EdgeInsets.fromLTRB(
          20, 20, 20, MediaQuery.of(context).viewInsets.bottom + 24),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        // Handle
        Container(
          width: 40, height: 4,
          decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(2)),
        ),
        const SizedBox(height: 18),

        // Title
        Text(widget.module.nom,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center),
        const SizedBox(height: 4),
        Text(widget.module.code,
            style: TextStyle(fontSize: 12, color: Colors.grey[500])),
        const SizedBox(height: 12),

        // Exam info banner
        if (widget.module.hasExam && widget.module.examJour != null)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
            decoration: BoxDecoration(
              color: Colors.red.shade50,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.red.shade200),
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                const Icon(Icons.event_busy, size: 14, color: Colors.red),
                const SizedBox(width: 6),
                const Text('Examen officiel programmé',
                    style: TextStyle(
                        color: Colors.red,
                        fontWeight: FontWeight.bold,
                        fontSize: 12)),
              ]),
              const SizedBox(height: 4),
              Text(
                '${widget.module.examJour}  •  ${widget.module.examCreneau}',
                style: const TextStyle(fontSize: 12, color: Colors.red),
              ),
              if (widget.module.examSalle != null)
                Text('Salle : ${widget.module.examSalle}',
                    style: const TextStyle(
                        fontSize: 11, color: Colors.redAccent)),
              if (widget.module.examCoordonnateur != null)
                Text(widget.module.examCoordonnateur!,
                    style: TextStyle(
                        fontSize: 10, color: Colors.red.shade300)),
            ]),
          ),
        const SizedBox(height: 20),

        // Number of questions
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          const Text('Nombre de questions',
              style: TextStyle(fontWeight: FontWeight.w600)),
          Text('$_nbQuestions',
              style: TextStyle(
                  color: AppTheme.primaryColor,
                  fontWeight: FontWeight.bold,
                  fontSize: 18)),
        ]),
        Slider(
          value: _nbQuestions.toDouble(),
          min: 3, max: 15, divisions: 12,
          label: '$_nbQuestions questions',
          activeColor: AppTheme.primaryColor,
          onChanged: (v) => setState(() => _nbQuestions = v.round()),
        ),
        const SizedBox(height: 12),

        // Difficulty
        const Align(
          alignment: Alignment.centerLeft,
          child: Text('Difficulté',
              style: TextStyle(fontWeight: FontWeight.w600)),
        ),
        const SizedBox(height: 8),
        SegmentedButton<String>(
          segments: _difficulties.entries
              .map((e) => ButtonSegment(value: e.key, label: Text(e.value)))
              .toList(),
          selected: {_difficulty},
          onSelectionChanged: (s) => setState(() => _difficulty = s.first),
          style: ButtonStyle(
            backgroundColor: WidgetStateProperty.resolveWith((states) {
              if (states.contains(WidgetState.selected)) {
                return AppTheme.primaryColor;
              }
              return null;
            }),
          ),
        ),
        const SizedBox(height: 24),

        // Generate button
        SizedBox(
          width: double.infinity,
          height: 50,
          child: ElevatedButton.icon(
            onPressed: isGenerating ? null : _generate,
            icon: isGenerating
                ? const SizedBox(
                    width: 18, height: 18,
                    child: CircularProgressIndicator(
                        strokeWidth: 2, color: Colors.white))
                : const Icon(Icons.auto_awesome),
            label: Text(
                isGenerating ? 'Génération...' : 'Générer le quiz',
                style: const TextStyle(fontSize: 16)),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ),
      ]),
    );
  }

  Future<void> _generate() async {
    final exam = await widget.ref.read(examsProvider.notifier).generateQuiz(
          subject: widget.module.nom,
          numQuestions: _nbQuestions,
          difficulty: _difficulty,
        );
    if (exam != null && mounted) {
      Navigator.pop(context); // close sheet
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => QuizScreen(exam: exam)),
      );
    }
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// Tab 1 — Assistant PDF
// ══════════════════════════════════════════════════════════════════════════════

class _PdfAssistantTab extends ConsumerStatefulWidget {
  const _PdfAssistantTab();

  @override
  ConsumerState<_PdfAssistantTab> createState() => _PdfAssistantTabState();
}

class _PdfAssistantTabState extends ConsumerState<_PdfAssistantTab> {
  final _questionCtrl = TextEditingController();
  String _uploadMatiere = '';

  @override
  void dispose() {
    _questionCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(examsProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // ── Upload section ──────────────────────────────────────────────────
        _SectionTitle(icon: Icons.upload_file, title: 'Importer un cours PDF'),
        const SizedBox(height: 10),
        _UploadCard(
          isUploading: state.isUploadingPdf,
          uploadError: state.uploadError,
          onUpload: _pickAndUpload,
        ),
        const SizedBox(height: 20),

        // ── Courses list ────────────────────────────────────────────────────
        if (state.isLoadingCourses)
          const Center(child: CircularProgressIndicator())
        else if (state.courses.isEmpty)
          _EmptyCourses()
        else ...[
          _SectionTitle(
              icon: Icons.library_books,
              title: 'Mes cours importés (${state.courses.length})'),
          const SizedBox(height: 10),
          ...state.courses.map((c) => _CourseChip(
                course: c,
                isSelected: state.selectedCourseId == c.id,
                onSelect: () {
                  ref.read(examsProvider.notifier).selectCourse(
                      state.selectedCourseId == c.id ? null : c.id);
                  _questionCtrl.clear();
                },
                onDelete: () => _confirmDelete(c),
              )),
        ],

        // ── AI panel (visible when a course is selected) ─────────────────
        if (state.selectedCourseId != null) ...[
          const SizedBox(height: 24),
          const Divider(),
          const SizedBox(height: 12),
          _SectionTitle(icon: Icons.smart_toy, title: 'Questions IA'),
          const SizedBox(height: 12),

          // Quick actions
          Wrap(spacing: 8, runSpacing: 8, children: [
            _QuickActionChip(
              label: 'Résumer',
              icon: Icons.summarize,
              color: const Color(0xFF1976D2),
              onTap: state.isAskingPdf
                  ? null
                  : () => _ask('Résume ce cours', type: 'resume'),
            ),
            _QuickActionChip(
              label: 'Notions clés',
              icon: Icons.key,
              color: const Color(0xFF7B1FA2),
              onTap: state.isAskingPdf
                  ? null
                  : () => _ask('Identifie les notions clés', type: 'notions'),
            ),
            _QuickActionChip(
              label: 'Générer examen',
              icon: Icons.quiz,
              color: const Color(0xFFE64A19),
              onTap: state.isAskingPdf
                  ? null
                  : () => _ask('Génère des questions d\'examen', type: 'examen'),
            ),
          ]),
          const SizedBox(height: 16),

          // Custom question field
          Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
            Expanded(
              child: TextField(
                controller: _questionCtrl,
                maxLines: 2,
                decoration: InputDecoration(
                  hintText: 'Posez votre question sur ce cours...',
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12)),
                  contentPadding: const EdgeInsets.all(12),
                ),
              ),
            ),
            const SizedBox(width: 8),
            SizedBox(
              height: 52,
              child: ElevatedButton(
                onPressed: state.isAskingPdf
                    ? null
                    : () {
                        final q = _questionCtrl.text.trim();
                        if (q.isNotEmpty) _ask(q, type: 'question');
                      },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryColor,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                  padding: const EdgeInsets.symmetric(horizontal: 14),
                ),
                child: state.isAskingPdf
                    ? const SizedBox(
                        width: 20, height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.send, color: Colors.white),
              ),
            ),
          ]),

          // Error
          if (state.pdfError != null) ...[
            const SizedBox(height: 10),
            _ErrorBanner(message: state.pdfError!),
          ],

          // AI response
          if (state.pdfAnswer != null) ...[
            const SizedBox(height: 16),
            _AiResponseCard(
              answer: state.pdfAnswer!,
              type: state.pdfAnswerType ?? 'question',
              onClear: () => ref.read(examsProvider.notifier).clearPdfAnswer(),
            ),
          ],
        ],
        const SizedBox(height: 32),
      ]),
    );
  }

  Future<void> _pickAndUpload() async {
    // Ask for matière name first
    final matiere = await _askMatiere();
    if (matiere == null || matiere.isEmpty) return;

    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
      withData: true,
    );
    if (result == null || result.files.isEmpty) return;

    final file = result.files.first;
    if (file.bytes == null) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Impossible de lire le fichier.')),
        );
      }
      return;
    }

    final ok = await ref.read(examsProvider.notifier).uploadPdf(
          matiere: matiere,
          titre: file.name,
          bytes: file.bytes!,
          filename: file.name,
        );

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(ok
            ? 'Cours importé avec succès !'
            : (ref.read(examsProvider).uploadError ?? 'Erreur lors de l\'import.')),
        backgroundColor: ok ? Colors.green : Colors.red,
      ));
    }
  }

  Future<String?> _askMatiere() async {
    final ctrl = TextEditingController(text: _uploadMatiere);
    return showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Nom du module'),
        content: TextField(
          controller: ctrl,
          autofocus: true,
          decoration: const InputDecoration(
            hintText: 'Ex : Machine Learning, Réseaux...',
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Annuler')),
          ElevatedButton(
            onPressed: () {
              _uploadMatiere = ctrl.text.trim();
              Navigator.pop(ctx, ctrl.text.trim());
            },
            child: const Text('Confirmer'),
          ),
        ],
      ),
    );
  }

  void _ask(String question, {required String type}) {
    final docId = ref.read(examsProvider).selectedCourseId;
    if (docId == null) return;
    ref.read(examsProvider.notifier).askCourse(
          docId: docId,
          question: question,
          type: type,
        );
  }

  Future<void> _confirmDelete(CourseDoc course) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Supprimer ce cours ?'),
        content: Text('${course.titre} sera supprimé définitivement.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: const Text('Annuler')),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Supprimer'),
          ),
        ],
      ),
    );
    if (ok == true) {
      ref.read(examsProvider.notifier).deleteCourse(course.id);
    }
  }
}

// ── Sub-widgets for PDF tab ───────────────────────────────────────────────────

class _SectionTitle extends StatelessWidget {
  final IconData icon;
  final String title;
  const _SectionTitle({required this.icon, required this.title});

  @override
  Widget build(BuildContext context) {
    return Row(children: [
      Icon(icon, size: 18, color: AppTheme.primaryColor),
      const SizedBox(width: 8),
      Text(title,
          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
    ]);
  }
}

class _UploadCard extends StatelessWidget {
  final bool isUploading;
  final String? uploadError;
  final VoidCallback onUpload;
  const _UploadCard(
      {required this.isUploading,
      required this.uploadError,
      required this.onUpload});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: isUploading ? null : onUpload,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 24),
        decoration: BoxDecoration(
          border: Border.all(
              color: AppTheme.primaryColor.withOpacity(0.4),
              width: 1.5,
              style: BorderStyle.solid),
          borderRadius: BorderRadius.circular(12),
          color: AppTheme.primaryColor.withOpacity(0.04),
        ),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          if (isUploading) ...[
            const CircularProgressIndicator(),
            const SizedBox(height: 10),
            const Text('Extraction du texte en cours...',
                style: TextStyle(color: Colors.grey, fontSize: 13)),
          ] else ...[
            Icon(Icons.cloud_upload_outlined,
                size: 40, color: AppTheme.primaryColor),
            const SizedBox(height: 8),
            Text('Appuyez pour importer un PDF',
                style: TextStyle(
                    color: AppTheme.primaryColor,
                    fontWeight: FontWeight.w600)),
            const SizedBox(height: 4),
            const Text('Le texte sera extrait automatiquement',
                style: TextStyle(color: Colors.grey, fontSize: 11)),
          ],
          if (uploadError != null) ...[
            const SizedBox(height: 10),
            _ErrorBanner(message: uploadError!),
          ],
        ]),
      ),
    );
  }
}

class _EmptyCourses extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 20),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.picture_as_pdf_outlined, size: 48, color: Colors.grey[400]),
          const SizedBox(height: 10),
          const Text('Aucun cours importé.',
              style: TextStyle(color: Colors.grey)),
          const Text('Importez un PDF ci-dessus pour commencer.',
              style: TextStyle(color: Colors.grey, fontSize: 12)),
        ]),
      ),
    );
  }
}

class _CourseChip extends StatelessWidget {
  final CourseDoc course;
  final bool isSelected;
  final VoidCallback onSelect;
  final VoidCallback onDelete;
  const _CourseChip({
    required this.course,
    required this.isSelected,
    required this.onSelect,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    final color = isSelected ? AppTheme.primaryColor : Colors.grey[700]!;
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: BorderSide(
            color: isSelected ? AppTheme.primaryColor : Colors.grey.shade300,
            width: isSelected ? 1.5 : 1),
      ),
      color: isSelected ? AppTheme.primaryColor.withOpacity(0.05) : null,
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.12),
          child: Icon(Icons.picture_as_pdf, color: color, size: 20),
        ),
        title: Text(course.titre,
            style: TextStyle(
                fontWeight: FontWeight.w600,
                color: isSelected ? AppTheme.primaryColor : null,
                fontSize: 13)),
        subtitle: Text(
          '${course.matiere} · ${_formatSize(course.chars)}',
          style: const TextStyle(fontSize: 11),
        ),
        trailing: Row(mainAxisSize: MainAxisSize.min, children: [
          if (course.hasResume)
            const Tooltip(
              message: 'Résumé disponible',
              child: Icon(Icons.summarize, size: 16, color: Colors.green),
            ),
          if (course.hasNotions)
            const Tooltip(
              message: 'Notions extraites',
              child: Icon(Icons.key, size: 16, color: Colors.purple),
            ),
          const SizedBox(width: 4),
          IconButton(
            icon: const Icon(Icons.delete_outline, size: 18, color: Colors.red),
            onPressed: onDelete,
            tooltip: 'Supprimer',
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(),
          ),
        ]),
        onTap: onSelect,
        selected: isSelected,
      ),
    );
  }

  String _formatSize(int chars) {
    if (chars < 1000) return '$chars car.';
    return '${(chars / 1000).toStringAsFixed(1)}k car.';
  }
}

class _QuickActionChip extends StatelessWidget {
  final String label;
  final IconData icon;
  final Color color;
  final VoidCallback? onTap;
  const _QuickActionChip(
      {required this.label,
      required this.icon,
      required this.color,
      required this.onTap});

  @override
  Widget build(BuildContext context) {
    return ActionChip(
      avatar: Icon(icon, size: 16, color: onTap == null ? Colors.grey : color),
      label: Text(label,
          style: TextStyle(
              fontSize: 12,
              color: onTap == null ? Colors.grey : color,
              fontWeight: FontWeight.w600)),
      backgroundColor: onTap == null ? Colors.grey[100] : color.withOpacity(0.1),
      side: BorderSide(color: onTap == null ? Colors.grey[300]! : color.withOpacity(0.4)),
      onPressed: onTap,
    );
  }
}

class _AiResponseCard extends StatelessWidget {
  final String answer;
  final String type;
  final VoidCallback onClear;
  const _AiResponseCard(
      {required this.answer, required this.type, required this.onClear});

  IconData get _icon {
    switch (type) {
      case 'resume':
        return Icons.summarize;
      case 'notions':
        return Icons.key;
      case 'examen':
        return Icons.quiz;
      default:
        return Icons.smart_toy;
    }
  }

  String get _title {
    switch (type) {
      case 'resume':
        return 'Résumé du cours';
      case 'notions':
        return 'Notions clés';
      case 'examen':
        return 'Questions d\'examen';
      default:
        return 'Réponse de l\'IA';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.blue.shade200),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Header
        Padding(
          padding: const EdgeInsets.fromLTRB(14, 12, 8, 8),
          child: Row(children: [
            Icon(_icon, size: 18, color: AppTheme.primaryColor),
            const SizedBox(width: 8),
            Text(_title,
                style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.primaryColor)),
            const Spacer(),
            IconButton(
              icon: const Icon(Icons.close, size: 16, color: Colors.grey),
              onPressed: onClear,
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
            ),
          ]),
        ),
        const Divider(height: 1),
        // Content
        Padding(
          padding: const EdgeInsets.all(14),
          child: answer.trim().isEmpty
              ? const Text(
                  'Aucun contenu reçu.',
                  style: TextStyle(color: Colors.grey, fontSize: 13),
                )
              : SelectableText(
                  answer,
                  style: const TextStyle(
                    fontSize: 13,
                    height: 1.55,
                    color: Colors.black87,
                  ),
                ),
        ),
      ]),
    );
  }
}

class _ErrorBanner extends StatelessWidget {
  final String message;
  const _ErrorBanner({required this.message});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.red.shade50,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.red.shade200),
      ),
      child: Row(children: [
        const Icon(Icons.error_outline, color: Colors.red, size: 16),
        const SizedBox(width: 8),
        Expanded(
          child: Text(message,
              style: const TextStyle(color: Colors.red, fontSize: 12)),
        ),
      ]),
    );
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// Tab 2 — Planning Officiel des examens
// ══════════════════════════════════════════════════════════════════════════════

class _OfficialScheduleTab extends ConsumerStatefulWidget {
  const _OfficialScheduleTab();

  @override
  ConsumerState<_OfficialScheduleTab> createState() =>
      _OfficialScheduleTabState();
}

class _OfficialScheduleTabState extends ConsumerState<_OfficialScheduleTab> {
  static const _days = [
    'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi',
  ];

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(examsProvider);

    if (state.isLoadingOfficialSchedule) {
      return const Center(child: CircularProgressIndicator());
    }

    // No schedule found → show filière picker if available
    if (state.officialSchedule.isEmpty) {
      return _buildEmpty(state);
    }

    // Group entries by day, handling both "Lundi" and "Lundi 12/01" formats
    final Map<String, List<OfficialExamEntry>> byDay = {};
    for (final d in _days) {
      byDay[d] = state.officialSchedule
          .where((e) => e.jour == d || e.jour.startsWith('$d '))
          .toList();
    }

    return RefreshIndicator(
      onRefresh: () => ref.read(examsProvider.notifier).loadOfficialSchedule(),
      child: CustomScrollView(
        slivers: [
          // Header banner
          SliverToBoxAdapter(
            child: _ScheduleHeader(
              session: state.officialScheduleSession,
              filiere: state.officialScheduleFiliere,
            ),
          ),
          // Per-day sections
          for (final day in _days)
            if ((byDay[day] ?? []).isNotEmpty) ...[
              SliverToBoxAdapter(
                child: Padding(
                  padding:
                      const EdgeInsets.fromLTRB(16, 16, 16, 6),
                  child: Row(children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppTheme.primaryColor,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                          byDay[day]!.first.jour,
                          style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 13)),
                    ),
                  ]),
                ),
              ),
              SliverPadding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (_, i) =>
                        _ExamEntryCard(entry: byDay[day]![i]),
                    childCount: byDay[day]!.length,
                  ),
                ),
              ),
            ],
          // Filière switcher at bottom
          SliverToBoxAdapter(
            child: _FiliereSwitcher(
              availableFilieres: state.availableFilieres,
              onSelect: (cle, sem) {
                ref
                    .read(examsProvider.notifier)
                    .loadOfficialSchedule(filiere: cle, semestre: sem);
              },
            ),
          ),
          const SliverToBoxAdapter(child: SizedBox(height: 32)),
        ],
      ),
    );
  }

  Widget _buildEmpty(ExamsState state) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.orange.shade50,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.orange.shade200),
          ),
          child: Row(children: [
            const Icon(Icons.info_outline, color: Colors.orange),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                state.officialScheduleFiliere.isEmpty
                    ? 'Planning non disponible pour votre filière. Complétez votre profil ou choisissez une filière ci-dessous.'
                    : 'Planning non trouvé pour "${state.officialScheduleFiliere}". Choisissez parmi les filières disponibles.',
                style: const TextStyle(fontSize: 12, color: Colors.orange),
              ),
            ),
          ]),
        ),
        const SizedBox(height: 20),
        _FiliereSwitcher(
          availableFilieres: state.availableFilieres,
          onSelect: (cle, sem) {
            ref
                .read(examsProvider.notifier)
                .loadOfficialSchedule(filiere: cle, semestre: sem);
          },
        ),
      ]),
    );
  }
}

class _ScheduleHeader extends StatelessWidget {
  final String session;
  final String filiere;
  const _ScheduleHeader({required this.session, required this.filiere});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            const Color(0xFF0052A5),
            AppTheme.accentColor,
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Icon(Icons.event_note, color: Colors.white, size: 22),
          const SizedBox(width: 10),
          const Text('Planning Officiel des Examens',
              style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 15)),
        ]),
        const SizedBox(height: 6),
        Text(session,
            style: const TextStyle(color: Colors.white70, fontSize: 12)),
        if (filiere.isNotEmpty) ...[
          const SizedBox(height: 4),
          Text(filiere,
              style: const TextStyle(
                  color: Colors.white,
                  fontSize: 13,
                  fontWeight: FontWeight.w600)),
        ],
      ]),
    );
  }
}

class _ExamEntryCard extends StatelessWidget {
  final OfficialExamEntry entry;
  const _ExamEntryCard({required this.entry});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Time column
          Container(
            width: 72,
            padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 6),
            decoration: BoxDecoration(
              color: AppTheme.primaryColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              entry.creneau.replaceAll('-', '\n'),
              style: TextStyle(
                  fontSize: 10,
                  color: AppTheme.primaryColor,
                  fontWeight: FontWeight.bold,
                  height: 1.4),
              textAlign: TextAlign.center,
            ),
          ),
          const SizedBox(width: 12),
          // Module info
          Expanded(
            child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
              Text(entry.module,
                  style: const TextStyle(
                      fontWeight: FontWeight.w600, fontSize: 13)),
              const SizedBox(height: 4),
              Row(children: [
                const Icon(Icons.person_outline,
                    size: 13, color: Colors.grey),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(entry.coordonnateur,
                      style: const TextStyle(
                          color: Colors.grey, fontSize: 11),
                      overflow: TextOverflow.ellipsis),
                ),
              ]),
              const SizedBox(height: 2),
              Row(children: [
                const Icon(Icons.room_outlined,
                    size: 13, color: Colors.grey),
                const SizedBox(width: 4),
                Text(entry.salle,
                    style: const TextStyle(
                        color: Colors.grey, fontSize: 11)),
              ]),
            ]),
          ),
        ]),
      ),
    );
  }
}

class _FiliereSwitcher extends StatelessWidget {
  final List<Map<String, dynamic>> availableFilieres;
  final void Function(String cle, String semestre) onSelect;
  const _FiliereSwitcher(
      {required this.availableFilieres, required this.onSelect});

  @override
  Widget build(BuildContext context) {
    if (availableFilieres.isEmpty) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Divider(),
        const Text('Voir le planning d\'une autre filière :',
            style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: Colors.grey)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 6,
          children: availableFilieres.map((f) {
            final cle = f['cle'] as String? ?? '';
            final nom = f['nom'] as String? ?? cle;
            final sem = f['semestre'] as String? ?? '';
            return ActionChip(
              label: Text('$nom $sem',
                  style: const TextStyle(fontSize: 11)),
              onPressed: () => onSelect(cle, sem),
            );
          }).toList(),
        ),
      ]),
    );
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// Tab 3 — Stats
// ══════════════════════════════════════════════════════════════════════════════

class _StatsTab extends ConsumerWidget {
  const _StatsTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final stats = ref.watch(examsProvider).stats;
    final completed = ref.watch(examsProvider).history
        .where((e) => e.status == 'completed')
        .toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
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
              title: 'Quiz terminés',
              value: '${stats.completedExams}',
              icon: Icons.check_circle_outline,
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
              Text('Va dans "Modules" pour commencer !',
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
        Text(title, style: TextStyle(fontSize: 11, color: Colors.grey[600])),
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
            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
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

// ══════════════════════════════════════════════════════════════════════════════
// Tab 3 — Historique
// ══════════════════════════════════════════════════════════════════════════════

class _HistoryTab extends ConsumerWidget {
  const _HistoryTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(examsProvider);

    if (state.isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (state.history.isEmpty) {
      return const Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.history, size: 64, color: Colors.grey),
          SizedBox(height: 12),
          Text('Aucun quiz dans l\'historique.',
              style: TextStyle(color: Colors.grey)),
        ]),
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
                  style: const TextStyle(
                      fontWeight: FontWeight.w600, fontSize: 13)),
              subtitle: Text(
                  '${exam.subject} · ${exam.questions.length} questions'),
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
                      style:
                          TextStyle(fontSize: 11, color: Colors.grey[500]),
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
// Quiz Screen
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
                    Text(
                      q.question,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 24),
                    ...q.options.map((opt) {
                      final selected = _answers[_currentIndex] == opt;
                      return GestureDetector(
                        onTap: () =>
                            setState(() => _answers[_currentIndex] = opt),
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
                              child: Text(
                                opt,
                                style: TextStyle(
                                  fontWeight: selected
                                      ? FontWeight.w600
                                      : FontWeight.normal,
                                  color: Colors.black87,
                                ),
                              ),
                            ),
                          ]),
                        ),
                      );
                    }),
                  ]),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(children: [
              if (_currentIndex > 0)
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => setState(() => _currentIndex--),
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
    final feedbackList =
        (_result!['feedback'] as List?)?.cast<Map<String, dynamic>>() ?? [];

    return Scaffold(
      appBar: AppBar(title: const Text('Résultat'), elevation: 0),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(children: [
          Text(emoji, style: const TextStyle(fontSize: 56)),
          const SizedBox(height: 8),
          Text(message,
              style:
                  const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: color.withOpacity(0.3)),
            ),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              Text('${pct.toStringAsFixed(0)}%',
                  style: TextStyle(
                      fontSize: 44,
                      fontWeight: FontWeight.bold,
                      color: color)),
              const SizedBox(width: 16),
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('$score / $total',
                    style: const TextStyle(
                        fontSize: 18, fontWeight: FontWeight.bold)),
                const Text('questions correctes',
                    style: TextStyle(fontSize: 12, color: Colors.grey)),
              ]),
            ]),
          ),
          const SizedBox(height: 24),
          if (feedbackList.isNotEmpty) ...[
            const Align(
              alignment: Alignment.centerLeft,
              child: Text('Correction détaillée',
                  style:
                      TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
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
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 8, vertical: 3),
                            decoration: BoxDecoration(
                              color: fbColor.withOpacity(0.12),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text('Q${i + 1}',
                                style: TextStyle(
                                    color: fbColor,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 12)),
                          ),
                          const SizedBox(width: 8),
                          Icon(
                              isCorrect
                                  ? Icons.check_circle
                                  : Icons.cancel,
                              color: fbColor,
                              size: 18),
                          const SizedBox(width: 4),
                          Text(isCorrect ? 'Correct' : 'Incorrect',
                              style: TextStyle(
                                  color: fbColor,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 13)),
                        ]),
                        const SizedBox(height: 8),
                        Text(fb['question'] as String? ?? '',
                            style: const TextStyle(
                                fontWeight: FontWeight.w600, fontSize: 13)),
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
                        if (fb['explanation'] != null &&
                            (fb['explanation'] as String).isNotEmpty) ...[
                          const SizedBox(height: 6),
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: Colors.blue.withOpacity(0.06),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Icon(Icons.lightbulb_outline,
                                      size: 14, color: Colors.blue),
                                  const SizedBox(width: 6),
                                  Expanded(
                                    child: Text(fb['explanation'] as String,
                                        style: const TextStyle(
                                            fontSize: 12,
                                            color: Colors.black87)),
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
  const _FeedbackRow(
      {required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text('$label : ',
          style: TextStyle(
              fontSize: 12, color: color, fontWeight: FontWeight.w600)),
      Expanded(
          child: Text(value, style: const TextStyle(fontSize: 12))),
    ]);
  }
}
