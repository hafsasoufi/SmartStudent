// import 'package:flutter/material.dart';
// import 'package:provider/provider.dart';
// import '../providers/board_provider.dart';
// import '../providers/theme_provider.dart';
// import '../providers/idea_provider.dart';
// import '../providers/auth_provider.dart';
// import '../screens/dashboard_screen.dart';
// import '../pages/kanban_page_dynamic.dart';
// import '../screens/roadmap_screen.dart';
// import '../screens/auth_screen.dart';
// import '../models/board.dart';

// class MainLayout extends StatefulWidget {
//   const MainLayout({super.key});

//   @override
//   State<MainLayout> createState() => _MainLayoutState();
// }

// class _MainLayoutState extends State<MainLayout> {
//   int _selectedNavIndex = 1; // Default to Kanban

//   @override
//   void initState() {
//     super.initState();
//     WidgetsBinding.instance.addPostFrameCallback((_) {
//       final authProvider = context.read<AuthProvider>();
//       final userId = authProvider.userId;

//       if (userId != null) {
//         context.read<BoardProvider>().setUserId(userId);
//         context.read<IdeaProvider>().setUserId(userId);
//       }
//     });
//   }

//   Widget _getSelectedPage() {
//     final boardProvider = context.watch<BoardProvider>();

//     // Show empty state if no boards exist
//     if (boardProvider.boards.isEmpty) {
//       return _NoboardsEmptyState(onCreateBoard: _showAddBoardDialog);
//     }

//     switch (_selectedNavIndex) {
//       case 0:
//         return const DashboardScreen();
//       case 1:
//         if (boardProvider.selectedBoardId == null) {
//           return _NoboardsEmptyState(onCreateBoard: _showAddBoardDialog);
//         }
//         return KanbanPageDynamic(
//           boardId: boardProvider.selectedBoardId,
//           boardName: boardProvider.boards.firstWhere(
//             (b) => b['id'] == boardProvider.selectedBoardId,
//             orElse: () => {'name': 'Board'},
//           )['name'],
//         );
//       case 2:
//         return const RoadmapScreen();
//       default:
//         return const DashboardScreen();
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     final theme = Theme.of(context);
//     final boardProvider = context.watch<BoardProvider>();
//     final themeProvider = context.watch<ThemeProvider>();

//     return Scaffold(
//       body: Row(
//         children: [
//           // Right Sidebar Navigation
//           Container(
//             width: 280,
//             decoration: BoxDecoration(
//               color: theme.colorScheme.surface,
//               border: Border(
//                 right: BorderSide(color: theme.dividerColor, width: 1),
//               ),
//             ),
//             child: Column(
//               crossAxisAlignment: CrossAxisAlignment.start,
//               children: [
//                 // App Header
//                 Container(
//                   padding: const EdgeInsets.all(24),
//                   child: Row(
//                     children: [
//                       Icon(
//                         Icons.waves,
//                         color: theme.colorScheme.primary,
//                         size: 28,
//                       ),
//                       const SizedBox(width: 12),
//                       Text(
//                         'KANFLOW',
//                         style: theme.textTheme.headlineSmall?.copyWith(
//                           fontWeight: FontWeight.bold,
//                           color: theme.colorScheme.primary,
//                         ),
//                       ),
//                     ],
//                   ),
//                 ),

//                 const Divider(height: 1),

//                 // Navigation Items
//                 Padding(
//                   padding: const EdgeInsets.all(16),
//                   child: Column(
//                     crossAxisAlignment: CrossAxisAlignment.start,
//                     children: [
//                       Text(
//                         'NAVIGATION',
//                         style: theme.textTheme.labelSmall?.copyWith(
//                           color: theme.colorScheme.onSurface.withOpacity(0.6),
//                           fontWeight: FontWeight.bold,
//                           letterSpacing: 1.2,
//                         ),
//                       ),
//                       const SizedBox(height: 12),
//                       _NavItem(
//                         icon: Icons.dashboard_rounded,
//                         label: 'Dashboard',
//                         isSelected: _selectedNavIndex == 0,
//                         onTap: () => setState(() => _selectedNavIndex = 0),
//                       ),
//                       _NavItem(
//                         icon: Icons.view_kanban_rounded,
//                         label: 'Kanban',
//                         isSelected: _selectedNavIndex == 1,
//                         onTap: () => setState(() => _selectedNavIndex = 1),
//                       ),
//                       _NavItem(
//                         icon: Icons.rocket_launch_rounded,
//                         label: 'Roadmap',
//                         isSelected: _selectedNavIndex == 2,
//                         onTap: () => setState(() => _selectedNavIndex = 2),
//                       ),
//                     ],
//                   ),
//                 ),

//                 const Divider(height: 1),

//                 // Boards Section
//                 Expanded(
//                   child: Padding(
//                     padding: const EdgeInsets.all(16),
//                     child: Column(
//                       crossAxisAlignment: CrossAxisAlignment.start,
//                       children: [
//                         Row(
//                           mainAxisAlignment: MainAxisAlignment.spaceBetween,
//                           children: [
//                             Text(
//                               'MES TABLEAUX',
//                               style: theme.textTheme.labelSmall?.copyWith(
//                                 color: theme.colorScheme.onSurface.withOpacity(
//                                   0.6,
//                                 ),
//                                 fontWeight: FontWeight.bold,
//                                 letterSpacing: 1.2,
//                               ),
//                             ),
//                             IconButton(
//                               icon: const Icon(
//                                 Icons.add_circle_outline,
//                                 size: 20,
//                               ),
//                               onPressed: _showAddBoardDialog,
//                               tooltip: 'Nouveau tableau',
//                             ),
//                           ],
//                         ),
//                         const SizedBox(height: 12),

//                         // Board List
//                         Expanded(
//                           child: boardProvider.boards.isEmpty
//                               ? _EmptyBoardsState(onAdd: _showAddBoardDialog)
//                               : ListView.builder(
//                                   itemCount: boardProvider.boards.length,
//                                   itemBuilder: (context, index) {
//                                     final board = boardProvider.boards[index];
//                                     final isSelected =
//                                         board['id'] ==
//                                         boardProvider.selectedBoardId;

//                                     return _BoardItem(
//                                       name: board['name'],
//                                       isSelected: isSelected,
//                                       onTap: () {
//                                         boardProvider.selectBoard(board['id']);
//                                         setState(
//                                           () => _selectedNavIndex = 1,
//                                         ); // Switch to Kanban
//                                       },
//                                       onRename: () => _showRenameBoardDialog(
//                                         board['id'],
//                                         board['name'],
//                                       ),
//                                       onDelete: () =>
//                                           _confirmDeleteBoard(board['id']),
//                                     );
//                                   },
//                                 ),
//                         ),
//                       ],
//                     ),
//                   ),
//                 ),

//                 const Divider(height: 1),

//                 // User Info & Logout
//                 Padding(
//                   padding: const EdgeInsets.all(16),
//                   child: Consumer<AuthProvider>(
//                     builder: (context, authProvider, _) {
//                       return Column(
//                         crossAxisAlignment: CrossAxisAlignment.start,
//                         children: [
//                           Row(
//                             children: [
//                               CircleAvatar(
//                                 radius: 20,
//                                 backgroundColor:
//                                     theme.colorScheme.primaryContainer,
//                                 child: Text(
//                                   authProvider.userName
//                                           ?.substring(0, 1)
//                                           .toUpperCase() ??
//                                       'U',
//                                   style: TextStyle(
//                                     fontWeight: FontWeight.bold,
//                                     color: theme.colorScheme.primary,
//                                   ),
//                                 ),
//                               ),
//                               const SizedBox(width: 12),
//                               Expanded(
//                                 child: Column(
//                                   crossAxisAlignment: CrossAxisAlignment.start,
//                                   children: [
//                                     Text(
//                                       authProvider.userName ?? 'User',
//                                       style: theme.textTheme.bodyMedium
//                                           ?.copyWith(
//                                             fontWeight: FontWeight.bold,
//                                           ),
//                                       overflow: TextOverflow.ellipsis,
//                                     ),
//                                     Text(
//                                       authProvider.userEmail ?? '',
//                                       style: theme.textTheme.bodySmall
//                                           ?.copyWith(
//                                             color: theme.colorScheme.onSurface
//                                                 .withOpacity(0.6),
//                                           ),
//                                       overflow: TextOverflow.ellipsis,
//                                     ),
//                                   ],
//                                 ),
//                               ),
//                             ],
//                           ),
//                           const SizedBox(height: 12),
//                           SizedBox(
//                             width: double.infinity,
//                             child: OutlinedButton.icon(
//                               onPressed: () {
//                                 authProvider.logout();
//                                 Navigator.of(context).pushReplacement(
//                                   MaterialPageRoute(
//                                     builder: (_) => const AuthScreen(),
//                                   ),
//                                 );
//                               },
//                               icon: const Icon(Icons.logout, size: 18),
//                               label: const Text('Déconnexion'),
//                               style: OutlinedButton.styleFrom(
//                                 foregroundColor: theme.colorScheme.error,
//                                 side: BorderSide(
//                                   color: theme.colorScheme.error,
//                                 ),
//                               ),
//                             ),
//                           ),
//                         ],
//                       );
//                     },
//                   ),
//                 ),

//                 const Divider(height: 1),

//                 // Theme Toggle
//                 Padding(
//                   padding: const EdgeInsets.all(16),
//                   child: Row(
//                     children: [
//                       Icon(
//                         themeProvider.isDarkMode
//                             ? Icons.dark_mode
//                             : Icons.light_mode,
//                         size: 20,
//                         color: theme.colorScheme.onSurface.withOpacity(0.7),
//                       ),
//                       const SizedBox(width: 12),
//                       Text(
//                         themeProvider.isDarkMode ? 'Mode sombre' : 'Mode clair',
//                         style: theme.textTheme.bodyMedium,
//                       ),
//                       const Spacer(),
//                       Switch(
//                         value: themeProvider.isDarkMode,
//                         onChanged: (value) => themeProvider.setDarkMode(value),
//                       ),
//                     ],
//                   ),
//                 ),
//               ],
//             ),
//           ),

//           // Main Content Area
//           Expanded(child: _getSelectedPage()),
//         ],
//       ),
//     );
//   }

//   void _showAddBoardDialog() {
//     final controller = TextEditingController();
//     final authProvider = context.read<AuthProvider>();
//     final userId = authProvider.userId;

//     if (userId == null) {
//       ScaffoldMessenger.of(context).showSnackBar(
//         const SnackBar(
//           content: Text('Vous devez être connecté pour créer un tableau'),
//         ),
//       );
//       return;
//     }

//     showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         title: const Text('Nouveau Tableau'),
//         content: TextField(
//           controller: controller,
//           autofocus: true,
//           decoration: const InputDecoration(
//             labelText: 'Nom du tableau',
//             border: OutlineInputBorder(),
//             hintText: 'Ex: Projet Marketing Q1',
//           ),
//         ),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.pop(context),
//             child: const Text('Annuler'),
//           ),
//        FilledButton(
//   onPressed: () {
//     if (controller.text.trim().isNotEmpty) {
//       final boardProvider = context.read<BoardProvider>();
//       boardProvider.addBoard(
//         Board(userId: userId.toString(), name: controller.text.trim()).toMap(), // <-- convertir en Map
//       );
//       Navigator.pop(context);
//     }
//   },
//   child: const Text('Créer'),
// ),

//         ],
//       ),
//     );
//   }

//   void _showRenameBoardDialog(int boardId, String currentName) {
//     final controller = TextEditingController(text: currentName);

//     showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         title: const Text('Renommer le Tableau'),
//         content: TextField(
//           controller: controller,
//           autofocus: true,
//           decoration: const InputDecoration(
//             labelText: 'Nouveau nom',
//             border: OutlineInputBorder(),
//           ),
//         ),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.pop(context),
//             child: const Text('Annuler'),
//           ),
//           FilledButton(
//             onPressed: () {
//               if (controller.text.trim().isNotEmpty) {
//                 context.read<BoardProvider>().updateBoard(boardId, {
//                   'name': controller.text.trim(),
//                 });
//                 Navigator.pop(context);
//               }
//             },
//             child: const Text('Renommer'),
//           ),
//         ],
//       ),
//     );
//   }

//   void _confirmDeleteBoard(int boardId) {
//     showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         title: const Text('Supprimer le tableau ?'),
//         content: const Text(
//           'Toutes les cartes et colonnes de ce tableau seront supprimées. Cette action est irréversible.',
//         ),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.pop(context),
//             child: const Text('Annuler'),
//           ),
//           FilledButton(
//             onPressed: () {
//               context.read<BoardProvider>().deleteBoard(boardId);
//               Navigator.pop(context);
//             },
//             style: FilledButton.styleFrom(backgroundColor: Colors.red),
//             child: const Text('Supprimer'),
//           ),
//         ],
//       ),
//     );
//   }
// }

// class _NavItem extends StatelessWidget {
//   final IconData icon;
//   final String label;
//   final bool isSelected;
//   final VoidCallback onTap;

//   const _NavItem({
//     required this.icon,
//     required this.label,
//     required this.isSelected,
//     required this.onTap,
//   });

//   @override
//   Widget build(BuildContext context) {
//     final theme = Theme.of(context);

//     return Material(
//       color: Colors.transparent,
//       child: InkWell(
//         onTap: onTap,
//         borderRadius: BorderRadius.circular(12),
//         child: Container(
//           padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
//           decoration: BoxDecoration(
//             color: isSelected
//                 ? theme.colorScheme.primaryContainer
//                 : Colors.transparent,
//             borderRadius: BorderRadius.circular(12),
//           ),
//           child: Row(
//             children: [
//               Icon(
//                 icon,
//                 color: isSelected
//                     ? theme.colorScheme.primary
//                     : theme.colorScheme.onSurface.withOpacity(0.7),
//                 size: 22,
//               ),
//               const SizedBox(width: 12),
//               Text(
//                 label,
//                 style: theme.textTheme.bodyMedium?.copyWith(
//                   color: isSelected
//                       ? theme.colorScheme.primary
//                       : theme.colorScheme.onSurface.withOpacity(0.7),
//                   fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
//                 ),
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }

// class _BoardItem extends StatelessWidget {
//   final String name;
//   final bool isSelected;
//   final VoidCallback onTap;
//   final VoidCallback onRename;
//   final VoidCallback onDelete;

//   const _BoardItem({
//     required this.name,
//     required this.isSelected,
//     required this.onTap,
//     required this.onRename,
//     required this.onDelete,
//   });

//   @override
//   Widget build(BuildContext context) {
//     final theme = Theme.of(context);

//     return Material(
//       color: Colors.transparent,
//       child: InkWell(
//         onTap: onTap,
//         borderRadius: BorderRadius.circular(8),
//         child: Container(
//           padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
//           margin: const EdgeInsets.only(bottom: 4),
//           decoration: BoxDecoration(
//             color: isSelected
//                 ? theme.colorScheme.secondaryContainer.withOpacity(0.5)
//                 : Colors.transparent,
//             borderRadius: BorderRadius.circular(8),
//             border: isSelected
//                 ? Border.all(color: theme.colorScheme.primary.withOpacity(0.3))
//                 : null,
//           ),
//           child: Row(
//             children: [
//               Icon(
//                 Icons.view_column_rounded,
//                 size: 18,
//                 color: isSelected
//                     ? theme.colorScheme.primary
//                     : theme.colorScheme.onSurface.withOpacity(0.6),
//               ),
//               const SizedBox(width: 10),
//               Expanded(
//                 child: Text(
//                   name,
//                   style: theme.textTheme.bodyMedium?.copyWith(
//                     fontWeight: isSelected
//                         ? FontWeight.w600
//                         : FontWeight.normal,
//                     color: isSelected
//                         ? theme.colorScheme.primary
//                         : theme.colorScheme.onSurface,
//                   ),
//                   overflow: TextOverflow.ellipsis,
//                 ),
//               ),
//               if (isSelected)
//                 PopupMenuButton(
//                   icon: Icon(
//                     Icons.more_vert,
//                     size: 18,
//                     color: theme.colorScheme.onSurface.withOpacity(0.6),
//                   ),
//                   itemBuilder: (context) => [
//                     PopupMenuItem(
//                       onTap: onRename,
//                       child: const Row(
//                         children: [
//                           Icon(Icons.edit, size: 18),
//                           SizedBox(width: 8),
//                           Text('Renommer'),
//                         ],
//                       ),
//                     ),
//                     PopupMenuItem(
//                       onTap: onDelete,
//                       child: const Row(
//                         children: [
//                           Icon(Icons.delete, size: 18, color: Colors.red),
//                           SizedBox(width: 8),
//                           Text(
//                             'Supprimer',
//                             style: TextStyle(color: Colors.red),
//                           ),
//                         ],
//                       ),
//                     ),
//                   ],
//                 ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }

// class _EmptyBoardsState extends StatelessWidget {
//   final VoidCallback onAdd;

//   const _EmptyBoardsState({required this.onAdd});

//   @override
//   Widget build(BuildContext context) {
//     final theme = Theme.of(context);

//     return Center(
//       child: Column(
//         mainAxisAlignment: MainAxisAlignment.center,
//         children: [
//           Icon(
//             Icons.view_kanban_outlined,
//             size: 48,
//             color: theme.colorScheme.onSurface.withOpacity(0.3),
//           ),
//           const SizedBox(height: 16),
//           Text(
//             'Aucun tableau',
//             style: theme.textTheme.titleMedium?.copyWith(
//               color: theme.colorScheme.onSurface.withOpacity(0.6),
//             ),
//           ),
//           const SizedBox(height: 8),
//           FilledButton.icon(
//             onPressed: onAdd,
//             icon: const Icon(Icons.add),
//             label: const Text('Créer un tableau'),
//           ),
//         ],
//       ),
//     );
//   }
// }

// // Main empty state when no boards exist
// class _NoboardsEmptyState extends StatelessWidget {
//   final VoidCallback onCreateBoard;

//   const _NoboardsEmptyState({required this.onCreateBoard});

//   @override
//   Widget build(BuildContext context) {
//     final theme = Theme.of(context);
//     final colorScheme = theme.colorScheme;

//     return Center(
//       child: Container(
//         constraints: const BoxConstraints(maxWidth: 500),
//         padding: const EdgeInsets.all(40),
//         child: Column(
//           mainAxisAlignment: MainAxisAlignment.center,
//           children: [
//             Container(
//               padding: const EdgeInsets.all(32),
//               decoration: BoxDecoration(
//                 color: colorScheme.primaryContainer.withOpacity(0.3),
//                 shape: BoxShape.circle,
//               ),
//               child: Icon(
//                 Icons.dashboard_customize_outlined,
//                 size: 80,
//                 color: colorScheme.primary,
//               ),
//             ),
//             const SizedBox(height: 32),
//             Text(
//               'Bienvenue dans KANFLOW',
//               style: theme.textTheme.headlineMedium?.copyWith(
//                 fontWeight: FontWeight.bold,
//                 color: colorScheme.primary,
//               ),
//               textAlign: TextAlign.center,
//             ),
//             const SizedBox(height: 16),
//             Text(
//               'Vous n\'avez pas encore de tableau. Créez votre premier tableau pour commencer à organiser vos tâches et projets.',
//               style: theme.textTheme.bodyLarge?.copyWith(
//                 color: colorScheme.onSurface.withOpacity(0.7),
//               ),
//               textAlign: TextAlign.center,
//             ),
//             const SizedBox(height: 40),
//             FilledButton.icon(
//               onPressed: onCreateBoard,
//               icon: const Icon(Icons.add_circle_outline, size: 24),
//               label: const Text(
//                 'Créer votre premier tableau',
//                 style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
//               ),
//               style: FilledButton.styleFrom(
//                 padding: const EdgeInsets.symmetric(
//                   horizontal: 32,
//                   vertical: 20,
//                 ),
//                 shape: RoundedRectangleBorder(
//                   borderRadius: BorderRadius.circular(12),
//                 ),
//               ),
//             ),
//             const SizedBox(height: 24),
//             Container(
//               padding: const EdgeInsets.all(20),
//               decoration: BoxDecoration(
//                 color: colorScheme.surfaceContainerHighest.withOpacity(0.3),
//                 borderRadius: BorderRadius.circular(12),
//                 border: Border.all(color: colorScheme.outline.withOpacity(0.2)),
//               ),
//               child: Row(
//                 children: [
//                   Icon(
//                     Icons.lightbulb_outline,
//                     color: colorScheme.primary,
//                     size: 24,
//                   ),
//                   const SizedBox(width: 16),
//                   Expanded(
//                     child: Text(
//                       'Un tableau vous permet d\'organiser vos tâches en colonnes personnalisables avec le système Kanban.',
//                       style: theme.textTheme.bodyMedium?.copyWith(
//                         color: colorScheme.onSurface.withOpacity(0.8),
//                       ),
//                     ),
//                   ),
//                 ],
//               ),
//             ),
//           ],
//         ),
//       ),
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/board_provider.dart';
import '../providers/theme_provider.dart';
import '../providers/idea_provider.dart';
import '../providers/auth_provider.dart';
import '../services/database_service.dart';
import '../screens/dashboard_screen.dart';
import '../pages/kanban_page_dynamic.dart';
import '../screens/roadmap_screen.dart';
import '../screens/statistics_screen.dart';
import '../screens/notification_page.dart';
import '../screens/pitch_deck_screen.dart';
import '../screens/assistant_screen.dart';
import '../screens/auth_screen.dart';
import '../models/board.dart';
import '../widgets/add_idea_dialog.dart';

class MainLayout extends StatefulWidget {
  const MainLayout({super.key});

  @override
  State<MainLayout> createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  int _selectedNavIndex = 1; // Default Kanban

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final authProvider = context.read<AuthProvider>();
      final userId = authProvider.userId;
      if (userId != null) {
        context.read<BoardProvider>().setUserId(userId);
        context.read<IdeaProvider>().setUserId(userId);
        // Import any shared boards for this user's email
        final email = authProvider.userEmail;
        if (email != null && email.isNotEmpty) {
          final db = DBService();
          db
              .getSharedBoardsForEmail(email)
              .then((shared) async {
                for (var row in shared) {
                  final boardJson = row['board_json'] as String?;
                  if (boardJson == null) continue;
                  final ownerBoardId = row['board_id'] as int? ?? 0;

                  // Check if we already have a mapping for this shared owner board -> our local board
                  final syncRows = await db
                      .getSharedBoardSyncByOwnerBoardIdAndEmail(
                        ownerBoardId,
                        email,
                      );
                  if (syncRows.isNotEmpty &&
                      (syncRows.first['shared_user_board_id'] as int? ?? 0) >
                          0) {
                    // Update the existing imported board instead of creating a new one
                    final existingBoardId =
                        syncRows.first['shared_user_board_id'] as int;
                    final updated = await db.updateImportedBoard(
                      existingBoardId,
                      boardJson,
                      userId,
                    );
                    if (updated > 0) {
                      await context.read<BoardProvider>().fetchBoards();
                      await context.read<IdeaProvider>().fetchIdeas();
                    }
                  } else {
                    // First import: create new board and save mapping
                    final newBoardId = await db.importSharedBoardForUser(
                      boardJson,
                      userId,
                    );
                    if (newBoardId > 0) {
                      try {
                        await db.setSharedUserBoardId(
                          ownerBoardId,
                          email,
                          newBoardId,
                        );
                      } catch (e) {
                        print('Error updating sync mapping: $e');
                      }

                      await context.read<BoardProvider>().fetchBoards();
                      await context.read<IdeaProvider>().fetchIdeas();
                    }
                  }
                }
              })
              .catchError((e) {
                print('Error fetching shared boards: $e');
              });
          // Start polling for updates from owners for shared boards
          try {
            context.read<BoardProvider>().startSharedBoardsPolling(
              email,
              userId,
            );
          } catch (e) {
            print('Error starting shared boards polling: $e');
          }
        }
      }
    });
  }

  Widget _getSelectedPage() {
    final boardProvider = context.watch<BoardProvider>();

    switch (_selectedNavIndex) {
      case 0:
        return const DashboardScreen(); // Accueil toujours accessible
      case 1:
        // Kanban : vérifier si un board est sélectionné
        if (boardProvider.boards.isEmpty ||
            boardProvider.selectedBoardId == null) {
          return _NoboardsEmptyState(onCreateBoard: _showAddBoardDialog);
        }
        return KanbanPageDynamic(
          boardId: boardProvider.selectedBoardId,
          boardName: boardProvider.boards.firstWhere(
            (b) => b['id'] == boardProvider.selectedBoardId,
            orElse: () => {'name': 'Board'},
          )['name'],
        );
      case 2:
        return const RoadmapScreen(); // Planning toujours accessible
      case 3:
        return const StatisticsScreen(); // Révisions / progression
      case 4:
        return const PitchDeckScreen(); // Orientation / carrière
      default:
        return const DashboardScreen();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, themeProvider, _) {
        return Scaffold(
          appBar: _buildAppBar(context, themeProvider),
          body: AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            child: _getSelectedPage(),
          ),
          bottomNavigationBar: _buildBottomNavigationBar(),
          drawer: _buildDrawer(context),
          floatingActionButton: _buildFloatingActionButton(context),
        );
      },
    );
  }

  // FloatingActionButton dynamique selon la page
  Widget? _buildFloatingActionButton(BuildContext context) {
    return Consumer<BoardProvider>(
      builder: (context, boardProvider, _) {
        // Afficher différents FAB selon la page active
        switch (_selectedNavIndex) {
          case 0: // Dashboard
            return FloatingActionButton.extended(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const AssistantScreen(),
                  ),
                );
              },
              icon: const Icon(Icons.auto_awesome),
              label: const Text('Assistant IA'),
              heroTag: 'openAssistant',
            );
          case 1: // Kanban
            if (boardProvider.boards.isEmpty ||
                boardProvider.selectedBoardId == null) {
              return FloatingActionButton.extended(
                onPressed: _showAddBoardDialog,
                icon: const Icon(Icons.add),
                label: const Text('Créer un espace'),
                heroTag: 'createBoard',
              );
            }
            return FloatingActionButton(
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AddIdeaDialog(
                    initialStatus: 'Backlog',
                    boardId: boardProvider.selectedBoardId,
                  ),
                );
              },
              child: const Icon(Icons.add),
              heroTag: 'addIdea',
              tooltip: 'Ajouter une demande',
            );
          case 2: // Roadmap
            return FloatingActionButton.extended(
              onPressed: () {
                setState(() => _selectedNavIndex = 1);
              },
              icon: const Icon(Icons.view_kanban),
              label: const Text('Voir assistant'),
              heroTag: 'gotoKanban',
            );
          default:
            return const SizedBox.shrink();
        }
      },
    );
  }

  // AppBar dynamique
  PreferredSizeWidget _buildAppBar(
    BuildContext context,
    ThemeProvider themeProvider,
  ) {
    return AppBar(
      title: Consumer<BoardProvider>(
        builder: (context, boardProvider, _) {
          // Titre dynamique basé sur le tableau sélectionné
          String title = 'SmartStudent';
          if (_selectedNavIndex == 1 &&
              boardProvider.selectedBoardId != null &&
              boardProvider.boards.isNotEmpty) {
            final selectedBoard = boardProvider.boards.firstWhere(
              (b) => b['id'] == boardProvider.selectedBoardId,
              orElse: () => {'name': 'Board'},
            );
            title = 'Assistant IA • ${selectedBoard['name'] ?? 'Espace'}';
          } else if (_selectedNavIndex == 1) {
            title = 'Assistant IA';
          } else if (_selectedNavIndex == 2) {
            title = 'Planning';
          } else if (_selectedNavIndex == 3) {
            title = 'Révisions';
          } else if (_selectedNavIndex == 4) {
            title = 'Orientation';
          }
          return Text(title);
        },
      ),
      actions: [
        // Bouton de notifications avec badge dynamique
        Consumer<IdeaProvider>(
          builder: (context, ideaProvider, _) {
            final now = DateTime.now();
            final overdueTasks = ideaProvider.ideas.where((idea) {
              if (idea['dueDate'] == null || idea['status'] == 'Done') {
                return false;
              }
              return DateTime.parse(idea['dueDate']).isBefore(now);
            }).length;

            final highPriorityTasks = ideaProvider.ideas
                .where(
                  (idea) => idea['priority'] == 2 && idea['status'] != 'Done',
                )
                .length;

            final totalNotifications = overdueTasks + highPriorityTasks;

            return Stack(
              children: [
                IconButton(
                  icon: const Icon(Icons.notifications_outlined),
                  onPressed: () {
                    final boardProvider = context.read<BoardProvider>();
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => NotificationPage(
                          boardId: boardProvider.selectedBoardId,
                          boardName:
                              boardProvider.boards.isNotEmpty &&
                                  boardProvider.selectedBoardId != null
                              ? boardProvider.boards.firstWhere(
                                  (b) =>
                                      b['id'] == boardProvider.selectedBoardId,
                                  orElse: () => {'name': 'Board'},
                                )['name']
                              : null,
                        ),
                      ),
                    );
                  },
                ),
                if (totalNotifications > 0)
                  Positioned(
                    right: 8,
                    top: 8,
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      padding: const EdgeInsets.all(4),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      constraints: const BoxConstraints(
                        minWidth: 18,
                        minHeight: 18,
                      ),
                      child: Text(
                        totalNotifications > 9
                            ? '9+'
                            : totalNotifications.toString(),
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
              ],
            );
          },
        ),
        IconButton(
          icon: Icon(
            themeProvider.isDarkMode ? Icons.dark_mode : Icons.light_mode,
          ),
          onPressed: () => themeProvider.setDarkMode(!themeProvider.isDarkMode),
        ),
      ],
    );
  }

  // BottomNavigationBar dynamique
  Widget _buildBottomNavigationBar() {
    return Consumer2<BoardProvider, IdeaProvider>(
      builder: (context, boardProvider, ideaProvider, _) {
        // Compter les tâches par section
        final totalTasks = ideaProvider.ideas.length;
        final boards = boardProvider.boards.length;

        return BottomNavigationBar(
          currentIndex: _selectedNavIndex,
          onTap: (index) => setState(() => _selectedNavIndex = index),
          type: BottomNavigationBarType.fixed,
          items: [
            BottomNavigationBarItem(
              icon: Badge(
                label: totalTasks > 0 ? Text(totalTasks.toString()) : null,
                child: const Icon(Icons.dashboard_rounded),
              ),
              label: 'Accueil',
            ),
            BottomNavigationBarItem(
              icon: Badge(
                label: boards > 0 ? Text(boards.toString()) : null,
                child: const Icon(Icons.view_kanban_rounded),
              ),
              label: 'Assistant',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.rocket_launch_rounded),
              label: 'Planning',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.bar_chart_rounded),
              label: 'Révisions',
            ),
            const BottomNavigationBarItem(
              icon: Icon(Icons.auto_awesome),
              label: 'Orientation',
            ),
          ],
        );
      },
    );
  }

  // ---------------- Méthodes ----------------
  void _showAddBoardDialog() {
    final controller = TextEditingController();
    final authProvider = context.read<AuthProvider>();
    final userId = authProvider.userId;

    if (userId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Row(
            children: [
              Icon(Icons.error, color: Colors.white),
              SizedBox(width: 8),
              Text('Vous devez être connecté pour créer un espace'),
            ],
          ),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(
              Icons.add_circle,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(width: 12),
            const Text('Nouvel espace'),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: controller,
              autofocus: true,
              decoration: InputDecoration(
                labelText: 'Nom de l\'espace',
                border: const OutlineInputBorder(),
                prefixIcon: const Icon(Icons.dashboard),
                hintText: 'Ex: Mémoire IA, Examens, Stage',
                helperText: 'Donnez un nom à votre espace de suivi',
              ),
              textCapitalization: TextCapitalization.words,
              onSubmitted: (_) =>
                  _createBoard(context, controller.text, userId),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Annuler'),
          ),
          FilledButton.icon(
            onPressed: () => _createBoard(context, controller.text, userId),
            icon: const Icon(Icons.check),
            label: const Text('Créer'),
          ),
        ],
      ),
    );
  }

  // Méthode pour créer un tableau avec feedback
  Future<void> _createBoard(
    BuildContext dialogContext,
    String name,
    int userId,
  ) async {
    if (name.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Row(
            children: [
              Icon(Icons.warning, color: Colors.white),
              SizedBox(width: 8),
              Text('Le nom de l\'espace ne peut pas être vide'),
            ],
          ),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    Navigator.pop(dialogContext); // Fermer le dialogue avec le bon context

    // Afficher un indicateur de chargement
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Row(
          children: [
            SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              ),
            ),
            SizedBox(width: 12),
            Text('Création de l\'espace en cours...'),
          ],
        ),
        duration: Duration(seconds: 2),
      ),
    );

    try {
      final boardProvider = context.read<BoardProvider>();
      await boardProvider.addBoard(
        Board(userId: userId.toString(), name: name.trim()).toMap(),
      );

      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.check_circle, color: Colors.white),
                const SizedBox(width: 8),
                Text('Espace "${name.trim()}" créé avec succès !'),
              ],
            ),
            backgroundColor: Colors.green,
            duration: const Duration(seconds: 2),
            action: SnackBarAction(
              label: 'Voir',
              textColor: Colors.white,
              onPressed: () {
                setState(() => _selectedNavIndex = 1);
              },
            ),
          ),
        );

        // Sélectionner automatiquement le nouvel espace et aller à l'assistant
        setState(() => _selectedNavIndex = 1);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: 8),
                Text('Erreur: ${e.toString()}'),
              ],
            ),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 3),
          ),
        );
      }
    }
  }

  void _showRenameBoardDialog(int boardId, String currentName) {
    final controller = TextEditingController(text: currentName);
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Renommer l\'espace'),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: const InputDecoration(
            labelText: 'Nouveau nom',
            border: OutlineInputBorder(),
            prefixIcon: Icon(Icons.edit),
          ),
          onSubmitted: (_) => _renameBoard(context, boardId, controller.text),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Annuler'),
          ),
          FilledButton.icon(
            onPressed: () => _renameBoard(context, boardId, controller.text),
            icon: const Icon(Icons.check),
            label: const Text('Renommer'),
          ),
        ],
      ),
    );
  }

  // Méthode pour renommer un espace avec feedback
  Future<void> _renameBoard(
    BuildContext context,
    int boardId,
    String newName,
  ) async {
    if (newName.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Row(
            children: [
              Icon(Icons.warning, color: Colors.white),
              SizedBox(width: 8),
              Text('Le nom ne peut pas être vide'),
            ],
          ),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    Navigator.pop(context);

    try {
      await context.read<BoardProvider>().updateBoard(boardId, {
        'name': newName.trim(),
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 8),
                Text('Espace renommé avec succès'),
              ],
            ),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: 8),
                Text('Erreur: ${e.toString()}'),
              ],
            ),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _confirmDeleteBoard(int boardId) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.warning, color: Colors.red),
            SizedBox(width: 12),
            Text('Supprimer l\'espace ?'),
          ],
        ),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Cette action est irréversible.',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text(
              'Toutes les cartes et colonnes de cet espace seront supprimées définitivement.',
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Annuler'),
          ),
          FilledButton.icon(
            onPressed: () => _deleteBoard(context, boardId),
            icon: const Icon(Icons.delete_forever),
            label: const Text('Supprimer'),
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteBoard(BuildContext context, int boardId) async {
    Navigator.pop(context);

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Row(
          children: [
            SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              ),
            ),
            SizedBox(width: 12),
            Text('Suppression de l\'espace en cours...'),
          ],
        ),
      ),
    );

    try {
      await context.read<BoardProvider>().deleteBoard(boardId);

      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 8),
                Text('Espace supprimé avec succès'),
              ],
            ),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erreur: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  // ---------------- Drawer complètement dynamique ----------------
  Widget _buildDrawer(BuildContext context) {
    return Consumer3<BoardProvider, AuthProvider, IdeaProvider>(
      builder: (context, boardProvider, authProvider, ideaProvider, _) {
        final theme = Theme.of(context);

        // Statistiques en temps réel
        final totalTasks = ideaProvider.ideas.length;
        final completedTasks = ideaProvider.ideas
            .where((i) => i['status'] == 'Done')
            .length;
        final inProgressTasks = ideaProvider.ideas
            .where((i) => i['status'] == 'In Progress')
            .length;
        final backlogTasks = ideaProvider.ideas
            .where((i) => i['status'] == 'Backlog')
            .length;

        return Drawer(
          child: ListView(
            padding: EdgeInsets.zero,
            children: [
              // Header utilisateur dynamique
              UserAccountsDrawerHeader(
                accountName: Text(authProvider.userName ?? 'User'),
                accountEmail: Text(authProvider.userEmail ?? ''),
                currentAccountPicture: CircleAvatar(
                  backgroundColor: theme.colorScheme.primaryContainer,
                  child: Text(
                    authProvider.userName?.substring(0, 1).toUpperCase() ?? 'U',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: theme.colorScheme.primary,
                    ),
                  ),
                ),
                decoration: BoxDecoration(
                  color: theme.colorScheme.primaryContainer,
                ),
              ),

              // Section Statistiques dynamiques avec animation
              if (totalTasks > 0)
                AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  margin: const EdgeInsets.all(16),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.primaryContainer.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: theme.colorScheme.primary.withOpacity(0.2),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.insights,
                            color: theme.colorScheme.primary,
                            size: 20,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            'Indicateurs en direct',
                            style: theme.textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      _buildStatRow(
                        Icons.task,
                        'Total',
                        totalTasks.toString(),
                        theme,
                      ),
                      _buildStatRow(
                        Icons.inbox,
                        'Backlog',
                        backlogTasks.toString(),
                        theme,
                      ),
                      _buildStatRow(
                        Icons.play_circle,
                        'En cours',
                        inProgressTasks.toString(),
                        theme,
                      ),
                      _buildStatRow(
                        Icons.check_circle,
                        'Terminées',
                        completedTasks.toString(),
                        theme,
                      ),
                      const SizedBox(height: 12),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: TweenAnimationBuilder<double>(
                          duration: const Duration(milliseconds: 500),
                          tween: Tween(
                            begin: 0,
                            end: totalTasks > 0
                                ? completedTasks / totalTasks
                                : 0,
                          ),
                          builder: (context, value, _) {
                            return LinearProgressIndicator(
                              value: value,
                              minHeight: 8,
                              backgroundColor:
                                  theme.colorScheme.surfaceContainerHighest,
                              color: theme.colorScheme.primary,
                            );
                          },
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '${totalTasks > 0 ? ((completedTasks / totalTasks) * 100).toStringAsFixed(0) : 0}% complété',
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: theme.colorScheme.onSurface.withOpacity(0.6),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                ),

              const Divider(),

              // Section Tableaux dynamique
              ListTile(
                leading: Icon(
                  Icons.view_kanban,
                  color: theme.colorScheme.primary,
                ),
                title: const Text('Mes espaces'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (boardProvider.boards.isNotEmpty)
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: theme.colorScheme.primaryContainer,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          boardProvider.boards.length.toString(),
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: theme.colorScheme.primary,
                          ),
                        ),
                      ),
                    const SizedBox(width: 8),
                    IconButton(
                      icon: const Icon(Icons.add_circle),
                      onPressed: _showAddBoardDialog,
                      tooltip: 'Nouvel espace',
                    ),
                  ],
                ),
              ),

              // Liste des tableaux avec animation
              AnimatedSwitcher(
                duration: const Duration(milliseconds: 300),
                child: boardProvider.boards.isEmpty
                    ? Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          children: [
                            Icon(
                              Icons.inbox_outlined,
                              size: 48,
                              color: theme.colorScheme.onSurface.withOpacity(
                                0.3,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Aucun espace',
                              style: theme.textTheme.bodyMedium?.copyWith(
                                color: theme.colorScheme.onSurface.withOpacity(
                                  0.6,
                                ),
                              ),
                            ),
                          ],
                        ),
                      )
                    : Column(
                        children: boardProvider.boards.map((board) {
                          final isSelected =
                              board['id'] == boardProvider.selectedBoardId;
                          return ListTile(
                            leading: Icon(
                              Icons.view_column_rounded,
                              color: isSelected
                                  ? theme.colorScheme.primary
                                  : theme.colorScheme.onSurface.withOpacity(
                                      0.6,
                                    ),
                            ),
                            title: Text(
                              board['name'],
                              style: TextStyle(
                                fontWeight: isSelected
                                    ? FontWeight.bold
                                    : FontWeight.normal,
                                color: isSelected
                                    ? theme.colorScheme.primary
                                    : null,
                              ),
                            ),
                            selected: isSelected,
                            selectedTileColor: theme
                                .colorScheme
                                .primaryContainer
                                .withOpacity(0.3),
                            onTap: () {
                              boardProvider.selectBoard(board['id']);
                              setState(() => _selectedNavIndex = 1);
                              Navigator.pop(context);
                            },
                            trailing: isSelected
                                ? PopupMenuButton(
                                    itemBuilder: (context) => [
                                      PopupMenuItem(
                                        onTap: () => Future.delayed(
                                          Duration.zero,
                                          () => _showRenameBoardDialog(
                                            board['id'],
                                            board['name'],
                                          ),
                                        ),
                                        child: const Row(
                                          children: [
                                            Icon(Icons.edit, size: 18),
                                            SizedBox(width: 8),
                                            Text('Renommer'),
                                          ],
                                        ),
                                      ),
                                      PopupMenuItem(
                                        onTap: () => Future.delayed(
                                          Duration.zero,
                                          () =>
                                              _confirmDeleteBoard(board['id']),
                                        ),
                                        child: const Row(
                                          children: [
                                            Icon(
                                              Icons.delete,
                                              size: 18,
                                              color: Colors.red,
                                            ),
                                            SizedBox(width: 8),
                                            Text(
                                              'Supprimer',
                                              style: TextStyle(
                                                color: Colors.red,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  )
                                : null,
                          );
                        }).toList(),
                      ),
              ),

              const Divider(),

              // Bouton de déconnexion dynamique
              ListTile(
                leading: const Icon(Icons.logout, color: Colors.red),
                title: const Text(
                  'Déconnexion',
                  style: TextStyle(color: Colors.red),
                ),
                onTap: () {
                  authProvider.logout();
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute(builder: (_) => const AuthScreen()),
                  );
                },
              ),
            ],
          ),
        );
      },
    );
  }

  // Widget helper pour les statistiques
  Widget _buildStatRow(
    IconData icon,
    String label,
    String value,
    ThemeData theme,
  ) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(icon, size: 18, color: theme.colorScheme.primary),
          const SizedBox(width: 8),
          Text(label, style: theme.textTheme.bodyMedium),
          const Spacer(),
          Text(
            value,
            style: theme.textTheme.bodyMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: theme.colorScheme.primary,
            ),
          ),
        ],
      ),
    );
  }
}

// ----------------- Widgets -----------------
class _NoboardsEmptyState extends StatelessWidget {
  final VoidCallback onCreateBoard;
  const _NoboardsEmptyState({required this.onCreateBoard});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: FilledButton.icon(
        onPressed: onCreateBoard,
        icon: const Icon(Icons.add_circle_outline),
        label: const Text('Créer votre premier espace'),
      ),
    );
  }
}
