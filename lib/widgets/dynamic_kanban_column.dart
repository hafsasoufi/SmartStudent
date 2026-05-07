import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';

class DynamicKanbanColumn extends StatefulWidget {
  final String title;
  final String subtitle;
  final Color color;
  final String status;
  final int boardId;
  final VoidCallback onAdd;
  final VoidCallback? onEdit;
  final VoidCallback? onDelete;
  final List<Map<String, dynamic>> Function(List<Map<String, dynamic>>)?
  filterIdeas;

  const DynamicKanbanColumn({
    super.key,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.status,
    required this.boardId,
    required this.onAdd,
    this.onEdit,
    this.onDelete,
    this.filterIdeas,
  });

  @override
  State<DynamicKanbanColumn> createState() => _DynamicKanbanColumnState();
}

class _DynamicKanbanColumnState extends State<DynamicKanbanColumn> {
  late final ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Color _getPriorityColor(int priority) {
    switch (priority) {
      case 2: // high
        return Colors.red;
      case 1: // medium
        return Colors.orange;
      case 0: // low
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  String _getPriorityLabel(int priority) {
    switch (priority) {
      case 2:
        return 'Haute';
      case 1:
        return 'Moyenne';
      case 0:
        return 'Basse';
      default:
        return 'Moyenne';
    }
  }

  IconData _getStatusIcon() {
    switch (widget.status) {
      case 'Backlog':
        return Icons.inbox;
      case 'In Progress':
        return Icons.play_circle;
      case 'Done':
        return Icons.check_circle;
      default:
        return Icons.dashboard;
    }
  }

  Widget _buildIdeaCard(
    BuildContext context,
    Map<String, dynamic> idea,
    ThemeData theme,
    IdeaProvider provider,
  ) {
    final priorityColor = _getPriorityColor(idea['priority'] ?? 0);
    final isOverdue =
        idea['dueDate'] != null &&
        DateTime.parse(idea['dueDate']).isBefore(DateTime.now()) &&
        idea['status'] != 'Done';

    final tags = idea['tags'] != null && idea['tags'].isNotEmpty
        ? (idea['tags'] as String).split(',')
        : <String>[];

    return GestureDetector(
      onVerticalDragUpdate: (details) {
        try {
          if (_scrollController.hasClients) {
            final newOffset = _scrollController.offset - details.delta.dy;
            final max = _scrollController.position.maxScrollExtent;
            final min = _scrollController.position.minScrollExtent;
            _scrollController.jumpTo(newOffset.clamp(min, max));
          }
        } catch (_) {}
      },
      child: LongPressDraggable<Map<String, dynamic>>(
        data: idea,
        feedback: Material(
          elevation: 8,
          borderRadius: BorderRadius.circular(12),
          child: Container(
            width: 250,
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: theme.colorScheme.primary, width: 2),
            ),
            child: Text(
              idea['title'] ?? 'Sans titre',
              style: theme.textTheme.titleSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        childWhenDragging: Opacity(
          opacity: 0.3,
          child: _buildCardContent(
            context,
            idea,
            theme,
            priorityColor,
            isOverdue,
            tags,
            provider,
          ),
        ),
        child: _buildCardContent(
          context,
          idea,
          theme,
          priorityColor,
          isOverdue,
          tags,
          provider,
        ),
      ),
    );
  }

  Widget _buildCardContent(
    BuildContext context,
    Map<String, dynamic> idea,
    ThemeData theme,
    Color priorityColor,
    bool isOverdue,
    List<String> tags,
    // provider is used for vote actions
    // pass the IdeaProvider from caller
    dynamic provider,
  ) {
    return Card(
      elevation: 1,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: isOverdue
            ? const BorderSide(color: Colors.red, width: 2)
            : BorderSide.none,
      ),
      child: InkWell(
        onTap: () => _showIdeaDetails(context, idea),
        borderRadius: BorderRadius.circular(10),
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      idea['title'] ?? 'Sans titre',
                      style: theme.textTheme.titleSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: priorityColor,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      _getPriorityLabel(idea['priority'] ?? 0),
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              if (idea['description'] != null &&
                  (idea['description'] as String).isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Text(
                    idea['description'],
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: theme.colorScheme.onSurface.withOpacity(0.7),
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              const SizedBox(height: 8),
              if (tags.isNotEmpty)
                Wrap(
                  spacing: 4,
                  runSpacing: 4,
                  children: tags.take(3).map((tag) {
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.secondaryContainer,
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        tag,
                        style: TextStyle(
                          fontSize: 9,
                          color: theme.colorScheme.onSecondaryContainer,
                        ),
                      ),
                    );
                  }).toList(),
                ),
              const SizedBox(height: 8),
              Row(
                children: [
                  if (idea['dueDate'] != null) ...[
                    Icon(
                      isOverdue ? Icons.warning_rounded : Icons.calendar_today,
                      size: 12,
                      color: isOverdue
                          ? Colors.red
                          : theme.colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      _formatDate(idea['dueDate']),
                      style: theme.textTheme.bodySmall?.copyWith(
                        fontSize: 10,
                        color: isOverdue ? Colors.red : null,
                      ),
                    ),
                  ] else ...[
                    Icon(
                      Icons.calendar_today,
                      size: 12,
                      color: theme.colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      idea['createdAt'] != null
                          ? _formatDate(idea['createdAt'])
                          : 'Aujourd\'hui',
                      style: theme.textTheme.bodySmall?.copyWith(fontSize: 10),
                    ),
                  ],
                  const Spacer(),
                  // Votes UI
                  Row(
                    children: [
                      GestureDetector(
                        onTap: () async {
                          try {
                            await provider.voteIdea(idea['id']);
                          } catch (_) {}
                        },
                        onLongPress: () async {
                          try {
                            await provider.unvoteIdea(idea['id']);
                          } catch (_) {}
                        },
                        child: Row(
                          children: [
                            Icon(
                              Icons.thumb_up,
                              size: 14,
                              color: theme.colorScheme.primary,
                            ),
                            const SizedBox(width: 4),
                          ],
                        ),
                      ),
                      Text(
                        (idea['votes'] as int? ?? 0).toString(),
                        style: theme.textTheme.bodySmall?.copyWith(
                          fontSize: 10,
                          color: theme.colorScheme.primary,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(width: 8),
                      if (_getAttachmentCount(idea['attachments']) > 0) ...[
                        Icon(
                          Icons.attach_file,
                          size: 12,
                          color: theme.colorScheme.primary,
                        ),
                        const SizedBox(width: 2),
                        Expanded(
                          child: Text(
                            _getAttachmentNames(idea['attachments']).join(', '),
                            style: theme.textTheme.bodySmall?.copyWith(
                              fontSize: 10,
                              color: theme.colorScheme.primary,
                              fontWeight: FontWeight.bold,
                            ),
                            overflow: TextOverflow.ellipsis,
                            maxLines: 1,
                          ),
                        ),
                      ],
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showIdeaDetails(BuildContext context, Map<String, dynamic> idea) {
    final provider = context.read<IdeaProvider>();

    showDialog(
      context: context,
      builder: (context) => _IdeaDetailDialog(idea: idea, provider: provider),
    );
  }

  String _formatDate(String dateStr) {
    try {
      final date = DateTime.parse(dateStr);
      final diff = DateTime.now().difference(date);
      if (diff.inDays == 0) return 'Aujourd\'hui';
      if (diff.inDays == 1) return 'Hier';
      if (diff.inDays < 7) return 'Il y a ${diff.inDays}j';
      if (diff.inDays < -1) return 'Dans ${-diff.inDays}j';
      return '${date.day}/${date.month}/${date.year}';
    } catch (e) {
      return 'Récent';
    }
  }

  int _getAttachmentCount(dynamic attachments) {
    // Robust handling: supports List, String(JSON), Map
    if (attachments == null) return 0;

    if (attachments is List) {
      return attachments.length;
    }

    final str = attachments.toString().trim();
    if (str.isEmpty || str == '[]') return 0;

    try {
      final decoded = jsonDecode(str);
      if (decoded is List) return decoded.length;
      if (decoded is Map) return 1; // single attachment as object
      return 0;
    } catch (_) {
      return 0;
    }
  }

  List<String> _getAttachmentNames(dynamic attachments) {
    if (attachments == null) return [];
    if (attachments is List) return attachments.map((e) => e.toString()).toList();
    final str = attachments.toString().trim();
    if (str.isEmpty || str == '[]') return [];
    try {
      final decoded = jsonDecode(str);
      if (decoded is List) return decoded.map((e) => e.toString()).toList();
      if (decoded is Map) return [decoded.toString()];
      return [str];
    } catch (_) {
      return [str];
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Consumer<IdeaProvider>(
      builder: (context, provider, child) {
        var ideas = provider.getIdeasByStatus(
          widget.status,
          boardId: widget.boardId,
        );

        // Apply filter if provided
        if (widget.filterIdeas != null) {
          ideas = widget.filterIdeas!(ideas);
        }

        // Trier les idées par priorité (décroissante: 2 haute -> 0 basse)
        try {
          ideas.sort(
            (a, b) => (b['priority'] ?? 0).compareTo(a['priority'] ?? 0),
          );
        } catch (_) {}

        return Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: theme.colorScheme.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: widget.color.withOpacity(0.3),
              width: 1.5,
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      widget.color.withOpacity(0.2),
                      widget.color.withOpacity(0.1),
                    ],
                  ),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(6),
                      decoration: BoxDecoration(
                        color: widget.color,
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Icon(
                        _getStatusIcon(),
                        color: Colors.white,
                        size: 16,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            widget.title,
                            style: theme.textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                              color: widget.color,
                            ),
                          ),
                          Text(
                            '${ideas.length} ${ideas.length > 1 ? "cartes" : "carte"}',
                            style: theme.textTheme.bodySmall?.copyWith(
                              color: theme.colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                    if (widget.onEdit != null || widget.onDelete != null)
                      PopupMenuButton(
                        icon: Icon(
                          Icons.more_vert,
                          size: 20,
                          color: theme.colorScheme.onSurface.withOpacity(0.6),
                        ),
                        itemBuilder: (context) => [
                          if (widget.onEdit != null)
                            PopupMenuItem(
                              onTap: widget.onEdit,
                              child: const Row(
                                children: [
                                  Icon(Icons.edit, size: 18),
                                  SizedBox(width: 8),
                                  Text('Modifier'),
                                ],
                              ),
                            ),
                          if (widget.onDelete != null)
                            PopupMenuItem(
                              onTap: widget.onDelete,
                              child: const Row(
                                children: [
                                  Icon(
                                    Icons.delete,
                                    size: 18,
                                    color: Colors.red,
                                  ),
                                  SizedBox(width: 8),
                                  Text(
                                    'Supprimer',
                                    style: TextStyle(color: Colors.red),
                                  ),
                                ],
                              ),
                            ),
                        ],
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 12),

              // Ideas List (scrollable per column)
              Expanded(
                child: ideas.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.inbox_outlined,
                              size: 48,
                              color: theme.colorScheme.outline.withOpacity(0.5),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Aucune carte',
                              style: theme.textTheme.bodyMedium?.copyWith(
                                color: theme.colorScheme.outline,
                              ),
                            ),
                          ],
                        ),
                      )
                    : Scrollbar(
                        controller: _scrollController,
                        thumbVisibility: true,
                        child: ListView.builder(
                          controller: _scrollController,
                          physics: const AlwaysScrollableScrollPhysics(),
                          itemCount: ideas.length,
                          itemBuilder: (context, index) {
                            final idea = ideas[index];
                            return Padding(
                              padding: const EdgeInsets.only(bottom: 6),
                              child: _buildIdeaCard(
                                context,
                                idea,
                                theme,
                                provider,
                              ),
                            );
                          },
                        ),
                      ),
              ),

              // Bouton ajouter
              const SizedBox(height: 8),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: widget.onAdd,
                  icon: const Icon(Icons.add_circle_outline, size: 16),
                  label: const Text('Ajouter', style: TextStyle(fontSize: 12)),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: widget.color,
                    side: BorderSide(color: widget.color, width: 1.5),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    padding: const EdgeInsets.symmetric(
                      vertical: 8,
                      horizontal: 12,
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

// Idea Detail Dialog
class _IdeaDetailDialog extends StatefulWidget {
  final Map<String, dynamic> idea;
  final IdeaProvider provider;

  const _IdeaDetailDialog({required this.idea, required this.provider});

  @override
  State<_IdeaDetailDialog> createState() => _IdeaDetailDialogState();
}

class _IdeaDetailDialogState extends State<_IdeaDetailDialog> {
  late TextEditingController _titleController;
  late TextEditingController _descriptionController;
  late TextEditingController _tagsController;
  late int _priority;
  DateTime? _dueDate;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.idea['title']);
    _descriptionController = TextEditingController(
      text: widget.idea['description'],
    );
    _priority = widget.idea['priority'] ?? 0;
    _dueDate = widget.idea['dueDate'] != null
        ? DateTime.parse(widget.idea['dueDate'])
        : null;

    final tags = widget.idea['tags'];
    _tagsController = TextEditingController(
      text: tags != null && tags.isNotEmpty ? tags : '',
    );
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    _tagsController.dispose();
    super.dispose();
  }

  Future<void> _selectDate() async {
    final date = await showDatePicker(
      context: context,
      initialDate: _dueDate ?? DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (date != null) {
      setState(() => _dueDate = date);
    }
  }

  void _save() async {
    final cardTitle = _titleController.text.trim();

    if (cardTitle.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              Icon(Icons.warning, color: Colors.white),
              SizedBox(width: 12),
              Text('Le titre ne peut pas être vide'),
            ],
          ),
          backgroundColor: Colors.orange,
          duration: Duration(seconds: 2),
        ),
      );
      return;
    }

    try {
      final boardProvider = Provider.of<BoardProvider>(context, listen: false);
      await widget.provider.updateIdea(widget.idea['id'], {
        'title': cardTitle,
        'description': _descriptionController.text.trim(),
        'priority': _priority,
        'dueDate': _dueDate?.toIso8601String(),
        'tags': _tagsController.text.trim(),
      }, boardProvider: boardProvider);

      if (context.mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Carte "$cardTitle" modifiée avec succès',
                    style: TextStyle(fontWeight: FontWeight.w500),
                  ),
                ),
              ],
            ),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 2),
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                Icon(Icons.error, color: Colors.white),
                SizedBox(width: 12),
                Expanded(child: Text('Erreur lors de la modification: $e')),
              ],
            ),
            backgroundColor: Colors.red,
            duration: Duration(seconds: 3),
          ),
        );
      }
    }
  }

  void _delete() {
    final cardTitle = widget.idea['title'] ?? 'cette carte';
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Supprimer la carte ?'),
        content: Text(
          'Voulez-vous vraiment supprimer "$cardTitle" ?\nCette action est irréversible.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Annuler'),
          ),
          FilledButton(
            onPressed: () async {
              try {
                final boardProvider = Provider.of<BoardProvider>(
                  context,
                  listen: false,
                );
                await widget.provider.deleteIdea(
                  widget.idea['id'],
                  boardProvider: boardProvider,
                );
                if (context.mounted) {
                  Navigator.pop(context); // Close confirmation
                  Navigator.pop(context); // Close detail dialog
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Row(
                        children: [
                          Icon(Icons.delete_outline, color: Colors.white),
                          SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              'Carte "$cardTitle" supprimée',
                              style: TextStyle(fontWeight: FontWeight.w500),
                            ),
                          ),
                        ],
                      ),
                      backgroundColor: Colors.orange.shade700,
                      duration: Duration(seconds: 3),
                      behavior: SnackBarBehavior.floating,
                    ),
                  );
                }
              } catch (e) {
                if (context.mounted) {
                  Navigator.pop(context);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Row(
                        children: [
                          Icon(Icons.error, color: Colors.white),
                          SizedBox(width: 12),
                          Text('Erreur lors de la suppression: $e'),
                        ],
                      ),
                      backgroundColor: Colors.red,
                      duration: Duration(seconds: 4),
                    ),
                  );
                }
              }
            },
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Supprimer'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Dialog(
      child: Container(
        width: 500,
        constraints: const BoxConstraints(maxHeight: 650),
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    'Modifier la carte',
                    style: theme.textTheme.headlineSmall,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const Divider(),
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    TextField(
                      controller: _titleController,
                      decoration: const InputDecoration(
                        labelText: 'Titre',
                        border: OutlineInputBorder(),
                      ),
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _descriptionController,
                      decoration: const InputDecoration(
                        labelText: 'Description',
                        border: OutlineInputBorder(),
                      ),
                      maxLines: 4,
                    ),
                    const SizedBox(height: 16),
                    Text('Priorité', style: theme.textTheme.titleSmall),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        ChoiceChip(
                          label: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.arrow_downward, size: 14),
                              SizedBox(width: 4),
                              Text('Basse', style: TextStyle(fontSize: 12)),
                            ],
                          ),
                          selected: _priority == 0,
                          onSelected: (selected) {
                            if (selected) setState(() => _priority = 0);
                          },
                        ),
                        ChoiceChip(
                          label: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.remove, size: 14),
                              SizedBox(width: 4),
                              Text('Moyenne', style: TextStyle(fontSize: 12)),
                            ],
                          ),
                          selected: _priority == 1,
                          onSelected: (selected) {
                            if (selected) setState(() => _priority = 1);
                          },
                        ),
                        ChoiceChip(
                          label: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.arrow_upward, size: 14),
                              SizedBox(width: 4),
                              Text('Haute', style: TextStyle(fontSize: 12)),
                            ],
                          ),
                          selected: _priority == 2,
                          onSelected: (selected) {
                            if (selected) setState(() => _priority = 2);
                          },
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Text('Date d\'échéance', style: theme.textTheme.titleSmall),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: _selectDate,
                            icon: const Icon(Icons.calendar_today),
                            label: Text(
                              _dueDate != null
                                  ? '${_dueDate!.day}/${_dueDate!.month}/${_dueDate!.year}'
                                  : 'Sélectionner une date',
                            ),
                          ),
                        ),
                        if (_dueDate != null) ...[
                          const SizedBox(width: 8),
                          IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () => setState(() => _dueDate = null),
                          ),
                        ],
                      ],
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _tagsController,
                      decoration: const InputDecoration(
                        labelText: 'Tags (séparés par des virgules)',
                        border: OutlineInputBorder(),
                        hintText: 'Ex: urgent, marketing, design',
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const Divider(),
            Row(
              children: [
                IconButton(
                  onPressed: _delete,
                  icon: const Icon(Icons.delete, color: Colors.red),
                  tooltip: 'Supprimer',
                ),
                const Spacer(),
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Annuler'),
                ),
                IconButton.filled(
                  onPressed: _save,
                  icon: const Icon(Icons.check),
                  tooltip: 'Enregistrer',
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
