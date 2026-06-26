import 'dart:async';
import 'dart:convert';
import 'dart:io' show File;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:open_file/open_file.dart';
import 'package:path_provider/path_provider.dart';
import '../../services/api_service.dart';
import '../../providers/auth_provider.dart';

// â”€â”€â”€ Palette â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const _kPrimary  = Color(0xFF0052A5);
const _kDark     = Color(0xFF0A1628);
const _kGreen    = Color(0xFF1B8A4E);
const _kOrange   = Color(0xFFE65100);
const _kPurple   = Color(0xFF6A1B9A);
const _kBg       = Color(0xFFF0F4FA);
const _kAgentBg  = Color(0xFFFFFFFF);
const _kUserBg   = Color(0xFF0052A5);

// â”€â”€â”€ Data models â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

enum _StepStatus { pending, running, done }

class _Step {
  final String label;
  _StepStatus status = _StepStatus.pending;
  _Step(this.label);
}

class _ActionResult {
  final String type;           // doc | request | info
  final String? docId;
  final String? pdfBase64;
  final String? requestId;

  const _ActionResult({
    required this.type,
    this.docId,
    this.pdfBase64,
    this.requestId,
  });
}

class _Msg {
  final bool isUser;
  final String text;
  final _ActionResult? action;
  final DateTime time;
  _Msg.user(this.text) : isUser = true, action = null, time = DateTime.now();
  _Msg.agent(this.text, {this.action}) : isUser = false, time = DateTime.now();
}

class _ActiveTask {
  final String label;
  final bool done;
  final String? ref;
  final DateTime time;
  _ActiveTask({required this.label, required this.done, this.ref, required this.time});
}

// â”€â”€â”€ Step inference â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
List<_Step> _inferSteps(String msg) {
  final m = msg.toLowerCase();
  if (m.contains('attestation') || m.contains('scolarite')) {
    return [
      _Step('Analyse de votre demande'),
      _Step('Verification de votre identite'),
      _Step('Controle de l\'inscription'),
      _Step('Generation du document PDF'),
      _Step('Archivage et validation'),
    ];
  }
  if (m.contains('reglement') || m.contains('gavel')) {
    return [
      _Step('Demande du reglement interieur'),
      _Step('Chargement du document officiel'),
      _Step('Generation du PDF'),
      _Step('Validation'),
    ];
  }
  if (m.contains('convention') || m.contains('entreprise:') ||
      (m.contains('stage') && !m.contains('certificat'))) {
    return [
      _Step('Verification du profil etudiant'),
      _Step('Preparation des informations du stage'),
      _Step('Generation de la convention PDF'),
      _Step('Archivage du document'),
      _Step('Validation'),
    ];
  }
  if (m.contains('statut') || m.contains('suivi') || m.contains('mes demandes') || m.contains('historique')) {
    return [
      _Step('Analyse de votre demande'),
      _Step('Consultation de la base de donnees'),
      _Step('Recuperation de l\'historique'),
      _Step('Compilation des resultats'),
    ];
  }
  return [
    _Step('Analyse de votre message'),
    _Step('Consultation des documents ENIAD'),
    _Step('Recherche d\'informations'),
    _Step('Preparation de la reponse'),
  ];
}

// â”€â”€â”€ AdminModule â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class AdminModule extends ConsumerStatefulWidget {
  const AdminModule({Key? key}) : super(key: key);
  @override
  ConsumerState<AdminModule> createState() => _AdminModuleState();
}

class _AdminModuleState extends ConsumerState<AdminModule>
    with SingleTickerProviderStateMixin {
  late TabController _tab;

  @override
  void initState() { super.initState(); _tab = TabController(length: 3, vsync: this); }
  @override
  void dispose()   { _tab.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _kBg,
      appBar: AppBar(
        title: Row(children: [
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(color: Colors.white.withAlpha(30), borderRadius: BorderRadius.circular(8)),
            child: const Icon(Icons.smart_toy, color: Colors.white, size: 18),
          ),
          const SizedBox(width: 10),
          const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Assistant Administratif', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white)),
            Text('ENIAD Â· Conseiller administratif intelligent', style: TextStyle(fontSize: 10, color: Colors.white70)),
          ]),
        ]),
        backgroundColor: _kDark,
        elevation: 0,
        bottom: TabBar(
          controller: _tab,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white54,
          labelStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600),
          tabs: const [
            Tab(icon: Icon(Icons.chat_bubble_outline, size: 18), text: 'Assistant'),
            Tab(icon: Icon(Icons.folder_outlined,     size: 18), text: 'Documents'),
            Tab(icon: Icon(Icons.assignment_outlined, size: 18), text: 'Demandes'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tab,
        children: [
          _AgentTab(onSwitchTab: (i) => _tab.animateTo(i)),
          const _DocumentsTab(),
          const _DemandesTab(),
        ],
      ),
    );
  }
}

// â”€â”€â”€ Agent Tab (main agentic interface) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _AgentTab extends ConsumerStatefulWidget {
  final void Function(int) onSwitchTab;
  const _AgentTab({required this.onSwitchTab});
  @override
  ConsumerState<_AgentTab> createState() => _AgentTabState();
}

class _AgentTabState extends ConsumerState<_AgentTab> {
  final _inputCtrl  = TextEditingController();
  final _scrollCtrl = ScrollController();
  final List<_Msg> _msgs = [];
  String? _convId;

  bool _isThinking   = false;
  List<_Step> _steps = [];
  int _stepIdx       = 0;
  Timer? _stepTimer;

  final List<_ActiveTask> _activeTasks = [];
  Map<String, dynamic> _profile = {};
  bool _profileLoaded = false;
  bool _showProfile   = false;

  static const _quickActions = [
    ('Mon attestation de scolarite', Icons.school_outlined,         _kPrimary),
    ('Convention de stage',          Icons.business_center_outlined, _kPurple),
    ("Reglement de l'ecole",         Icons.gavel_outlined,           _kGreen),
    ('Procedures ENIAD',             Icons.help_center_outlined,     Color(0xFF283593)),
  ];

  @override
  void initState() {
    super.initState();
    _convId = 'conv_${DateTime.now().millisecondsSinceEpoch}';
    _loadProfile();
    WidgetsBinding.instance.addPostFrameCallback((_) => _addWelcome());
  }

  @override
  void dispose() {
    _stepTimer?.cancel();
    _inputCtrl.dispose();
    _scrollCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadProfile() async {
    try {
      final api  = ref.read(apiServiceProvider);
      final data = await api.getUserProfile();
      if (mounted) setState(() { _profile = data; _profileLoaded = true; });
    } catch (_) {
      if (mounted) setState(() => _profileLoaded = true);
    }
  }

  void _addWelcome() {
    final name = (_profile['full_name'] as String?) ??
                 (_profile['username'] as String?) ?? 'etudiant(e)';
    setState(() => _msgs.add(_Msg.agent(
      'Bonjour $name ! Je suis votre assistant administratif ENIAD.\n\n'
      'Je genere les documents officiels suivants :\n'
      'â€¢ Attestation de scolarite â€” certifie votre inscription\n'
      'â€¢ Convention de stage â€” accord ENIAD / etudiant / entreprise\n'
      "â€¢ Reglement de l'ecole â€” reglement interieur officiel ENIAD\n\n"
      'Je peux aussi :\n'
      'â€¢ Vous guider sur les 15 demarches administratives de l\'ENIAD\n'
      'â€¢ Repondre a vos questions sur les procedures et services\n'
      'â€¢ Identifier le bon service et le responsable a contacter\n\n'
      'Decrivez votre situation et je vous guide etape par etape.',
    )));
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.animateTo(
          _scrollCtrl.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  // â”€â”€ Convention de Stage form dialog â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  Future<void> _showConventionDialog() async {
    // Controllers are owned by _ConventionFormSheet (a StatefulWidget).
    // Flutter disposes them only after the close animation fully completes,
    // preventing "ChangeNotifier used after dispose" errors.
    final result = await showModalBottomSheet<Map<String, String>?>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) => const _ConventionFormSheet(),
    );

    // At this point the modal widget tree is fully gone â€” safe to setState.
    if (result != null && mounted) {
      _sendConvention(
        entreprise: result['entreprise']!,
        adresse:    result['adresse']!,
        telephone:  result['telephone']!,
        fax:        result['fax']!,
        tuteur:     result['tuteur']!,
        poste:      result['poste']!,
        debut:      result['debut']!,
        fin:        result['fin']!,
      );
    }
  }

  void _sendConvention({
    required String entreprise,
    required String adresse,
    required String telephone,
    required String fax,
    required String tuteur,
    required String poste,
    required String debut,
    required String fin,
  }) {
    final buf = StringBuffer('Genere ma convention de stage.\n');
    buf.writeln('Entreprise: $entreprise');
    if (adresse.isNotEmpty)   buf.writeln('Adresse: $adresse');
    if (telephone.isNotEmpty) buf.writeln('Tel: $telephone');
    if (fax.isNotEmpty)       buf.writeln('Fax: $fax');
    if (tuteur.isNotEmpty)    buf.writeln('Tuteur: $tuteur');
    buf.writeln('Poste/Sujet: ${poste.isNotEmpty ? poste : "Stage de fin d etudes"}');
    if (debut.isNotEmpty)     buf.writeln('Date de debut: $debut');
    if (fin.isNotEmpty)       buf.writeln('Date de fin: $fin');
    _send(buf.toString().trim());
  }

  // ── Attestation de scolarité: smart flow ──────────────────────────────────
  Future<void> _triggerAttestationFlow() async {
    if (_isThinking) return;
    final api = ref.read(apiServiceProvider);

    // 1. Check what fields are already in the profile
    if (mounted) setState(() => _isThinking = true);
    Map<String, dynamic> prefill;
    try {
      prefill = await api.getAttestationPrefill();
    } catch (e) {
      if (mounted) setState(() {
        _isThinking = false;
        _msgs.add(_Msg.agent('Impossible de charger votre profil. Veuillez reessayer.'));
      });
      return;
    }
    if (mounted) setState(() => _isThinking = false);

    final missing = Map<String, String>.from(
        (prefill['missing_fields'] as Map? ?? {}).map(
          (k, v) => MapEntry(k.toString(), v.toString()),
        ));

    if (missing.isEmpty) {
      // All fields present → generate immediately
      _generateAttestationDirect({});
    } else {
      // Show form for missing fields only
      if (!mounted) return;
      final extraFields = await showModalBottomSheet<Map<String, dynamic>?>(
        context: context,
        isScrollControlled: true,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        ),
        builder: (ctx) => _AttestationMissingFieldsSheet(missingFields: missing),
      );
      if (extraFields != null && mounted) {
        _generateAttestationDirect(extraFields);
      }
    }
  }

  Future<void> _generateAttestationDirect(Map<String, dynamic> extraFields) async {
    if (_isThinking) return;
    final api = ref.read(apiServiceProvider);

    final steps = _inferSteps('attestation');
    steps[0].status = _StepStatus.running;

    setState(() {
      _msgs.add(_Msg.user('Je veux mon attestation de scolarite'));
      _isThinking = true;
      _steps  = steps;
      _stepIdx = 0;
    });
    _scrollToBottom();

    _stepTimer = Timer.periodic(const Duration(milliseconds: 1400), (t) {
      if (!mounted) { t.cancel(); return; }
      setState(() {
        if (_stepIdx < _steps.length) {
          _steps[_stepIdx].status = _StepStatus.done;
          _stepIdx++;
          if (_stepIdx < _steps.length) _steps[_stepIdx].status = _StepStatus.running;
        }
      });
    });

    try {
      final result = await api.generateAttestation(extraFields: extraFields);
      _stepTimer?.cancel();

      final action = _ActionResult(
        type: 'doc',
        docId: result['doc_id'] as String?,
        pdfBase64: result['pdf_base64'] as String?,
      );

      if (mounted) setState(() {
        for (final s in _steps) s.status = _StepStatus.done;
        _isThinking = false;
        _msgs.add(_Msg.agent(
          result['message'] as String? ?? 'Attestation generee avec succes.',
          action: action,
        ));
        _activeTasks.insert(0, _ActiveTask(
          label: 'Attestation generee',
          done: true,
          ref: result['doc_id'] as String?,
          time: DateTime.now(),
        ));
        if (_activeTasks.length > 5) _activeTasks.removeLast();
      });
      _scrollToBottom();
    } catch (e) {
      _stepTimer?.cancel();
      if (mounted) setState(() {
        _isThinking = false;
        _msgs.add(_Msg.agent(
          'Erreur lors de la generation : $e\nVeuillez verifier votre profil ou contacter le secretariat.',
        ));
      });
    }
  }

  Future<void> _send(String text) async {
    if (text.trim().isEmpty || _isThinking) return;
    _inputCtrl.clear();

    final steps = _inferSteps(text);
    steps[0].status = _StepStatus.running;

    setState(() {
      _msgs.add(_Msg.user(text));
      _isThinking = true;
      _steps = steps;
      _stepIdx = 0;
    });
    _scrollToBottom();

    _stepTimer = Timer.periodic(const Duration(milliseconds: 1400), (t) {
      if (!mounted) { t.cancel(); return; }
      setState(() {
        if (_stepIdx < _steps.length) {
          _steps[_stepIdx].status = _StepStatus.done;
          _stepIdx++;
          if (_stepIdx < _steps.length) _steps[_stepIdx].status = _StepStatus.running;
        }
      });
    });

    try {
      final api    = ref.read(apiServiceProvider);
      final result = await api.askAdminAgent(question: text, conversationId: _convId);
      _stepTimer?.cancel();

      final actionResult = _buildAction(result);
      final label = _actionLabel(result);

      if (mounted) setState(() {
        for (final s in _steps) s.status = _StepStatus.done;
        _isThinking = false;
        _msgs.add(_Msg.agent(result['response'] as String? ?? 'Demande traitee.', action: actionResult));
        if (label != null) {
          _activeTasks.insert(0, _ActiveTask(label: label, done: true, ref: actionResult?.docId ?? actionResult?.requestId, time: DateTime.now()));
          if (_activeTasks.length > 5) _activeTasks.removeLast();
        }
      });
    } catch (e) {
      _stepTimer?.cancel();
      if (mounted) setState(() {
        _isThinking = false;
        _msgs.add(_Msg.agent('Une erreur est survenue : $e\n\nVeuillez reessayer ou contacter le secretariat ENIAD.'));
      });
    }
    _scrollToBottom();
  }

  _ActionResult? _buildAction(Map<String, dynamic> r) {
    if (r['doc_id'] != null) {
      return _ActionResult(type: 'doc', docId: r['doc_id'] as String?, pdfBase64: r['pdf_base64'] as String?);
    }
    if (r['request_id'] != null) {
      return _ActionResult(type: 'request', requestId: r['request_id'] as String?);
    }
    return null;
  }

  String? _actionLabel(Map<String, dynamic> r) {
    if (r['doc_id'] != null)     return 'Document genere';
    if (r['request_id'] != null) return 'Demande creee';
    return null;
  }

  Future<void> _openPdf(String? base64str, String? docId) async {
    if (kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Telechargement PDF disponible sur l\'app mobile'),
        backgroundColor: _kOrange,
      ));
      return;
    }
    try {
      List<int> bytes;
      if (base64str != null && base64str.isNotEmpty) {
        bytes = base64Decode(base64str);
      } else if (docId != null) {
        // Fetch directly from backend if base64 not in response
        bytes = await ref.read(apiServiceProvider).downloadDocumentBytes(docId);
      } else {
        return;
      }
      final dir  = await getTemporaryDirectory();
      final file = File('${dir.path}/doc_${docId?.substring(0, 8) ?? 'dl'}.pdf');
      await file.writeAsBytes(bytes);
      await OpenFile.open(file.path);
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erreur: $e'), backgroundColor: Colors.red),
      );
    }
  }

  String _fmt(DateTime t) {
    final now = DateTime.now();
    final diff = now.difference(t);
    if (diff.inSeconds < 60)  return 'a l\'instant';
    if (diff.inMinutes < 60)  return 'il y a ${diff.inMinutes} min';
    if (diff.inHours < 24)    return 'il y a ${diff.inHours}h';
    return '${t.day}/${t.month}';
  }

  @override
  Widget build(BuildContext context) {
    final name   = (_profile['full_name'] as String?) ?? (_profile['username'] as String?) ?? '';
    final major  = (_profile['major']     as String?) ?? '';
    final year   = _profile['year']?.toString() ?? '';

    return Column(children: [
      // â”€â”€ Student memory banner
      if (_profileLoaded && (name.isNotEmpty || major.isNotEmpty))
        GestureDetector(
          onTap: () => setState(() => _showProfile = !_showProfile),
          child: Container(
            color: _kDark.withAlpha(240),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            child: Column(children: [
              Row(children: [
                CircleAvatar(radius: 16, backgroundColor: _kPrimary,
                    child: Text(name.isNotEmpty ? name[0].toUpperCase() : 'E',
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13))),
                const SizedBox(width: 10),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(name, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
                  if (major.isNotEmpty || year.isNotEmpty)
                    Text('${major.isNotEmpty ? major : ''} ${year.isNotEmpty ? "Â· Annee $year" : ""}',
                        style: const TextStyle(color: Colors.white60, fontSize: 11)),
                ])),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(color: _kGreen.withAlpha(50), borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: _kGreen.withAlpha(100))),
                  child: const Row(mainAxisSize: MainAxisSize.min, children: [
                    Icon(Icons.circle, color: _kGreen, size: 8),
                    SizedBox(width: 4),
                    Text('En ligne', style: TextStyle(color: _kGreen, fontSize: 10, fontWeight: FontWeight.w600)),
                  ]),
                ),
                const SizedBox(width: 8),
                Icon(_showProfile ? Icons.expand_less : Icons.expand_more, color: Colors.white54, size: 18),
              ]),
              if (_showProfile) ...[
                const SizedBox(height: 10),
                const Divider(color: Colors.white12, height: 1),
                const SizedBox(height: 10),
                Row(children: [
                  _MemoryChip(Icons.school_outlined, 'Filiere', major.isNotEmpty ? major : 'Non renseignee'),
                  const SizedBox(width: 8),
                  _MemoryChip(Icons.calendar_today, 'Annee', year.isNotEmpty ? 'Annee $year' : '-'),
                  const SizedBox(width: 8),
                  _MemoryChip(Icons.language, 'Langue', 'Francais'),
                ]),
                const SizedBox(height: 6),
                const Text('L\'agent utilise ces informations automatiquement',
                    style: TextStyle(color: Colors.white38, fontSize: 10, fontStyle: FontStyle.italic)),
              ],
            ]),
          ),
        ),

      // â”€â”€ Active tasks
      if (_activeTasks.isNotEmpty)
        Container(
          color: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('Actions effectuees', style: TextStyle(fontSize: 11, color: Colors.grey, fontWeight: FontWeight.w600)),
            const SizedBox(height: 6),
            SizedBox(
              height: 32,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                itemCount: _activeTasks.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (_, i) {
                  final t = _activeTasks[i];
                  return Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: _kGreen.withAlpha(20),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: _kGreen.withAlpha(60)),
                    ),
                    child: Row(mainAxisSize: MainAxisSize.min, children: [
                      const Icon(Icons.check_circle, color: _kGreen, size: 13),
                      const SizedBox(width: 5),
                      Text(t.label, style: const TextStyle(fontSize: 11, color: _kGreen, fontWeight: FontWeight.w500)),
                      const SizedBox(width: 5),
                      Text(_fmt(t.time), style: const TextStyle(fontSize: 10, color: Colors.grey)),
                    ]),
                  );
                },
              ),
            ),
          ]),
        ),

      // â”€â”€ Chat messages
      Expanded(
        child: ListView.builder(
          controller: _scrollCtrl,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          itemCount: _msgs.length + (_isThinking ? 1 : 0),
          itemBuilder: (_, i) {
            if (i == _msgs.length && _isThinking) {
              return _ThinkingCard(steps: _steps);
            }
            final msg = _msgs[i];
            return msg.isUser ? _UserBubble(msg: msg) : _AgentBubble(msg: msg, onOpenPdf: _openPdf);
          },
        ),
      ),

      // â”€â”€ Quick actions chips
      Container(
        color: Colors.white,
        padding: const EdgeInsets.only(left: 12, right: 12, top: 8),
        child: SizedBox(
          height: 38,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: _quickActions.length,
            separatorBuilder: (_, __) => const SizedBox(width: 8),
            itemBuilder: (_, i) {
              final (label, icon, color) = _quickActions[i];
              return GestureDetector(
                onTap: () {
                  if (label == 'Convention de stage') {
                    _showConventionDialog();
                  } else if (label == 'Mon attestation de scolarite') {
                    _triggerAttestationFlow();
                  } else {
                    _send(label);
                  }
                },
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: color.withAlpha(20),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: color.withAlpha(80)),
                  ),
                  child: Row(mainAxisSize: MainAxisSize.min, children: [
                    Icon(icon, size: 14, color: color),
                    const SizedBox(width: 5),
                    Text(label, style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w500)),
                  ]),
                ),
              );
            },
          ),
        ),
      ),

      // â”€â”€ Text input
      Container(
        color: Colors.white,
        padding: const EdgeInsets.fromLTRB(12, 8, 12, 16),
        child: Row(children: [
          Expanded(
            child: TextField(
              controller: _inputCtrl,
              maxLines: 3,
              minLines: 1,
              enabled: !_isThinking,
              style: const TextStyle(fontSize: 14, color: Colors.black87),
              decoration: InputDecoration(
                hintText: 'Ecrivez votre demande...',
                hintStyle: TextStyle(color: Colors.grey.shade400, fontSize: 13),
                filled: true,
                fillColor: _kBg,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              ),
              onSubmitted: (v) => _send(v),
            ),
          ),
          const SizedBox(width: 8),
          AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            child: FloatingActionButton.small(
              heroTag: 'admin_send',
              backgroundColor: _isThinking ? Colors.grey.shade300 : _kPrimary,
              onPressed: _isThinking ? null : () => _send(_inputCtrl.text),
              child: _isThinking
                  ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.send, color: Colors.white, size: 18),
            ),
          ),
        ]),
      ),
    ]);
  }
}

// â”€â”€â”€ Thinking card with animated steps â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _ThinkingCard extends StatelessWidget {
  final List<_Step> steps;
  const _ThinkingCard({required this.steps});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16, right: 60),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(
          width: 32, height: 32,
          decoration: const BoxDecoration(color: _kPrimary, shape: BoxShape.circle),
          child: const Icon(Icons.smart_toy, color: Colors.white, size: 16),
        ),
        const SizedBox(width: 8),
        Expanded(child: Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: const BorderRadius.only(
              topRight: Radius.circular(16), bottomLeft: Radius.circular(16), bottomRight: Radius.circular(16)),
            boxShadow: [BoxShadow(color: Colors.black.withAlpha(10), blurRadius: 8, offset: const Offset(0, 2))],
            border: Border.all(color: _kPrimary.withAlpha(30)),
          ),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2, color: _kPrimary)),
              const SizedBox(width: 8),
              const Text('Agent en cours de traitement...',
                  style: TextStyle(fontSize: 12, color: _kPrimary, fontWeight: FontWeight.w600)),
            ]),
            const SizedBox(height: 12),
            ...steps.map((s) => Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: Row(children: [
                SizedBox(width: 18, height: 18, child: switch (s.status) {
                  _StepStatus.done    => const Icon(Icons.check_circle, color: _kGreen, size: 16),
                  _StepStatus.running => const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2, color: _kPrimary)),
                  _StepStatus.pending => Icon(Icons.radio_button_unchecked, color: Colors.grey.shade300, size: 16),
                }),
                const SizedBox(width: 8),
                Flexible(child: Text(
                  s.label,
                  style: TextStyle(
                    fontSize: 12,
                    color: switch (s.status) {
                      _StepStatus.done    => _kGreen,
                      _StepStatus.running => _kPrimary,
                      _StepStatus.pending => Colors.grey.shade400,
                    },
                    fontWeight: s.status == _StepStatus.running ? FontWeight.w600 : FontWeight.normal,
                  ),
                )),
              ]),
            )),
          ]),
        )),
      ]),
    );
  }
}

// â”€â”€â”€ User bubble â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _UserBubble extends StatelessWidget {
  final _Msg msg;
  const _UserBubble({required this.msg});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12, left: 60),
      child: Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
          decoration: const BoxDecoration(
            color: _kUserBg,
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(16), topRight: Radius.circular(4),
              bottomLeft: Radius.circular(16), bottomRight: Radius.circular(16)),
          ),
          child: Text(msg.text, style: const TextStyle(color: Colors.white, fontSize: 14)),
        ),
        Padding(
          padding: const EdgeInsets.only(top: 4),
          child: Text('${msg.time.hour.toString().padLeft(2, '0')}:${msg.time.minute.toString().padLeft(2, '0')}',
              style: const TextStyle(fontSize: 10, color: Colors.grey)),
        ),
      ]),
    );
  }
}

// â”€â”€â”€ Agent bubble â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _AgentBubble extends StatelessWidget {
  final _Msg msg;
  final Future<void> Function(String?, String?) onOpenPdf;
  const _AgentBubble({required this.msg, required this.onOpenPdf});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16, right: 40),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(
          width: 32, height: 32,
          decoration: const BoxDecoration(color: _kPrimary, shape: BoxShape.circle),
          child: const Icon(Icons.smart_toy, color: Colors.white, size: 16),
        ),
        const SizedBox(width: 8),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: _kAgentBg,
              borderRadius: const BorderRadius.only(
                topRight: Radius.circular(16), bottomLeft: Radius.circular(16), bottomRight: Radius.circular(16)),
              boxShadow: [BoxShadow(color: Colors.black.withAlpha(10), blurRadius: 8, offset: const Offset(0, 2))],
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Agent Administratif',
                  style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: _kPrimary)),
              const SizedBox(height: 6),
              Text(msg.text, style: const TextStyle(fontSize: 14, height: 1.5, color: Color(0xFF1A1A2E))),
            ]),
          ),

          // Action result card
          if (msg.action != null) ...[
            const SizedBox(height: 8),
            _ActionCard(action: msg.action!, onOpenPdf: onOpenPdf),
          ],

          Padding(
            padding: const EdgeInsets.only(top: 4, left: 4),
            child: Text('${msg.time.hour.toString().padLeft(2, '0')}:${msg.time.minute.toString().padLeft(2, '0')}',
                style: const TextStyle(fontSize: 10, color: Colors.grey)),
          ),
        ])),
      ]),
    );
  }
}

// â”€â”€â”€ Action result card â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _ActionCard extends StatelessWidget {
  final _ActionResult action;
  final Future<void> Function(String?, String?) onOpenPdf;
  const _ActionCard({required this.action, required this.onOpenPdf});

  @override
  Widget build(BuildContext context) {
    if (action.type == 'doc') {
      return Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: [_kGreen.withAlpha(20), _kGreen.withAlpha(5)]),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: _kGreen.withAlpha(80)),
        ),
        child: Row(children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(color: _kGreen.withAlpha(30), borderRadius: BorderRadius.circular(8)),
            child: const Icon(Icons.picture_as_pdf, color: _kGreen, size: 22),
          ),
          const SizedBox(width: 10),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('Document genere avec succes',
                style: TextStyle(color: _kGreen, fontWeight: FontWeight.bold, fontSize: 13)),
            if (action.docId != null)
              Text('Ref: ${action.docId!.substring(0, 8).toUpperCase()}',
                  style: const TextStyle(fontFamily: 'monospace', fontSize: 12, color: Colors.grey)),
          ])),
          if (!kIsWeb && action.docId != null)
            ElevatedButton.icon(
              onPressed: () => onOpenPdf(action.pdfBase64, action.docId),
              style: ElevatedButton.styleFrom(
                backgroundColor: _kGreen,
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20))),
              icon: const Icon(Icons.download, size: 14, color: Colors.white),
              label: const Text('PDF', style: TextStyle(fontSize: 12, color: Colors.white)),
            )
          else if (kIsWeb && action.docId != null)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(color: _kGreen.withAlpha(30), borderRadius: BorderRadius.circular(20)),
              child: const Text('PDF pret', style: TextStyle(fontSize: 11, color: _kGreen, fontWeight: FontWeight.w600)),
            ),
        ]),
      );
    }
    return const SizedBox.shrink();
  }
}

// ─── Attestation: missing fields form sheet ───────────────────────────────────
class _AttestationMissingFieldsSheet extends StatefulWidget {
  final Map<String, String> missingFields;
  const _AttestationMissingFieldsSheet({required this.missingFields});
  @override
  State<_AttestationMissingFieldsSheet> createState() =>
      _AttestationMissingFieldsSheetState();
}

class _AttestationMissingFieldsSheetState
    extends State<_AttestationMissingFieldsSheet> {
  final Map<String, TextEditingController> _ctrl = {};
  String? _selectedYear;

  static const _filiereSuggestions = [
    'Intelligence Artificielle',
    'Genie Informatique',
    'Robotique et Objets Connectes',
    'Reseaux et Systemes',
  ];

  @override
  void initState() {
    super.initState();
    for (final key in widget.missingFields.keys) {
      if (key != 'year') _ctrl[key] = TextEditingController();
    }
  }

  @override
  void dispose() {
    for (final c in _ctrl.values) c.dispose();
    super.dispose();
  }

  String _hint(String key) {
    switch (key) {
      case 'cne':            return 'Ex : R137526890';
      case 'cin':            return 'Ex : AB123456';
      case 'date_naissance': return 'JJ/MM/AAAA';
      case 'major':          return 'Ex : Intelligence Artificielle';
      default:               return '';
    }
  }

  void _submit() {
    final data = <String, dynamic>{};
    for (final entry in widget.missingFields.entries) {
      if (entry.key == 'year') {
        if (_selectedYear == null) {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
            content: Text('Veuillez selectionner votre niveau'),
            backgroundColor: Colors.orange,
          ));
          return;
        }
        data['year'] = int.parse(_selectedYear!);
      } else {
        final val = _ctrl[entry.key]?.text.trim() ?? '';
        if (val.isEmpty) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('Veuillez remplir : ${entry.value}'),
            backgroundColor: Colors.orange,
          ));
          return;
        }
        data[entry.key] = val;
      }
    }
    Navigator.pop(context, data);
  }

  @override
  Widget build(BuildContext context) {
    final bottom = MediaQuery.of(context).viewInsets.bottom;
    return SingleChildScrollView(
      padding: EdgeInsets.fromLTRB(24, 24, 24, bottom + 24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Row(children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: _kPrimary.withAlpha(20),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.school_outlined, color: _kPrimary, size: 22),
            ),
            const SizedBox(width: 12),
            const Expanded(child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Completer votre profil',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
                Text('Informations manquantes pour l\'attestation',
                    style: TextStyle(fontSize: 12, color: Colors.grey)),
              ],
            )),
            IconButton(
              icon: const Icon(Icons.close, color: Colors.grey),
              onPressed: () => Navigator.pop(context, null),
            ),
          ]),
          const SizedBox(height: 10),
          // Info banner
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: BoxDecoration(
              color: Colors.blue.shade50,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.blue.shade100),
            ),
            child: Row(children: [
              Icon(Icons.info_outline, color: Colors.blue.shade700, size: 16),
              const SizedBox(width: 8),
              const Expanded(child: Text(
                'Ces informations seront sauvegardees dans votre profil pour vos prochaines demandes.',
                style: TextStyle(fontSize: 12, color: Color(0xFF1565C0)),
              )),
            ]),
          ),
          const SizedBox(height: 20),

          // Dynamic fields
          ...widget.missingFields.entries.map((entry) => Padding(
            padding: const EdgeInsets.only(bottom: 18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(entry.value,
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                const SizedBox(height: 8),
                if (entry.key == 'year')
                  DropdownButtonFormField<String>(
                    value: _selectedYear,
                    decoration: InputDecoration(
                      hintText: 'Selectionnez votre annee',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
                    ),
                    items: const [
                      DropdownMenuItem(value: '1', child: Text('1ere annee')),
                      DropdownMenuItem(value: '2', child: Text('2eme annee')),
                      DropdownMenuItem(value: '3', child: Text('3eme annee')),
                    ],
                    onChanged: (v) => setState(() => _selectedYear = v),
                  )
                else if (entry.key == 'major')
                  DropdownButtonFormField<String>(
                    value: null,
                    decoration: InputDecoration(
                      hintText: _hint('major'),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
                    ),
                    items: _filiereSuggestions
                        .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                        .toList(),
                    onChanged: (v) { if (v != null) _ctrl['major']?.text = v; },
                  )
                else
                  TextField(
                    controller: _ctrl[entry.key],
                    keyboardType: entry.key == 'date_naissance'
                        ? TextInputType.datetime : TextInputType.text,
                    style: const TextStyle(fontSize: 14, color: Colors.black87),
                    decoration: InputDecoration(
                      hintText: _hint(entry.key),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
                    ),
                  ),
              ],
            ),
          )),

          // Submit button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _submit,
              icon: const Icon(Icons.picture_as_pdf),
              label: const Text('Generer mon attestation',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
              style: ElevatedButton.styleFrom(
                backgroundColor: _kPrimary,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 15),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ─── Convention de Stage modal sheet ─────────────────────────────────────────
// Owns all TextEditingControllers; Flutter disposes them after the close
// animation completes (when the widget is fully unmounted from the tree).
class _ConventionFormSheet extends StatefulWidget {
  const _ConventionFormSheet();

  @override
  State<_ConventionFormSheet> createState() => _ConventionFormSheetState();
}

class _ConventionFormSheetState extends State<_ConventionFormSheet> {
  final _entrepriseCtrl = TextEditingController();
  final _adresseCtrl    = TextEditingController();
  final _telephoneCtrl  = TextEditingController();
  final _faxCtrl        = TextEditingController();
  final _tuteurCtrl     = TextEditingController();
  final _posteCtrl      = TextEditingController();
  final _debutCtrl      = TextEditingController();
  final _finCtrl        = TextEditingController();

  @override
  void dispose() {
    _entrepriseCtrl.dispose();
    _adresseCtrl.dispose();
    _telephoneCtrl.dispose();
    _faxCtrl.dispose();
    _tuteurCtrl.dispose();
    _posteCtrl.dispose();
    _debutCtrl.dispose();
    _finCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom + 16,
        left: 20, right: 20, top: 20,
      ),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                    color: _kPurple.withAlpha(20),
                    borderRadius: BorderRadius.circular(8)),
                child: const Icon(Icons.business_center_outlined,
                    color: _kPurple, size: 20),
              ),
              const SizedBox(width: 10),
              const Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Convention de Stage',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  Text('Informations du stage',
                      style: TextStyle(color: Colors.grey, fontSize: 12)),
                ]),
              ),
              IconButton(
                  icon: const Icon(Icons.close, size: 20),
                  onPressed: () => Navigator.pop(context)),
            ]),
            const SizedBox(height: 12),
            const Divider(),
            const SizedBox(height: 12),

            // Fields
            _ConvFormField(
                ctrl: _entrepriseCtrl,
                label: 'Entreprise / Organisme *',
                hint: 'Ex: TechCorp Maroc',
                icon: Icons.business_outlined),
            const SizedBox(height: 10),
            _ConvFormField(
                ctrl: _adresseCtrl,
                label: "Adresse de l'entreprise",
                hint: 'Ex: 23 Rue Hassan II, Casablanca',
                icon: Icons.location_on_outlined),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _ConvFormField(
                  ctrl: _telephoneCtrl,
                  label: 'TÃ©lÃ©phone',
                  hint: 'Ex: +212 5XX XX XX XX',
                  icon: Icons.phone_outlined)),
              const SizedBox(width: 10),
              Expanded(child: _ConvFormField(
                  ctrl: _faxCtrl,
                  label: 'Fax',
                  hint: 'Ex: +212 5XX XX XX XX',
                  icon: Icons.fax_outlined)),
            ]),
            const SizedBox(height: 10),
            _ConvFormField(
                ctrl: _tuteurCtrl,
                label: 'Tuteur de stage',
                hint: 'Ex: M. Karim Alaoui',
                icon: Icons.person_outline),
            const SizedBox(height: 10),
            _ConvFormField(
                ctrl: _posteCtrl,
                label: 'Sujet / Poste',
                hint: "Ex: Developpement d'une API IA",
                icon: Icons.work_outline),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _ConvFormField(
                  ctrl: _debutCtrl,
                  label: 'Date de debut',
                  hint: 'JJ/MM/AAAA',
                  icon: Icons.calendar_today_outlined)),
              const SizedBox(width: 10),
              Expanded(child: _ConvFormField(
                  ctrl: _finCtrl,
                  label: 'Date de fin',
                  hint: 'JJ/MM/AAAA',
                  icon: Icons.event_outlined)),
            ]),
            const SizedBox(height: 8),
            Text('(*) Requis pour un document complet',
                style: TextStyle(
                    fontSize: 11,
                    color: Colors.grey.shade500,
                    fontStyle: FontStyle.italic)),
            const SizedBox(height: 16),

            // Buttons
            Row(children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: () => Navigator.pop(context),
                  style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Colors.grey)),
                  child: const Text('Annuler',
                      style: TextStyle(color: Colors.grey)),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                flex: 2,
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: _kPurple,
                      padding: const EdgeInsets.symmetric(vertical: 12)),
                  icon: const Icon(Icons.picture_as_pdf,
                      color: Colors.white, size: 16),
                  label: const Text('Generer le PDF',
                      style: TextStyle(color: Colors.white,
                          fontWeight: FontWeight.bold)),
                  onPressed: () {
                    final entreprise = _entrepriseCtrl.text.trim();
                    if (entreprise.isEmpty) {
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
                        content: Text("Veuillez saisir le nom de l'entreprise"),
                        backgroundColor: _kOrange,
                        duration: Duration(seconds: 2),
                      ));
                      return;
                    }
                    Navigator.pop(context, {
                      'entreprise': entreprise,
                      'adresse':    _adresseCtrl.text.trim(),
                      'telephone':  _telephoneCtrl.text.trim(),
                      'fax':        _faxCtrl.text.trim(),
                      'tuteur':     _tuteurCtrl.text.trim(),
                      'poste':      _posteCtrl.text.trim(),
                      'debut':      _debutCtrl.text.trim(),
                      'fin':        _finCtrl.text.trim(),
                    });
                  },
                ),
              ),
            ]),
          ],
        ),
      ),
    );
  }
}

// â”€â”€â”€ Convention de Stage form field â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _ConvFormField extends StatelessWidget {
  final TextEditingController ctrl;
  final String label;
  final String hint;
  final IconData icon;
  const _ConvFormField(
      {required this.ctrl,
      required this.label,
      required this.hint,
      required this.icon});

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: ctrl,
      style: const TextStyle(fontSize: 13, color: Colors.black87),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        hintStyle: TextStyle(fontSize: 12, color: Colors.grey.shade400),
        prefixIcon: Icon(icon, size: 18, color: _kPrimary),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        isDense: true,
      ),
    );
  }
}

// â”€â”€â”€ Memory chip â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _MemoryChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _MemoryChip(this.icon, this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.white.withAlpha(10),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.white24),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Icon(icon, size: 11, color: Colors.white54),
          const SizedBox(width: 4),
          Text(label, style: const TextStyle(color: Colors.white54, fontSize: 9)),
        ]),
        const SizedBox(height: 2),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600), maxLines: 1, overflow: TextOverflow.ellipsis),
      ]),
    ));
  }
}

// â”€â”€â”€ Documents Tab â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _DocumentsTab extends ConsumerStatefulWidget {
  const _DocumentsTab();
  @override
  ConsumerState<_DocumentsTab> createState() => _DocumentsTabState();
}

class _DocumentsTabState extends ConsumerState<_DocumentsTab> {
  List<dynamic> _docs = [];
  bool _loading = true;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final data = await ref.read(apiServiceProvider).getAdminRequests();
      if (mounted) setState(() => _docs = data.where((r) => r['doc_id'] != null).toList());
    } catch (_) {}
    finally { if (mounted) setState(() => _loading = false); }
  }

  Future<void> _download(String docId, String docType) async {
    if (kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Telechargement disponible sur l\'app mobile'), backgroundColor: _kOrange));
      return;
    }
    try {
      final bytes = await ref.read(apiServiceProvider).downloadDocumentBytes(docId);
      final dir   = await getTemporaryDirectory();
      final file  = File('${dir.path}/${docType.replaceAll(' ', '_')}_${docId.substring(0, 8)}.pdf');
      await file.writeAsBytes(bytes);
      await OpenFile.open(file.path);
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erreur: $e'), backgroundColor: Colors.red));
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_docs.isEmpty) {
      return Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
        Icon(Icons.picture_as_pdf_outlined, size: 60, color: Colors.grey.shade300),
        const SizedBox(height: 12),
        const Text('Aucun document genere', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        const Text('Utilisez l\'Agent pour generer vos documents', style: TextStyle(color: Colors.grey, fontSize: 13)),
      ]));
    }
    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _docs.length,
        itemBuilder: (ctx, i) {
          final d  = _docs[i];
          final id = d['doc_id'] as String?;
          return Card(
            margin: const EdgeInsets.only(bottom: 10),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: ListTile(
              leading: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8)),
                child: const Icon(Icons.picture_as_pdf, color: Colors.red, size: 22),
              ),
              title: Text(d['request_type'] as String? ?? 'Document',
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
              subtitle: Text((d['created_at'] as String? ?? '').length >= 10
                  ? 'Genere le ${(d['created_at'] as String).substring(0, 10)}' : '',
                  style: const TextStyle(fontSize: 11)),
              trailing: id != null ? IconButton(
                icon: const Icon(Icons.download, color: _kPrimary),
                onPressed: () => _download(id, d['request_type'] as String? ?? 'doc'),
              ) : null,
            ),
          );
        },
      ),
    );
  }
}

// â”€â”€â”€ Demandes Tab â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class _DemandesTab extends ConsumerStatefulWidget {
  const _DemandesTab();
  @override
  ConsumerState<_DemandesTab> createState() => _DemandesTabState();
}

class _DemandesTabState extends ConsumerState<_DemandesTab> {
  List<dynamic> _items = [];
  bool _loading = true;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final data = await ref.read(apiServiceProvider).getAdminRequests();
      if (mounted) setState(() => _items = data);
    } catch (_) {}
    finally { if (mounted) setState(() => _loading = false); }
  }

  String _label(String s) {
    const m = {'pending': 'En attente', 'in_progress': 'En cours', 'validated': 'Validee', 'refused': 'Refusee'};
    return m[s] ?? s;
  }

  Color _color(String s) {
    switch (s) {
      case 'validated': return _kGreen;
      case 'in_progress': return const Color(0xFF1565C0);
      case 'refused': return const Color(0xFFC62828);
      default: return _kOrange;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_items.isEmpty) return Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
      Icon(Icons.assignment_outlined, size: 60, color: Colors.grey.shade300),
      const SizedBox(height: 12),
      const Text('Aucune demande', style: TextStyle(fontWeight: FontWeight.bold)),
      const SizedBox(height: 4),
      const Text('Demandez via l\'Agent IA', style: TextStyle(color: Colors.grey, fontSize: 13)),
    ]));

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _items.length,
        itemBuilder: (_, i) {
          final r      = _items[i];
          final status = r['status'] as String? ?? 'pending';
          final color  = _color(status);
          final steps  = ['En attente', 'En cours', 'Validee'];
          final idx    = status == 'validated' ? 2 : status == 'in_progress' ? 1 : 0;
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            child: Padding(padding: const EdgeInsets.all(14), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                const Icon(Icons.picture_as_pdf, color: Colors.red, size: 18),
                const SizedBox(width: 8),
                Expanded(child: Text(r['request_type'] as String? ?? '',
                    style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13))),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(color: color.withAlpha(30), borderRadius: BorderRadius.circular(10)),
                  child: Text(_label(status), style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.bold)),
                ),
              ]),
              const SizedBox(height: 10),
              if (status != 'refused')
                Row(children: List.generate(steps.length, (j) {
                  final done = j <= idx;
                  final last = j == steps.length - 1;
                  return Expanded(child: Row(children: [
                    Expanded(child: Column(children: [
                      Container(width: 20, height: 20,
                        decoration: BoxDecoration(color: done ? _kGreen : Colors.grey.shade200, shape: BoxShape.circle),
                        child: Center(child: Icon(done ? Icons.check : Icons.circle, size: 11,
                            color: done ? Colors.white : Colors.grey.shade400))),
                      const SizedBox(height: 3),
                      Text(steps[j], textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 9, color: done ? _kGreen : Colors.grey,
                              fontWeight: done ? FontWeight.w600 : FontWeight.normal)),
                    ])),
                    if (!last) Expanded(child: Container(height: 2, margin: const EdgeInsets.only(bottom: 16),
                        color: idx > j ? _kGreen : Colors.grey.shade200)),
                  ]));
                })),
            ])),
          );
        },
      ),
    );
  }
}
