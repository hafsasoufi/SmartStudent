import 'package:flutter/material.dart';

class CampusScreen extends StatelessWidget {
  const CampusScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Campus')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.campus_rounded, size: 60, color: Colors.purple),
            const SizedBox(height: 16),
            const Text('Campus Module'),
            const SizedBox(height: 8),
            Text(
              'Events • Clubs • Groups',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
