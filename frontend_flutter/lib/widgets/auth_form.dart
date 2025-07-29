import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../pages/home_page.dart';

class AuthForm extends StatefulWidget {
  const AuthForm({super.key});

  @override
  State<AuthForm> createState() => _AuthFormState();
}

class _AuthFormState extends State<AuthForm> {
  final _formKey = GlobalKey<FormState>();
  bool isLogin = true;  // Start with login by default
  String fullName = '';
  String username = '';
  String email = '';
  String password = '';
  String confirmPassword = '';
  String message = '';
  bool isLoading = false;

  // ✅ Set this to your computer's local IP and port
  final String baseUrl = 'http://0.0.0.0:3000'; //Replace with your server url.

  Future<void> submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      isLoading = true;
      message = '';
    });

    try {
      final url = isLogin
          ? Uri.parse('$baseUrl/login')
          : Uri.parse('$baseUrl/authAdapter');

      final body = isLogin
          ? {
              'username': username,  // FIXED: Use username instead of email for login
              'password': password,
            }
          : {
              'fullName': fullName,  // FIXED: Match backend field name
              'username': username,
              'email': email,
              'password': password,
              'confirmPassword': confirmPassword,  // FIXED: Match backend field name
            };

      print('Sending request to: $url');
      print('Request body: $body');

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode(body),
      );

      print('Response status: ${response.statusCode}');
      print('Response body: ${response.body}');

      final resData = json.decode(response.body);

      if (response.statusCode == 200) {
        if (isLogin) {
          // FIXED: Check for correct status code and pass user data
          if (resData['statusCode'] == 'SC200') {
            final userData = resData['user'];
            // Navigate to HomePage with user data
            Navigator.of(context).pushReplacement(
              MaterialPageRoute(
                builder: (context) => HomePage(userData: userData),
              ),
            );
          } else {
            setState(() {
              message = resData['statusDesc'] ?? 'Login failed';
            });
          }
        } else {
          // Registration successful
          setState(() {
            message = resData['statusDesc'] ?? 'Registration successful! Please login.';
            isLogin = true; // Switch to login after successful registration
          });
        }
      } else {
        setState(() {
          message = resData['statusDesc'] ?? 'Something went wrong';
        });
      }
    } catch (e) {
      setState(() {
        message = 'Network error: $e';
      });
      print('Error: $e');
    }

    setState(() {
      isLoading = false;
    });
  }

  String? validateEmail(String? value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(value)) {
      return 'Enter a valid email';
    }
    return null;
  }

  String? validateUsername(String? value) {
    if (value == null || value.isEmpty) {
      return 'Username is required';
    }
    if (value.length < 3) {
      return 'Username must be at least 3 characters';
    }
    return null;
  }

  String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    if (value.length < 6) {
      return 'Password must be at least 6 characters';
    }
    return null;
  }

  String? validateConfirmPassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Please confirm your password';
    }
    if (value != password) {
      return 'Passwords do not match';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              // Logo/App Name
              Container(
                margin: const EdgeInsets.only(bottom: 30),
                child: Column(
                  children: [
                    Icon(
                      Icons.restaurant,
                      size: 60,
                      color: Colors.white,
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'CaloriQ',
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              ),
              
              Text(
                isLogin ? 'Welcome Back!' : 'Create Account',
                style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.white),
              ),
              const SizedBox(height: 20),

              // Form Fields
              if (!isLogin) ...[
                TextFormField(
                  decoration: InputDecoration(
                    labelText: 'Full Name',
                    labelStyle: const TextStyle(color: Colors.white70),
                    enabledBorder: const UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white70),
                    ),
                    focusedBorder: const UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                  ),
                  style: const TextStyle(color: Colors.white),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Full name is required';
                    }
                    return null;
                  },
                  onChanged: (value) => fullName = value,
                ),
                const SizedBox(height: 16),
              ],

              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Username',
                  labelStyle: const TextStyle(color: Colors.white70),
                  enabledBorder: const UnderlineInputBorder(
                    borderSide: BorderSide(color: Colors.white70),
                  ),
                  focusedBorder: const UnderlineInputBorder(
                    borderSide: BorderSide(color: Colors.white),
                  ),
                ),
                style: const TextStyle(color: Colors.white),
                validator: validateUsername,
                onChanged: (value) => username = value,
              ),
              const SizedBox(height: 16),

              if (!isLogin) ...[
                TextFormField(
                  decoration: InputDecoration(
                    labelText: 'Email',
                    labelStyle: const TextStyle(color: Colors.white70),
                    enabledBorder: const UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white70),
                    ),
                    focusedBorder: const UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                  ),
                  style: const TextStyle(color: Colors.white),
                  validator: validateEmail,
                  onChanged: (value) => email = value,
                ),
                const SizedBox(height: 16),
              ],

              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Password',
                  labelStyle: const TextStyle(color: Colors.white70),
                  enabledBorder: const UnderlineInputBorder(
                    borderSide: BorderSide(color: Colors.white70),
                  ),
                  focusedBorder: const UnderlineInputBorder(
                    borderSide: BorderSide(color: Colors.white),
                  ),
                ),
                style: const TextStyle(color: Colors.white),
                obscureText: true,
                validator: validatePassword,
                onChanged: (value) => password = value,
              ),
              const SizedBox(height: 16),

              if (!isLogin) ...[
                TextFormField(
                  decoration: InputDecoration(
                    labelText: 'Confirm Password',
                    labelStyle: const TextStyle(color: Colors.white70),
                    enabledBorder: const UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white70),
                    ),
                    focusedBorder: const UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                  ),
                  style: const TextStyle(color: Colors.white),
                  obscureText: true,
                  validator: validateConfirmPassword,
                  onChanged: (value) => confirmPassword = value,
                ),
                const SizedBox(height: 20),
              ] else ...[
                const SizedBox(height: 20),
              ],

              // Error/Success Message
              if (message.isNotEmpty)
                Container(
                  padding: const EdgeInsets.all(12),
                  margin: const EdgeInsets.only(bottom: 16),
                  decoration: BoxDecoration(
                    color: message.toLowerCase().contains('success')
                        ? Colors.green.withOpacity(0.2)
                        : Colors.red.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: message.toLowerCase().contains('success')
                          ? Colors.green
                          : Colors.red,
                    ),
                  ),
                  child: Text(
                    message,
                    style: TextStyle(
                      color: message.toLowerCase().contains('success')
                          ? Colors.green
                          : Colors.red,
                      fontWeight: FontWeight.w500,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),

              // Submit Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: isLoading ? null : submit,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        )
                      : Text(
                          isLogin ? 'Login' : 'Register',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),

              const SizedBox(height: 20),

              // Toggle Login/Register
              TextButton(
                onPressed: () {
                  setState(() {
                    isLogin = !isLogin;
                    message = '';
                    // Clear form when switching
                    fullName = '';
                    username = '';
                    email = '';
                    password = '';
                    confirmPassword = '';
                  });
                },
                child: Text(
                  isLogin
                      ? 'Don\'t have an account? Register here'
                      : 'Already have an account? Login here',
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 14,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}