import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/event_model.dart';
import '../../providers/campus_provider.dart';
import '../../theme/app_theme.dart';
import '../../widgets/module_agent_chat.dart';

class CampusModule extends ConsumerStatefulWidget {
  const CampusModule({super.key});

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
                const ModuleAgentChat(
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
                const _EventsTab(),
                const _ClubsTab(),
                _StudyGroupsTab(),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Onglet Événements (données réelles — passés + à venir) ───────────────────
class _EventsTab extends ConsumerStatefulWidget {
  const _EventsTab();
  @override
  ConsumerState<_EventsTab> createState() => _EventsTabState();
}

class _EventsTabState extends ConsumerState<_EventsTab> {
  // 0 = Tous, 1 = À venir, 2 = Passés
  int _filter = 0;

  @override
  Widget build(BuildContext context) {
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

    final all = state.all;
    final upcoming = state.upcoming;
    final past = state.past;

    final events = _filter == 1 ? upcoming : _filter == 2 ? past : all;

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
          child: Row(
            children: [
              _FilterChip(label: 'Tous (${all.length})', selected: _filter == 0,
                  onTap: () => setState(() => _filter = 0)),
              const SizedBox(width: 8),
              _FilterChip(label: 'À venir (${upcoming.length})', selected: _filter == 1,
                  color: Colors.green, onTap: () => setState(() => _filter = 1)),
              const SizedBox(width: 8),
              _FilterChip(label: 'Passés (${past.length})', selected: _filter == 2,
                  color: Colors.grey, onTap: () => setState(() => _filter = 2)),
            ],
          ),
        ),
        if (events.isEmpty)
          Expanded(
            child: Center(
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.event_busy, size: 64, color: Colors.grey),
                const SizedBox(height: 12),
                Text(
                  _filter == 1 ? 'Aucun événement à venir.' : 'Aucun événement.',
                  style: const TextStyle(fontSize: 16, color: Colors.grey),
                ),
              ]),
            ),
          )
        else
          Expanded(
            child: RefreshIndicator(
              onRefresh: () => ref.read(campusProvider.notifier).loadEvents(),
              child: ListView.builder(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
                itemCount: events.length,
                itemBuilder: (_, i) => _EventCard(event: events[i]),
              ),
            ),
          ),
      ],
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;
  final Color? color;
  final VoidCallback onTap;

  const _FilterChip({
    required this.label,
    required this.selected,
    this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final c = color ?? AppTheme.primaryColor;
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: selected ? c.withOpacity(0.15) : Colors.transparent,
          border: Border.all(color: selected ? c : Colors.grey[400]!),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: selected ? FontWeight.bold : FontWeight.normal,
            color: selected ? c : Colors.grey[600],
          ),
        ),
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

    final isPast = event.startDate.isBefore(DateTime.now());
    final effectiveColor = isPast ? Colors.grey : color;

    return Opacity(
      opacity: isPast ? 0.72 : 1.0,
      child: Card(
        margin: const EdgeInsets.only(bottom: 12),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(color: effectiveColor.withOpacity(0.3)),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: effectiveColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(typeLabel,
                    style: TextStyle(
                        fontSize: 11, color: effectiveColor, fontWeight: FontWeight.bold)),
              ),
              const SizedBox(width: 6),
              if (isPast)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                  decoration: BoxDecoration(
                    color: Colors.grey.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Text('Passé',
                      style: TextStyle(fontSize: 10, color: Colors.grey)),
                ),
              const Spacer(),
              Text(dateStr,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600])),
            ]),
            const SizedBox(height: 8),
            Text(event.title,
                style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    color: isPast ? Colors.grey[600] : null)),
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
      ),
    );
  }
}

// ── Onglet Clubs (données réelles depuis l'API) ──────────────────────────────
class _ClubsTab extends ConsumerStatefulWidget {
  const _ClubsTab();

  @override
  ConsumerState<_ClubsTab> createState() => _ClubsTabState();
}

class _ClubsTabState extends ConsumerState<_ClubsTab> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(campusProvider.notifier).loadClubs());
  }

  static const _domainIcons = {
    'Cybersécurité': Icons.security,
    'Génie Informatique': Icons.code,
    'Intelligence Artificielle': Icons.psychology,
    'Robotique': Icons.precision_manufacturing,
    'Social et humanitaire': Icons.volunteer_activism,
    'Entrepreneuriat social': Icons.lightbulb,
  };

  static const _domainColors = {
    'Cybersécurité': Colors.red,
    'Génie Informatique': Colors.blue,
    'Intelligence Artificielle': Colors.deepPurple,
    'Robotique': Colors.teal,
    'Social et humanitaire': Colors.orange,
    'Entrepreneuriat social': Colors.green,
  };

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(campusProvider);

    if (state.isLoadingClubs && state.clubs.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    if (state.clubs.isEmpty) {
      return Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Icon(Icons.people_outline, size: 48, color: Colors.grey),
          const SizedBox(height: 12),
          const Text('Impossible de charger les clubs',
              style: TextStyle(color: Colors.grey)),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: () => ref.read(campusProvider.notifier).loadClubs(),
            child: const Text('Réessayer'),
          ),
        ]),
      );
    }

    return RefreshIndicator(
      onRefresh: () => ref.read(campusProvider.notifier).loadClubs(),
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: state.clubs.length,
        itemBuilder: (_, i) {
          final club = state.clubs[i];
          final color = _domainColors[club.domain] ?? AppTheme.primaryColor;
          final icon = _domainIcons[club.domain] ?? Icons.group;

          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
              side: BorderSide(color: color.withOpacity(0.25)),
            ),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Row(children: [
                  CircleAvatar(
                    backgroundColor: color.withOpacity(0.12),
                    child: Icon(icon, color: color, size: 22),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(club.name,
                          style: const TextStyle(
                              fontWeight: FontWeight.bold, fontSize: 15)),
                      Text(club.domain,
                          style: TextStyle(fontSize: 12, color: color)),
                    ]),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(
                      color: color.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text('${club.members} membres',
                        style: TextStyle(
                            fontSize: 11, color: color, fontWeight: FontWeight.w600)),
                  ),
                ]),
                const SizedBox(height: 10),
                Text(club.description,
                    style: TextStyle(fontSize: 12, color: Colors.grey[700]),
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: club.isMember
                      ? OutlinedButton.icon(
                          onPressed: () =>
                              ref.read(campusProvider.notifier).toggleClub(club.id),
                          icon: const Icon(Icons.check, size: 16),
                          label: const Text('Membre • Quitter'),
                          style: OutlinedButton.styleFrom(foregroundColor: Colors.grey),
                        )
                      : ElevatedButton.icon(
                          onPressed: () =>
                              ref.read(campusProvider.notifier).toggleClub(club.id),
                          icon: const Icon(Icons.add, size: 16),
                          label: const Text('Rejoindre le club'),
                          style: ElevatedButton.styleFrom(backgroundColor: color),
                        ),
                ),
              ]),
            ),
          );
        },
      ),
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
