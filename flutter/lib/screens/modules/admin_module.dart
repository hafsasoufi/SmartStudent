import 'dart:async';
import 'dart:convert';
import 'dart:io' show File;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:open_file/open_file.dart';
import 'package:path_provider/path_provider.dart';
import '../../services/api_service.dart';

// ─── Palette ─────────────────────────────────────────────────────────────────
const _kPrimary  = Color(0xFF0052A5);
const _kDark     = Color(0xFF0A1628);
const _kGreen    = Color(0xFF1B8A4E);
const _kOrange   = Color(0xFFE65100);
const _kPurple   = Color(0xFF6A1B9A);
const _kBg       = Color(0xFFF0F4FA);
const _kAgentBg  = Color(0xFFFFFFFF);
const _kUserBg   = Color(0xFF0052A5);

// ─── Data models ─────────────────────────────────────────────────────────────

enum _StepStatus { pending, running, done }

class _Step {
  final String label;
  _StepStatus status = _StepStatus.pending;
  _Step(this.label);
}

class _ActionResult {
  final String type;           // doc | ticket | status | info
  final String? docId;
  final String? pdfBase64;
  final String? ticketId;
  final String? requestId;

  const _ActionResult({
    required this.type,
    this.docId,
    this.pdfBase64,
    this.ticketId,
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

// ─── Step inference ───────────────────────────────────────────────────────────
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
  if (m.contains('releve') || m.contains('notes') || m.contains('moyenne')) {
    return [
      _Step('Analyse de votre demande'),
      _Step('Recuperation de vos notes'),
      _Step('Calcul de la moyenne generale'),
      _Step('Generation du releve officiel'),
      _Step('Archivage et validation'),
    ];
  }
  if (m.contains('convention') || (m.contains('stage') && !m.contains('certificat'))) {
    return [
      _Step('Analyse de votre demande'),
      _Step('Verification du profil etudiant'),
      _Step('Preparation de la convention'),
      _Step('Generation du document officiel'),
      _Step('Archivage et validation'),
    ];
  }
  if (m.contains('reclamation') || m.contains('probleme') || m.contains('plainte') || m.contains('signalement')) {
    return [
      _Step('Analyse de votre reclamation'),
      _Step('Classification automatique'),
      _Step('Creation du ticket de suivi'),
      _Step('Attribution du numero COMP'),
      _Step('Confirmation d\'enregistrement'),
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

// ─── AdminModule ──────────────────────────────────────────────────────────────
class AdminModule extends ConsumerStatefulWidget {
  const AdminModule({Key? key}) : super(key: key);
  @override
  ConsumerState<AdminModule> createState() => _AdminModuleState();
}

class _AdminModuleState extends ConsumerState<AdminModule>
    with SingleTickerProviderStateMixin {
  late TabController _tab;

  @override
  void initState() { super.initState(); _tab = TabController(length: 4, vsync: this); }
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
            Text('Agent Administratif', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white)),
            Text('ENIAD · Propulse par Groq Llama 3.3', style: TextStyle(fontSize: 10, color: Colors.white70)),
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
            Tab(icon: Icon(Icons.chat_bubble_outline, size: 18), text: 'Agent'),
            Tab(icon: Icon(Icons.folder_outlined,     size: 18), text: 'Documents'),
            Tab(icon: Icon(Icons.assignment_outlined, size: 18), text: 'Demandes'),
            Tab(icon: Icon(Icons.report_outlined,     size: 18), text: 'Reclamations'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tab,
        children: [
          _AgentTab(onSwitchTab: (i) => _tab.animateTo(i)),
          const _DocumentsTab(),
          const _DemandesTab(),
          const _ReclamationsTab(),
        ],
      ),
    );
  }
}

// ─── Agent Tab (main agentic interface) ──────────────────────────────────────
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
    ('Mon attestation de scolarite', Icons.school_outlined,      _kPrimary),
    ('Mon releve de notes',          Icons.grade_outlined,        _kGreen),
    ('Convention de stage',          Icons.business_center_outlined, _kPurple),
    ('Etat de mes demandes',         Icons.track_changes_outlined, Color(0xFF00695C)),
    ('Deposer une reclamation',      Icons.report_problem_outlined, _kOrange),
    ('Procedures ENIAD',             Icons.help_center_outlined,  Color(0xFF283593)),
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
      'Bonjour $name ! Je suis votre assistant administratif.\n\n'
      'Je peux vous aider a :\n'
      '• Obtenir une attestation de scolarite\n'
      '• Generer un releve de notes avec vos vraies notes\n'
      '• Preparer une convention de stage\n'
      '• Suivre vos demandes et reclamations\n'
      '• Repondre a vos questions sur les procedures ENIAD\n\n'
      'Que puis-je faire pour vous ?',
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
          _activeTasks.insert(0, _ActiveTask(label: label, done: true, ref: actionResult?.docId ?? actionResult?.ticketId, time: DateTime.now()));
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
    if (r['ticket_id'] != null) {
      return _ActionResult(type: 'ticket', ticketId: r['ticket_id'] as String?);
    }
    if (r['request_id'] != null) {
      return _ActionResult(type: 'request', requestId: r['request_id'] as String?);
    }
    return null;
  }

  String? _actionLabel(Map<String, dynamic> r) {
    if (r['doc_id'] != null)     return 'Document genere';
    if (r['ticket_id'] != null)  return 'Reclamation enregistree';
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
      // ── Student memory banner
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
                    Text('${major.isNotEmpty ? major : ''} ${year.isNotEmpty ? "· Annee $year" : ""}',
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

      // ── Active tasks
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

      // ── Chat messages
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

      // ── Quick actions chips
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
                onTap: () => _send(label),
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

      // ── Text input
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
              style: const TextStyle(fontSize: 14),
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

// ─── Thinking card with animated steps ───────────────────────────────────────
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

// ─── User bubble ──────────────────────────────────────────────────────────────
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

// ─── Agent bubble ─────────────────────────────────────────────────────────────
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

// ─── Action result card ───────────────────────────────────────────────────────
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
    if (action.type == 'ticket') {
      return Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: [_kOrange.withAlpha(20), _kOrange.withAlpha(5)]),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: _kOrange.withAlpha(80)),
        ),
        child: Row(children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(color: _kOrange.withAlpha(30), borderRadius: BorderRadius.circular(8)),
            child: const Icon(Icons.confirmation_number, color: _kOrange, size: 22),
          ),
          const SizedBox(width: 10),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('Reclamation enregistree', style: TextStyle(color: _kOrange, fontWeight: FontWeight.bold, fontSize: 13)),
            if (action.ticketId != null)
              Text('Ticket: ${action.ticketId}',
                  style: const TextStyle(fontFamily: 'monospace', fontSize: 12, color: Colors.grey)),
            const Text('Traitement sous 48h ouvrables', style: TextStyle(fontSize: 11, color: Colors.grey)),
          ]),
        ]),
      );
    }
    return const SizedBox.shrink();
  }
}

// ─── Memory chip ─────────────────────────────────────────────────────────────
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

// ─── Documents Tab ────────────────────────────────────────────────────────────
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

// ─── Demandes Tab ─────────────────────────────────────────────────────────────
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

// ─── Reclamations Tab ─────────────────────────────────────────────────────────
class _ReclamationsTab extends ConsumerStatefulWidget {
  const _ReclamationsTab();
  @override
  ConsumerState<_ReclamationsTab> createState() => _ReclamationsTabState();
}

class _ReclamationsTabState extends ConsumerState<_ReclamationsTab> {
  List<dynamic> _items = [];
  bool _loading = true;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final data = await ref.read(apiServiceProvider).getComplaints();
      if (mounted) setState(() => _items = data);
    } catch (_) {}
    finally { if (mounted) setState(() => _loading = false); }
  }

  Color _color(String s) {
    switch (s) {
      case 'resolved': return _kGreen;
      case 'in_progress': return const Color(0xFF1565C0);
      case 'closed': return Colors.grey;
      default: return _kOrange;
    }
  }

  String _label(String s) {
    const m = {'open': 'Ouverte', 'in_progress': 'En cours', 'resolved': 'Resolue', 'closed': 'Fermee'};
    return m[s] ?? s;
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_items.isEmpty) return Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
      Icon(Icons.report_outlined, size: 60, color: Colors.grey.shade300),
      const SizedBox(height: 12),
      const Text('Aucune reclamation', style: TextStyle(fontWeight: FontWeight.bold)),
      const SizedBox(height: 4),
      const Text('Dites a l\'Agent "je veux deposer une reclamation"', style: TextStyle(color: Colors.grey, fontSize: 13)),
    ]));

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _items.length,
        itemBuilder: (_, i) {
          final c      = _items[i];
          final status = c['status'] as String? ?? 'open';
          final color  = _color(status);
          return Card(
            margin: const EdgeInsets.only(bottom: 10),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(padding: const EdgeInsets.all(14), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(color: const Color(0xFF0052A5).withAlpha(15), borderRadius: BorderRadius.circular(6)),
                  child: Text(c['id'] as String? ?? '',
                      style: const TextStyle(fontFamily: 'monospace', fontWeight: FontWeight.bold, fontSize: 12, color: _kPrimary)),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(color: color.withAlpha(30), borderRadius: BorderRadius.circular(10)),
                  child: Text(_label(status), style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.bold)),
                ),
              ]),
              const SizedBox(height: 8),
              Text(c['category'] as String? ?? '', style: TextStyle(fontSize: 12, color: Colors.grey.shade600, fontStyle: FontStyle.italic)),
              const SizedBox(height: 4),
              Text(
                (c['description'] as String? ?? '').length > 120
                    ? '${(c['description'] as String).substring(0, 120)}...'
                    : (c['description'] as String? ?? ''),
                style: const TextStyle(fontSize: 13, height: 1.4),
              ),
              const SizedBox(height: 6),
              Text('Cree le: ${(c['created_at'] as String? ?? '').length >= 10 ? (c['created_at'] as String).substring(0, 10) : ''}',
                  style: const TextStyle(fontSize: 10, color: Colors.grey)),
            ])),
          );
        },
      ),
    );
  }
}
