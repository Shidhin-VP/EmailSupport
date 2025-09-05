import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:dash_chat_2/dash_chat_2.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final ChatUser user = ChatUser(id: '1', firstName: 'User');
  final ChatUser assistant = ChatUser(id: '2', firstName: 'Assistant');

  List<ChatMessage> messages = [];

  /// Converts the user message into a structured email JSON
  Map<String, dynamic> buildEmailJson(String messageText) {
    return {
      "id": "flutter-${DateTime.now().millisecondsSinceEpoch}",
      "from_email": "mobileuser@example.com",
      "subject": "User Query from Flutter App",
      "body": messageText,
    };
  }

  /// Sends the email JSON to backend and receives structured response
  Future<Map<String, dynamic>> sendEmailToBackend(String userMessage) async {
    final endpoint = dotenv.env['endPoint'];
    if (endpoint == null) throw Exception("Backend endpoint not configured");

    final emailJson = buildEmailJson(userMessage);

    final response = await http.post(
      Uri.parse(endpoint),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(emailJson),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body); // contains category, urgency, reply
    } else {
      throw Exception("Failed with status ${response.statusCode}: ${response.body}");
    }
  }

  /// Handles sending user message and getting AI reply
  Future<void> handleUserMessage(ChatMessage message) async {
    setState(() {
      messages.insert(0, message);
    });

    try {
      final response = await sendEmailToBackend(message.text);

      final replyText = '''
🧠 *Category:* ${response['category'] ?? 'N/A'}
⚠️ *Urgency:* ${response['urgency'] ?? 'N/A'}
✉️ *Reply:* ${response['reply'] ?? 'N/A'}
''';

      final botMessage = ChatMessage(
        user: assistant,
        text: replyText,
        createdAt: DateTime.now(),
      );

      setState(() {
        messages.insert(0, botMessage);
      });
    } catch (e) {
      final errorMessage = ChatMessage(
        user: assistant,
        text: "❌ Error: ${e.toString()}",
        createdAt: DateTime.now(),
      );

      setState(() {
        messages.insert(0, errorMessage);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Email Support"),
        centerTitle: true,
        elevation: 5,
        backgroundColor: Colors.deepOrangeAccent,
      ),
      body: SafeArea(
        child: DashChat(
          currentUser: user,
          onSend: handleUserMessage,
          messages: messages,
        ),
      ),
    );
  }
}
