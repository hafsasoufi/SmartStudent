import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:convert';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';
import '../providers/auth_provider.dart';
import '../widgets/dynamic_kanban_column.dart';
import '../widgets/add_idea_dialog.dart';
import '../models/kanban_column.dart';
import '../services/database_service.dart';

class KanbanPageDynamic extends StatefulWidget {
  final int? boardId;
  final String? boardName;

  const KanbanPageDynamic({super.key, this.boardId, this.boardName});

  @override
  State<KanbanPageDynamic> createState() => _KanbanPageDynamicState();
}

class _KanbanPageDynamicState extends State<KanbanPageDynamic> {
  final TextEditingController _searchController = TextEditingController();
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<IdeaProvider>().fetchIdeas();
      context.read<BoardProvider>().fetchColumns();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  List<Map<String, dynamic>> _filterIdeas(List<Map<String, dynamic>> ideas) {
    if (_searchQuery.isEmpty) return ideas;

    final query = _searchQuery.toLowerCase();
    return ideas.where((idea) {
      final title = (idea['title'] as String? ?? '').toLowerCase();
      final description = (idea['description'] as String? ?? '').toLowerCase();
      final tags = (idea['tags'] as String? ?? '').toLowerCase();

      return title.contains(query) ||
          description.contains(query) ||
          tags.contains(query);
    }).toList();
  }

  void _addColumn() {
    if (widget.boardId == null) return;

    final titleController = TextEditingController();
    final statusController = TextEditingController();
    Color selectedColor = Colors.blue;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Nouvelle Colonne'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: titleController,
                decoration: const InputDecoration(
                  labelText: 'Titre de la colonne',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: statusController,
                decoration: const InputDecoration(
                  labelText: 'Statut (ex: To Do)',
                  border: OutlineInputBorder(),
                  hintText: 'Unique pour ce tableau',
                ),
              ),
              const SizedBox(height: 16),
              const Text('Couleur:'),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                children:
                    [
                      Colors.blue,
                      Colors.green,
                      Colors.orange,
                      Colors.red,
                      Colors.purple,
                      Colors.teal,
                      Colors.indigo,
                      Colors.pink,
                    ].map((color) {
                      return ChoiceChip(
                        label: Container(
                          width: 30,
                          height: 30,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                          ),
                        ),
                        selected: selectedColor == color,
                        onSelected: (_) {
                          setState(() {
                            selectedColor = color;
                          });
                        },
                      );
                    }).toList(),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Annuler'),
            ),
              FilledButton(
              onPressed: () async {
                if (titleController.text.isNotEmpty &&
                    statusController.text.isNotEmpty) {
                  final authProvider = context.read<AuthProvider>();
                  final userId = authProvider.userId;

                  if (userId == null) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Vous devez être connecté')),
                    );
                    return;
                  }

                  final boardProvider = context.read<BoardProvider>();
                  final ideaProvider = context.read<IdeaProvider>();

                  await boardProvider.addColumn(
                    KanbanColumn(
                      userId: userId.toString(), // <-- force en String
                      boardId: widget.boardId!,
                      title: titleController.text,
                      status: statusController.text,
                      color: selectedColor,
                      position: boardProvider.columns.length,
                    ).toMap(),
                  );

                  // Refresh ideas and update shared board JSON if needed
                  await ideaProvider.fetchIdeas();
                  await boardProvider.refreshSharedBoardIfNeeded(
                    widget.boardId!,
                    ideaProvider.getIdeasByBoard(widget.boardId!),
                  );

                  Navigator.pop(context);
                }
              },
              child: const Text('Ajouter'),
            ),
          ],
        ),
      ),
    );
  }

  void _editColumn(Map<String, dynamic> column) {
    final titleController = TextEditingController(text: column['title']);
    Color selectedColor = Color(column['color']);

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Modifier la Colonne'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: titleController,
                decoration: const InputDecoration(
                  labelText: 'Titre de la colonne',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              const Text('Couleur:'),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                children:
                    [
                      Colors.blue,
                      Colors.green,
                      Colors.orange,
                      Colors.red,
                      Colors.purple,
                      Colors.teal,
                      Colors.indigo,
                      Colors.pink,
                    ].map((color) {
                      return ChoiceChip(
                        label: Container(
                          width: 30,
                          height: 30,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                          ),
                        ),
                        selected: selectedColor == color,
                        onSelected: (_) {
                          setState(() {
                            selectedColor = color;
                          });
                        },
                      );
                    }).toList(),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Annuler'),
            ),
              FilledButton(
              onPressed: () async {
                if (titleController.text.isNotEmpty) {
                  final boardProvider = context.read<BoardProvider>();
                  final ideaProvider = context.read<IdeaProvider>();

                  await boardProvider.updateColumn(column['id'], {
                    'title': titleController.text,
                    'color': selectedColor.value,
                  });

                  await ideaProvider.fetchIdeas();
                  await boardProvider.refreshSharedBoardIfNeeded(
                    widget.boardId!,
                    ideaProvider.getIdeasByBoard(widget.boardId!),
                  );

                  Navigator.pop(context);
                }
              },
              child: const Text('Enregistrer'),
            ),
          ],
        ),
      ),
    );
  }

  void _deleteColumn(Map<String, dynamic> column) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Supprimer la colonne ?'),
        content: Text(
          'Les cartes de "${column['title']}" seront déplacées vers la première colonne.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Annuler'),
          ),
          FilledButton(
            onPressed: () async {
              final boardProvider = context.read<BoardProvider>();
              final ideaProvider = context.read<IdeaProvider>();

              await boardProvider.deleteColumn(column['id']);
              await ideaProvider.fetchIdeas();
              await boardProvider.refreshSharedBoardIfNeeded(
                widget.boardId!,
                ideaProvider.getIdeasByBoard(widget.boardId!),
              );

              Navigator.pop(context);
            },
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Supprimer'),
          ),
        ],
      ),
    );
  }

  void _addNewIdea(String status) {
    showDialog(
      context: context,
      builder: (context) =>
          AddIdeaDialog(initialStatus: status, boardId: widget.boardId ?? 1),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final boardProvider = context.watch<BoardProvider>();
    final columns = boardProvider.columns;

    if (widget.boardId == null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.view_kanban_outlined,
              size: 64,
              color: theme.colorScheme.onSurface.withOpacity(0.3),
            ),
            const SizedBox(height: 16),
            Text(
              'Sélectionnez un tableau',
              style: theme.textTheme.headlineSmall?.copyWith(
                color: theme.colorScheme.onSurface.withOpacity(0.6),
              ),
            ),
          ],
        ),
      );
    }

    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor,
      body: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              border: Border(
                bottom: BorderSide(color: theme.dividerColor, width: 1),
              ),
            ),
            child: Column(
              children: [
                Row(
                  children: [
                    Icon(
                      Icons.view_kanban_rounded,
                      size: 32,
                      color: theme.colorScheme.primary,
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            widget.boardName ?? 'Kanban Board',
                            style: theme.textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            '${columns.length} colonnes',
                            style: theme.textTheme.bodyMedium?.copyWith(
                              color: theme.colorScheme.onSurface.withOpacity(
                                0.6,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Row(
                      children: [
                        IconButton(
                          onPressed: () async {
                            final emailController = TextEditingController();
                            final ok = await showDialog<bool>(
                              context: context,
                              builder: (context) => AlertDialog(
                                title: const Text('Partager le tableau'),
                                content: TextField(
                                  controller: emailController,
                                  decoration: const InputDecoration(
                                    labelText: 'Email de la personne',
                                  ),
                                  keyboardType: TextInputType.emailAddress,
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(context, false),
                                    child: const Text('Annuler'),
                                  ),
                                  FilledButton(
                                    onPressed: () => Navigator.pop(context, true),
                                    child: const Text('Partager'),
                                  ),
                                ],
                              ),
                            );
                            if (!mounted || ok != true) return;
                            final email = emailController.text.trim();
                            if (email.isEmpty) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Email requis')),
                              );
                              return;
                            }

                            try {
                              final db = DBService();
                              final boardProvider = context.read<BoardProvider>();
                              final ideaProvider = context.read<IdeaProvider>();
                              final authProvider = context.read<AuthProvider>();

                              final board = boardProvider.boards.firstWhere(
                                (b) => b['id'] == widget.boardId,
                                orElse: () => {'name': widget.boardName ?? 'Board'},
                              );

                              // Ensure latest ideas are loaded
                              await ideaProvider.fetchIdeas();

                              // Fetch the owner's columns from DB to include default columns
                              List<Map<String, dynamic>> ownerColumns = [];
                              if (widget.boardId != null && authProvider.userId != null) {
                                ownerColumns = await db.getColumnsByBoard(widget.boardId!, authProvider.userId!);
                              }

                              // Get ideas for this board
                              final ideas = ideaProvider.getIdeasByBoard(widget.boardId ?? -1);

                              // Log the sharing payload for debugging
                              print('📤 SHARING: Board=${board['name']}, Columns=${ownerColumns.length}, Ideas=${ideas.length}');
                              print('   Columns: ${ownerColumns.map((c) => c['title']).toList()}');
                              print('   Ideas: ${ideas.map((i) => i['title']).toList()}');

                              final payload = {
                                'board': board,
                                'columns': ownerColumns,
                                'ideas': ideas,
                              };

                              final boardJson = jsonEncode(payload);
                              print('   JSON length: ${boardJson.length} chars');
                              await db.addSharedBoard(widget.boardId ?? 0, boardJson, email);

                              // Register sync link
                              if (authProvider.userId != null) {
                                await db.addSharedBoardSync(
                                  widget.boardId ?? 0,
                                  authProvider.userId!.toString(),
                                  email,
                                  0, // Will be filled when recipient imports
                                );
                              }

                              if (!mounted) return;
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Tableau partagé')),
                              );
                            } catch (e) {
                              if (!mounted) return;
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text('Erreur: $e')),
                              );
                            }
                          },
                          icon: const Icon(Icons.share),
                          tooltip: 'Partager',
                        ),
                        FilledButton.icon(
                          onPressed: _addColumn,
                          icon: const Icon(Icons.add),
                          label: const Text('Nouvelle colonne'),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                // Search Bar
                TextField(
                  controller: _searchController,
                  onChanged: (value) {
                    setState(() {
                      _searchQuery = value;
                    });
                  },
                  decoration: InputDecoration(
                    hintText: 'Rechercher par titre, description ou tags...',
                    prefixIcon: Icon(
                      Icons.search,
                      color: theme.colorScheme.primary,
                    ),
                    suffixIcon: _searchQuery.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              setState(() {
                                _searchController.clear();
                                _searchQuery = '';
                              });
                            },
                          )
                        : null,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: theme.colorScheme.surfaceContainerHighest
                        .withOpacity(0.3),
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Kanban Columns
          Expanded(
            child: columns.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.view_column_outlined,
                          size: 64,
                          color: theme.colorScheme.onSurface.withOpacity(0.3),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Aucune colonne',
                          style: theme.textTheme.headlineSmall?.copyWith(
                            color: theme.colorScheme.onSurface.withOpacity(0.6),
                          ),
                        ),
                        const SizedBox(height: 8),
                        FilledButton.icon(
                          onPressed: _addColumn,
                          icon: const Icon(Icons.add),
                          label: const Text('Créer une colonne'),
                        ),
                      ],
                    ),
                  )
                : Consumer<IdeaProvider>(
                    builder: (context, provider, child) {
                      return ListView(
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.all(16),
                        children: columns.map((columnData) {
                          return Container(
                            width: 280,
                            margin: const EdgeInsets.only(right: 12),
                            child: DragTarget<Map<String, dynamic>>(
                              onWillAcceptWithDetails: (details) {
                                final idea = details.data;
                                return idea['status'] != columnData['status'];
                              },
                              onAcceptWithDetails: (details) async {
                                final idea = details.data;
                                final cardTitle = idea['title'] ?? 'Carte';
                                final newStatus = columnData['status'];

                                try {
                                  final boardProvider = context.read<BoardProvider>();
                                  await provider.updateIdeaStatus(
                                    idea['id'],
                                    newStatus,
                                    boardProvider: boardProvider,
                                  );

                                  if (context.mounted) {
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      SnackBar(
                                        content: Row(
                                          children: [
                                            Icon(
                                              Icons.check_circle_outline,
                                              color: Colors.white,
                                            ),
                                            SizedBox(width: 12),
                                            Expanded(
                                              child: Text(
                                                '"$cardTitle" → $newStatus',
                                                style: TextStyle(
                                                  fontWeight: FontWeight.w500,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                        backgroundColor: Colors.blue.shade700,
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
                                            Icon(
                                              Icons.error,
                                              color: Colors.white,
                                            ),
                                            SizedBox(width: 12),
                                            Text('Erreur: $e'),
                                          ],
                                        ),
                                        backgroundColor: Colors.red,
                                      ),
                                    );
                                  }
                                }
                              },
                              builder: (context, candidateData, rejectedData) {
                                final isHighlighted = candidateData.isNotEmpty;
                                return AnimatedContainer(
                                  duration: const Duration(milliseconds: 200),
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(16),
                                    border: isHighlighted
                                        ? Border.all(
                                            color: theme.colorScheme.primary,
                                            width: 2,
                                          )
                                        : null,
                                  ),
                                  child: DynamicKanbanColumn(
                                    title: columnData['title'],
                                    subtitle: columnData['status'],
                                    color: Color(columnData['color']),
                                    status: columnData['status'],
                                    boardId: widget.boardId!,
                                    filterIdeas: _filterIdeas,
                                    onAdd: () =>
                                        _addNewIdea(columnData['status']),
                                    onEdit: () => _editColumn(columnData),
                                    onDelete: columns.length > 1
                                        ? () => _deleteColumn(columnData)
                                        : null,
                                  ),
                                );
                              },
                            ),
                          );
                        }).toList(),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
