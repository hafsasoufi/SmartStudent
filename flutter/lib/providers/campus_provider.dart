import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/event_model.dart';
import '../services/api_service.dart';

class ClubData {
  final String id;
  final String name;
  final String domain;
  final String description;
  final int members;
  final bool isMember;

  ClubData({
    required this.id,
    required this.name,
    required this.domain,
    required this.description,
    required this.members,
    required this.isMember,
  });

  factory ClubData.fromJson(Map<String, dynamic> j) => ClubData(
        id: j['id'] as String,
        name: j['name'] as String,
        domain: j['domain'] as String,
        description: j['description'] as String,
        members: j['members'] as int,
        isMember: j['is_member'] as bool,
      );

  ClubData copyWith({bool? isMember, int? members}) => ClubData(
        id: id,
        name: name,
        domain: domain,
        description: description,
        members: members ?? this.members,
        isMember: isMember ?? this.isMember,
      );
}

class CampusState {
  final List<Event> events;
  final List<ClubData> clubs;
  final bool isLoading;
  final bool isLoadingClubs;
  final String? error;

  CampusState({
    this.events = const [],
    this.clubs = const [],
    this.isLoading = false,
    this.isLoadingClubs = false,
    this.error,
  });

  CampusState copyWith({
    List<Event>? events,
    List<ClubData>? clubs,
    bool? isLoading,
    bool? isLoadingClubs,
    String? error,
  }) =>
      CampusState(
        events: events ?? this.events,
        clubs: clubs ?? this.clubs,
        isLoading: isLoading ?? this.isLoading,
        isLoadingClubs: isLoadingClubs ?? this.isLoadingClubs,
        error: error,
      );

  List<Event> get upcoming => events
      .where((e) => e.startDate.isAfter(DateTime.now()))
      .toList()
    ..sort((a, b) => a.startDate.compareTo(b.startDate));
}

class CampusNotifier extends StateNotifier<CampusState> {
  final ApiService _api;

  CampusNotifier(this._api) : super(CampusState());

  Future<void> loadEvents() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final data = await _api.getEvents();
      final events = (data as List)
          .map((j) => Event.fromJson(j as Map<String, dynamic>))
          .toList();
      state = state.copyWith(events: events, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  Future<void> loadClubs() async {
    state = state.copyWith(isLoadingClubs: true);
    try {
      final data = await _api.getClubs();
      final clubs = data
          .map((j) => ClubData.fromJson(j as Map<String, dynamic>))
          .toList();
      state = state.copyWith(clubs: clubs, isLoadingClubs: false);
    } catch (e) {
      state = state.copyWith(isLoadingClubs: false);
    }
  }

  Future<void> toggleClub(String clubId) async {
    final prev = state.clubs.firstWhere((c) => c.id == clubId);
    final newMember = !prev.isMember;
    // Optimistic update
    state = state.copyWith(
      clubs: state.clubs.map((c) {
        if (c.id != clubId) return c;
        return c.copyWith(
          isMember: newMember,
          members: newMember ? c.members + 1 : c.members - 1,
        );
      }).toList(),
    );
    try {
      await _api.toggleClubMembership(clubId);
    } catch (_) {
      // Revert on failure
      state = state.copyWith(
        clubs: state.clubs.map((c) {
          if (c.id != clubId) return c;
          return c.copyWith(
            isMember: prev.isMember,
            members: prev.members,
          );
        }).toList(),
      );
    }
  }
}

final campusProvider = StateNotifierProvider<CampusNotifier, CampusState>((ref) {
  return CampusNotifier(ref.watch(apiServiceProvider));
});
