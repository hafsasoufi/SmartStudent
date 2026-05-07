import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';
import '../widgets/quick_stats_widget.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Consumer2<IdeaProvider, BoardProvider>(
            builder: (context, ideaProvider, boardProvider, _) {
              final totalRequests = ideaProvider.ideas.length;
              final activeSpaces = boardProvider.boards.length;
              final overdue = ideaProvider.ideas.where((idea) {
                if (idea['dueDate'] == null || idea['status'] == 'Done') {
                  return false;
                }
                final dueDate = DateTime.tryParse(idea['dueDate']);
                return dueDate != null && dueDate.isBefore(DateTime.now());
              }).length;
              final completed = ideaProvider.ideas
                  .where((idea) => idea['status'] == 'Done')
                  .length;

              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          theme.colorScheme.primary,
                          theme.colorScheme.secondary,
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(24),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.white.withOpacity(0.16),
                                borderRadius: BorderRadius.circular(18),
                              ),
                              child: const Icon(
                                Icons.school_rounded,
                                color: Colors.white,
                                size: 28,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'SmartStudent',
                                    style: theme.textTheme.headlineMedium
                                        ?.copyWith(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold,
                                        ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'Plateforme agentique IA pour les étudiants en ingénierie et master',
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      color: Colors.white.withOpacity(0.9),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 20),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: const [
                            _HeroChip(label: 'Administratif'),
                            _HeroChip(label: 'Planning'),
                            _HeroChip(label: 'Révisions'),
                            _HeroChip(label: 'Orientation'),
                            _HeroChip(label: 'Campus'),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  GridView.count(
                    crossAxisCount: MediaQuery.of(context).size.width > 900
                        ? 4
                        : MediaQuery.of(context).size.width > 600
                        ? 2
                        : 1,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.9,
                    children: [
                      _MetricTile(
                        icon: Icons.bolt_rounded,
                        label: 'Demandes actives',
                        value: totalRequests.toString(),
                        color: Colors.indigo,
                      ),
                      _MetricTile(
                        icon: Icons.space_dashboard_rounded,
                        label: 'Espaces suivis',
                        value: activeSpaces.toString(),
                        color: Colors.teal,
                      ),
                      _MetricTile(
                        icon: Icons.error_outline_rounded,
                        label: 'Rappels urgents',
                        value: overdue.toString(),
                        color: Colors.orange,
                      ),
                      _MetricTile(
                        icon: Icons.check_circle_rounded,
                        label: 'Traités',
                        value: completed.toString(),
                        color: Colors.green,
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  Text(
                    'Vos modules SmartStudent',
                    style: theme.textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  GridView.count(
                    crossAxisCount: MediaQuery.of(context).size.width > 900
                        ? 3
                        : MediaQuery.of(context).size.width > 600
                        ? 2
                        : 1,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.45,
                    children: const [
                      _ModuleCard(
                        icon: Icons.description_rounded,
                        title: 'Administratif',
                        subtitle: 'FAQ, documents, demandes et suivi',
                      ),
                      _ModuleCard(
                        icon: Icons.calendar_month_rounded,
                        title: 'Planning',
                        subtitle: 'Emploi du temps, deadlines et rappels',
                      ),
                      _ModuleCard(
                        icon: Icons.quiz_rounded,
                        title: 'Examens & Révisions',
                        subtitle: 'Quiz génératifs, progression et feedback',
                      ),
                      _ModuleCard(
                        icon: Icons.work_outline_rounded,
                        title: 'Orientation',
                        subtitle: 'CV, lettres, stages et carrière',
                      ),
                      _ModuleCard(
                        icon: Icons.groups_rounded,
                        title: 'Vie de campus',
                        subtitle: 'Clubs, événements et groupes de travail',
                      ),
                      _ModuleCard(
                        icon: Icons.favorite_rounded,
                        title: 'Bien-être',
                        subtitle: 'Équilibre, accompagnement et routines',
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  Text(
                    'Activité récente',
                    style: theme.textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  const QuickStatsWidget(),
                ],
              );
            },
          ),
        ),
      ),
    );
  }
}

class _MetricTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _MetricTile({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: color.withOpacity(0.12),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Icon(icon, color: color),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    value,
                    style: theme.textTheme.headlineSmall?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: color,
                    ),
                  ),
                  Text(
                    label,
                    style: theme.textTheme.bodySmall,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ModuleCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;

  const _ModuleCard({
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: theme.colorScheme.primaryContainer.withOpacity(0.6),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Icon(icon, color: theme.colorScheme.primary),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: theme.colorScheme.onSurface.withOpacity(0.7),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HeroChip extends StatelessWidget {
  final String label;

  const _HeroChip({required this.label});

  @override
  Widget build(BuildContext context) {
    return Chip(
      label: Text(label, style: const TextStyle(color: Colors.white)),
      backgroundColor: Colors.white.withOpacity(0.16),
      side: BorderSide.none,
    );
  }
}
