import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';

class StatisticsScreen extends StatelessWidget {
  const StatisticsScreen({super.key});

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
                  Icons.bar_chart_rounded,
                  size: 24,
                  color: theme.colorScheme.primary,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Révisions',
                        style: theme.textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'Suivi de progression, quiz et performance',
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

                // Calculs pour graphiques
                final statusCounts = {
                  'Backlog': backlog,
                  'In Progress': inProgress,
                  'Done': done,
                };

                final priorityCounts = {
                  0: allIdeas.where((i) => i['priority'] == 0).length,
                  1: allIdeas.where((i) => i['priority'] == 1).length,
                  2: allIdeas.where((i) => i['priority'] == 2).length,
                };

                // Activité sur 7 jours
                final today = DateTime.now();
                List<int> last7DaysCounts = List.generate(7, (index) {
                  final day = DateTime(
                    today.year,
                    today.month,
                    today.day - (6 - index),
                  );
                  return allIdeas.where((idea) {
                    DateTime? created;
                    DateTime? updated;
                    if (idea['createdAt'] != null) {
                      created = DateTime.tryParse(idea['createdAt']);
                    }
                    if (idea['updatedAt'] != null) {
                      updated = DateTime.tryParse(idea['updatedAt']);
                    }
                    bool sameDay(DateTime d) =>
                        d.year == day.year &&
                        d.month == day.month &&
                        d.day == day.day;
                    return (created != null && sameDay(created)) ||
                        (updated != null && sameDay(updated));
                  }).length;
                });

                if (total == 0) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.analytics_outlined,
                          size: 80,
                          color: theme.colorScheme.onSurface.withOpacity(0.3),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Aucune donnée disponible',
                          style: theme.textTheme.titleLarge?.copyWith(
                            color: theme.colorScheme.onSurface.withOpacity(0.6),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Créez des cartes pour voir les statistiques',
                          style: theme.textTheme.bodyMedium?.copyWith(
                            color: theme.colorScheme.onSurface.withOpacity(0.5),
                          ),
                        ),
                      ],
                    ),
                  );
                }

                return ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    // Vue d'ensemble
                    Row(
                      children: [
                        Expanded(
                          child: _MetricCard(
                            icon: Icons.task,
                            label: 'Total des tâches',
                            value: total.toString(),
                            color: Colors.blue,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: _MetricCard(
                            icon: Icons.check_circle,
                            label: 'Terminées',
                            value: done.toString(),
                            color: Colors.green,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: _MetricCard(
                            icon: Icons.trending_up,
                            label: 'Progression',
                            value:
                                '${total > 0 ? ((done / total) * 100).toStringAsFixed(0) : 0}%',
                            color: Colors.orange,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

                    // Graphiques
                    Text(
                      'Répartition des tâches',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Répartition des statuts (camembert)
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Par statut',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                  ),
                                ),
                                const SizedBox(height: 12),
                                SizedBox(
                                  height: 180,
                                  child: PieChart(
                                    PieChartData(
                                      sectionsSpace: 2,
                                      centerSpaceRadius: 40,
                                      sections: [
                                        PieChartSectionData(
                                          color: Colors.blueGrey,
                                          value: statusCounts['Backlog']!
                                              .toDouble(),
                                          title: '${statusCounts['Backlog']}',
                                          radius: 50,
                                          titleStyle: const TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                          ),
                                        ),
                                        PieChartSectionData(
                                          color: Colors.orange,
                                          value: statusCounts['In Progress']!
                                              .toDouble(),
                                          title:
                                              '${statusCounts['In Progress']}',
                                          radius: 50,
                                          titleStyle: const TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                          ),
                                        ),
                                        PieChartSectionData(
                                          color: Colors.green,
                                          value: statusCounts['Done']!
                                              .toDouble(),
                                          title: '${statusCounts['Done']}',
                                          radius: 50,
                                          titleStyle: const TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 12),
                                _Legend(
                                  items: [
                                    LegendItem(
                                      'Backlog',
                                      Colors.blueGrey,
                                      statusCounts['Backlog']!,
                                    ),
                                    LegendItem(
                                      'En cours',
                                      Colors.orange,
                                      statusCounts['In Progress']!,
                                    ),
                                    LegendItem(
                                      'Terminé',
                                      Colors.green,
                                      statusCounts['Done']!,
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 12),
                        // Répartition des priorités (barres)
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Par priorité',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                  ),
                                ),
                                const SizedBox(height: 12),
                                SizedBox(
                                  height: 180,
                                  child: BarChart(
                                    BarChartData(
                                      titlesData: FlTitlesData(
                                        rightTitles: const AxisTitles(
                                          sideTitles: SideTitles(
                                            showTitles: false,
                                          ),
                                        ),
                                        topTitles: const AxisTitles(
                                          sideTitles: SideTitles(
                                            showTitles: false,
                                          ),
                                        ),
                                        bottomTitles: AxisTitles(
                                          sideTitles: SideTitles(
                                            showTitles: true,
                                            getTitlesWidget: (value, meta) {
                                              switch (value.toInt()) {
                                                case 0:
                                                  return const Text('Basse');
                                                case 1:
                                                  return const Text('Moyenne');
                                                case 2:
                                                  return const Text('Haute');
                                              }
                                              return const SizedBox.shrink();
                                            },
                                          ),
                                        ),
                                        leftTitles: AxisTitles(
                                          sideTitles: SideTitles(
                                            showTitles: true,
                                          ),
                                        ),
                                      ),
                                      borderData: FlBorderData(show: false),
                                      gridData: FlGridData(
                                        show: true,
                                        drawVerticalLine: false,
                                      ),
                                      barGroups: [
                                        BarChartGroupData(
                                          x: 0,
                                          barRods: [
                                            BarChartRodData(
                                              toY: priorityCounts[0]!
                                                  .toDouble(),
                                              color: Colors.blue,
                                              width: 40,
                                              borderRadius:
                                                  const BorderRadius.vertical(
                                                    top: Radius.circular(6),
                                                  ),
                                            ),
                                          ],
                                        ),
                                        BarChartGroupData(
                                          x: 1,
                                          barRods: [
                                            BarChartRodData(
                                              toY: priorityCounts[1]!
                                                  .toDouble(),
                                              color: Colors.orange,
                                              width: 40,
                                              borderRadius:
                                                  const BorderRadius.vertical(
                                                    top: Radius.circular(6),
                                                  ),
                                            ),
                                          ],
                                        ),
                                        BarChartGroupData(
                                          x: 2,
                                          barRods: [
                                            BarChartRodData(
                                              toY: priorityCounts[2]!
                                                  .toDouble(),
                                              color: Colors.red,
                                              width: 40,
                                              borderRadius:
                                                  const BorderRadius.vertical(
                                                    top: Radius.circular(6),
                                                  ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 12),
                    // Activité récente (ligne)
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Activité récente (7 derniers jours)',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                            const SizedBox(height: 12),
                            SizedBox(
                              height: 200,
                              child: LineChart(
                                LineChartData(
                                  titlesData: FlTitlesData(
                                    rightTitles: const AxisTitles(
                                      sideTitles: SideTitles(showTitles: false),
                                    ),
                                    topTitles: const AxisTitles(
                                      sideTitles: SideTitles(showTitles: false),
                                    ),
                                    bottomTitles: AxisTitles(
                                      sideTitles: SideTitles(
                                        showTitles: true,
                                        getTitlesWidget: (value, meta) {
                                          final idx = value.toInt();
                                          if (idx < 0 || idx > 6) {
                                            return const SizedBox.shrink();
                                          }
                                          final d = DateTime(
                                            today.year,
                                            today.month,
                                            today.day - (6 - idx),
                                          );
                                          return Text('${d.day}/${d.month}');
                                        },
                                      ),
                                    ),
                                    leftTitles: AxisTitles(
                                      sideTitles: SideTitles(showTitles: true),
                                    ),
                                  ),
                                  borderData: FlBorderData(show: false),
                                  gridData: FlGridData(
                                    show: true,
                                    drawVerticalLine: false,
                                  ),
                                  lineBarsData: [
                                    LineChartBarData(
                                      spots: List.generate(
                                        7,
                                        (i) => FlSpot(
                                          i.toDouble(),
                                          last7DaysCounts[i].toDouble(),
                                        ),
                                      ),
                                      isCurved: true,
                                      color: theme.colorScheme.primary,
                                      barWidth: 3,
                                      dotData: const FlDotData(show: true),
                                      belowBarData: BarAreaData(
                                        show: true,
                                        color: theme.colorScheme.primary
                                            .withOpacity(0.1),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                    const SizedBox(height: 24),

                    // Statistiques par tableau
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

class _MetricCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _MetricCard({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            Text(
              label,
              style: const TextStyle(fontSize: 12),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

class LegendItem {
  final String label;
  final Color color;
  final int value;

  LegendItem(this.label, this.color, this.value);
}

class _Legend extends StatelessWidget {
  final List<LegendItem> items;

  const _Legend({required this.items});

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 16,
      runSpacing: 8,
      children: items.map((item) {
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 12,
              height: 12,
              decoration: BoxDecoration(
                color: item.color,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(width: 6),
            Text(
              '${item.label} (${item.value})',
              style: const TextStyle(fontSize: 12),
            ),
          ],
        );
      }).toList(),
    );
  }
}
