import 'package:flutter/material.dart';
import 'package:frontend/screens/theme/theme_provider.dart';
import 'package:frontend/services/api_service.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final oldPasswordController = TextEditingController();
  final newPasswordController = TextEditingController();
  final confirmNewPasswordController = TextEditingController();

  String? oldPasswordError;
  String? newPasswordError;
  String? confirmPasswordError;
  bool isLoading = false;
  bool showOldPassword = false;
  bool showNewPassword = false;
  bool showConfirmPassword = false;

  final passwordRegex =
      RegExp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.]).{8,}$');

  Future<void> _changePassword() async {
    setState(() {
      oldPasswordError = null;
      newPasswordError = null;
      confirmPasswordError = null;
    });

    final old = oldPasswordController.text.trim();
    final newP = newPasswordController.text.trim();
    final confirm = confirmNewPasswordController.text.trim();

    bool hasError = false;

    if (!passwordRegex.hasMatch(newP)) {
      newPasswordError =
          "Minimum 8 characters, must include letter, number, and symbol.";
      hasError = true;
    }

    if (old == newP) {
      newPasswordError =
          "New password must be different from the old password.";
      hasError = true;
    }

    if (newP != confirm) {
      confirmPasswordError = "Passwords do not match.";
      hasError = true;
    }

    if (hasError) {
      setState(() {});
      return;
    }

    setState(() => isLoading = true);

    try {
      await ApiService.changePassword(
        oldPassword: old,
        newPassword: newP,
        confirmNewPassword: confirm,
      );

      _showSnackBar("Password changed successfully", isSuccess: true);

      oldPasswordController.clear();
      newPasswordController.clear();
      confirmNewPasswordController.clear();
    } catch (e) {
      final error = e.toString().toLowerCase();
      if (error.contains("old password")) {
        setState(() => oldPasswordError = "Old password is incorrect.");
      } else if (error.contains("match")) {
        setState(() => confirmPasswordError = "Passwords do not match.");
      } else if (error.contains("must be different")) {
        setState(() => newPasswordError = "New password must be different.");
      } else {
        _showSnackBar("Error: ${e.toString()}");
      }
    } finally {
      setState(() => isLoading = false);
    }
  }

  void _showSnackBar(String message, {bool isSuccess = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: const Duration(seconds: 2),
        backgroundColor:
            isSuccess ? Colors.green.shade400 : Colors.red.shade400,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    const lightBgColor = Color(0xFFF0F6FF);
    const lightTextColor = Color(0xFF4991FF);
    const yellowBoxColor = Color(0xFFFFF3CD);

    final textColor = isDark ? Colors.white : lightTextColor;
    final bgColor = isDark ? Colors.black : lightBgColor;
    final cardColor = isDark ? Colors.grey[850] : yellowBoxColor;

    return Scaffold(
      backgroundColor: bgColor,
      floatingActionButton: Padding(
        padding: const EdgeInsets.only(bottom: 2),
        child: FloatingActionButton(
          onPressed: () => context.go('/scan-select'),
          backgroundColor: Colors.blue,
          shape: const CircleBorder(),
          child: const Icon(Icons.camera_alt),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 480),
          child: Column(
            children: [
              // Custom AppBar replacement
              SafeArea(
                bottom: false,
                child: Container(
                  color: bgColor,
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 12),
                  child: Row(
                    children: [
                      const SizedBox(width: 8),
                      Text(
                        'Settings',
                        style: TextStyle(
                          color: textColor,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              // Scrollable body content
              Expanded(
                child: ListView(
                  padding: const EdgeInsets.all(20),
                  children: [
                    ListTile(
                      contentPadding: EdgeInsets.zero,
                      leading: Icon(Icons.dark_mode, color: textColor),
                      title: Text(
                        'Dark Mode',
                        style: TextStyle(
                          color: textColor,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      trailing: GestureDetector(
                        onTap: () => themeProvider
                            .toggleTheme(!themeProvider.isDarkMode),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          width: 60,
                          height: 30,
                          padding: const EdgeInsets.all(4),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(30),
                            color: themeProvider.isDarkMode
                                ? Colors.grey[800]
                                : Colors.grey[300],
                          ),
                          child: AnimatedAlign(
                            duration: const Duration(milliseconds: 300),
                            alignment: themeProvider.isDarkMode
                                ? Alignment.centerRight
                                : Alignment.centerLeft,
                            child: Container(
                              width: 24,
                              height: 24,
                              decoration: const BoxDecoration(
                                shape: BoxShape.circle,
                                color: Colors.white,
                              ),
                              child: Icon(
                                themeProvider.isDarkMode
                                    ? Icons.nightlight_round
                                    : Icons.wb_sunny_rounded,
                                size: 16,
                                color: themeProvider.isDarkMode
                                    ? Colors.black
                                    : Colors.orangeAccent,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: cardColor,
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.04),
                            blurRadius: 6,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          const Text(
                            "Change Password",
                            style: TextStyle(
                                fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 16),
                          _buildPasswordField(
                            label: "Old Password",
                            controller: oldPasswordController,
                            show: showOldPassword,
                            toggle: () => setState(
                                () => showOldPassword = !showOldPassword),
                            errorText: oldPasswordError,
                          ),
                          const SizedBox(height: 12),
                          _buildPasswordField(
                            label: "New Password",
                            controller: newPasswordController,
                            show: showNewPassword,
                            toggle: () => setState(
                                () => showNewPassword = !showNewPassword),
                            errorText: newPasswordError,
                          ),
                          const SizedBox(height: 12),
                          _buildPasswordField(
                            label: "Confirm New Password",
                            controller: confirmNewPasswordController,
                            show: showConfirmPassword,
                            toggle: () => setState(() =>
                                showConfirmPassword = !showConfirmPassword),
                            errorText: confirmPasswordError,
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: isLoading ? null : _changePassword,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: lightTextColor,
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 40, vertical: 12),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                            child: Text(
                              isLoading ? "Changing..." : "Change Password",
                              style: const TextStyle(color: Colors.white),
                            ),
                          ),
                        ],
                      ),
                    )
                  ],
                ),
              ),
              // Custom bottom navbar
              SafeArea(
                top: false,
                child: Container(
                  color: bgColor,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      SizedBox(
                        height: 56,
                        child: IconButton(
                          icon: Icon(Icons.home,
                              color: isDark ? Colors.white70 : Colors.black),
                          onPressed: () => context.go('/home'),
                        ),
                      ),
                      SizedBox(
                        height: 56,
                        child: IconButton(
                          icon: Icon(Icons.history,
                              color: isDark ? Colors.white70 : Colors.black),
                          onPressed: () => context.go('/reports'),
                        ),
                      ),
                      const SizedBox(width: 56),
                      SizedBox(
                        height: 56,
                        child: IconButton(
                          icon: Icon(Icons.person,
                              color: isDark ? Colors.white70 : Colors.black),
                          onPressed: () => context.go('/profile'),
                        ),
                      ),
                      SizedBox(
                        height: 56,
                        child: IconButton(
                          icon: const Icon(Icons.settings,
                              color: Colors.blueAccent),
                          onPressed: () => context.go('/settings-screen'),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPasswordField({
    required String label,
    required TextEditingController controller,
    required bool show,
    required VoidCallback toggle,
    String? errorText,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextField(
          controller: controller,
          obscureText: !show,
          decoration: InputDecoration(
            labelText: label,
            border: const OutlineInputBorder(),
            suffixIcon: IconButton(
              icon: Icon(show ? Icons.visibility : Icons.visibility_off),
              onPressed: toggle,
            ),
          ),
        ),
        if (errorText != null)
          Padding(
            padding: const EdgeInsets.only(top: 6, left: 4),
            child: Text(
              errorText,
              style: const TextStyle(color: Colors.red, fontSize: 13),
            ),
          ),
      ],
    );
  }
}
