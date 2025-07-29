import 'package:flutter/material.dart';
import 'pages/auth_page.dart';
import 'pages/home_page.dart';
import 'pages/profile_page.dart';

void main() {
  runApp(const CalorieApp());
}

class CalorieApp extends StatelessWidget {
  const CalorieApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CaloriQ - Food Calorie Predictor',
      theme: ThemeData(
        primarySwatch: Colors.green,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.green,
          foregroundColor: Colors.white,
          elevation: 2,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),
      ),
      home: const AuthPage(),
      // Using onGenerateRoute for better parameter passing
      onGenerateRoute: (RouteSettings settings) {
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(
              builder: (context) => const AuthPage(),
            );
          case '/auth':
            return MaterialPageRoute(
              builder: (context) => const AuthPage(),
            );
          case '/home':
            final userData = settings.arguments as Map<String, dynamic>?;
            return MaterialPageRoute(
              builder: (context) => HomePage(userData: userData),
            );
          case '/profile':
            final userData = settings.arguments as Map<String, dynamic>;
            return MaterialPageRoute(
              builder: (context) => ProfilePage(userData: userData),
            );
          default:
            // Return 404 page or redirect to auth
            return MaterialPageRoute(
              builder: (context) => const AuthPage(),
            );
        }
      },
      debugShowCheckedModeBanner: false,
    );
  }
}