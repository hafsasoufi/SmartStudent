import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';

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

class _TemplatesTab extends StatelessWidget {
  const _TemplatesTab();

  static const _items = [
    {
      'titre': 'Modèle CV Ingénieur Informatique',
      'desc': 'Format ATS-friendly pour les ESN marocaines (Capgemini, Atos, etc.)',
      'type': 'DOCX / PDF',
      'icon': Icons.person_outline,
    },
    {
      'titre': 'Lettre de motivation stage PFE',
      'desc': 'Template adapté aux stages de fin d\'études (3 mois / 6 mois)',
      'type': 'DOCX',
      'icon': Icons.description_outlined,
    },
    {
      'titre': 'CV en anglais (international)',
      'desc': 'Pour postuler aux programmes Google, Microsoft, entreprises EU',
      'type': 'DOCX / PDF',
      'icon': Icons.language,
    },
    {
      'titre': 'Guide LinkedIn pour ingénieurs',
      'desc': 'Optimiser son profil LinkedIn pour être recruté au Maroc',
      'type': 'PDF',
      'icon': Icons.people_outline,
    },
    {
      'titre': 'Préparation entretien technique',
      'desc': 'Algorithmes, structures de données, questions courantes',
      'type': 'PDF',
      'icon': Icons.quiz_outlined,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      Container(
        margin: const EdgeInsets.all(16),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: AppTheme.primaryColor.withOpacity(0.08),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Row(children: [
          Icon(Icons.smart_toy, color: AppTheme.primaryColor),
          const SizedBox(width: 10),
          const Expanded(
            child: Text(
              'l\'Agent IA peut générer un CV ou une LM personnalisée pour vous !',
              style: TextStyle(fontSize: 13),
            ),
          ),
        ]),
      ),
      Expanded(
        child: ListView.builder(
          padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
          itemCount: _items.length,
          itemBuilder: (_, i) {
            final item = _items[i];
            return Card(
              margin: const EdgeInsets.only(bottom: 10),
              child: ListTile(
                leading: Icon(item['icon'] as IconData, color: AppTheme.primaryColor),
                title: Text(item['titre'] as String,
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 2),
                    Text(item['desc'] as String, style: const TextStyle(fontSize: 12)),
                    const SizedBox(height: 4),
                    Text(item['type'] as String,
                        style: TextStyle(
                            fontSize: 11,
                            color: AppTheme.primaryColor,
                            fontWeight: FontWeight.bold)),
                  ],
                ),
                isThreeLine: true,
                trailing: IconButton(
                  icon: const Icon(Icons.file_download_outlined),
                  onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Téléchargement : ${item['titre']}')),
                  ),
                ),
              ),
            );
          },
        ),
      ),
    ]);
  }
}

// ── Tab Stages ────────────────────────────────────────────────────────────────

class _StagesTab extends StatelessWidget {
  const _StagesTab();

  static const _stages = [
    {
      'entreprise': 'OCP Group',
      'poste': 'Stage PFE — Intelligence Artificielle',
      'lieu': 'Khouribga, Maroc',
      'duree': '4–6 mois',
      'profil': 'IA / Data Science',
    },
    {
      'entreprise': 'Maroc Telecom',
      'poste': 'Stage PFE — Cybersécurité',
      'lieu': 'Rabat, Maroc',
      'duree': '4–6 mois',
      'profil': 'IRSI',
    },
    {
      'entreprise': 'Capgemini Maroc',
      'poste': 'Stage développement Full Stack',
      'lieu': 'Casablanca, Maroc',
      'duree': '2–6 mois',
      'profil': 'GINF / IA',
    },
    {
      'entreprise': 'INWI',
      'poste': 'Stage IoT & Réseaux',
      'lieu': 'Casablanca, Maroc',
      'duree': '3–6 mois',
      'profil': 'ROC / IRSI',
    },
    {
      'entreprise': 'UM6P Ventures',
      'poste': 'Stage Data Engineer',
      'lieu': 'Ben Guerir, Maroc',
      'duree': '3–4 mois',
      'profil': 'IA / GINF',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      Container(
        margin: const EdgeInsets.all(16),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.orange.withOpacity(0.08),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: Colors.orange.withOpacity(0.3)),
        ),
        child: Row(children: [
          const Icon(Icons.info_outline, color: Colors.orange),
          const SizedBox(width: 10),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Convention de stage ENIAD',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
              const SizedBox(height: 2),
              const Text('Téléchargez la convention sur eniad.ump.ma',
                  style: TextStyle(fontSize: 12)),
            ]),
          ),
        ]),
      ),
      Expanded(
        child: ListView.builder(
          padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
          itemCount: _stages.length,
          itemBuilder: (_, i) {
            final s = _stages[i];
            return Card(
              margin: const EdgeInsets.only(bottom: 10),
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(s['entreprise']!,
                          style: const TextStyle(
                              fontWeight: FontWeight.bold, fontSize: 15)),
                      _Badge(s['profil']!, AppTheme.primaryColor),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(s['poste']!,
                      style: TextStyle(fontSize: 13, color: Colors.grey[800])),
                  const SizedBox(height: 8),
                  Row(children: [
                    Icon(Icons.location_on, size: 14, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(s['lieu']!,
                        style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                    const SizedBox(width: 12),
                    Icon(Icons.schedule, size: 14, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(s['duree']!,
                        style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                  ]),
                  const SizedBox(height: 10),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                      onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Candidature : ${s['entreprise']}')),
                      ),
                      child: const Text('Voir l\'offre'),
                    ),
                  ),
                ]),
              ),
            );
          },
        ),
      ),
    ]);
  }
}
