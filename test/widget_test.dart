import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:startuplaunchpad/providers/auth_provider.dart';
import 'package:startuplaunchpad/screens/auth_screen.dart';

void main() {
  testWidgets('renders SmartStudent auth screen', (WidgetTester tester) async {
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => AuthProvider(),
        child: const MaterialApp(home: AuthScreen()),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('SmartStudent'), findsOneWidget);
    expect(find.text('Accédez à votre assistant étudiant IA'), findsOneWidget);
  });
}
