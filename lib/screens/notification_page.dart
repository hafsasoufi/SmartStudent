import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';

class NotificationPage extends StatelessWidget {
  final int? boardId;
  final String? boardName;

  const NotificationPage({super.key, this.boardId, this.boardName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          boardName != null ? 'Notifications - $boardName' : 'Notifications',
        ),
      ),
      body: Consumer<IdeaProvider>(
        builder: (context, provider, _) {
          final activities = boardId != null
              ? provider.activityLog
                    .where((log) => log.contains('Tableau: $boardId'))
                    .toList()
              : provider.activityLog;

          final ideas = boardId != null
              ? provider.getIdeasByBoard(boardId!)
              : provider.ideas;

          final highPriority = ideas
              .where((i) => i['priority'] == 'Haute')
              .length;
          final completed = ideas.where((i) => i['status'] == 'Done').length;
          final total = ideas.length;
          final completionRate = total > 0
              ? (completed / total * 100).toStringAsFixed(0)
              : '0';

          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              if (highPriority > 0)
                Card(
                  color: Colors.red.shade50,
                  child: ListTile(
                    leading: const Icon(Icons.warning, color: Colors.red),
                    title: Text('$highPriority tâches en priorité haute'),
                  ),
                ),
              if (completed > 0 && total > 0)
                Card(
                  color: Colors.green.shade50,
                  child: ListTile(
                    leading: const Icon(
                      Icons.check_circle,
                      color: Colors.green,
                    ),
                    title: Text(
                      'Vous avez terminé $completionRate% de vos objectifs',
                    ),
                  ),
                ),
              const SizedBox(height: 16),
              const Text(
                'Activité récente:',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              ...activities.map(
                (activity) => Card(child: ListTile(title: Text(activity))),
              ),
            ],
          );
        },
      ),
    );
  }
}
