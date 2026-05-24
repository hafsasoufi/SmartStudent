class QuizQuestion {
  final String question;
  final List<String> options;
  final String answer;
  final String? explanation;
  String? userAnswer;

  QuizQuestion({
    required this.question,
    required this.options,
    required this.answer,
    this.explanation,
    this.userAnswer,
  });

  bool get isAnswered => userAnswer != null;
  bool get isCorrect => userAnswer == answer;

  factory QuizQuestion.fromJson(Map<String, dynamic> json) {
    return QuizQuestion(
      question: json['question'] as String? ?? json['text'] as String? ?? '',
      options: (json['options'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      answer: json['answer'] as String? ??
          json['correct_answer'] as String? ??
          '',
      explanation: json['explanation'] as String?,
    );
  }
}

class ExamRecord {
  final int id;
  final int userId;
  final String title;
  final String subject;
  final List<QuizQuestion> questions;
  final int? score;
  final int totalPoints;
  final String status;
  final DateTime createdAt;
  final DateTime? completedAt;

  ExamRecord({
    required this.id,
    required this.userId,
    required this.title,
    required this.subject,
    required this.questions,
    this.score,
    required this.totalPoints,
    required this.status,
    required this.createdAt,
    this.completedAt,
  });

  double get percentage =>
      totalPoints > 0 ? (score ?? 0) / totalPoints * 100 : 0;

  factory ExamRecord.fromJson(Map<String, dynamic> json) {
    final rawQuestions = json['questions'];
    List<QuizQuestion> questions = [];
    if (rawQuestions is List) {
      questions = rawQuestions
          .map((q) => QuizQuestion.fromJson(q as Map<String, dynamic>))
          .toList();
    }
    return ExamRecord(
      id: json['id'] as int,
      userId: json['user_id'] as int,
      title: json['title'] as String,
      subject: json['subject'] as String,
      questions: questions,
      score: json['score'] as int?,
      totalPoints: json['total_points'] as int? ?? questions.length,
      status: json['status'] as String? ?? 'draft',
      createdAt: DateTime.parse(json['created_at'] as String),
      completedAt: json['completed_at'] != null
          ? DateTime.parse(json['completed_at'] as String)
          : null,
    );
  }
}

class ExamStats {
  final double averageScore;
  final int totalExams;
  final int completedExams;
  final List<String> weakSubjects;
  final List<String> strongSubjects;

  ExamStats({
    required this.averageScore,
    required this.totalExams,
    required this.completedExams,
    required this.weakSubjects,
    required this.strongSubjects,
  });

  factory ExamStats.fromJson(Map<String, dynamic> json) {
    return ExamStats(
      averageScore: (json['average_score'] as num?)?.toDouble() ?? 0,
      totalExams: json['total_exams'] as int? ?? 0,
      completedExams: json['completed_exams'] as int? ?? 0,
      weakSubjects: (json['weak_subjects'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      strongSubjects: (json['strong_subjects'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }

  factory ExamStats.empty() => ExamStats(
        averageScore: 0,
        totalExams: 0,
        completedExams: 0,
        weakSubjects: [],
        strongSubjects: [],
      );
}
