import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/plan_model.dart';
import '../services/api_service.dart';

class PlanningState {
  final List<Plan> tasks;
  final bool isLoading;
  final String? error;

  PlanningState({
    this.tasks = const [],
    this.isLoading = false,
    this.error,
  });

  PlanningState copyWith({
    List<Plan>? tasks,
    bool? isLoading,
    String? error,
  }) =>
      PlanningState(
        tasks: tasks ?? this.tasks,
        isLoading: isLoading ?? this.isLoading,
        error: error,
      );

  List<Plan> get pending =>
      tasks.where((t) => t.status == 'pending').toList()
        ..sort((a, b) => a.dueDate.compareTo(b.dueDate));

  List<Plan> get completed =>
      tasks.where((t) => t.status == 'completed').toList();

  List<Plan> get urgent =>
      tasks.where((t) => t.isUrgent).toList();
}

class PlanningNotifier extends StateNotifier<PlanningState> {
  final ApiService _api;

  PlanningNotifier(this._api) : super(PlanningState());

  Future<void> loadTasks() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final data = await _api.getTasks();
      final tasks = (data as List).map((j) => Plan.fromJson(j as Map<String, dynamic>)).toList();
      state = state.copyWith(tasks: tasks, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  Future<void> addTask({
    required String title,
    required String category,
    required DateTime dueDate,
    String? description,
    int priority = 1,
  }) async {
    try {
      final data = await _api.createTask(
        title: title,
        category: category,
        dueDate: dueDate,
        description: description,
        priority: priority,
      );
      final newTask = Plan.fromJson(data as Map<String, dynamic>);
      state = state.copyWith(tasks: [...state.tasks, newTask]);
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> toggleComplete(int taskId) async {
    final task = state.tasks.firstWhere((t) => t.id == taskId);
    final newStatus = task.isCompleted ? 'pending' : 'completed';
    try {
      await _api.updateTask(taskId: taskId, status: newStatus);
      state = state.copyWith(
        tasks: state.tasks.map((t) => t.id == taskId ? t.copyWith(status: newStatus) : t).toList(),
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> deleteTask(int taskId) async {
    try {
      await _api.deleteTask(taskId);
      state = state.copyWith(tasks: state.tasks.where((t) => t.id != taskId).toList());
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }
}

final planningProvider = StateNotifierProvider<PlanningNotifier, PlanningState>((ref) {
  return PlanningNotifier(ref.watch(apiServiceProvider));
});
