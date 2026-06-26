import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:open_file/open_file.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';
import '../../services/api_service.dart';

class OrientationModule extends ConsumerWidget {
  const OrientationModule({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Orientation & Carrière'), elevation: 0),
      body: DefaultTabController(
        length: 4,
        child: Column(children: [
          const TabBar(
            isScrollable: true,
            tabs: [
              Tab(icon: Icon(Icons.smart_toy), text: 'Agent IA'),
              Tab(icon: Icon(Icons.work_outline), text: 'Métiers'),
              Tab(icon: Icon(Icons.description_outlined), text: 'CV & LM'),
              Tab(icon: Icon(Icons.business_center_outlined), text: 'Stages'),
            ],
          ),
          const Expanded(
            child: TabBarView(children: [
              _AgentTab(),
              _MetiersTab(),
              _TemplatesTab(),
              _StagesTab(),
            ]),
          ),
        ]),
      ),
    );
  }
}

// ── Tab Agent IA ─────────────────────────────────────────────────────────────

class _AgentTab extends StatelessWidget {
  const _AgentTab();

  @override
  Widget build(BuildContext context) {
    return ModuleAgentChat(
      module: 'orientation',
      agentLabel: 'Agent Orientation',
      placeholder: 'Ex: Comment préparer mon CV pour un stage en IA ?',
      suggestions: [
        'Conseils pour un CV informatique',
        'Trouver un stage au Maroc',
        'Quels métiers après ENIAD ?',
        'Préparer un entretien technique',
        'Lettre de motivation stage',
      ],
    );
  }
}

// ── Tab Métiers ───────────────────────────────────────────────────────────────

class _MetiersTab extends StatelessWidget {
  const _MetiersTab();

  static const _metiers = [
    {
      'titre': 'Ingénieur en Intelligence Artificielle',
      'demande': 'Très forte',
      'secteur': 'Tech / Data',
      'description': 'Développement de modèles ML, NLP, vision par ordinateur. Profil très recherché au Maroc et à l\'international.',
      'icon': Icons.psychology,
      'color': Colors.deepPurple,
    },
    {
      'titre': 'Ingénieur DevOps / Cloud',
      'demande': 'Forte',
      'secteur': 'Infrastructure',
      'description': 'Automatisation CI/CD, AWS/Azure/GCP, Kubernetes. Forte demande dans les ESN marocaines.',
      'icon': Icons.cloud,
      'color': Colors.blue,
    },
    {
      'titre': 'Ingénieur Réseaux & Cybersécurité',
      'demande': 'Forte',
      'secteur': 'Sécurité',
      'description': 'Sécurisation des infrastructures, pentest, SOC. Compétences très valorisées au Maroc.',
      'icon': Icons.security,
      'color': Colors.red,
    },
    {
      'titre': 'Data Scientist / Analyste',
      'demande': 'Forte',
      'secteur': 'Data',
      'description': 'Analyse de données massives, dashboards BI, Python/R/SQL. Profil clé dans les banques, télécom.',
      'icon': Icons.bar_chart,
      'color': Colors.teal,
    },
    {
      'titre': 'Développeur Full Stack',
      'demande': 'Moyenne',
      'secteur': 'Développement',
      'description': 'React, Node.js, Python/FastAPI. Profils freelance très actifs sur les plateformes marocaines.',
      'icon': Icons.code,
      'color': Colors.orange,
    },
    {
      'titre': 'Ingénieur IoT / Robotique',
      'demande': 'En croissance',
      'secteur': 'Industrie 4.0',
      'description': 'Capteurs, Arduino/Raspberry Pi, automatisation industrielle. Secteur en forte expansion.',
      'icon': Icons.precision_manufacturing,
      'color': Colors.green,
    },
  ];

  Color _demandColor(String d) {
    if (d.contains('Très')) return Colors.green;
    if (d.contains('Forte')) return Colors.blue;
    if (d.contains('croissance')) return Colors.orange;
    return Colors.grey;
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _metiers.length,
      itemBuilder: (_, i) {
        final m = _metiers[i];
        final color = m['color'] as Color;
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
            side: BorderSide(color: color.withOpacity(0.2)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(m['icon'] as IconData, color: color, size: 26),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(m['titre'] as String,
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  const SizedBox(height: 4),
                  Text(m['description'] as String,
                      style: TextStyle(fontSize: 12, color: Colors.grey[700])),
                  const SizedBox(height: 8),
                  Row(children: [
                    _Badge(m['secteur'] as String, Colors.grey),
                    const SizedBox(width: 6),
                    _Badge(m['demande'] as String, _demandColor(m['demande'] as String)),
                  ]),
                ]),
              ),
            ]),
          ),
        );
      },
    );
  }
}

class _Badge extends StatelessWidget {
  final String label;
  final Color color;
  const _Badge(this.label, this.color);

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
        decoration: BoxDecoration(
          color: color.withOpacity(0.12),
          borderRadius: BorderRadius.circular(6),
        ),
        child: Text(label,
            style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w600)),
      );
}

// ── Tab CV & LM ───────────────────────────────────────────────────────────────

class _TemplatesTab extends ConsumerStatefulWidget {
  const _TemplatesTab();

  @override
  ConsumerState<_TemplatesTab> createState() => _TemplatesTabState();
}

class _TemplatesTabState extends ConsumerState<_TemplatesTab>
    with SingleTickerProviderStateMixin {
  late TabController _subTab;

  // CV Analysis
  String? _cvFileName;
  Uint8List? _cvBytes;
  final _posteController = TextEditingController();
  bool _cvLoading = false;
  String? _cvResult;
  String? _cvError;

  // LM Generation
  final _lmPosteController = TextEditingController();
  final _lmEntrepriseController = TextEditingController();
  final _lmCompetencesController = TextEditingController();
  final _lmProjetsController = TextEditingController();
  String _lmType = 'startup';
  bool _lmLoading = false;
  String? _lmResult;
  String? _lmError;

  @override
  void initState() {
    super.initState();
    _subTab = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _subTab.dispose();
    _posteController.dispose();
    _lmPosteController.dispose();
    _lmEntrepriseController.dispose();
    _lmCompetencesController.dispose();
    _lmProjetsController.dispose();
    super.dispose();
  }

  Future<void> _pickCV() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
      withData: true,
    );
    if (result != null && result.files.isNotEmpty) {
      final file = result.files.single;
      setState(() {
        _cvFileName = file.name;
        _cvBytes = file.bytes;
        _cvResult = null;
        _cvError = null;
      });
    }
  }

  Future<void> _analyzeCV() async {
    if (_cvBytes == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Veuillez sélectionner votre CV en PDF')),
      );
      return;
    }
    setState(() {
      _cvLoading = true;
      _cvResult = null;
      _cvError = null;
    });
    try {
      final api = ref.read(apiServiceProvider);
      final result = await api.analyzeCv(
        fileBytes: _cvBytes!.toList(),
        filename: _cvFileName ?? 'cv.pdf',
        posteCible: _posteController.text.trim().isNotEmpty
            ? _posteController.text.trim()
            : null,
      );
      // Essayer plusieurs clés possibles retournées par le backend
      final raw = (result['analyse'] as String?
              ?? result['analysis'] as String?
              ?? result['result'] as String?
              ?? result['content'] as String?
              ?? result['response'] as String?
              ?? '')
          .trim();
      setState(() {
        if (raw.isNotEmpty) {
          _cvResult = raw;
        } else {
          _cvError = 'Le serveur a retourné une réponse vide. Vérifiez que votre PDF contient du texte lisible et réessayez.';
        }
      });
    } catch (e) {
      setState(() => _cvError = e.toString());
    } finally {
      setState(() => _cvLoading = false);
    }
  }

  Future<void> _generateLM() async {
    if (_lmPosteController.text.trim().isEmpty ||
        _lmEntrepriseController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Veuillez renseigner le poste et l'entreprise")),
      );
      return;
    }
    setState(() {
      _lmLoading = true;
      _lmResult = null;
      _lmError = null;
    });
    try {
      final api = ref.read(apiServiceProvider);
      final result = await api.generateLm(
        poste: _lmPosteController.text.trim(),
        entreprise: _lmEntrepriseController.text.trim(),
        typeLm: _lmType,
        competences: _lmCompetencesController.text.trim().isNotEmpty
            ? _lmCompetencesController.text.trim()
            : null,
        projets: _lmProjetsController.text.trim().isNotEmpty
            ? _lmProjetsController.text.trim()
            : null,
      );
      final raw = (result['lettre'] as String?
              ?? result['letter'] as String?
              ?? result['content'] as String?
              ?? result['response'] as String?
              ?? '')
          .trim();
      setState(() {
        if (raw.isNotEmpty) {
          _lmResult = raw;
        } else {
          _lmError = 'Le serveur a retourné une lettre vide. Réessayez dans quelques secondes.';
        }
      });
    } catch (e) {
      setState(() => _lmError = e.toString());
    } finally {
      setState(() => _lmLoading = false);
    }
  }

  Future<void> _downloadLM() async {
    if (_lmResult == null) return;
    try {
      final dir = await getApplicationDocumentsDirectory();
      final safe = RegExp(r'[^\wÀ-ɏ]');
      final ent = _lmEntrepriseController.text.trim().replaceAll(safe, '_');
      final pos = _lmPosteController.text.trim().replaceAll(safe, '_');
      final filename = 'LM_${ent}_$pos.txt';
      final file = File('${dir.path}/$filename');
      await file.writeAsString(_lmResult!);
      final result = await OpenFile.open(file.path);
      if (result.type != ResultType.done && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Fichier sauvegardé : ${file.path}')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erreur téléchargement : $e')),
        );
      }
    }
  }

  void _copy(String text, String label) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('$label copié dans le presse-papiers')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      TabBar(
        controller: _subTab,
        labelColor: AppTheme.primaryColor,
        unselectedLabelColor: Colors.grey,
        indicatorColor: AppTheme.primaryColor,
        tabs: const [
          Tab(icon: Icon(Icons.analytics_outlined), text: 'Analyser CV'),
          Tab(icon: Icon(Icons.edit_note), text: 'Générer LM'),
        ],
      ),
      Expanded(
        child: TabBarView(
          controller: _subTab,
          children: [_buildCvTab(), _buildLmTab()],
        ),
      ),
    ]);
  }

  Widget _buildCvTab() {
    final picked = _cvFileName != null;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        _infoBanner(
          icon: Icons.smart_toy,
          color: AppTheme.primaryColor,
          text: "Uploadez votre CV en PDF — l'IA l'analyse et vous donne des recommandations personnalisées pour le marché marocain.",
        ),
        const SizedBox(height: 20),

        // ── Upload zone ──
        GestureDetector(
          onTap: _cvLoading ? null : _pickCV,
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 28, horizontal: 16),
            decoration: BoxDecoration(
              color: picked
                  ? Colors.green.shade50
                  : AppTheme.primaryColor.withOpacity(0.04),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(
                color: picked ? Colors.green.shade300 : AppTheme.primaryColor.withOpacity(0.3),
                width: 2,
                strokeAlign: BorderSide.strokeAlignInside,
              ),
            ),
            child: Column(children: [
              Icon(
                picked ? Icons.picture_as_pdf : Icons.upload_file,
                size: 48,
                color: picked ? Colors.green : AppTheme.primaryColor,
              ),
              const SizedBox(height: 10),
              Text(
                picked ? _cvFileName! : 'Appuyez pour choisir votre CV',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: picked ? Colors.green.shade700 : AppTheme.primaryColor,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              Text(
                picked ? 'Appuyez pour changer de fichier' : 'Format PDF uniquement • Max 5 Mo',
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
            ]),
          ),
        ),

        const SizedBox(height: 14),
        TextField(
          controller: _posteController,
          decoration: _inputDeco(
            label: 'Poste ciblé (optionnel)',
            hint: 'Ex: Stage en IA, DevOps, Cybersécurité…',
            icon: Icons.work_outline,
          ),
        ),
        const SizedBox(height: 16),
        _actionButton(
          loading: _cvLoading,
          icon: Icons.analytics,
          label: 'Analyser mon CV',
          loadingLabel: 'Extraction & analyse en cours…',
          color: AppTheme.primaryColor,
          onPressed: _analyzeCV,
        ),
        if (_cvError != null) _errorBox(_cvError!),
        if (_cvResult != null) ...[
          const SizedBox(height: 16),
          _resultHeader("Résultat de l'analyse", onCopy: () => _copy(_cvResult!, 'Analyse')),
          _resultBox(_cvResult!, color: Colors.grey.shade50, border: Colors.grey.shade200),
        ],
      ]),
    );
  }

  Widget _buildLmTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        _infoBanner(
          icon: Icons.auto_awesome,
          color: Colors.purple,
          text: 'Générez une lettre de motivation personnalisée en quelques secondes.',
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _lmPosteController,
          decoration: _inputDeco(
            label: 'Poste *',
            hint: 'Ex: Stage en Intelligence Artificielle',
            icon: Icons.work_outline,
          ),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _lmEntrepriseController,
          decoration: _inputDeco(
            label: 'Entreprise *',
            hint: 'Ex: OCP Group, Capgemini Maroc…',
            icon: Icons.business,
          ),
        ),
        const SizedBox(height: 12),
        DropdownButtonFormField<String>(
          value: _lmType,
          decoration: _inputDeco(label: "Type d'entreprise", icon: Icons.category_outlined),
          items: const [
            DropdownMenuItem(value: 'startup', child: Text('Startup / PME')),
            DropdownMenuItem(value: 'multinational', child: Text('Grande entreprise / Multinationale')),
          ],
          onChanged: (v) => setState(() => _lmType = v ?? 'startup'),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _lmCompetencesController,
          maxLines: 2,
          decoration: _inputDeco(
            label: 'Compétences clés (optionnel)',
            hint: 'Ex: Python, TensorFlow, React, Docker…',
            icon: null,
            align: true,
          ),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _lmProjetsController,
          maxLines: 2,
          decoration: _inputDeco(
            label: 'Projets / expériences (optionnel)',
            hint: "Ex: PFA sur la détection d'anomalies, stage chez X…",
            icon: null,
            align: true,
          ),
        ),
        const SizedBox(height: 16),
        _actionButton(
          loading: _lmLoading,
          icon: Icons.auto_awesome,
          label: 'Générer ma lettre',
          loadingLabel: 'Génération en cours…',
          color: Colors.purple,
          onPressed: _generateLM,
        ),
        if (_lmError != null) _errorBox(_lmError!),
        if (_lmResult != null) ...[
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Lettre générée',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
              Row(children: [
                TextButton.icon(
                  onPressed: () => _copy(_lmResult!, 'Lettre'),
                  icon: const Icon(Icons.copy, size: 16),
                  label: const Text('Copier', style: TextStyle(fontSize: 12)),
                ),
                TextButton.icon(
                  onPressed: _downloadLM,
                  icon: const Icon(Icons.download_outlined, size: 16),
                  label: const Text('Télécharger', style: TextStyle(fontSize: 12)),
                  style: TextButton.styleFrom(foregroundColor: Colors.purple),
                ),
              ]),
            ],
          ),
          _resultBox(
            _lmResult!,
            color: Colors.purple.shade50,
            border: Colors.purple.shade100,
            lineHeight: 1.6,
          ),
        ],
      ]),
    );
  }

  InputDecoration _inputDeco({
    required String label,
    String? hint,
    IconData? icon,
    bool align = false,
  }) {
    return InputDecoration(
      labelText: label,
      hintText: hint,
      alignLabelWithHint: align,
      prefixIcon: icon != null ? Icon(icon) : null,
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
    );
  }

  Widget _infoBanner({required IconData icon, required Color color, required String text}) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(width: 10),
        Expanded(child: Text(text, style: const TextStyle(fontSize: 12))),
      ]),
    );
  }

  Widget _actionButton({
    required bool loading,
    required IconData icon,
    required String label,
    required String loadingLabel,
    required Color color,
    required VoidCallback onPressed,
  }) {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed: loading ? null : onPressed,
        icon: loading
            ? SizedBox(
                width: 18, height: 18,
                child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
              )
            : Icon(icon),
        label: Text(loading ? loadingLabel : label),
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 14),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      ),
    );
  }

  Widget _errorBox(String msg) {
    return Container(
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.red.shade50,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.red.shade200),
      ),
      child: Text(msg, style: TextStyle(color: Colors.red.shade700, fontSize: 13)),
    );
  }

  Widget _resultHeader(String title, {required VoidCallback onCopy}) {
    return Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
      Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
      TextButton.icon(
        onPressed: onCopy,
        icon: const Icon(Icons.copy, size: 16),
        label: const Text('Copier', style: TextStyle(fontSize: 12)),
      ),
    ]);
  }

  Widget _resultBox(String text, {required Color color, required Color border, double lineHeight = 1.5}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: border),
      ),
      child: text.trim().isEmpty
          ? const Text(
              'Aucun contenu reçu.',
              style: TextStyle(color: Colors.grey, fontSize: 13),
            )
          : SelectableText(
              text,
              style: TextStyle(
                fontSize: 13,
                height: lineHeight,
                color: Colors.black87,
              ),
            ),
    );
  }
}

// ── Tab Stages ────────────────────────────────────────────────────────────────

class _StagesTab extends ConsumerStatefulWidget {
  const _StagesTab();

  @override
  ConsumerState<_StagesTab> createState() => _StagesTabState();
}

class _StagesTabState extends ConsumerState<_StagesTab> {
  bool _loading = false;
  String? _error;
  List<Map<String, dynamic>> _stages = [];
  List<Map<String, dynamic>> _platforms = [];
  String _filiere = '';
  String _typeFilter = '';

  @override
  void initState() {
    super.initState();
    _loadStages();
  }

  Future<void> _loadStages() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final api = ref.read(apiServiceProvider);
      final result = await api.getStages(
        filiere: _filiere.isNotEmpty ? _filiere : null,
        typeStage: _typeFilter.isNotEmpty ? _typeFilter : null,
      );
      setState(() {
        _stages = (result['stages'] as List).cast<Map<String, dynamic>>();
        _platforms = (result['platforms'] as List).cast<Map<String, dynamic>>();
        if (_filiere.isEmpty && result['filiere'] != null) {
          _filiere = result['filiere'] as String;
        }
      });
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      setState(() => _loading = false);
    }
  }

  void _applyFilter(String type) {
    setState(() => _typeFilter = type);
    _loadStages();
  }

  void _copyLink(String url, String label) {
    Clipboard.setData(ClipboardData(text: url));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Lien copié : $label')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      // Filter chips
      const SizedBox(height: 8),
      SizedBox(
        height: 36,
        child: ListView(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 16),
          children: [
            _FilterChip(label: 'Tous', selected: _typeFilter.isEmpty,
                onTap: () => _applyFilter('')),
            const SizedBox(width: 8),
            _FilterChip(label: 'PFE', selected: _typeFilter == 'pfe',
                onTap: () => _applyFilter('pfe')),
            const SizedBox(width: 8),
            _FilterChip(label: 'Stage court', selected: _typeFilter == 'stage',
                onTap: () => _applyFilter('stage')),
            const SizedBox(width: 8),
            _FilterChip(label: 'Alternance', selected: _typeFilter == 'alternance',
                onTap: () => _applyFilter('alternance')),
            const SizedBox(width: 8),
            _FilterChip(label: 'Recherche', selected: _typeFilter == 'recherche',
                onTap: () => _applyFilter('recherche')),
          ],
        ),
      ),
      const SizedBox(height: 8),

      Expanded(
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : _error != null
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Icon(Icons.error_outline, color: Colors.red.shade300, size: 48),
                        const SizedBox(height: 12),
                        Text(_error!, textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.red.shade600, fontSize: 13)),
                        const SizedBox(height: 16),
                        TextButton(onPressed: _loadStages, child: const Text('Réessayer')),
                      ]),
                    ),
                  )
                : ListView(
                    padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                    children: [
                      if (_stages.isEmpty)
                        const Padding(
                          padding: EdgeInsets.symmetric(vertical: 32),
                          child: Center(
                            child: Text('Aucune offre trouvée pour ce filtre.',
                                style: TextStyle(color: Colors.grey)),
                          ),
                        ),
                      ..._stages.map((s) => _StageCard(
                            stage: s,
                            onCopyLink: () =>
                                _copyLink(s['lien'] ?? '', s['entreprise'] ?? ''),
                          )),
                      if (_platforms.isNotEmpty) ...[
                        const Padding(
                          padding: EdgeInsets.symmetric(vertical: 12),
                          child: Text('Plateformes de recherche',
                              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        ),
                        ..._platforms.map((p) => Card(
                              margin: const EdgeInsets.only(bottom: 8),
                              child: ListTile(
                                leading: Container(
                                  padding: const EdgeInsets.all(8),
                                  decoration: BoxDecoration(
                                    color: AppTheme.primaryColor.withOpacity(0.1),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Icon(Icons.link,
                                      color: AppTheme.primaryColor, size: 20),
                                ),
                                title: Text(p['nom'] ?? '',
                                    style: const TextStyle(
                                        fontWeight: FontWeight.w600, fontSize: 13)),
                                subtitle: Text(p['description'] ?? '',
                                    style: const TextStyle(fontSize: 12)),
                                trailing: IconButton(
                                  icon: const Icon(Icons.copy, size: 18),
                                  tooltip: 'Copier le lien',
                                  onPressed: () =>
                                      _copyLink(p['lien'] ?? '', p['nom'] ?? ''),
                                ),
                              ),
                            )),
                      ],
                    ],
                  ),
      ),
    ]);
  }
}

class _StageCard extends StatelessWidget {
  final Map<String, dynamic> stage;
  final VoidCallback onCopyLink;
  const _StageCard({required this.stage, required this.onCopyLink});

  static const _typeColors = {
    'pfe': Colors.deepPurple,
    'alternance': Colors.blue,
    'stage': Colors.teal,
    'recherche': Colors.green,
  };

  static const _typeLabels = {
    'pfe': 'PFE',
    'alternance': 'Alternance',
    'stage': 'Stage',
    'recherche': 'Recherche',
  };

  @override
  Widget build(BuildContext context) {
    final profils = (stage['profil'] as List? ?? []).join(' / ');
    final type = stage['type'] as String? ?? '';
    final typeColor = _typeColors[type] ?? Colors.grey;
    final typeLabel = _typeLabels[type] ?? type;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            Expanded(
              child: Text(stage['entreprise'] ?? '',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                  overflow: TextOverflow.ellipsis),
            ),
            const SizedBox(width: 8),
            _Badge(profils, AppTheme.primaryColor),
          ]),
          const SizedBox(height: 4),
          Text(stage['poste'] ?? '',
              style: TextStyle(fontSize: 13, color: Colors.grey[800])),
          if ((stage['description'] as String?)?.isNotEmpty == true) ...[
            const SizedBox(height: 4),
            Text(stage['description'] as String,
                style: TextStyle(fontSize: 12, color: Colors.grey[600])),
          ],
          const SizedBox(height: 8),
          Row(children: [
            Icon(Icons.location_on, size: 14, color: Colors.grey[600]),
            const SizedBox(width: 4),
            Expanded(
              child: Text(stage['lieu'] ?? '',
                  style: TextStyle(fontSize: 12, color: Colors.grey[600])),
            ),
            Icon(Icons.schedule, size: 14, color: Colors.grey[600]),
            const SizedBox(width: 4),
            Text(stage['duree'] ?? '',
                style: TextStyle(fontSize: 12, color: Colors.grey[600])),
          ]),
          const SizedBox(height: 10),
          Row(children: [
            Expanded(
              child: OutlinedButton.icon(
                onPressed: onCopyLink,
                icon: const Icon(Icons.copy, size: 16),
                label: const Text('Copier le lien'),
                style: OutlinedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8)),
                ),
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
              decoration: BoxDecoration(
                color: typeColor.withOpacity(0.12),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(typeLabel,
                  style: TextStyle(
                      fontSize: 11,
                      color: typeColor,
                      fontWeight: FontWeight.w600)),
            ),
          ]),
        ]),
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;
  const _FilterChip({required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        decoration: BoxDecoration(
          color: selected ? AppTheme.primaryColor : Colors.grey.shade100,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: selected ? AppTheme.primaryColor : Colors.grey.shade300,
          ),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: selected ? Colors.white : Colors.grey.shade700,
            fontWeight: selected ? FontWeight.w600 : FontWeight.normal,
          ),
        ),
      ),
    );
  }
}
