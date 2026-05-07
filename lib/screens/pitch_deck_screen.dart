import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/pitch_deck.dart';
import '../providers/pitch_deck_provider.dart';
import '../providers/idea_provider.dart';
import '../widgets/pitch_slide_widget.dart';

class PitchDeckScreen extends StatefulWidget {
  final Map<String, dynamic>? selectedIdea;

  const PitchDeckScreen({Key? key, this.selectedIdea}) : super(key: key);

  @override
  State<PitchDeckScreen> createState() => _PitchDeckScreenState();
}

class _PitchDeckScreenState extends State<PitchDeckScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);

    // Load pitch decks from database on init
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final ideaProvider = context.read<IdeaProvider>();
      final pitchProvider = context.read<PitchDeckProvider>();
      pitchProvider.loadPitchDecksByUser(ideaProvider.getUserId());
    });

    // Auto-generate pitch deck if idea is provided
    if (widget.selectedIdea != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _generatePitchDeckFromIdea();
      });
    }
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _generatePitchDeckFromIdea() {
    final pitchProvider = context.read<PitchDeckProvider>();
    final ideaProvider = context.read<IdeaProvider>();

    if (widget.selectedIdea != null) {
      pitchProvider.generatePitchDeck(
        title: widget.selectedIdea!['title'] ?? 'Untitled Idea',
        description: widget.selectedIdea!['description'] ?? 'No description',
        category: widget.selectedIdea!['category'] ?? 'general',
        ideaId: widget.selectedIdea!['id'],
        userId: ideaProvider.getUserId(),
      );
    }
  }

  String getUserId() {
    final ideaProvider = context.read<IdeaProvider>();
    return ideaProvider.getUserId();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Pitch Deck Generator'),
        elevation: 0,
        backgroundColor: isDark ? const Color(0xFF1A1A1A) : Colors.white,
        foregroundColor: Colors.teal,
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.teal,
          labelColor: Colors.teal,
          unselectedLabelColor: isDark ? Colors.grey[400] : Colors.grey[600],
          tabs: const [
            Tab(icon: Icon(Icons.auto_awesome), text: 'Generate'),
            Tab(icon: Icon(Icons.list), text: 'My Decks'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [_buildGenerateTab(), _buildMyDecksTab()],
      ),
    );
  }

  Widget _buildGenerateTab() {
    final ideaProvider = context.watch<IdeaProvider>();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.teal.shade300, Colors.teal.shade700],
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Orientation & CV',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Préparez votre CV, votre lettre de motivation et votre pitch carrière',
                  style: TextStyle(color: Colors.white70),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Ideas list
          Text(
            'Profils disponibles',
            style: Theme.of(
              context,
            ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),

          if (ideaProvider.ideas.isEmpty)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(32),
                child: Column(
                  children: [
                    Icon(
                      Icons.lightbulb_outline,
                      size: 48,
                      color: Colors.grey[400],
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'No ideas yet',
                      style: Theme.of(context).textTheme.headlineSmall,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Create an idea first to generate a pitch deck',
                      style: Theme.of(
                        context,
                      ).textTheme.bodyMedium?.copyWith(color: Colors.grey[500]),
                    ),
                  ],
                ),
              ),
            )
          else
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: ideaProvider.ideas.length,
              itemBuilder: (context, index) {
                final idea = ideaProvider.ideas[index];
                return _buildIdeaCard(idea, isDark);
              },
            ),
        ],
      ),
    );
  }

  Widget _buildIdeaCard(Map<String, dynamic> idea, bool isDark) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [Colors.teal.shade300, Colors.teal.shade700],
            ),
            borderRadius: BorderRadius.circular(8),
          ),
          child: const Center(
            child: Icon(Icons.lightbulb, color: Colors.white),
          ),
        ),
        title: Text(
          idea['title'] ?? 'Untitled',
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(
          idea['description'] ?? 'No description',
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        trailing: ElevatedButton.icon(
          onPressed: () => _generateAndViewPitch(idea),
          icon: const Icon(Icons.auto_awesome),
          label: const Text('Generate'),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.teal,
            foregroundColor: Colors.white,
          ),
        ),
      ),
    );
  }

  void _generateAndViewPitch(Map<String, dynamic> idea) {
    final pitchProvider = context.read<PitchDeckProvider>();
    final ideaProvider = context.read<IdeaProvider>();

    pitchProvider
        .generatePitchDeck(
          title: idea['title'] ?? 'Untitled Idea',
          description: idea['description'] ?? 'No description',
          category: idea['category'] ?? 'general',
          ideaId: idea['id'],
          userId: ideaProvider.getUserId(),
        )
        .then((pitchDeck) {
          if (mounted) {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) =>
                    PitchDeckViewerScreen(pitchDeck: pitchDeck),
              ),
            );
          }
        })
        .catchError((e) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Error generating pitch: $e'),
                duration: const Duration(seconds: 3),
              ),
            );
          }
        });
  }

  Widget _buildMyDecksTab() {
    final pitchProvider = context.watch<PitchDeckProvider>();
    final ideaProvider = context.read<IdeaProvider>();

    final userDecks = pitchProvider.getPitchDecksByUser(
      ideaProvider.getUserId(),
    );

    return userDecks.isEmpty
        ? Center(
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.description, size: 48, color: Colors.grey[400]),
                  const SizedBox(height: 16),
                  Text(
                    'No pitch decks yet',
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Generate your first pitch deck from an idea',
                    style: Theme.of(
                      context,
                    ).textTheme.bodyMedium?.copyWith(color: Colors.grey[500]),
                  ),
                ],
              ),
            ),
          )
        : ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: userDecks.length,
            itemBuilder: (context, index) {
              final deck = userDecks[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  leading: Container(
                    width: 50,
                    height: 50,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          Colors.purple.shade300,
                          Colors.purple.shade700,
                        ],
                      ),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Center(
                      child: Icon(Icons.description, color: Colors.white),
                    ),
                  ),
                  title: Text(
                    deck.title,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text(
                    '${deck.slides.length} slides • Created ${_formatDate(deck.createdAt)}',
                  ),
                  trailing: PopupMenuButton(
                    itemBuilder: (context) => [
                      PopupMenuItem(
                        child: const Text('View'),
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) =>
                                PitchDeckViewerScreen(pitchDeck: deck),
                          ),
                        ),
                      ),
                      PopupMenuItem(
                        child: const Text('Delete'),
                        onTap: () async {
                          if (deck.id != null) {
                            await pitchProvider.deletePitchDeck(deck.id!);
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('✅ Pitch deck deleted'),
                                  duration: Duration(seconds: 2),
                                ),
                              );
                            }
                          }
                        },
                      ),
                    ],
                  ),
                ),
              );
            },
          );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}

class PitchDeckViewerScreen extends StatefulWidget {
  final PitchDeck pitchDeck;

  const PitchDeckViewerScreen({Key? key, required this.pitchDeck})
    : super(key: key);

  @override
  State<PitchDeckViewerScreen> createState() => _PitchDeckViewerScreenState();
}

class _PitchDeckViewerScreenState extends State<PitchDeckViewerScreen> {
  late PageController _pageController;
  int _currentSlideIndex = 0;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.pitchDeck.title),
        elevation: 0,
        backgroundColor: isDark ? const Color(0xFF1A1A1A) : Colors.white,
        foregroundColor: Colors.teal,
        actions: [
          IconButton(icon: const Icon(Icons.share), onPressed: _sharePitchDeck),
        ],
      ),
      body: Column(
        children: [
          // Slide counter and progress
          Container(
            padding: const EdgeInsets.all(16),
            color: isDark ? const Color(0xFF252525) : Colors.grey[100],
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Slide ${_currentSlideIndex + 1} of ${widget.pitchDeck.slides.length}',
                  style: Theme.of(
                    context,
                  ).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value:
                            (_currentSlideIndex + 1) /
                            widget.pitchDeck.slides.length,
                        minHeight: 6,
                        backgroundColor: isDark
                            ? Colors.grey[700]
                            : Colors.grey[300],
                        valueColor: const AlwaysStoppedAnimation(Colors.teal),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Slides viewer
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              onPageChanged: (index) {
                setState(() => _currentSlideIndex = index);
              },
              itemCount: widget.pitchDeck.slides.length,
              itemBuilder: (context, index) {
                final slide = widget.pitchDeck.slides[index];
                return PitchSlideWidget(
                  slideIndex: index,
                  title: slide.title,
                  content: slide.content,
                  bullets: slide.bullets,
                  isEditable: true,
                  onEdit: (content, bullets) async {
                    final updatedSlide = PitchSlide(
                      type: slide.type,
                      title: slide.title,
                      content: content,
                      bullets: bullets,
                    );
                    try {
                      await context.read<PitchDeckProvider>().updateSlide(
                        index,
                        updatedSlide,
                      );
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('✅ Slide changes saved'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      }
                    } catch (e) {
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('❌ Error saving: $e'),
                            duration: const Duration(seconds: 3),
                          ),
                        );
                      }
                    }
                  },
                );
              },
            ),
          ),

          // Navigation buttons
          Container(
            padding: const EdgeInsets.all(16),
            color: isDark ? const Color(0xFF252525) : Colors.grey[100],
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton.icon(
                  onPressed: _currentSlideIndex > 0
                      ? () => _pageController.previousPage(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                        )
                      : null,
                  icon: const Icon(Icons.arrow_back),
                  label: const Text('Previous'),
                ),
                ElevatedButton.icon(
                  onPressed:
                      _currentSlideIndex < widget.pitchDeck.slides.length - 1
                      ? () => _pageController.nextPage(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                        )
                      : null,
                  icon: const Icon(Icons.arrow_forward),
                  label: const Text('Next'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _sharePitchDeck() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Share feature coming soon!'),
        duration: Duration(seconds: 2),
      ),
    );
  }
}
