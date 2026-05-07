import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';

class RoadmapScreen extends StatelessWidget {
  const RoadmapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor,
      body: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              border: Border(
                bottom: BorderSide(color: theme.dividerColor, width: 1),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.rocket_launch_rounded,
                  size: 24,
                  color: theme.colorScheme.primary,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Planning',
                        style: theme.textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'Échéances, rappels et progression étudiante',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: theme.colorScheme.onSurface.withOpacity(0.6),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Content
          Expanded(
            child: Consumer2<IdeaProvider, BoardProvider>(
              builder: (context, ideaProvider, boardProvider, _) {
                final allIdeas = ideaProvider.ideas;
                final backlog = allIdeas
                    .where((i) => i['status'] == 'Backlog')
                    .length;
                final inProgress = allIdeas
                    .where((i) => i['status'] == 'In Progress')
                    .length;
                final done = allIdeas
                    .where((i) => i['status'] == 'Done')
                    .length;
                final total = allIdeas.length;
                final progress = total > 0 ? done / total : 0.0;

                // Get overdue and high priority tasks
                final now = DateTime.now();
                final overdueTasks = allIdeas.where((idea) {
                  if (idea['dueDate'] == null || idea['status'] == 'Done') {
                    return false;
                  }
                  return DateTime.parse(idea['dueDate']).isBefore(now);
                }).toList();

                final highPriorityTasks = allIdeas
                    .where(
                      (idea) =>
                          idea['priority'] == 2 && idea['status'] != 'Done',
                    )
                    .toList();

                return ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    // Progress Card
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: theme.colorScheme.primaryContainer,
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Icon(
                                    Icons.trending_up,
                                    color: theme.colorScheme.primary,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      const Text(
                                        'Progression Globale',
                                        style: TextStyle(
                                          fontSize: 20,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      Text(
                                        '$total tâches au total',
                                        style: TextStyle(
                                          color: theme.colorScheme.onSurface
                                              .withOpacity(0.6),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                Text(
                                  '${(progress * 100).toStringAsFixed(0)}%',
                                  style: TextStyle(
                                    fontSize: 36,
                                    fontWeight: FontWeight.bold,
                                    color: theme.colorScheme.primary,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 20),
                            ClipRRect(
                              borderRadius: BorderRadius.circular(10),
                              child: LinearProgressIndicator(
                                value: progress,
                                minHeight: 12,
                                backgroundColor:
                                    theme.colorScheme.surfaceVariant,
                                valueColor: AlwaysStoppedAnimation<Color>(
                                  theme.colorScheme.primary,
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),
                            Row(
                              children: [
                                Expanded(
                                  child: _StatCard(
                                    icon: Icons.inbox,
                                    label: 'À faire',
                                    value: backlog.toString(),
                                    color: Colors.blueGrey,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: _StatCard(
                                    icon: Icons.play_circle,
                                    label: 'En cours',
                                    value: inProgress.toString(),
                                    color: Colors.orange,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: _StatCard(
                                    icon: Icons.check_circle,
                                    label: 'Terminé',
                                    value: done.toString(),
                                    color: Colors.green,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Alerts Row
                    Row(
                      children: [
                        if (overdueTasks.isNotEmpty)
                          Expanded(
                            child: Card(
                              color: Colors.red.shade50,
                              child: Padding(
                                padding: const EdgeInsets.all(16),
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.warning_rounded,
                                      color: Colors.red.shade700,
                                      size: 32,
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            '${overdueTasks.length} tâche${overdueTasks.length > 1 ? "s" : ""} en retard',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.red.shade700,
                                            ),
                                          ),
                                          Text(
                                            'Nécessite votre attention',
                                            style: TextStyle(
                                              fontSize: 12,
                                              color: Colors.red.shade600,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                        if (overdueTasks.isNotEmpty &&
                            highPriorityTasks.isNotEmpty)
                          const SizedBox(width: 12),
                        if (highPriorityTasks.isNotEmpty)
                          Expanded(
                            child: Card(
                              color: Colors.orange.shade50,
                              child: Padding(
                                padding: const EdgeInsets.all(16),
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.priority_high_rounded,
                                      color: Colors.orange.shade700,
                                      size: 32,
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            '${highPriorityTasks.length} priorité haute',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.orange.shade700,
                                            ),
                                          ),
                                          Text(
                                            'À traiter rapidement',
                                            style: TextStyle(
                                              fontSize: 12,
                                              color: Colors.orange.shade600,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                      ],
                    ),

                    const SizedBox(height: 24),
                    // Vue trimestrielle
                    Text(
                      'Vue Trimestrielle',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: _QuarterOverview(
                          ideas: allIdeas,
                          progress: progress,
                        ),
                      ),
                    ),

                    const SizedBox(height: 24),
                    // Frise chronologique interactive (Roadmap avancée)
                    Text(
                      'Frise chronologique',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: _Timeline(allIdeas: allIdeas),
                      ),
                    ),

                    const SizedBox(height: 24),

                    // Top Voted Ideas (Votes Graph)
                    Text(
                      'Top idées par votes',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: FutureBuilder<List<Map<String, dynamic>>>(
                          future: ideaProvider.getTopVotedIdeas(limit: 5),
                          builder: (context, snapshot) {
                            if (snapshot.connectionState !=
                                ConnectionState.done) {
                              return const SizedBox(
                                height: 120,
                                child: Center(
                                  child: CircularProgressIndicator(),
                                ),
                              );
                            }
                            final items = snapshot.data ?? [];
                            if (items.isEmpty) {
                              return const Text('Aucune idée votée');
                            }

                            final maxVotes = items
                                .map((e) => (e['votes'] as int?) ?? 0)
                                .fold<int>(0, (prev, v) => v > prev ? v : prev);

                            return SizedBox(
                              height: 240,
                              child: BarChart(
                                BarChartData(
                                  alignment: BarChartAlignment.spaceAround,
                                  maxY: (maxVotes + 2).toDouble(),
                                  barTouchData: BarTouchData(enabled: true),
                                  gridData: FlGridData(show: true),
                                  titlesData: FlTitlesData(
                                    leftTitles: AxisTitles(
                                      sideTitles: SideTitles(showTitles: true),
                                    ),
                                    bottomTitles: AxisTitles(
                                      sideTitles: SideTitles(
                                        showTitles: true,
                                        getTitlesWidget: (value, meta) {
                                          final index = value.toInt();
                                          if (index < 0 ||
                                              index >= items.length)
                                            return const SizedBox();
                                          final title =
                                              (items[index]['title'] ?? '')
                                                  .toString();
                                          return Padding(
                                            padding: const EdgeInsets.only(
                                              top: 6,
                                            ),
                                            child: Text(
                                              title,
                                              style: const TextStyle(
                                                fontSize: 10,
                                              ),
                                              maxLines: 1,
                                              overflow: TextOverflow.ellipsis,
                                            ),
                                          );
                                        },
                                      ),
                                    ),
                                  ),
                                  borderData: FlBorderData(show: false),
                                  barGroups: List.generate(items.length, (i) {
                                    final v = (items[i]['votes'] as int?) ?? 0;
                                    return BarChartGroupData(
                                      x: i,
                                      barRods: [
                                        BarChartRodData(
                                          toY: v.toDouble(),
                                          color: theme.colorScheme.primary,
                                          width: 18,
                                          borderRadius: BorderRadius.circular(
                                            4,
                                          ),
                                        ),
                                      ],
                                    );
                                  }),
                                ),
                              ),
                            );
                          },
                        ),
                      ),
                    ),

                    const SizedBox(height: 24),

                    // Boards Progress
                    if (boardProvider.boards.isNotEmpty) ...[
                      Text(
                        'Progression par Tableau',
                        style: theme.textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      ...boardProvider.boards.map((board) {
                        final boardIdeas = allIdeas
                            .where((i) => i['boardId'] == board['id'])
                            .toList();
                        final boardDone = boardIdeas
                            .where((i) => i['status'] == 'Done')
                            .length;
                        final boardTotal = boardIdeas.length;
                        final boardProgress = boardTotal > 0
                            ? boardDone / boardTotal
                            : 0.0;

                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      Icons.view_column_rounded,
                                      color: theme.colorScheme.primary,
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Text(
                                        board['name'],
                                        style: const TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 16,
                                        ),
                                      ),
                                    ),
                                    Text(
                                      '$boardDone / $boardTotal',
                                      style: TextStyle(
                                        color: theme.colorScheme.primary,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 12),
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(8),
                                  child: LinearProgressIndicator(
                                    value: boardProgress,
                                    minHeight: 8,
                                    backgroundColor:
                                        theme.colorScheme.surfaceVariant,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      }),
                    ],
                  ],
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _StatCard({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 6),
          Text(
            value,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          Text(
            label,
            style: TextStyle(fontSize: 11, color: color),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}

class _Timeline extends StatefulWidget {
  final List<Map<String, dynamic>> allIdeas;
  const _Timeline({required this.allIdeas});

  @override
  State<_Timeline> createState() => _TimelineState();
}

class _TimelineState extends State<_Timeline> {
  int? _selectedIndex;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    // Trier par date d'échéance
    final items = widget.allIdeas.where((i) => i['dueDate'] != null).toList()
      ..sort(
        (a, b) => DateTime.parse(
          a['dueDate'],
        ).compareTo(DateTime.parse(b['dueDate'])),
      );

    if (items.isEmpty) {
      return const Text('Aucune échéance planifiée.');
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          height: 140,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            separatorBuilder: (_, __) => const SizedBox(width: 24),
            itemBuilder: (context, index) {
              final idea = items[index];
              final date = DateTime.parse(idea['dueDate']);
              final status = idea['status']?.toString() ?? 'Backlog';
              final priority = idea['priority'] ?? 1;
              final color = status == 'Done'
                  ? Colors.green
                  : status == 'In Progress'
                  ? Colors.orange
                  : Colors.blueGrey;
              final size = 14.0 + (priority * 6.0);
              final selected = _selectedIndex == index;

              return GestureDetector(
                onTap: () => setState(() => _selectedIndex = index),
                child: Column(
                  children: [
                    TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0, end: selected ? 1 : 0.6),
                      duration: const Duration(milliseconds: 300),
                      curve: Curves.easeOut,
                      builder: (context, value, child) {
                        return Opacity(opacity: value, child: child!);
                      },
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 300),
                        width: size,
                        height: size,
                        decoration: BoxDecoration(
                          color: color,
                          shape: BoxShape.circle,
                          boxShadow: [
                            if (selected)
                              BoxShadow(
                                color: color.withOpacity(0.4),
                                blurRadius: 12,
                                spreadRadius: 2,
                              ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '${date.day}/${date.month}',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    SizedBox(
                      width: 140,
                      child: Text(
                        idea['title'] ?? '',
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: theme.textTheme.bodySmall,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
        const SizedBox(height: 12),
        if (_selectedIndex != null)
          _TimelineDetail(idea: items[_selectedIndex!]),
      ],
    );
  }
}

class _TimelineDetail extends StatelessWidget {
  final Map<String, dynamic> idea;
  const _TimelineDetail({required this.idea});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final date = DateTime.tryParse(idea['dueDate'] ?? '');
    final status = idea['status'] ?? 'Backlog';
    final priority = idea['priority'] ?? 1;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceVariant,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            idea['title'] ?? '',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 6),
          Wrap(
            spacing: 12,
            children: [
              if (date != null)
                Row(
                  children: [
                    const Icon(Icons.event, size: 16),
                    const SizedBox(width: 4),
                    Text('${date.day}/${date.month}/${date.year}'),
                  ],
                ),
              Row(
                children: [
                  const Icon(Icons.label, size: 16),
                  const SizedBox(width: 4),
                  Text(status),
                ],
              ),
              Row(
                children: [
                  const Icon(Icons.flag, size: 16),
                  const SizedBox(width: 4),
                  Text(
                    priority == 2
                        ? 'Haute'
                        : priority == 1
                        ? 'Moyenne'
                        : 'Basse',
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 6),
          if ((idea['attachments'] ?? '').toString().isNotEmpty)
            Text('Pièces jointes disponibles'),
        ],
      ),
    );
  }
}

class _QuarterOverview extends StatelessWidget {
  final List<Map<String, dynamic>> ideas;
  final double progress;
  const _QuarterOverview({required this.ideas, required this.progress});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final now = DateTime.now();
    final quarterEnd = DateTime(now.year, now.month + 3, now.day);

    final upcoming = ideas.where((i) {
      final due = i['dueDate'] != null ? DateTime.tryParse(i['dueDate']) : null;
      return due != null && due.isAfter(now) && due.isBefore(quarterEnd);
    }).toList();

    final objectives = upcoming
        .where((i) => (i['priority'] ?? 1) == 2)
        .take(5)
        .toList();
    final features = upcoming
        .where(
          (i) => (i['tags'] ?? '').toString().toLowerCase().contains('feature'),
        )
        .take(5)
        .toList();
    final deadlines = upcoming.where((i) => i['dueDate'] != null).toList()
      ..sort(
        (a, b) => DateTime.parse(
          a['dueDate'],
        ).compareTo(DateTime.parse(b['dueDate'])),
      );

    return Column(
      children: [
        Column(
          children: [
            _QuarterList(
              title: 'Objectifs du trimestre',
              icon: Icons.flag,
              color: Colors.orange,
              items: objectives,
            ),
            const SizedBox(height: 12),
            _QuarterList(
              title: 'Fonctionnalités majeures',
              icon: Icons.auto_awesome,
              color: Colors.blue,
              items: features,
            ),
          ],
        ),
        const SizedBox(height: 12),
        Column(
          children: [
            _QuarterList(
              title: 'Échéances',
              icon: Icons.event,
              color: Colors.red,
              items: deadlines.take(8).toList(),
              subtitleBuilder: (i) {
                final d = DateTime.parse(i['dueDate']);
                return '${d.day}/${d.month}/${d.year}';
              },
            ),
            const SizedBox(height: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Text(
                  'Progression globale',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Center(
                  child: SizedBox(
                    height: 100,
                    width: 100,
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        CircularProgressIndicator(
                          value: progress,
                          strokeWidth: 8,
                          color: theme.colorScheme.primary,
                        ),
                        Text(
                          '${(progress * 100).toStringAsFixed(0)}%',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }
}

class _QuarterList extends StatelessWidget {
  final String title;
  final IconData icon;
  final Color color;
  final List<Map<String, dynamic>> items;
  final String Function(Map<String, dynamic>)? subtitleBuilder;

  const _QuarterList({
    required this.title,
    required this.icon,
    required this.color,
    required this.items,
    this.subtitleBuilder,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceVariant,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 18),
              const SizedBox(width: 6),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 13,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ...items.map(
            (i) => ListTile(
              dense: true,
              contentPadding: EdgeInsets.zero,
              leading: Icon(Icons.chevron_right, color: color),
              title: Text(i['title'] ?? ''),
              subtitle: subtitleBuilder != null
                  ? Text(subtitleBuilder!(i))
                  : null,
            ),
          ),
          if (items.isEmpty)
            Text('Aucun élément', style: theme.textTheme.bodySmall),
        ],
      ),
    );
  }
}
