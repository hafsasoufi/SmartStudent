import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/idea_provider.dart';
import '../providers/board_provider.dart';
import '../providers/auth_provider.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:convert';

class AddIdeaDialog extends StatefulWidget {
  final String? initialStatus;
  final int? boardId;

  const AddIdeaDialog({super.key, this.initialStatus, this.boardId});

  @override
  State<AddIdeaDialog> createState() => _AddIdeaDialogState();
}

class _AddIdeaDialogState extends State<AddIdeaDialog> {
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _tagsController = TextEditingController();
  int _selectedPriority = 1; // 0=low, 1=medium, 2=high
  String _selectedCategory = 'other'; // Catégorie par défaut
  late String _selectedStatus;
  DateTime? _dueDate;
  List<PlatformFile> _attachments = [];

  final List<String> _statuses = ['Backlog', 'In Progress', 'Done'];
  final List<Map<String, dynamic>> _categories = [
    {'value': 'product', 'label': 'Produit', 'icon': Icons.inventory_2},
    {'value': 'marketing', 'label': 'Marketing', 'icon': Icons.campaign},
    {'value': 'business', 'label': 'Business', 'icon': Icons.business_center},
    {'value': 'tech', 'label': 'Tech', 'icon': Icons.code},
    {'value': 'design', 'label': 'Design', 'icon': Icons.palette},
    {'value': 'sales', 'label': 'Ventes', 'icon': Icons.attach_money},
    {'value': 'other', 'label': 'Autre', 'icon': Icons.lightbulb},
  ];

  @override
  void initState() {
    super.initState();
    // S'assurer que le statut initial est valide
    if (widget.initialStatus != null &&
        _statuses.contains(widget.initialStatus)) {
      _selectedStatus = widget.initialStatus!;
    } else {
      _selectedStatus = 'Backlog'; // Valeur par défaut
    }
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

  Future<void> _pickAttachments() async {
    final result = await FilePicker.platform.pickFiles(
      allowMultiple: true,
      type: FileType.custom,
      allowedExtensions: ['png', 'jpg', 'jpeg', 'pdf'],
      withReadStream: false,
    );
    if (result != null) {
      setState(() {
        _attachments = result.files;
      });
    }
  }

  void _saveIdea() async {
    if (_titleController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Row(
            children: [
              Icon(Icons.warning, color: Colors.white),
              SizedBox(width: 8),
              Text('Le titre est obligatoire'),
            ],
          ),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final userId = authProvider.userId;

    if (userId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Vous devez être connecté pour créer une carte'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    final idea = {
      'boardId': widget.boardId ?? 1,
      'title': _titleController.text.trim(),
      'description': _descriptionController.text.trim(),
      'priority': _selectedPriority,
      'category': _selectedCategory,
      'status': _selectedStatus,
      'dueDate': _dueDate?.toIso8601String(),
      'tags': _tagsController.text.trim(),
      'attachments': _attachments.isEmpty
          ? null
          : jsonEncode(
              _attachments
                  .map((f) => {'name': f.name, 'path': f.path})
                  .toList(),
            ),
    };

    print('Creating idea with data: ${idea.toString()}'); // Debug

    try {
      final ideaProvider = Provider.of<IdeaProvider>(context, listen: false);
      final boardProvider = Provider.of<BoardProvider>(context, listen: false);
      await ideaProvider.addIdea(idea, boardProvider: boardProvider);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Carte "${_titleController.text.trim()}" ajoutée avec succès !',
                    style: TextStyle(fontWeight: FontWeight.w500),
                  ),
                ),
              ],
            ),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 3),
            behavior: SnackBarBehavior.floating,
          ),
        );
        Navigator.of(context).pop();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                Icon(Icons.error, color: Colors.white),
                SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Erreur lors de l\'ajout: $e',
                    style: TextStyle(fontWeight: FontWeight.w500),
                  ),
                ),
              ],
            ),
            backgroundColor: Colors.red,
            duration: Duration(seconds: 4),
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Dialog(
      child: Container(
        width: 600,
        constraints: const BoxConstraints(maxHeight: 700),
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                Icon(
                  Icons.add_card,
                  color: theme.colorScheme.primary,
                  size: 28,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Nouvelle Carte',
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
                      autofocus: true,
                      decoration: const InputDecoration(
                        labelText: 'Titre *',
                        border: OutlineInputBorder(),
                        hintText: 'Ex: Implémenter la nouvelle fonctionnalité',
                      ),
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    Text('Pièces jointes', style: theme.textTheme.titleSmall),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        FilledButton.icon(
                          onPressed: _pickAttachments,
                          icon: const Icon(Icons.attach_file),
                          label: const Text('Ajouter des fichiers'),
                        ),
                        const SizedBox(width: 12),
                        if (_attachments.isNotEmpty)
                          Text(
                            '${_attachments.length} fichier(s) sélectionné(s)',
                          ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    if (_attachments.isNotEmpty)
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: _attachments
                            .map(
                              (f) => Chip(
                                label: Text(f.name),
                                avatar: Icon(
                                  f.extension?.toLowerCase() == 'pdf'
                                      ? Icons.picture_as_pdf
                                      : Icons.image,
                                ),
                                onDeleted: () {
                                  setState(() {
                                    _attachments.remove(f);
                                  });
                                },
                              ),
                            )
                            .toList(),
                      ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _descriptionController,
                      decoration: const InputDecoration(
                        labelText: 'Description',
                        border: OutlineInputBorder(),
                        hintText: 'Détails de la tâche...',
                      ),
                      maxLines: 4,
                    ),
                    const SizedBox(height: 16),
                    Text('Catégorie', style: theme.textTheme.titleSmall),
                    const SizedBox(height: 8),
                    DropdownButtonFormField<String>(
                      value: _selectedCategory,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                      ),
                      items: _categories.map((category) {
                        return DropdownMenuItem(
                          value: category['value'] as String,
                          child: Row(
                            children: [
                              Icon(category['icon'] as IconData, size: 20),
                              const SizedBox(width: 8),
                              Text(category['label'] as String),
                            ],
                          ),
                        );
                      }).toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => _selectedCategory = value);
                        }
                      },
                    ),
                    const SizedBox(height: 16),
                    Text('Priorité', style: theme.textTheme.titleSmall),
                    const SizedBox(height: 8),
                    SegmentedButton<int>(
                      segments: const [
                        ButtonSegment(
                          value: 0,
                          label: Text('Basse'),
                          icon: Icon(Icons.arrow_downward, size: 18),
                        ),
                        ButtonSegment(
                          value: 1,
                          label: Text('Moyenne'),
                          icon: Icon(Icons.remove, size: 18),
                        ),
                        ButtonSegment(
                          value: 2,
                          label: Text('Haute'),
                          icon: Icon(Icons.arrow_upward, size: 18),
                        ),
                      ],
                      selected: {_selectedPriority},
                      onSelectionChanged: (Set<int> selected) {
                        setState(() => _selectedPriority = selected.first);
                      },
                    ),
                    const SizedBox(height: 16),
                    Text('Statut', style: theme.textTheme.titleSmall),
                    const SizedBox(height: 8),
                    DropdownButtonFormField<String>(
                      value: _selectedStatus,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                      ),
                      items: _statuses.map((status) {
                        return DropdownMenuItem(
                          value: status,
                          child: Text(status),
                        );
                      }).toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => _selectedStatus = value);
                        }
                      },
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
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Annuler'),
                ),
                const SizedBox(width: 8),
                FilledButton.icon(
                  onPressed: _saveIdea,
                  icon: const Icon(Icons.check),
                  label: const Text('Créer'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
