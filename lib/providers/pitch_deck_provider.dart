import 'package:flutter/material.dart';
import 'dart:convert';
import '../models/pitch_deck.dart';
import '../services/database_service.dart';

class PitchDeckProvider extends ChangeNotifier {
  final DBService _dbService = DBService();
  final List<PitchDeck> _pitchDecks = [];
  PitchDeck? _currentPitchDeck;

  List<PitchDeck> get pitchDecks => _pitchDecks;
  PitchDeck? get currentPitchDeck => _currentPitchDeck;

  // Generate a pitch deck from an idea
  Future<PitchDeck> generatePitchDeck({
    required String title,
    required String description,
    required String category,
    int? ideaId,
    required String userId,
  }) async {
    final pitchDeck = PitchDeck(
      userId: userId,
      ideaId: ideaId,
      title: title,
      subtitle: _generateSubtitle(title),
      description: description,
      duration: 5,
    );

    // Generate slides based on content
    pitchDeck.slides = _generateSlides(
      title: title,
      description: description,
      category: category,
    );

    // Save to database
    final slidesJson = jsonEncode(
      pitchDeck.slides.map((s) => {
        'type': s.type.name,
        'title': s.title,
        'content': s.content,
        'bullets': s.bullets,
      }).toList(),
    );

    try {
      final id = await _dbService.addPitchDeck({
        'ideaId': ideaId,
        'userId': userId,
        'title': pitchDeck.title,
        'subtitle': pitchDeck.subtitle,
        'description': pitchDeck.description,
        'slides': slidesJson,
        'duration': pitchDeck.duration,
        'targetAudience': pitchDeck.targetAudience.join(','),
        'createdAt': pitchDeck.createdAt.toIso8601String(),
        'updatedAt': pitchDeck.updatedAt?.toIso8601String(),
      });
      pitchDeck.id = id;
    } catch (e) {
      print('Error saving pitch deck: $e');
    }

    _pitchDecks.add(pitchDeck);
    _currentPitchDeck = pitchDeck;
    notifyListeners();

    return pitchDeck;
  }

  List<PitchSlide> _generateSlides({
    required String title,
    required String description,
    required String category,
  }) {
    List<PitchSlide> slides = [];

    // 1. Title Slide
    slides.add(PitchSlide(
      type: PitchSlideType.title,
      title: title,
      content: title,
      bullets: ['Innovation in $category', 'Transform the way we work'],
    ));

    // 2. Problem Slide
    slides.add(PitchSlide(
      type: PitchSlideType.problem,
      title: 'The Problem',
      content: _generateProblemStatement(description, category),
      bullets: [
        'Current challenges identified',
        'Market gap exists',
        'Customer pain points',
      ],
    ));

    // 3. Solution Slide
    slides.add(PitchSlide(
      type: PitchSlideType.solution,
      title: 'Our Solution',
      content: description,
      bullets: [
        'Innovative approach',
        'Easy to implement',
        'Scalable framework',
      ],
    ));

    // 4. Market Slide
    slides.add(PitchSlide(
      type: PitchSlideType.market,
      title: 'Market Opportunity',
      content: _generateMarketOpportunity(category),
      bullets: [
        'Large addressable market',
        'Growing demand',
        'Competitive advantage',
      ],
    ));

    // 5. Business Model Slide
    slides.add(PitchSlide(
      type: PitchSlideType.business,
      title: 'Business Model',
      content: _generateBusinessModel(category),
      bullets: [
        'Revenue streams',
        'Cost structure',
        'Profitability path',
      ],
    ));

    // 6. Traction Slide
    slides.add(PitchSlide(
      type: PitchSlideType.traction,
      title: 'Traction & Metrics',
      content: 'Track key performance indicators and milestones',
      bullets: [
        'User growth trajectory',
        'Revenue milestones',
        'Key partnerships',
      ],
    ));

    // 7. Team Slide
    slides.add(PitchSlide(
      type: PitchSlideType.team,
      title: 'The Team',
      content: 'Experienced leadership with proven track record',
      bullets: [
        'Domain expertise',
        'Execution capability',
        'Industry connections',
      ],
    ));

    // 8. Closing Slide
    slides.add(PitchSlide(
      type: PitchSlideType.closing,
      title: 'The Ask',
      content: 'Join us on this journey to transform the $category space',
      bullets: [
        'Investment opportunity',
        'Partnership potential',
        'Contact & Next Steps',
      ],
    ));

    return slides;
  }

  String _generateSubtitle(String title) {
    return 'Pitch Deck - $title';
  }

  String _generateProblemStatement(String description, String category) {
    return 'The current $category landscape faces significant challenges that limit innovation and efficiency. Our market research identifies critical gaps that present a compelling opportunity for transformation.';
  }

  String _generateMarketOpportunity(String category) {
    return 'The global $category market is experiencing unprecedented growth. With increasing demand and evolving customer expectations, there\'s a substantial opportunity for solutions that address current pain points effectively.';
  }

  String _generateBusinessModel(String category) {
    return 'We employ a scalable, sustainable business model designed to capture value across the $category sector. Our revenue approach leverages multiple streams while maintaining a lean operational structure.';
  }

  // Select a pitch deck
  void selectPitchDeck(PitchDeck deck) {
    _currentPitchDeck = deck;
    notifyListeners();
  }

  // Update a slide
  Future<void> updateSlide(int slideIndex, PitchSlide slide) async {
    if (_currentPitchDeck != null && slideIndex < _currentPitchDeck!.slides.length) {
      _currentPitchDeck!.slides[slideIndex] = slide;
      _currentPitchDeck!.updatedAt = DateTime.now();

      // Save to database
      if (_currentPitchDeck!.id != null) {
        final slidesJson = jsonEncode(
          _currentPitchDeck!.slides.map((s) => {
            'type': s.type.name,
            'title': s.title,
            'content': s.content,
            'bullets': s.bullets,
          }).toList(),
        );

        try {
          await _dbService.updatePitchDeck(_currentPitchDeck!.id!, {
            'title': _currentPitchDeck!.title,
            'subtitle': _currentPitchDeck!.subtitle,
            'description': _currentPitchDeck!.description,
            'slides': slidesJson,
            'duration': _currentPitchDeck!.duration,
            'targetAudience': _currentPitchDeck!.targetAudience.join(','),
            'updatedAt': _currentPitchDeck!.updatedAt?.toIso8601String(),
          });
          print('✅ Slide updated and saved to database');
        } catch (e) {
          print('❌ Error saving slide update: $e');
        }
      }

      notifyListeners();
    }
  }

  // Add a custom slide
  void addCustomSlide(PitchSlide slide) {
    if (_currentPitchDeck != null) {
      _currentPitchDeck!.slides.add(slide);
      notifyListeners();
    }
  }

  // Remove a slide
  void removeSlide(int slideIndex) {
    if (_currentPitchDeck != null && slideIndex < _currentPitchDeck!.slides.length) {
      _currentPitchDeck!.slides.removeAt(slideIndex);
      notifyListeners();
    }
  }

  // Get pitch decks by idea
  List<PitchDeck> getPitchDecksByIdea(int ideaId) {
    return _pitchDecks.where((deck) => deck.ideaId == ideaId).toList();
  }

  // Get pitch decks by user
  List<PitchDeck> getPitchDecksByUser(String userId) {
    return _pitchDecks.where((deck) => deck.userId == userId).toList();
  }

  // Delete a pitch deck
  Future<void> deletePitchDeck(int id) async {
    try {
      final deck = _pitchDecks.cast<PitchDeck?>().firstWhere(
        (d) => d?.id == id,
        orElse: () => null,
      );
      
      if (deck != null) {
        await _dbService.deletePitchDeck(id);
        print('✅ Pitch deck deleted from database');
        _pitchDecks.removeWhere((d) => d.id == id);
        if (_currentPitchDeck?.id == id) {
          _currentPitchDeck = _pitchDecks.isNotEmpty ? _pitchDecks.first : null;
        }
        notifyListeners();
      }
    } catch (e) {
      print('❌ Error deleting pitch deck: $e');
      rethrow;
    }
  }

  // Charger les pitch decks d'un utilisateur
  Future<void> loadPitchDecksByUser(String userId) async {
    try {
      final results = await _dbService.getPitchDecksByUser(userId);
      _pitchDecks.clear();
      
      for (var result in results) {
        try {
          final slidesJson = jsonDecode(result['slides'] as String);
          final slides = (slidesJson as List).map((s) => PitchSlide.fromMap(s as Map<String, dynamic>)).toList();
          
          final pitchDeck = PitchDeck(
            id: result['id'] as int,
            ideaId: result['idea_id'] as int?,
            userId: result['user_id'] as String,
            title: result['title'] as String,
            subtitle: result['subtitle'] as String? ?? '',
            description: result['description'] as String? ?? '',
            slides: slides,
            duration: result['duration'] as int? ?? 5,
            targetAudience: (result['target_audience'] as String?)?.split(',') ?? [],
            createdAt: DateTime.parse(result['created_at'] as String),
            updatedAt: result['updated_at'] != null ? DateTime.parse(result['updated_at'] as String) : null,
          );
          _pitchDecks.add(pitchDeck);
        } catch (e) {
          print('Error parsing pitch deck: $e');
        }
      }
      notifyListeners();
      print('✅ Loaded ${_pitchDecks.length} pitch decks from database');
    } catch (e) {
      print('❌ Error loading pitch decks: $e');
    }
  }

  // Clear current selection
  void clearSelection() {
    _currentPitchDeck ??= null;
    notifyListeners();
  }
}
