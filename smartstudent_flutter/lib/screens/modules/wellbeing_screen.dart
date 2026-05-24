import 'package:flutter/material.dart';

class WellbeingScreen extends StatelessWidget {
  const WellbeingScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Well-being')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.favorite, size: 60, color: Colors.pink),
            const SizedBox(height: 16),
            const Text('Well-being Module'),
            const SizedBox(height: 8),
            Text(
              'Health • Support • Wellness',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
