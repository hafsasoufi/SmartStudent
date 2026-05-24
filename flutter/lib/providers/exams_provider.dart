import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/exam_model.dart';
import '../services/api_service.dart';

class ExamsState {
  final List<ExamRecord> history;
  final ExamStats stats;
  final ExamRecord? activeExam;
  final bool isLoading;
  final bool isGenerating;
  final String? error;

  ExamsState({
    this.history = const [],
    ExamStats? stats,
    this.activeExam,
    this.isLoading = false,
    this.isGenerating = false,
    this.error,
  }) : stats = stats ?? ExamStats.empty();

  ExamsState copyWith({
    List<ExamRecord>? history,
    ExamStats? stats,
    ExamRecord? activeExam,
    bool? isLoading,
    bool? isGenerating,
    String? error,
    bool clearActiveExam = false,
  }) =>
      ExamsState(
        history: history ?? this.history,
        stats: stats ?? this.stats,
        activeExam: clearActiveExam ? null : (activeExam ?? this.activeExam),
        isLoading: isLoading ?? this.isLoading,
        isGenerating: isGenerating ?? this.isGenerating,
        error: error,
      );
}

class ExamsNotifier extends StateNotifier<ExamsState> {
  final ApiService _api;

  ExamsNotifier(this._api) : super(ExamsState());

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
}

final examsProvider = StateNotifierProvider<ExamsNotifier, ExamsState>((ref) {
  return ExamsNotifier(ref.watch(apiServiceProvider));
});
