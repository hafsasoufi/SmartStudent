import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/exam_model.dart';
import '../services/api_service.dart';

// ── Domain models ─────────────────────────────────────────────────────────────

class ModuleItem {
  final String nom;
  final String code;
  final double coefficient;
  final bool hasExam;
  final String? examJour;
  final String? examCreneau;
  final String? examSalle;
  final String? examCoordonnateur;

  const ModuleItem({
    required this.nom,
    required this.code,
    required this.coefficient,
    this.hasExam = false,
    this.examJour,
    this.examCreneau,
    this.examSalle,
    this.examCoordonnateur,
  });

  factory ModuleItem.fromJson(Map<String, dynamic> j) => ModuleItem(
        nom: j['nom'] as String? ?? '',
        code: j['code'] as String? ?? '',
        coefficient: (j['coefficient'] as num?)?.toDouble() ?? 1.0,
        hasExam: j['has_exam'] as bool? ?? false,
        examJour: j['exam_jour'] as String?,
        examCreneau: j['exam_creneau'] as String?,
        examSalle: j['exam_salle'] as String?,
        examCoordonnateur: j['exam_coordonnateur'] as String?,
      );
}

class OfficialExamEntry {
  final String jour;
  final String creneau;
  final String module;
  final String coordonnateur;
  final String salle;

  const OfficialExamEntry({
    required this.jour,
    required this.creneau,
    required this.module,
    required this.coordonnateur,
    required this.salle,
  });
}

class CourseDoc {
  final int id;
  final String matiere;
  final String titre;
  final int chars;
  final bool hasResume;
  final bool hasNotions;
  final DateTime createdAt;

  const CourseDoc({
    required this.id,
    required this.matiere,
    required this.titre,
    required this.chars,
    required this.hasResume,
    required this.hasNotions,
    required this.createdAt,
  });

  factory CourseDoc.fromJson(Map<String, dynamic> j) => CourseDoc(
        id: j['id'] as int,
        matiere: j['matiere'] as String? ?? '',
        titre: j['titre'] as String? ?? '',
        chars: j['chars'] as int? ?? 0,
        hasResume: j['has_resume'] as bool? ?? false,
        hasNotions: j['has_notions'] as bool? ?? false,
        createdAt: DateTime.tryParse(j['created_at'] as String? ?? '') ?? DateTime.now(),
      );
}

// ── State ─────────────────────────────────────────────────────────────────────

class ExamsState {
  final List<ExamRecord> history;
  final ExamStats stats;
  final ExamRecord? activeExam;
  final bool isLoading;
  final bool isGenerating;
  final String? error;

  // Modules
  final List<ModuleItem> modules;
  final String filiere;
  final String semestre;
  final String session;
  final int niveau;
  final int totalExamens;
  final bool isLoadingModules;

  // Official schedule
  final List<OfficialExamEntry> officialSchedule;
  final String officialScheduleFiliere;
  final String officialScheduleSession;
  final bool isLoadingOfficialSchedule;
  final List<Map<String, dynamic>> availableFilieres;

  // Courses / PDF assistant
  final List<CourseDoc> courses;
  final bool isLoadingCourses;
  final bool isUploadingPdf;
  final bool isAskingPdf;
  final String? pdfAnswer;
  final String? pdfAnswerType;
  final int? selectedCourseId;
  final String? pdfError;
  final String? uploadError;

  ExamsState({
    this.history = const [],
    ExamStats? stats,
    this.activeExam,
    this.isLoading = false,
    this.isGenerating = false,
    this.error,
    this.modules = const [],
    this.filiere = '',
    this.semestre = '',
    this.session = '',
    this.niveau = 1,
    this.totalExamens = 0,
    this.isLoadingModules = false,
    this.officialSchedule = const [],
    this.officialScheduleFiliere = '',
    this.officialScheduleSession = '',
    this.isLoadingOfficialSchedule = false,
    this.availableFilieres = const [],
    this.courses = const [],
    this.isLoadingCourses = false,
    this.isUploadingPdf = false,
    this.isAskingPdf = false,
    this.pdfAnswer,
    this.pdfAnswerType,
    this.selectedCourseId,
    this.pdfError,
    this.uploadError,
  }) : stats = stats ?? ExamStats.empty();

  ExamsState copyWith({
    List<ExamRecord>? history,
    ExamStats? stats,
    ExamRecord? activeExam,
    bool? isLoading,
    bool? isGenerating,
    String? error,
    bool clearActiveExam = false,
    List<ModuleItem>? modules,
    String? filiere,
    String? semestre,
    String? session,
    int? niveau,
    int? totalExamens,
    bool? isLoadingModules,
    List<OfficialExamEntry>? officialSchedule,
    String? officialScheduleFiliere,
    String? officialScheduleSession,
    bool? isLoadingOfficialSchedule,
    List<Map<String, dynamic>>? availableFilieres,
    List<CourseDoc>? courses,
    bool? isLoadingCourses,
    bool? isUploadingPdf,
    bool? isAskingPdf,
    String? pdfAnswer,
    String? pdfAnswerType,
    int? selectedCourseId,
    bool clearSelectedCourse = false,
    String? pdfError,
    String? uploadError,
    bool clearPdfAnswer = false,
  }) =>
      ExamsState(
        history: history ?? this.history,
        stats: stats ?? this.stats,
        activeExam: clearActiveExam ? null : (activeExam ?? this.activeExam),
        isLoading: isLoading ?? this.isLoading,
        isGenerating: isGenerating ?? this.isGenerating,
        error: error,
        modules: modules ?? this.modules,
        filiere: filiere ?? this.filiere,
        semestre: semestre ?? this.semestre,
        session: session ?? this.session,
        niveau: niveau ?? this.niveau,
        totalExamens: totalExamens ?? this.totalExamens,
        isLoadingModules: isLoadingModules ?? this.isLoadingModules,
        officialSchedule: officialSchedule ?? this.officialSchedule,
        officialScheduleFiliere: officialScheduleFiliere ?? this.officialScheduleFiliere,
        officialScheduleSession: officialScheduleSession ?? this.officialScheduleSession,
        isLoadingOfficialSchedule: isLoadingOfficialSchedule ?? this.isLoadingOfficialSchedule,
        availableFilieres: availableFilieres ?? this.availableFilieres,
        courses: courses ?? this.courses,
        isLoadingCourses: isLoadingCourses ?? this.isLoadingCourses,
        isUploadingPdf: isUploadingPdf ?? this.isUploadingPdf,
        isAskingPdf: isAskingPdf ?? this.isAskingPdf,
        pdfAnswer: clearPdfAnswer ? null : (pdfAnswer ?? this.pdfAnswer),
        pdfAnswerType: clearPdfAnswer ? null : (pdfAnswerType ?? this.pdfAnswerType),
        selectedCourseId: clearSelectedCourse ? null : (selectedCourseId ?? this.selectedCourseId),
        pdfError: pdfError,
        uploadError: uploadError,
      );
}

// ── Notifier ──────────────────────────────────────────────────────────────────

class ExamsNotifier extends StateNotifier<ExamsState> {
  final ApiService _api;

  ExamsNotifier(this._api) : super(ExamsState());

  // ── Quiz history & stats ─────────────────────────────────────────────────

  Future<void> loadHistory() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final data = await _api.getExamHistory();
      final history = (data as List)
          .map((j) => ExamRecord.fromJson(j as Map<String, dynamic>))
          .toList();
      state = state.copyWith(history: history, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  Future<void> loadStats() async {
    try {
      final data = await _api.getExamStats();
      state = state.copyWith(stats: ExamStats.fromJson(data as Map<String, dynamic>));
    } catch (_) {}
  }

  Future<ExamRecord?> generateQuiz({
    required String subject,
    int numQuestions = 5,
    String difficulty = 'medium',
  }) async {
    state = state.copyWith(isGenerating: true, error: null);
    try {
      final data = await _api.generateExam(
        subject: subject,
        numQuestions: numQuestions,
        difficulty: difficulty,
      );
      final exam = ExamRecord.fromJson(data as Map<String, dynamic>);
      state = state.copyWith(
        activeExam: exam,
        isGenerating: false,
        history: [...state.history, exam],
      );
      return exam;
    } catch (e) {
      state = state.copyWith(isGenerating: false, error: e.toString());
      return null;
    }
  }

  Future<Map<String, dynamic>?> submitQuiz({
    required int examId,
    required List<String?> answers,
  }) async {
    try {
      final result = await _api.submitExam(examId: examId, answers: answers);
      await loadHistory();
      await loadStats();
      state = state.copyWith(clearActiveExam: true);
      return result as Map<String, dynamic>;
    } catch (e) {
      state = state.copyWith(error: e.toString());
      return null;
    }
  }

  void clearActiveExam() => state = state.copyWith(clearActiveExam: true);

  // ── Modules ──────────────────────────────────────────────────────────────

  Future<void> loadModules({String? semestre}) async {
    state = state.copyWith(isLoadingModules: true);
    try {
      final data = await _api.getModules(semestre: semestre);
      final modules = (data['modules'] as List? ?? [])
          .map((j) => ModuleItem.fromJson(j as Map<String, dynamic>))
          .toList();
      state = state.copyWith(
        modules: modules,
        filiere: data['filiere'] as String? ?? '',
        semestre: data['semestre'] as String? ?? '',
        session: data['session'] as String? ?? '',
        niveau: (data['niveau'] as int?) ?? 1,
        totalExamens: (data['total_examens'] as int?) ?? 0,
        isLoadingModules: false,
      );
    } catch (e) {
      state = state.copyWith(isLoadingModules: false, error: e.toString());
    }
  }

  // ── Official schedule ────────────────────────────────────────────────────

  Future<void> loadOfficialSchedule({String? filiere, String? semestre}) async {
    state = state.copyWith(isLoadingOfficialSchedule: true);
    try {
      final data = await _api.getOfficialSchedule(filiere: filiere, semestre: semestre);
      final planningRaw = data['planning'] as Map<String, dynamic>? ?? {};
      final entries = <OfficialExamEntry>[];
      planningRaw.forEach((jour, slots) {
        if (slots is Map<String, dynamic>) {
          slots.forEach((creneau, info) {
            if (info is Map<String, dynamic>) {
              entries.add(OfficialExamEntry(
                jour: jour,
                creneau: creneau,
                module: info['module'] as String? ?? '',
                coordonnateur: info['coordonnateur'] as String? ?? '',
                salle: info['salle'] as String? ?? '',
              ));
            }
          });
        }
      });
      final rawFilieres = data['available_filieres'] as List?;
      state = state.copyWith(
        officialSchedule: entries,
        officialScheduleFiliere: data['filiere'] as String? ?? filiere ?? '',
        officialScheduleSession: data['session'] as String? ?? '',
        isLoadingOfficialSchedule: false,
        availableFilieres: rawFilieres != null
            ? rawFilieres.cast<Map<String, dynamic>>()
            : state.availableFilieres,
      );
    } catch (e) {
      state = state.copyWith(isLoadingOfficialSchedule: false, error: e.toString());
    }
  }

  // ── Course PDF assistant ──────────────────────────────────────────────────

  Future<void> loadCourses() async {
    state = state.copyWith(isLoadingCourses: true);
    try {
      final data = await _api.getCourses();
      final courses = data
          .map((j) => CourseDoc.fromJson(j as Map<String, dynamic>))
          .toList();
      state = state.copyWith(courses: courses, isLoadingCourses: false);
    } catch (e) {
      state = state.copyWith(isLoadingCourses: false, pdfError: e.toString());
    }
  }

  Future<bool> uploadPdf({
    required String matiere,
    required String titre,
    required List<int> bytes,
    required String filename,
  }) async {
    state = state.copyWith(isUploadingPdf: true, uploadError: null);
    try {
      await _api.uploadCoursePdf(
        matiere: matiere,
        titre: titre,
        bytes: bytes,
        filename: filename,
      );
      await loadCourses();
      state = state.copyWith(isUploadingPdf: false);
      return true;
    } catch (e) {
      state = state.copyWith(isUploadingPdf: false, uploadError: e.toString());
      return false;
    }
  }

  Future<void> deleteCourse(int docId) async {
    try {
      await _api.deleteCourse(docId);
      final updated = state.courses.where((c) => c.id != docId).toList();
      final selId = state.selectedCourseId == docId ? null : state.selectedCourseId;
      state = state.copyWith(
        courses: updated,
        clearSelectedCourse: selId == null,
        selectedCourseId: selId,
        clearPdfAnswer: selId == null,
      );
    } catch (e) {
      state = state.copyWith(pdfError: e.toString());
    }
  }

  void selectCourse(int? docId) {
    state = state.copyWith(
      selectedCourseId: docId,
      clearPdfAnswer: true,
    );
  }

  Future<void> askCourse({
    required int docId,
    required String question,
    String type = 'question',
  }) async {
    state = state.copyWith(isAskingPdf: true, pdfError: null, clearPdfAnswer: true);
    try {
      final data = await _api.askCoursePdf(docId: docId, question: question, type: type);
      // Essayer plusieurs clés possibles retournées par le backend
      final raw = (data['response'] as String?
              ?? data['answer'] as String?
              ?? data['content'] as String?
              ?? data['result'] as String?
              ?? '')
          .trim();
      if (raw.isNotEmpty) {
        state = state.copyWith(
          isAskingPdf: false,
          pdfAnswer: raw,
          pdfAnswerType: type,
        );
      } else {
        state = state.copyWith(
          isAskingPdf: false,
          clearPdfAnswer: true,
          pdfError: 'Réponse vide reçue. Vérifiez que le cours contient du texte et réessayez.',
        );
      }
    } catch (e) {
      state = state.copyWith(isAskingPdf: false, pdfError: e.toString());
    }
  }

  void clearPdfAnswer() => state = state.copyWith(clearPdfAnswer: true);
}

final examsProvider = StateNotifierProvider<ExamsNotifier, ExamsState>((ref) {
  return ExamsNotifier(ref.watch(apiServiceProvider));
});
