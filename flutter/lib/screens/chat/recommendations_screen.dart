import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/auth_provider.dart';
import '../../services/api_service.dart';

// ─── Palette ─────────────────────────────────────────────────────────────────
const _kPrimary  = Color(0xFF0052A5);
const _kDark     = Color(0xFF0A1628);
const _kGreen    = Color(0xFF1B8A4E);
const _kOrange   = Color(0xFFE65100);
const _kPurple   = Color(0xFF6A1B9A);
const _kBg       = Color(0xFFF0F4FA);

// ─── Filieres & options ───────────────────────────────────────────────────────
const _filieres = [
  'Intelligence Artificielle',
  'Génie Informatique',
  'Robotique',
  'Réseaux & Systèmes',
];

const _annees = ['1ère année', '2ème année', '3ème année'];

const _typesDemande = [
  'Changement de filière',
  'Problème sur les notes',
  'Réclamation sur un examen',
  'Demande de documents (attestation, relevé…)',
  'Convention de stage',
  'Problème avec un module / dispense',
  'Bourse / aide sociale',
  'Problème technique (compte, WiFi…)',
  'PFE / mémoire',
  'Inscription / réinscription',
  'Problème administratif général',
  'Orientation professionnelle',
  'Autre',
];

// ─── Main screen ──────────────────────────────────────────────────────────────
class RecommendationsScreen extends ConsumerStatefulWidget {
  const RecommendationsScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<RecommendationsScreen> createState() =>
      _RecommendationsScreenState();
}

class _RecommendationsScreenState
    extends ConsumerState<RecommendationsScreen> {
  final _formKey       = GlobalKey<FormState>();
  final _prenomCtrl    = TextEditingController();
  final _nomCtrl       = TextEditingController();
  final _cneCtrl       = TextEditingController();
  final _descCtrl      = TextEditingController();

  String _filiere    = _filieres[0];
  String _annee      = _annees[0];
  String _typeDemande = _typesDemande[0];

  bool _loading = false;
  Map<String, dynamic>? _result;

  @override
  void initState() {
    super.initState();
    _prefillFromProfile();
  }

  void _prefillFromProfile() {
    final user = ref.read(authProvider).user;
    if (user == null) return;
    _prenomCtrl.text = user.firstName ?? (user.fullName.split(' ').isNotEmpty ? user.fullName.split(' ').first : '');
    _nomCtrl.text    = user.lastName  ?? (user.fullName.split(' ').length > 1   ? user.fullName.split(' ').skip(1).join(' ') : '');
  }

  @override
  void dispose() {
    _prenomCtrl.dispose();
    _nomCtrl.dispose();
    _cneCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() { _loading = true; _result = null; });
    try {
      final data = await ref.read(apiServiceProvider).generateRecommendations(
        prenom:      _prenomCtrl.text.trim(),
        nom:         _nomCtrl.text.trim(),
        cne:         _cneCtrl.text.trim(),
        filiere:     _filiere,
        annee:       _annee,
        typeDemande: _typeDemande,
        description: _descCtrl.text.trim(),
      );
      if (mounted) setState(() => _result = data);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erreur : $e'), backgroundColor: _kOrange),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _reset() => setState(() { _result = null; _descCtrl.clear(); });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _kBg,
      appBar: AppBar(
        backgroundColor: _kDark,
        title: Row(children: [
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(color: Colors.white.withAlpha(25), borderRadius: BorderRadius.circular(8)),
            child: const Icon(Icons.support_agent, color: Colors.white, size: 18),
          ),
          const SizedBox(width: 10),
          const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Assistance Administrative', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white)),
            Text('Support intelligent ENIAD', style: TextStyle(fontSize: 10, color: Colors.white70)),
          ]),
        ]),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.of(context).pop(),
        ),
        actions: [
          if (_result != null)
            IconButton(
              icon: const Icon(Icons.refresh, color: Colors.white),
              tooltip: 'Nouvelle demande',
              onPressed: _reset,
            ),
        ],
      ),
      body: _loading
          ? _buildLoading()
          : _result != null
              ? _buildResults(_result!)
              : _buildForm(),
    );
  }

  // ─── Loading ─────────────────────────────────────────────────────────────────
  Widget _buildLoading() => Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
    Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(20), boxShadow: [BoxShadow(color: Colors.black.withAlpha(10), blurRadius: 20)]),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        const SizedBox(width: 56, height: 56, child: CircularProgressIndicator(strokeWidth: 3, color: _kPrimary)),
        const SizedBox(height: 20),
        const Text('Analyse en cours…', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: _kDark)),
        const SizedBox(height: 6),
        Text('Identification du service et du processus adapté à votre situation', style: TextStyle(fontSize: 12, color: Colors.grey.shade600), textAlign: TextAlign.center),
      ]),
    ),
  ]));

  // ─── Form ────────────────────────────────────────────────────────────────────
  Widget _buildForm() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Form(
        key: _formKey,
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Header banner
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [_kPrimary, Color(0xFF1565C0)], begin: Alignment.topLeft, end: Alignment.bottomRight),
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Icon(Icons.support_agent, color: Colors.white, size: 28),
                SizedBox(width: 10),
                Expanded(child: Text('Obtenir de l\'aide administrative', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 17))),
              ]),
              SizedBox(height: 8),
              Text('Décrivez votre problème. Le système identifie automatiquement le bon service, le responsable et vous guide étape par étape jusqu\'à la résolution complète.', style: TextStyle(color: Colors.white70, fontSize: 12, height: 1.5)),
            ]),
          ),
          const SizedBox(height: 20),

          // Section: Informations personnelles
          _sectionHeader('Informations personnelles', Icons.person_outline),
          const SizedBox(height: 10),
          Row(children: [
            Expanded(child: _field(_prenomCtrl, 'Prénom *', Icons.badge_outlined,
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Requis' : null)),
            const SizedBox(width: 10),
            Expanded(child: _field(_nomCtrl, 'Nom *', Icons.badge_outlined,
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Requis' : null)),
          ]),
          const SizedBox(height: 12),
          _field(_cneCtrl, 'CNE / N° Carte étudiant', Icons.credit_card_outlined),
          const SizedBox(height: 20),

          // Section: Cursus
          _sectionHeader('Cursus universitaire', Icons.school_outlined),
          const SizedBox(height: 10),
          _dropdown<String>(
            label: 'Filière *',
            value: _filiere,
            icon: Icons.account_tree_outlined,
            items: _filieres,
            onChanged: (v) => setState(() => _filiere = v!),
          ),
          const SizedBox(height: 12),
          _dropdown<String>(
            label: 'Année d\'étude *',
            value: _annee,
            icon: Icons.timeline_outlined,
            items: _annees,
            onChanged: (v) => setState(() => _annee = v!),
          ),
          const SizedBox(height: 20),

          // Section: Demande
          _sectionHeader('Votre demande', Icons.help_outline),
          const SizedBox(height: 10),
          _dropdown<String>(
            label: 'Type de demande *',
            value: _typeDemande,
            icon: Icons.category_outlined,
            items: _typesDemande,
            onChanged: (v) => setState(() => _typeDemande = v!),
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: _descCtrl,
            maxLines: 5,
            decoration: InputDecoration(
              labelText: 'Description du problème *',
              hintText: 'Décrivez votre situation en détail. Plus vous êtes précis(e), meilleures seront les recommandations…',
              alignLabelWithHint: true,
              prefixIcon: const Padding(padding: EdgeInsets.only(bottom: 80), child: Icon(Icons.description_outlined, size: 20)),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              filled: true,
              fillColor: Colors.white,
              contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
            ),
            validator: (v) => (v == null || v.trim().length < 15) ? 'Minimum 15 caractères' : null,
          ),
          const SizedBox(height: 8),

          // Hint
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: _kPrimary.withAlpha(12), borderRadius: BorderRadius.circular(8)),
            child: const Row(children: [
              Icon(Icons.info_outline, size: 15, color: _kPrimary),
              SizedBox(width: 8),
              Expanded(child: Text('Le système identifie automatiquement le service compétent, le responsable et génère un processus guidé étape par étape.', style: TextStyle(fontSize: 11, color: _kPrimary))),
            ]),
          ),
          const SizedBox(height: 20),

          // Submit
          SizedBox(width: double.infinity, child: ElevatedButton.icon(
            onPressed: _loading ? null : _submit,
            style: ElevatedButton.styleFrom(
              backgroundColor: _kPrimary,
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              elevation: 2,
            ),
            icon: const Icon(Icons.support_agent, color: Colors.white, size: 20),
            label: const Text('Analyser ma situation', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15)),
          )),
          const SizedBox(height: 30),
        ]),
      ),
    );
  }

  // ─── Results ─────────────────────────────────────────────────────────────────
  Widget _buildResults(Map<String, dynamic> data) {
    final student         = data['student'] as Map<String, dynamic>? ?? {};
    final recommendations = (data['recommendations'] as List<dynamic>? ?? [])
        .cast<Map<String, dynamic>>();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Student context summary
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            gradient: const LinearGradient(colors: [_kDark, Color(0xFF1A2A4A)], begin: Alignment.topLeft, end: Alignment.bottomRight),
            borderRadius: BorderRadius.circular(14),
          ),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Row(children: [
              Icon(Icons.person_pin_outlined, color: Colors.white70, size: 16),
              SizedBox(width: 6),
              Text('Analyse pour', style: TextStyle(color: Colors.white70, fontSize: 12)),
            ]),
            const SizedBox(height: 6),
            Text('${student['prenom'] ?? ''} ${student['nom'] ?? ''}'.trim(),
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 4),
            Row(children: [
              _infoBadge(student['filiere'] as String? ?? ''),
              const SizedBox(width: 8),
              _infoBadge(student['annee'] as String? ?? ''),
            ]),
            const SizedBox(height: 6),
            Text(student['type_demande'] as String? ?? '',
                style: const TextStyle(color: Colors.white60, fontSize: 12, fontStyle: FontStyle.italic)),
          ]),
        ),
        const SizedBox(height: 16),

        const Text('Résultat de l\'analyse — Service identifié',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: _kPrimary)),
        const SizedBox(height: 12),

        ...recommendations.asMap().entries.map((e) => _buildRecommendationCard(e.key, e.value)),

        const SizedBox(height: 16),
        SizedBox(width: double.infinity, child: OutlinedButton.icon(
          onPressed: _reset,
          icon: const Icon(Icons.edit_outlined, color: _kPrimary, size: 18),
          label: const Text('Modifier ma demande', style: TextStyle(color: _kPrimary, fontWeight: FontWeight.w600)),
          style: OutlinedButton.styleFrom(
            side: const BorderSide(color: _kPrimary),
            padding: const EdgeInsets.symmetric(vertical: 13),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
        )),
        const SizedBox(height: 30),
      ]),
    );
  }

  Widget _buildRecommendationCard(int index, Map<String, dynamic> rec) {
    final titre     = rec['titre'] as String? ?? '';
    final desc      = rec['description'] as String? ?? '';
    final priorite  = rec['priorite'] as int? ?? 2;
    final processus = rec['processus'] as Map<String, dynamic>? ?? {};

    final priColor = priorite == 1
        ? const Color(0xFFB71C1C)
        : priorite == 2
            ? _kOrange
            : _kGreen;
    final priLabel = priorite == 1 ? 'Urgent' : priorite == 2 ? 'Important' : 'Informatif';

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.black.withAlpha(8), blurRadius: 12, offset: const Offset(0, 4))],
        border: Border(left: BorderSide(color: priColor, width: 4)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Card header
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 10),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(color: priColor.withAlpha(20), borderRadius: BorderRadius.circular(6)),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.flag_rounded, size: 12, color: priColor),
                  const SizedBox(width: 4),
                  Text(priLabel, style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: priColor)),
                ]),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(color: _kPrimary.withAlpha(15), borderRadius: BorderRadius.circular(6)),
                child: const Row(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.support_agent, size: 11, color: _kPrimary),
                  SizedBox(width: 4),
                  Text('Guide administratif', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: _kPrimary)),
                ]),
              ),
            ]),
            const SizedBox(height: 10),
            Text(titre, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: _kDark)),
            const SizedBox(height: 8),
            Text(desc, style: const TextStyle(fontSize: 13, color: Color(0xFF444444), height: 1.5)),
          ]),
        ),

        const Divider(height: 1, color: Color(0xFFEEEEEE)),

        // Administrative process
        _buildProcessus(processus),
      ]),
    );
  }

  Widget _buildProcessus(Map<String, dynamic> p) {
    final service      = p['service']          as String? ?? '';
    final responsable  = p['responsable']      as String? ?? '';
    final email        = p['email']            as String? ?? '';
    final telephone    = p['telephone']        as String? ?? '';
    final docs         = (p['documents_requis'] as List<dynamic>? ?? []).cast<String>();
    final etapes       = (p['etapes']           as List<dynamic>? ?? []).cast<String>();
    final delai        = p['delai_estime']     as String? ?? '';
    final resultat     = p['resultat_attendu'] as String? ?? '';

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Section title
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFFF0F4FA),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: _kPrimary.withAlpha(30)),
          ),
          child: const Row(children: [
            Icon(Icons.account_balance_outlined, size: 16, color: _kPrimary),
            SizedBox(width: 8),
            Text('Service responsable & processus guidé', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: _kPrimary)),
          ]),
        ),
        const SizedBox(height: 14),

        // Service + Contact
        _processRow(Icons.business_outlined, 'Service concerné', service),
        const SizedBox(height: 10),
        _processRow(Icons.person_outlined, 'Responsable', responsable),
        if (email.isNotEmpty) ...[
          const SizedBox(height: 10),
          _processRow(Icons.email_outlined, 'Email', email),
        ],
        if (telephone.isNotEmpty) ...[
          const SizedBox(height: 10),
          _processRow(Icons.phone_outlined, 'Téléphone', telephone),
        ],

        if (docs.isNotEmpty) ...[
          const SizedBox(height: 16),
          _subTitle('Documents requis', Icons.folder_outlined),
          const SizedBox(height: 8),
          ...docs.map((d) => Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(width: 6, height: 6, margin: const EdgeInsets.fromLTRB(2, 6, 10, 0),
                  decoration: const BoxDecoration(color: _kPrimary, shape: BoxShape.circle)),
              Expanded(child: Text(d, style: const TextStyle(fontSize: 13, height: 1.4))),
            ]),
          )),
        ],

        if (etapes.isNotEmpty) ...[
          const SizedBox(height: 16),
          _subTitle('Étapes à suivre', Icons.checklist_outlined),
          const SizedBox(height: 8),
          ...etapes.asMap().entries.map((e) => Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFFF8FAFD),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.grey.shade200),
            ),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                width: 24, height: 24,
                decoration: BoxDecoration(color: _kPrimary, borderRadius: BorderRadius.circular(12)),
                child: Center(child: Text('${e.key + 1}', style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold))),
              ),
              const SizedBox(width: 10),
              Expanded(child: Text(
                e.value.replaceFirst(RegExp(r'^Étape\s*\d+\s*:\s*', caseSensitive: false), ''),
                style: const TextStyle(fontSize: 13, height: 1.4),
              )),
            ]),
          )),
        ],

        if (delai.isNotEmpty) ...[
          const SizedBox(height: 12),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: _kOrange.withAlpha(12),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: _kOrange.withAlpha(40)),
            ),
            child: Row(children: [
              const Icon(Icons.schedule_outlined, size: 18, color: _kOrange),
              const SizedBox(width: 10),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('Délai estimé', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: _kOrange)),
                Text(delai, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
              ])),
            ]),
          ),
        ],

        if (resultat.isNotEmpty) ...[
          const SizedBox(height: 10),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: _kGreen.withAlpha(12),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: _kGreen.withAlpha(40)),
            ),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Icon(Icons.check_circle_outline, size: 18, color: _kGreen),
              const SizedBox(width: 10),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('Résultat attendu', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: _kGreen)),
                const SizedBox(height: 2),
                Text(resultat, style: const TextStyle(fontSize: 13, height: 1.4)),
              ])),
            ]),
          ),
        ],
      ]),
    );
  }

  // ─── Helpers ─────────────────────────────────────────────────────────────────

  Widget _sectionHeader(String title, IconData icon) => Row(children: [
    Icon(icon, size: 18, color: _kPrimary),
    const SizedBox(width: 8),
    Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: _kDark)),
  ]);

  Widget _field(TextEditingController ctrl, String label, IconData icon,
      {String? Function(String?)? validator}) =>
      TextFormField(
        controller: ctrl,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, size: 20),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.white,
          contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        ),
        validator: validator,
      );

  Widget _dropdown<T>({
    required String label,
    required T value,
    required IconData icon,
    required List<T> items,
    required void Function(T?) onChanged,
  }) =>
      DropdownButtonFormField<T>(
        value: value,
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, size: 20),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
          fillColor: Colors.white,
          contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        ),
        items: items.map((i) => DropdownMenuItem<T>(value: i, child: Text(i.toString(), overflow: TextOverflow.ellipsis))).toList(),
        onChanged: onChanged,
        isExpanded: true,
      );

  Widget _infoBadge(String text) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
    decoration: BoxDecoration(color: Colors.white.withAlpha(25), borderRadius: BorderRadius.circular(6)),
    child: Text(text, style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w500)),
  );

  Widget _processRow(IconData icon, String label, String value) => Row(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Icon(icon, size: 16, color: _kPrimary),
      const SizedBox(width: 8),
      SizedBox(width: 90, child: Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.w500))),
      const SizedBox(width: 4),
      Expanded(child: Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500))),
    ],
  );

  Widget _subTitle(String t, IconData icon) => Row(children: [
    Icon(icon, size: 15, color: _kDark),
    const SizedBox(width: 6),
    Text(t, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: _kDark)),
  ]);
}
