import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../providers/auth_provider.dart';
import '../../services/api_service.dart';

class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _firstNameController   = TextEditingController();
  final _lastNameController    = TextEditingController();
  final _studentCardController = TextEditingController();
  final _fieldOfStudyController = TextEditingController();
  final _emailController       = TextEditingController();
  final _usernameController    = TextEditingController();
  final _passwordController    = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  int? _selectedYear;

  static const _years = [1, 2, 3, 4, 5];

  @override
  void dispose() {
    _firstNameController.dispose();
    _lastNameController.dispose();
    _studentCardController.dispose();
    _fieldOfStudyController.dispose();
    _emailController.dispose();
    _usernameController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _handleRegister() async {
    if (_formKey.currentState!.validate()) {
      final firstName = _firstNameController.text.trim();
      final lastName  = _lastNameController.text.trim();
      try {
        await ref.read(authProvider.notifier).register(
          email:         _emailController.text.trim(),
          username:      _usernameController.text.trim(),
          password:      _passwordController.text,
          fullName:      '$firstName $lastName'.trim(),
          firstName:     firstName,
          lastName:      lastName,
          studentCardId: _studentCardController.text.trim(),
          fieldOfStudy:  _fieldOfStudyController.text.trim(),
          academicYear:  _selectedYear,
        );
        if (mounted && context.mounted) context.go('/home');
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Inscription echouee: $e')),
          );
        }
      }
    }
  }

  Widget _field({
    required TextEditingController controller,
    required String label,
    required String hint,
    required IconData icon,
    bool obscure = false,
    TextInputType? keyboard,
    String? Function(String?)? validator,
  }) {
    return TextFormField(
      controller: controller,
      decoration: InputDecoration(labelText: label, hintText: hint, prefixIcon: Icon(icon)),
      obscureText: obscure,
      keyboardType: keyboard,
      validator: validator,
    );
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    const kBlue = Color(0xFF0052A5);

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header
                Icon(Icons.school, size: 52, color: kBlue),
                const SizedBox(height: 12),
                const Text('Inscription SmartStudent',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center),
                const SizedBox(height: 4),
                Text('Renseignez vos informations académiques',
                    style: TextStyle(fontSize: 13, color: Colors.grey[600]),
                    textAlign: TextAlign.center),
                const SizedBox(height: 28),

                // ── Identité
                _sectionLabel('Identite'),
                const SizedBox(height: 10),
                Row(children: [
                  Expanded(child: _field(
                    controller: _firstNameController, label: 'Prenom', hint: 'Votre prenom',
                    icon: Icons.person_outline,
                    validator: (v) => (v?.isEmpty ?? true) ? 'Requis' : null,
                  )),
                  const SizedBox(width: 12),
                  Expanded(child: _field(
                    controller: _lastNameController, label: 'Nom', hint: 'Votre nom',
                    icon: Icons.person,
                    validator: (v) => (v?.isEmpty ?? true) ? 'Requis' : null,
                  )),
                ]),
                const SizedBox(height: 14),
                _field(
                  controller: _studentCardController,
                  label: 'N° Carte etudiant', hint: 'Ex: 20251234',
                  icon: Icons.badge_outlined,
                  validator: (v) => (v?.isEmpty ?? true) ? 'Requis pour les documents PDF' : null,
                ),

                const SizedBox(height: 20),
                // ── Académique
                _sectionLabel('Informations academiques'),
                const SizedBox(height: 10),
                _field(
                  controller: _fieldOfStudyController,
                  label: 'Filiere', hint: 'Ex: Genie Informatique',
                  icon: Icons.menu_book_outlined,
                  validator: (v) => (v?.isEmpty ?? true) ? 'Requis' : null,
                ),
                const SizedBox(height: 14),
                DropdownButtonFormField<int>(
                  value: _selectedYear,
                  decoration: const InputDecoration(
                    labelText: 'Annee d\'etude',
                    prefixIcon: Icon(Icons.calendar_today_outlined),
                  ),
                  items: _years.map((y) => DropdownMenuItem(
                    value: y, child: Text('Annee $y'),
                  )).toList(),
                  onChanged: (v) => setState(() => _selectedYear = v),
                  validator: (v) => v == null ? 'Selectionnez votre annee' : null,
                ),

                const SizedBox(height: 20),
                // ── Compte
                _sectionLabel('Compte'),
                const SizedBox(height: 10),
                _field(
                  controller: _emailController, label: 'Email', hint: 'votre@email.com',
                  icon: Icons.email_outlined, keyboard: TextInputType.emailAddress,
                  validator: (v) {
                    if (v?.isEmpty ?? true) return 'Email requis';
                    if (!v!.contains('@')) return 'Email invalide';
                    return null;
                  },
                ),
                const SizedBox(height: 14),
                _field(
                  controller: _usernameController, label: 'Nom d\'utilisateur',
                  hint: 'Choisissez un identifiant', icon: Icons.account_circle_outlined,
                  validator: (v) {
                    if (v?.isEmpty ?? true) return 'Requis';
                    if (v!.length < 3) return 'Minimum 3 caracteres';
                    return null;
                  },
                ),
                const SizedBox(height: 14),
                _field(
                  controller: _passwordController, label: 'Mot de passe',
                  hint: 'Minimum 8 caracteres', icon: Icons.lock_outline, obscure: true,
                  validator: (v) {
                    if (v?.isEmpty ?? true) return 'Requis';
                    if (v!.length < 8) return 'Minimum 8 caracteres';
                    return null;
                  },
                ),
                const SizedBox(height: 14),
                _field(
                  controller: _confirmPasswordController, label: 'Confirmer le mot de passe',
                  hint: 'Repetez le mot de passe', icon: Icons.lock, obscure: true,
                  validator: (v) {
                    if (v?.isEmpty ?? true) return 'Requis';
                    if (v != _passwordController.text) return 'Les mots de passe ne correspondent pas';
                    return null;
                  },
                ),

                const SizedBox(height: 28),
                ElevatedButton(
                  onPressed: authState.isLoading ? null : _handleRegister,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: kBlue,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: authState.isLoading
                    ? const SizedBox(height: 20, width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('Creer mon compte',
                        style: TextStyle(fontSize: 16, color: Colors.white, fontWeight: FontWeight.bold)),
                ),

                const SizedBox(height: 16),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  const Text('Deja un compte ? '),
                  GestureDetector(
                    onTap: () => context.push('/login'),
                    child: Text('Se connecter',
                      style: TextStyle(color: kBlue, fontWeight: FontWeight.w600)),
                  ),
                ]),

              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _sectionLabel(String text) {
    return Row(children: [
      Container(width: 4, height: 16, color: const Color(0xFF0052A5),
          margin: const EdgeInsets.only(right: 8)),
      Text(text.toUpperCase(),
          style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold,
              letterSpacing: 1.2, color: Color(0xFF0052A5))),
    ]);
  }
}
