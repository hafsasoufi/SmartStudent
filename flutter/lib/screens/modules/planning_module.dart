import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/plan_model.dart';
import '../../providers/planning_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';

class PlanningModule extends ConsumerStatefulWidget {
  const PlanningModule({Key? key}) : super(key: key);

  @override
  ConsumerState<PlanningModule> createState() => _PlanningModuleState();
}

class _PlanningModuleState extends ConsumerState<PlanningModule> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(planningProvider.notifier).loadTasks());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mon Planning'), elevation: 0),
      body: DefaultTabController(
        length: 4,
        child: Column(
          children: [
            const TabBar(
              isScrollable: true,
              tabs: [
                Tab(icon: Icon(Icons.smart_toy), text: 'Agent IA'),
                Tab(icon: Icon(Icons.assignment_late), text: 'Urgent'),
                Tab(icon: Icon(Icons.list_alt), text: 'Tâches'),
                Tab(icon: Icon(Icons.check_circle_outline), text: 'Terminé'),
              ],
            ),
            Expanded(
              child: TabBarView(children: [
                ModuleAgentChat(
                  module: 'planning',
                  agentLabel: 'Agent Planning',
                  placeholder: 'Aide-moi à organiser mes révisions...',
                  suggestions: const [
                    'Organiser mes révisions',
                    'Deadlines cette semaine',
                    'Planning examens',
                    'Méthode Pomodoro',
                    'Prioriser mes tâches',
                  ],
                ),
                const _UrgentTab(),
                const _TasksTab(),
                const _CompletedTab(),
              ]),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAddTaskDialog(context),
        icon: const Icon(Icons.add),
        label: const Text('Ajouter'),
      ),
    );
  }

  void _showAddTaskDialog(BuildContext context) {
    final titleCtrl = TextEditingController();
    final descCtrl = TextEditingController();
    DateTime selectedDate = DateTime.now().add(const Duration(days: 3));
    String selectedCategory = 'study';
    int selectedPriority = 2;

    showDialog(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          title: const Text('Nouvelle tâche'),
          content: SingleChildScrollView(
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              TextField(
                controller: titleCtrl,
                decoration: const InputDecoration(
                  labelText: 'Titre *',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: descCtrl,
                decoration: const InputDecoration(
                  labelText: 'Description',
                  border: OutlineInputBorder(),
                ),
                maxLines: 2,
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: selectedCategory,
                decoration: const InputDecoration(
                  labelText: 'Catégorie',
                  border: OutlineInputBorder(),
                ),
                items: const [
                  DropdownMenuItem(value: 'study', child: Text('Étude')),
                  DropdownMenuItem(value: 'project', child: Text('Projet')),
                  DropdownMenuItem(value: 'personal', child: Text('Personnel')),
                  DropdownMenuItem(value: 'exam', child: Text('Examen')),
                ],
                onChanged: (v) => setDialogState(() => selectedCategory = v!),
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<int>(
                value: selectedPriority,
                decoration: const InputDecoration(
                  labelText: 'Priorité',
                  border: OutlineInputBorder(),
                ),
                items: const [
                  DropdownMenuItem(value: 1, child: Text('Basse')),
                  DropdownMenuItem(value: 2, child: Text('Normale')),
                  DropdownMenuItem(value: 3, child: Text('Haute')),
                  DropdownMenuItem(value: 4, child: Text('Urgente')),
                ],
                onChanged: (v) => setDialogState(() => selectedPriority = v!),
              ),
              const SizedBox(height: 12),
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.calendar_today),
                title: Text(
                  'Échéance : ${selectedDate.day}/${selectedDate.month}/${selectedDate.year}',
                ),
                trailing: const Icon(Icons.edit, size: 18),
                onTap: () async {
                  final date = await showDatePicker(
                    context: ctx,
                    initialDate: selectedDate,
                    firstDate: DateTime.now(),
                    lastDate: DateTime.now().add(const Duration(days: 365)),
                  );
                  if (date != null) setDialogState(() => selectedDate = date);
                },
              ),
            ]),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Annuler'),
            ),
            ElevatedButton(
              onPressed: () async {
                if (titleCtrl.text.trim().isEmpty) return;
                Navigator.pop(ctx);
                await ref.read(planningProvider.notifier).addTask(
                      title: titleCtrl.text.trim(),
                      category: selectedCategory,
                      dueDate: selectedDate,
                      description: descCtrl.text.trim().isEmpty
                          ? null
                          : descCtrl.text.trim(),
                      priority: selectedPriority,
                    );
              },
              child: const Text('Ajouter'),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Onglet Urgent ────────────────────────────────────────────────────────────
class _UrgentTab extends ConsumerWidget {
  const _UrgentTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(planningProvider);
    if (state.isLoading) return const Center(child: CircularProgressIndicator());
    final urgent = state.urgent;
    if (urgent.isEmpty) {
      return const Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.check_circle, size: 64, color: Colors.green),
          SizedBox(height: 12),
          Text('Aucune tâche urgente !', style: TextStyle(fontSize: 16)),
        ]),
      );
    }
    return _TaskList(tasks: urgent, urgent: true);
  }
}

// ── Onglet Tâches ────────────────────────────────────────────────────────────
class _TasksTab extends ConsumerWidget {
  const _TasksTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(planningProvider);
    if (state.isLoading) return const Center(child: CircularProgressIndicator());
    if (state.error != null) {
      return Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Icon(Icons.error_outline, color: Colors.red, size: 48),
          const SizedBox(height: 8),
          Text(state.error!, textAlign: TextAlign.center),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: () => ref.read(planningProvider.notifier).loadTasks(),
            child: const Text('Réessayer'),
          ),
        ]),
      );
    }
    final pending = state.pending;
    if (pending.isEmpty) {
      return const Center(child: Text('Aucune tâche en cours.\nAppuyez sur + pour en ajouter.', textAlign: TextAlign.center));
    }
    return _TaskList(tasks: pending, urgent: false);
  }
}

// ── Onglet Terminé ───────────────────────────────────────────────────────────
class _CompletedTab extends ConsumerWidget {
  const _CompletedTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final completed = ref.watch(planningProvider).completed;
    if (completed.isEmpty) {
      return const Center(child: Text('Aucune tâche terminée.'));
    }
    return _TaskList(tasks: completed, urgent: false);
  }
}

// ── Liste de tâches commune ──────────────────────────────────────────────────
class _TaskList extends ConsumerWidget {
  final List<Plan> tasks;
  final bool urgent;

  const _TaskList({required this.tasks, required this.urgent});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: tasks.length,
      itemBuilder: (_, i) => _TaskCard(task: tasks[i]),
    );
  }
}

class _TaskCard extends ConsumerWidget {
  final Plan task;
  const _TaskCard({required this.task});

  static const _categoryIcons = {
    'study': Icons.school,
    'project': Icons.folder,
    'personal': Icons.person,
    'exam': Icons.quiz,
  };

  static const _priorityColors = {
    1: Colors.grey,
    2: Colors.blue,
    3: Colors.orange,
    4: Colors.red,
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isCompleted = task.isCompleted;
    final borderColor = task.isUrgent
        ? Colors.red
        : (_priorityColors[task.priority] ?? Colors.grey);

    return Dismissible(
      key: Key('task_${task.id}'),
      direction: DismissDirection.endToStart,
      background: Container(
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 16),
        color: Colors.red,
        child: const Icon(Icons.delete, color: Colors.white),
      ),
      onDismissed: (_) => ref.read(planningProvider.notifier).deleteTask(task.id),
      child: Card(
        margin: const EdgeInsets.only(bottom: 10),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
          side: BorderSide(color: borderColor.withOpacity(0.5), width: 1.5),
        ),
        child: ListTile(
          leading: Checkbox(
            value: isCompleted,
            onChanged: (_) =>
                ref.read(planningProvider.notifier).toggleComplete(task.id),
            activeColor: AppTheme.primaryColor,
          ),
          title: Text(
            task.title,
            style: TextStyle(
              decoration: isCompleted ? TextDecoration.lineThrough : null,
              color: isCompleted ? Colors.grey : null,
              fontWeight: FontWeight.w600,
            ),
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (task.description != null && task.description!.isNotEmpty)
                Text(task.description!, style: const TextStyle(fontSize: 12)),
              const SizedBox(height: 4),
              Row(children: [
                Icon(_categoryIcons[task.category] ?? Icons.label,
                    size: 13, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(_categoryLabel(task.category),
                    style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                const SizedBox(width: 12),
                Icon(Icons.calendar_today, size: 13, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(
                  _dueDateLabel(task),
                  style: TextStyle(
                    fontSize: 12,
                    color: task.isUrgent ? Colors.red : Colors.grey[600],
                    fontWeight: task.isUrgent ? FontWeight.bold : null,
                  ),
                ),
              ]),
            ],
          ),
          trailing: Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: borderColor.withOpacity(0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              _priorityLabel(task.priority),
              style: TextStyle(
                  fontSize: 11,
                  color: borderColor,
                  fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ),
    );
  }

  String _dueDateLabel(Plan task) {
    final days = task.daysLeft;
    if (task.isCompleted) return 'Terminé';
    if (days < 0) return 'En retard';
    if (days == 0) return "Aujourd'hui";
    if (days == 1) return 'Demain';
    return 'Dans $days jours';
  }

  String _categoryLabel(String cat) {
    const labels = {'study': 'Étude', 'project': 'Projet', 'personal': 'Personnel', 'exam': 'Examen'};
    return labels[cat] ?? cat;
  }

  String _priorityLabel(int p) {
    const labels = {1: 'Basse', 2: 'Normale', 3: 'Haute', 4: 'Urgente'};
    return labels[p] ?? 'P$p';
  }
}
