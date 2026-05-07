import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';

/// Widget dynamique pour afficher des indicateurs rapides en temps réel
class QuickStatsWidget extends StatelessWidget {
  const QuickStatsWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Consumer2<IdeaProvider, BoardProvider>(
      builder: (context, ideaProvider, boardProvider, _) {
        final ideas = ideaProvider.ideas;
        final now = DateTime.now();

        // Calculs dynamiques

        return Card(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Espaces actifs',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Builder(
                  builder: (context) {
                    final boardIdsWithIdeas = ideas
                        .map((i) => i['boardId'])
                        .toSet();
                    final activeBoards = boardProvider.boards
                        .where((b) => boardIdsWithIdeas.contains(b['id']))
                        .toList();
                    if (activeBoards.isEmpty) {
                      return Text(
                        'Aucun espace actif',
                        style: theme.textTheme.bodySmall,
                      );
                    }
                    return Wrap(
                      spacing: 8,
                      runSpacing: 6,
                      children: activeBoards.map((b) {
                        final count = ideas
                            .where((i) => i['boardId'] == b['id'])
                            .length;
                        return Chip(
                          label: Text(
                            '${b['name']} ($count)',
                            style: theme.textTheme.bodySmall,
                          ),
                          backgroundColor: theme.colorScheme.surfaceVariant,
                        );
                      }).toList(),
                    );
                  },
                ),

                const SizedBox(height: 12),
                Text(
                  'Activité récente',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Builder(
                  builder: (context) {
                    List<Map<String, dynamic>> recent = List.from(ideas);
                    recent.sort((a, b) {
                      final ta =
                          DateTime.tryParse(
                            a['updatedAt'] ?? a['createdAt'] ?? '',
                          ) ??
                          DateTime.fromMillisecondsSinceEpoch(0);
                      final tb =
                          DateTime.tryParse(
                            b['updatedAt'] ?? b['createdAt'] ?? '',
                          ) ??
                          DateTime.fromMillisecondsSinceEpoch(0);
                      return tb.compareTo(ta);
                    });
                    recent = recent.take(5).toList();
                    if (recent.isEmpty)
                      return Text(
                        'Aucune activité récente',
                        style: theme.textTheme.bodySmall,
                      );
                    return Column(
                      children: recent.map((it) {
                        final when =
                            DateTime.tryParse(
                              it['updatedAt'] ?? it['createdAt'] ?? '',
                            ) ??
                            DateTime.now();
                        final ago = _timeAgo(now.difference(when));
                        final attachments = _parseAttachmentNames(
                          it['attachments'],
                        );
                        return ListTile(
                          dense: true,
                          contentPadding: EdgeInsets.zero,
                          leading: Icon(
                            Icons.auto_awesome,
                            size: 20,
                            color: theme.colorScheme.primary,
                          ),
                          title: Text(
                            it['title'] ?? 'Sans titre',
                            style: theme.textTheme.bodySmall,
                          ),
                          subtitle: Row(
                            children: [
                              Text(ago, style: theme.textTheme.labelSmall),
                              if (attachments.isNotEmpty) ...[
                                const SizedBox(width: 8),
                                Icon(Icons.attach_file, size: 14),
                                const SizedBox(width: 4),
                                Flexible(
                                  child: Text(
                                    attachments.first,
                                    style: theme.textTheme.labelSmall,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                              ],
                            ],
                          ),
                        );
                      }).toList(),
                    );
                  },
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

// Helpers
List<String> _parseAttachmentNames(dynamic attachments) {
  if (attachments == null) return [];
  try {
    if (attachments is List) {
      return attachments.map((e) => e.toString()).toList();
    }
    final s = attachments.toString();
    if (s.trim().isEmpty) return [];
    final decoded = s.trim().startsWith('[') ? (jsonDecode(s) as List?) : null;
    if (decoded != null) return decoded.map((e) => e.toString()).toList();
    return [s];
  } catch (_) {
    return [attachments.toString()];
  }
}

String _timeAgo(Duration diff) {
  if (diff.inSeconds < 60) return '${diff.inSeconds}s';
  if (diff.inMinutes < 60) return '${diff.inMinutes}m';
  if (diff.inHours < 24) return '${diff.inHours}h';
  if (diff.inDays < 30) return '${diff.inDays}j';
  return '${(diff.inDays / 30).floor()}mois';
}
