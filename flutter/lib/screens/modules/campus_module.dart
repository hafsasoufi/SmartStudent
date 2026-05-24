import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/event_model.dart';
import '../../providers/campus_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';

class CampusModule extends ConsumerStatefulWidget {
  const CampusModule({Key? key}) : super(key: key);

  @override
  ConsumerState<CampusModule> createState() => _CampusModuleState();
}

class _CampusModuleState extends ConsumerState<CampusModule> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(campusProvider.notifier).loadEvents());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Vie de Campus'), elevation: 0),
      body: DefaultTabController(
        length: 4,
        child: Column(
          children: [
            const TabBar(
              isScrollable: true,
              tabs: [
                Tab(icon: Icon(Icons.smart_toy), text: 'Agent IA'),
                Tab(icon: Icon(Icons.event), text: 'Événements'),
                Tab(icon: Icon(Icons.people), text: 'Clubs'),
                Tab(icon: Icon(Icons.groups), text: 'Groupes'),
              ],
            ),
            Expanded(
              child: TabBarView(children: [
                ModuleAgentChat(
                  module: 'campus',
                  agentLabel: 'Agent Campus',
                  placeholder: 'Quels événements cette semaine à l\'ENIAD ?',
                  suggestions: [
                    'Événements cette semaine',
                    'Clubs disponibles à l\'ENIAD',
                    'Créer un groupe de travail',
                    'Activités parascolaires',
                    'Conférences à venir',
                  ],
                ),
                _EventsTab(),
                _ClubsTab(),
                _StudyGroupsTab(),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Onglet Événements (données réelles) ──────────────────────────────────────
class _EventsTab extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(campusProvider);

    if (state.isLoading) return const Center(child: CircularProgressIndicator());

    if (state.error != null) {
      return Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Icon(Icons.wifi_off, size: 48, color: Colors.grey),
          const SizedBox(height: 8),
          Text('Impossible de charger les événements',
              style: TextStyle(color: Colors.grey[600])),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: () => ref.read(campusProvider.notifier).loadEvents(),
            child: const Text('Réessayer'),
          ),
        ]),
      );
    }

    final events = state.upcoming;

    if (events.isEmpty) {
      return const Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.event_busy, size: 64, color: Colors.grey),
          SizedBox(height: 12),
          Text('Aucun événement à venir.',
              style: TextStyle(fontSize: 16, color: Colors.grey)),
        ]),
      );
    }

    return RefreshIndicator(
      onRefresh: () => ref.read(campusProvider.notifier).loadEvents(),
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: events.length,
        itemBuilder: (_, i) => _EventCard(event: events[i]),
      ),
    );
  }
}

class _EventCard extends StatelessWidget {
  final Event event;
  const _EventCard({required this.event});

  static const _typeColors = {
    'event': Colors.blue,
    'deadline': Colors.red,
    'conference': Colors.purple,
    'workshop': Colors.orange,
    'reminder': Colors.teal,
  };

  static const _typeLabels = {
    'event': 'Événement',
    'deadline': 'Deadline',
    'conference': 'Conférence',
    'workshop': 'Workshop',
    'reminder': 'Rappel',
  };

  @override
  Widget build(BuildContext context) {
    final color = _typeColors[event.eventType] ?? Colors.blue;
    final typeLabel = _typeLabels[event.eventType] ?? event.eventType;
    final date = event.startDate;
    final dateStr =
        '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
    final timeStr =
        '${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}';

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: color.withOpacity(0.3)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: color.withOpacity(0.15),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(typeLabel,
                  style: TextStyle(
                      fontSize: 11, color: color, fontWeight: FontWeight.bold)),
            ),
            const Spacer(),
            Text(dateStr,
                style: TextStyle(fontSize: 12, color: Colors.grey[600])),
          ]),
          const SizedBox(height: 8),
          Text(event.title,
              style: const TextStyle(
                  fontSize: 15, fontWeight: FontWeight.bold)),
          if (event.description != null && event.description!.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(event.description!,
                style: TextStyle(fontSize: 13, color: Colors.grey[700]),
                maxLines: 2,
                overflow: TextOverflow.ellipsis),
          ],
          const SizedBox(height: 8),
          Row(children: [
            if (event.location != null) ...[
              Icon(Icons.location_on, size: 14, color: Colors.grey[600]),
              const SizedBox(width: 4),
              Text(event.location!,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              const SizedBox(width: 12),
            ],
            Icon(Icons.access_time, size: 14, color: Colors.grey[600]),
            const SizedBox(width: 4),
            Text(timeStr,
                style: TextStyle(fontSize: 12, color: Colors.grey[600])),
          ]),
        ]),
      ),
    );
  }
}

// ── Onglet Clubs (statique pour l'instant) ───────────────────────────────────
class _ClubsTab extends StatelessWidget {
  static const _clubs = [
    {'name': 'Club IA & Data Science', 'members': 85, 'category': 'Technologie'},
    {'name': 'Club Entrepreneuriat', 'members': 120, 'category': 'Business'},
    {'name': 'Club Robotique', 'members': 60, 'category': 'Ingénierie'},
    {'name': 'Club Débat', 'members': 45, 'category': 'Communication'},
    {'name': 'Club Sport & Bien-être', 'members': 200, 'category': 'Sport'},
  ];

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _clubs.length,
      itemBuilder: (_, i) {
        final club = _clubs[i];
        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: AppTheme.primaryColor.withOpacity(0.15),
              child: Icon(Icons.group, color: AppTheme.primaryColor),
            ),
            title: Text(club['name'] as String,
                style: const TextStyle(fontWeight: FontWeight.w600)),
            subtitle: Text(
                '${club['category']} • ${club['members']} membres'),
            trailing: OutlinedButton(
              onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Rejoint : ${club['name']}')),
              ),
              child: const Text('Rejoindre'),
            ),
          ),
        );
      },
    );
  }
}

// ── Onglet Groupes de travail (statique) ─────────────────────────────────────
class _StudyGroupsTab extends StatelessWidget {
  static const _groups = [
    {'subject': 'Machine Learning', 'members': 6, 'meeting': 'Lun & Mer 17h', 'location': 'Salle Info 3'},
    {'subject': 'Algorithmes & Structures', 'members': 8, 'meeting': 'Mar & Jeu 16h', 'location': 'Bibliothèque'},
    {'subject': 'Bases de Données', 'members': 5, 'meeting': 'Ven 14h', 'location': 'Salle TP2'},
    {'subject': 'Réseaux & Sécurité', 'members': 7, 'meeting': 'Mer 15h', 'location': 'Labo Réseaux'},
  ];

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _groups.length,
      itemBuilder: (_, i) {
        final g = _groups[i];
        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                Text(g['subject'] as String,
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text('${g['members']} membres',
                      style: TextStyle(fontSize: 11, color: AppTheme.primaryColor)),
                ),
              ]),
              const SizedBox(height: 6),
              Row(children: [
                Icon(Icons.schedule, size: 14, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(g['meeting'] as String,
                    style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              ]),
              Row(children: [
                Icon(Icons.location_on, size: 14, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(g['location'] as String,
                    style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              ]),
              const SizedBox(height: 10),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Rejoint : ${g['subject']}')),
                  ),
                  child: const Text('Rejoindre le groupe'),
                ),
              ),
            ]),
          ),
        );
      },
    );
  }
}
