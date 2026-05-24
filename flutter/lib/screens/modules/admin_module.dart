import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';

class AdminModule extends ConsumerWidget {
  const AdminModule({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Administration ENIAD'), elevation: 0),
      body: DefaultTabController(
        length: 4,
        child: Column(children: [
          const TabBar(
            isScrollable: true,
            tabs: [
              Tab(icon: Icon(Icons.smart_toy), text: 'Agent IA'),
              Tab(icon: Icon(Icons.help_outline), text: 'FAQ'),
              Tab(icon: Icon(Icons.picture_as_pdf_outlined), text: 'Documents'),
              Tab(icon: Icon(Icons.assignment_outlined), text: 'Demandes'),
            ],
          ),
          const Expanded(
            child: TabBarView(children: [
              _AgentTab(),
              _FaqTab(),
              _DocumentsTab(),
              _DemandesTab(),
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
      module: 'admin',
      agentLabel: 'Agent Administratif',
      placeholder: 'Ex: Comment telecharger la convention de stage ?',
      suggestions: [
        'Emploi du temps IA S5',
        'Convention de stage PDF',
        'Calendrier examens',
        'Filieres disponibles a l\'ENIAD',
        'Inscription et scolarite',
      ],
    );
  }
}

// ── Tab FAQ ───────────────────────────────────────────────────────────────────

class _FaqTab extends StatelessWidget {
  const _FaqTab();

  static const _faqs = [
    {
      'q': 'Comment telecharger mon emploi du temps ?',
      'a': 'Rendez-vous sur eniad.ump.ma > Espace etudiant > Emplois du temps. Selectionnez votre filiere et semestre. Vous pouvez aussi demander a l\'Agent IA ci-dessus.',
    },
    {
      'q': 'Comment obtenir une attestation de scolarite ?',
      'a': 'Deposez une demande au service de la scolarite (batiment administration). Delai : 3 a 5 jours ouvrables. Munissez-vous de votre CNI et carte etudiant.',
    },
    {
      'q': 'Quand ont lieu les examens ?',
      'a': 'Les examens de fin de semestre automne sont generalement en janvier, ceux du semestre printemps en juin. Consultez le calendrier sur eniad.ump.ma.',
    },
    {
      'q': 'Comment telecharger la convention de stage ?',
      'a': 'Disponible sur eniad.ump.ma > Documents > Convention de stage. Faites-la signer par votre encadrant entreprise et l\'ENIAD avant le debut du stage.',
    },
    {
      'q': 'Quelles sont les filieres disponibles a l\'ENIAD ?',
      'a': 'L\'ENIAD propose 5 programmes : IA (Intelligence Artificielle), IRSI (Reseaux & Securite), ROC (Robotique & IoT), GINF (Genie Informatique), et le cycle preparatoire EPSI.',
    },
    {
      'q': 'Comment acceder a la plateforme e-learning ?',
      'a': 'Plateforme disponible sur eniadelearning.ump.ma. Utilisez vos identifiants universitaires (meme que le portail etudiant).',
    },
    {
      'q': 'Comment contacter l\'administration ?',
      'a': 'Email : eniad@ump.ac.ma\nTel : +212 536...\nHoraires : Lun-Ven 8h-16h\nBatiment principal, bureau de la scolarite.',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _faqs.length,
      itemBuilder: (_, i) {
        final faq = _faqs[i];
        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: ExpansionTile(
            tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            leading: Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: AppTheme.primaryColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(Icons.help_outline, color: AppTheme.primaryColor, size: 20),
            ),
            title: Text(faq['q']!,
                style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                child: Text(faq['a']!,
                    style: TextStyle(fontSize: 13, color: Colors.grey[700], height: 1.5)),
              ),
            ],
          ),
        );
      },
    );
  }
}

// ── Tab Documents ─────────────────────────────────────────────────────────────

class _DocumentsTab extends StatelessWidget {
  const _DocumentsTab();

  static const _sections = [
    {
      'titre': 'Emplois du temps 2025-2026',
      'docs': [
        {'nom': 'EDT IA S5 - Automne 2025-2026', 'prog': 'IA', 'url': 'https://eniad.ump.ma/storage/files/1/AA%20ET%2025-26/68fd0162b6a04.pdf'},
        {'nom': 'EDT IA S7 - Automne 2025-2026', 'prog': 'IA', 'url': 'https://eniad.ump.ma/storage/files/1/AA%20ET%2025-26/68fd01a89baf6.pdf'},
        {'nom': 'EDT IRSI S5 - Automne 2025-2026', 'prog': 'IRSI', 'url': 'https://eniad.ump.ma/storage/files/1/AA%20ET%2025-26/68fd016bd63d1.pdf'},
        {'nom': 'EDT GINF S5 - Automne 2025-2026', 'prog': 'GINF', 'url': 'https://eniad.ump.ma/storage/files/1/AA%20ET%2025-26/68fd0169cbf6e.pdf'},
        {'nom': 'EDT ROC S5 - Automne 2025-2026', 'prog': 'ROC', 'url': 'https://eniad.ump.ma/storage/files/1/AA%20ET%2025-26/68fd0170506c7.pdf'},
        {'nom': 'EDT EPSI S1 - Automne 2025-2026', 'prog': 'EPSI', 'url': 'https://eniad.ump.ma/storage/files/1/AA%20ET%2025-26/68fd014765fb7.pdf'},
      ],
    },
    {
      'titre': 'Documents administratifs',
      'docs': [
        {'nom': 'Convention de stage', 'prog': 'Tous', 'url': 'https://eniad.ump.ma/storage/files/1/convention_stage.pdf'},
        {'nom': 'Planning examens automne 2025', 'prog': 'Tous', 'url': 'https://eniad.ump.ma/storage/files/1/planning_examens_automne_2526.pdf'},
      ],
    },
  ];

  static const _progColors = {
    'IA': Colors.deepPurple,
    'IRSI': Colors.blue,
    'ROC': Colors.green,
    'GINF': Colors.orange,
    'EPSI': Colors.teal,
    'Tous': Colors.grey,
  };

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: _sections.map((section) {
        final docs = section['docs'] as List;
        return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Padding(
            padding: const EdgeInsets.only(bottom: 10, top: 6),
            child: Text(section['titre'] as String,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
          ),
          ...docs.map((doc) {
            final color = _progColors[doc['prog']] ?? Colors.grey;
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                leading: const Icon(Icons.picture_as_pdf, color: Colors.red),
                title: Text(doc['nom'] as String,
                    style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
                subtitle: Container(
                  margin: const EdgeInsets.only(top: 4),
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    doc['prog'] as String,
                    style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.bold),
                  ),
                ),
                trailing: IconButton(
                  icon: const Icon(Icons.open_in_browser, color: Colors.blue),
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Ouverture : ${doc['nom']}'),
                        action: SnackBarAction(
                          label: 'OK',
                          onPressed: () {},
                        ),
                      ),
                    );
                  },
                ),
              ),
            );
          }),
          const SizedBox(height: 8),
        ]);
      }).toList(),
    );
  }
}

// ── Tab Demandes ──────────────────────────────────────────────────────────────

class _DemandesTab extends StatefulWidget {
  const _DemandesTab();

  @override
  State<_DemandesTab> createState() => _DemandesTabState();
}

class _DemandesTabState extends State<_DemandesTab> {
  final _typeCtrl = TextEditingController();
  final _descCtrl = TextEditingController();
  String _selectedType = 'Attestation de scolarite';

  static const _types = [
    'Attestation de scolarite',
    'Releve de notes',
    'Certificat de stage',
    'Demande de redoublement',
    'Equivalence / Transfert',
    'Autre',
  ];

  @override
  void dispose() {
    _typeCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Nouvelle demande',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey.shade200),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(children: [
            DropdownButtonFormField<String>(
              value: _selectedType,
              decoration: InputDecoration(
                labelText: 'Type de demande',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
              ),
              items: _types
                  .map((t) => DropdownMenuItem(value: t, child: Text(t, style: const TextStyle(fontSize: 13))))
                  .toList(),
              onChanged: (v) => setState(() => _selectedType = v!),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _descCtrl,
              maxLines: 3,
              decoration: InputDecoration(
                labelText: 'Description / Motif',
                hintText: 'Precisions sur votre demande...',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  _descCtrl.clear();
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Demande "$_selectedType" soumise.'),
                      backgroundColor: Colors.green,
                    ),
                  );
                },
                icon: const Icon(Icons.send),
                label: const Text('Soumettre la demande'),
              ),
            ),
          ]),
        ),
        const SizedBox(height: 24),
        const Text('Mes demandes recentes',
            style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        _RequestCard(
            titre: 'Attestation de scolarite',
            statut: 'Approuve',
            date: '10 Jan 2026'),
        _RequestCard(
            titre: 'Releve de notes S5',
            statut: 'En attente',
            date: '05 Jan 2026'),
      ]),
    );
  }
}

class _RequestCard extends StatelessWidget {
  final String titre;
  final String statut;
  final String date;

  const _RequestCard({required this.titre, required this.statut, required this.date});

  @override
  Widget build(BuildContext context) {
    final isApproved = statut == 'Approuve';
    final color = isApproved ? Colors.green : Colors.orange;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        leading: Icon(
          isApproved ? Icons.check_circle_outline : Icons.hourglass_empty,
          color: color,
        ),
        title: Text(titre, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
        subtitle: Text(date, style: const TextStyle(fontSize: 12)),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: color.withOpacity(0.12),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(statut,
              style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
        ),
      ),
    );
  }
}
