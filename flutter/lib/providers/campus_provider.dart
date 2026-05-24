import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/event_model.dart';
import '../services/api_service.dart';

class CampusState {
  final List<Event> events;
  final bool isLoading;
  final String? error;

  CampusState({this.events = const [], this.isLoading = false, this.error});

  CampusState copyWith({List<Event>? events, bool? isLoading, String? error}) =>
      CampusState(
        events: events ?? this.events,
        isLoading: isLoading ?? this.isLoading,
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
}

final campusProvider = StateNotifierProvider<CampusNotifier, CampusState>((ref) {
  return CampusNotifier(ref.watch(apiServiceProvider));
});
