import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';

class VoteButton extends StatelessWidget {
  final Map<String, dynamic> idea;

  const VoteButton({super.key, required this.idea});

  @override
  Widget build(BuildContext context) {
    final votes = (idea['votes'] as int?) ?? 0;
    final theme = Theme.of(context);

    return Consumer<IdeaProvider>(
      builder: (context, provider, _) {
        return Container(
          decoration: BoxDecoration(
            color: theme.colorScheme.primaryContainer.withOpacity(0.3),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Icon(Icons.thumb_up, size: 18),
                onPressed: () async {
                  try {
                    await provider.voteIdea(idea['id']);
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Row(
                            children: [
                              Icon(Icons.check_circle, color: Colors.white),
                              SizedBox(width: 8),
                              Text('Vote ajouté !'),
                            ],
                          ),
                          backgroundColor: Colors.green,
                          duration: Duration(seconds: 1),
                        ),
                      );
                    }
                  } catch (e) {
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Erreur: $e'),
                          backgroundColor: Colors.red,
                        ),
                      );
                    }
                  }
                },
                tooltip: 'Voter pour cette idée',
                padding: const EdgeInsets.all(8),
              ),
              Text(
                votes.toString(),
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: theme.colorScheme.primary,
                ),
              ),
              if (votes > 0)
                IconButton(
                  icon: const Icon(Icons.thumb_down, size: 18),
                  onPressed: () async {
                    try {
                      await provider.unvoteIdea(idea['id']);
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Row(
                              children: [
                                Icon(Icons.info, color: Colors.white),
                                SizedBox(width: 8),
                                Text('Vote retiré'),
                              ],
                            ),
                            backgroundColor: Colors.orange,
                            duration: Duration(seconds: 1),
                          ),
                        );
                      }
                    } catch (e) {
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Erreur: $e'),
                            backgroundColor: Colors.red,
                          ),
                        );
                      }
                    }
                  },
                  tooltip: 'Retirer votre vote',
                  padding: const EdgeInsets.all(8),
                ),
            ],
          ),
        );
      },
    );
  }
}
