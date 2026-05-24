import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

enum AppLanguage {
  english('en', 'English'),
  spanish('es', 'Español'),
  french('fr', 'Français'),
  german('de', 'Deutsch'),
  chinese('zh', '中文'),
  japanese('ja', '日本語');

  final String code;
  final String name;

  const AppLanguage(this.code, this.name);
}

class LocalizationNotifier extends StateNotifier<AppLanguage> {
  LocalizationNotifier() : super(AppLanguage.english);

  void setLanguage(AppLanguage language) {
    state = language;
  }

  Locale getLocale() {
    return Locale(state.code);
  }
}

final localizationProvider =
    StateNotifierProvider<LocalizationNotifier, AppLanguage>((ref) {
  return LocalizationNotifier();
});

final currentLocaleProvider = Provider<Locale>((ref) {
  final language = ref.watch(localizationProvider);
  return Locale(language.code);
});
