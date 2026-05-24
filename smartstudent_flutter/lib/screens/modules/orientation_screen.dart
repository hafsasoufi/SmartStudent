import 'package:flutter/material.dart';

class OrientationScreen extends StatelessWidget {
  const OrientationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Orientation')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.work, size: 60, color: Colors.green),
            const SizedBox(height: 16),
            const Text('Orientation Module'),
            const SizedBox(height: 8),
            Text(
              'Career • CV • Internships',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
