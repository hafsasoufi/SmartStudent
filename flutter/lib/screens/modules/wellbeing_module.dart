import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_service.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';

class WellbeingModule extends ConsumerStatefulWidget {
  const WellbeingModule({Key? key}) : super(key: key);

  @override
  ConsumerState<WellbeingModule> createState() => _WellbeingModuleState();
}

class _WellbeingModuleState extends ConsumerState<WellbeingModule> {
  int _moodRating = 3;
  bool _savingMood = false;
  List<Map<String, dynamic>> _moodHistory = [];

  @override
  void initState() {
    super.initState();
    Future.microtask(_loadMoodHistory);
  }

  Future<void> _loadMoodHistory() async {
    try {
      final api = ref.read(apiServiceProvider);
      final data = await api.getMoods();
      if (mounted) setState(() => _moodHistory = data.cast<Map<String, dynamic>>());
    } catch (_) {}
  }

  Future<void> _saveMood() async {
    if (_savingMood) return;
    setState(() => _savingMood = true);
    try {
      final api = ref.read(apiServiceProvider);
      await api.saveMood(rating: _moodRating);
      await _loadMoodHistory();
      if (mounted) {
        const labels = ['Très mal', 'Pas bien', 'Neutre', 'Bien', 'Excellent'];
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Humeur enregistrée : ${labels[_moodRating - 1]}'),
          backgroundColor: Colors.green,
          behavior: SnackBarBehavior.floating,
        ));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Erreur : $e'),
          backgroundColor: Colors.red,
        ));
      }
    } finally {
      if (mounted) setState(() => _savingMood = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bien-être Étudiant'), elevation: 0),
      body: DefaultTabController(
        length: 4,
        child: Column(children: [
          const TabBar(
            isScrollable: true,
            tabs: [
              Tab(icon: Icon(Icons.smart_toy), text: 'Agent IA'),
              Tab(icon: Icon(Icons.favorite_outline), text: 'Mon humeur'),
              Tab(icon: Icon(Icons.self_improvement), text: 'Conseils'),
              Tab(icon: Icon(Icons.phone_outlined), text: 'Support ENIAD'),
            ],
          ),
          Expanded(
            child: TabBarView(children: [
              const _AgentTab(),
              _MoodTab(
                moodRating: _moodRating,
                onMoodChanged: (v) => setState(() => _moodRating = v),
                onSave: _saveMood,
                isSaving: _savingMood,
                history: _moodHistory,
              ),
              const _ConseilsTab(),
              const _SupportTab(),
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
      module: 'wellbeing',
      agentLabel: 'Agent Bien-être',
      placeholder: 'Comment vous sentez-vous aujourd\'hui ?',
      suggestions: [
        'Je me sens stressé(e) par les examens',
        'J\'ai du mal à me concentrer',
        'Techniques de gestion du stress',
        'Je manque de motivation',
        'Comment mieux dormir ?',
      ],
    );
  }
}

// ── Tab Humeur ────────────────────────────────────────────────────────────────

class _MoodTab extends StatelessWidget {
  final int moodRating;
  final ValueChanged<int> onMoodChanged;
  final VoidCallback onSave;
  final bool isSaving;
  final List<Map<String, dynamic>> history;

  const _MoodTab({
    required this.moodRating,
    required this.onMoodChanged,
    required this.onSave,
    required this.isSaving,
    required this.history,
  });

  static const _moodEmojis = ['😞', '😕', '😐', '🙂', '😄'];
  static const _moodLabels = ['Très mal', 'Pas bien', 'Neutre', 'Bien', 'Excellent'];
  static const _moodColors = [
    Colors.red, Colors.orange, Colors.amber, Colors.lightGreen, Colors.green
  ];

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Comment vous sentez-vous aujourd\'hui ?',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 20),
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                AppTheme.primaryColor.withOpacity(0.05),
                AppTheme.primaryColor.withOpacity(0.1),
              ],
            ),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: List.generate(5, (i) {
                final selected = moodRating == i + 1;
                return GestureDetector(
                  onTap: () => onMoodChanged(i + 1),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: selected
                          ? _moodColors[i].withOpacity(0.2)
                          : Colors.transparent,
                      shape: BoxShape.circle,
                      border: selected
                          ? Border.all(color: _moodColors[i], width: 2)
                          : null,
                    ),
                    child: Text(_moodEmojis[i],
                        style: TextStyle(fontSize: selected ? 34 : 26)),
                  ),
                );
              }),
            ),
            const SizedBox(height: 12),
            Text(
              _moodLabels[moodRating - 1],
              style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: _moodColors[moodRating - 1]),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: isSaving ? null : onSave,
                icon: isSaving
                    ? const SizedBox(
                        width: 16, height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                      )
                    : const Icon(Icons.check),
                label: Text(isSaving ? 'Enregistrement...' : 'Enregistrer mon humeur'),
              ),
            ),
          ]),
        ),
        const SizedBox(height: 24),
        const Text('Suivi hebdomadaire',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        _WeekBar(history: history),
      ]),
    );
  }
}

class _WeekBar extends StatelessWidget {
  final List<Map<String, dynamic>> history;
  const _WeekBar({required this.history});

  static const _dayLabels = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
  static const _ratingColors = [
    Colors.red, Colors.orange, Colors.amber, Colors.lightGreen, Colors.green,
  ];

  @override
  Widget build(BuildContext context) {
    // Build 7-slot array: fill from history (oldest first), pad left with 0
    final values = List<int>.filled(7, 0);
    final recent = history.length > 7 ? history.sublist(history.length - 7) : history;
    final offset = 7 - recent.length;
    for (var i = 0; i < recent.length; i++) {
      values[offset + i] = (recent[i]['rating'] as int?) ?? 0;
    }

    // Day labels: last 7 days ending today
    final today = DateTime.now();
    final dayLabels = List.generate(7, (i) {
      final d = today.subtract(Duration(days: 6 - i));
      return _dayLabels[d.weekday - 1];
    });

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      crossAxisAlignment: CrossAxisAlignment.end,
      children: List.generate(7, (i) {
        final v = values[i];
        final color = v > 0 ? _ratingColors[v - 1] : Colors.grey.shade300;
        return Column(children: [
          AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            width: 32,
            height: v > 0 ? v * 10.0 : 6,
            decoration: BoxDecoration(
              color: color.withOpacity(0.75),
              borderRadius: BorderRadius.circular(4),
            ),
          ),
          const SizedBox(height: 4),
          Text(dayLabels[i], style: const TextStyle(fontSize: 12)),
        ]);
      }),
    );
  }
}

// ── Tab Conseils ──────────────────────────────────────────────────────────────

class _ConseilsTab extends StatelessWidget {
  const _ConseilsTab();

  static const _sections = [
    {
      'titre': 'Gérer le stress des examens',
      'items': [
        {'label': 'Technique Pomodoro', 'desc': '25 min de travail, 5 min de pause. Efficace pour rester concentré.', 'icon': Icons.timer},
        {'label': 'Cohérence cardiaque', 'desc': '5 respirations profondes/min pendant 5 min, 3 fois par jour.', 'icon': Icons.air},
        {'label': 'Planifier ses révisions', 'desc': 'Répartir les matières sur plusieurs jours, éviter le bachotage.', 'icon': Icons.calendar_today},
      ],
    },
    {
      'titre': 'Sommeil & Énergie',
      'items': [
        {'label': 'Règle des 8 heures', 'desc': 'Dormir 7-9h améliore la mémorisation et la concentration.', 'icon': Icons.nights_stay},
        {'label': 'Pas d\'écran avant dormir', 'desc': 'Éteindre les écrans 30 min avant de se coucher.', 'icon': Icons.no_photography},
        {'label': 'Réveil régulier', 'desc': 'Se lever à la même heure stabilise l\'horloge biologique.', 'icon': Icons.alarm},
      ],
    },
    {
      'titre': 'Alimentation & Activité',
      'items': [
        {'label': 'Hydratation', 'desc': 'Boire 1,5–2L d\'eau par jour améliore les fonctions cognitives.', 'icon': Icons.local_drink},
        {'label': 'Pause active', 'desc': '10 min de marche après chaque session de travail.', 'icon': Icons.directions_walk},
        {'label': 'Collations légères', 'desc': 'Fruits, noix : meilleure concentration que les sucreries.', 'icon': Icons.restaurant},
      ],
    },
  ];

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: _sections.map((section) {
        final items = section['items'] as List;
        return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Padding(
            padding: const EdgeInsets.only(bottom: 10, top: 6),
            child: Text(section['titre'] as String,
                style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
          ),
          ...items.map((item) => Card(
                margin: const EdgeInsets.only(bottom: 8),
                child: ListTile(
                  leading: Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppTheme.primaryColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(item['icon'] as IconData,
                        color: AppTheme.primaryColor, size: 20),
                  ),
                  title: Text(item['label'] as String,
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                  subtitle: Text(item['desc'] as String,
                      style: const TextStyle(fontSize: 12)),
                ),
              )),
          const SizedBox(height: 8),
        ]);
      }).toList(),
    );
  }
}

// ── Tab Support ENIAD ─────────────────────────────────────────────────────────

class _SupportTab extends StatelessWidget {
  const _SupportTab();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Bannière agent
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            gradient: LinearGradient(colors: [
              AppTheme.primaryColor.withOpacity(0.1),
              AppTheme.primaryColor.withOpacity(0.05),
            ]),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(children: [
            Icon(Icons.smart_toy, color: AppTheme.primaryColor, size: 32),
            const SizedBox(width: 12),
            const Expanded(
              child: Text(
                'L\'Agent Bien-être est disponible dans le tab "Agent IA" pour t\'écouter et te conseiller à tout moment.',
                style: TextStyle(fontSize: 13),
              ),
            ),
          ]),
        ),
        const SizedBox(height: 20),
        const Text('Services de soutien ENIAD',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        _ServiceCard(
          titre: 'Cellule d\'écoute ENIAD',
          desc: 'Soutien psychologique confidentiel pour les étudiants en difficulté.',
          contact: 'Secrétariat pédagogique, bâtiment principal',
          icon: Icons.psychology,
          color: Colors.purple,
        ),
        _ServiceCard(
          titre: 'Service de la scolarité',
          desc: 'Difficultés administratives, orientation, réorientation.',
          contact: 'Bâtiment administration • Lun–Ven 8h–16h',
          icon: Icons.school,
          color: Colors.blue,
        ),
        _ServiceCard(
          titre: 'Service médical UMP',
          desc: 'Centre médical universitaire, consultations gratuites.',
          contact: 'Campus UMP Oujda',
          icon: Icons.local_hospital,
          color: Colors.red,
        ),
        _ServiceCard(
          titre: 'Numéro d\'urgence nationale',
          desc: 'Ligne d\'écoute psychologique nationale 24h/24.',
          contact: '080 100 47 47 (gratuit)',
          icon: Icons.phone_in_talk,
          color: Colors.teal,
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.amber.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.amber.withOpacity(0.4)),
          ),
          child: Row(children: [
            const Icon(Icons.favorite, color: Colors.amber),
            const SizedBox(width: 10),
            const Expanded(
              child: Text(
                'Tu n\'es pas seul(e). Demander de l\'aide est un acte de courage. N\'hésite pas à parler à l\'Agent Bien-être ou à un conseiller.',
                style: TextStyle(fontSize: 13),
              ),
            ),
          ]),
        ),
      ]),
    );
  }
}

class _ServiceCard extends StatelessWidget {
  final String titre;
  final String desc;
  final String contact;
  final IconData icon;
  final Color color;

  const _ServiceCard({
    required this.titre,
    required this.desc,
    required this.contact,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
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
            child: Icon(icon, color: color, size: 24),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(titre,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
              const SizedBox(height: 4),
              Text(desc, style: TextStyle(fontSize: 12, color: Colors.grey[700])),
              const SizedBox(height: 6),
              Row(children: [
                Icon(Icons.location_on, size: 13, color: color),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(contact,
                      style: TextStyle(
                          fontSize: 12, color: color, fontWeight: FontWeight.w600)),
                ),
              ]),
            ]),
          ),
        ]),
      ),
    );
  }
}
