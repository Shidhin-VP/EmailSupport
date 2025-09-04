CLASSIFY_PROMPT = """
Given this email, classify it and flag its urgency:

---
Subject: {subject}
Body: {body}
---

Respond in JSON like:
{{
  "category": "...",
  "urgency": "urgent" or "not urgent"
}}
"""

REPLY_PROMPT = """
You're a customer support agent for a software platform. Write a short, professional, friendly, and helpful reply to this email.

Email:
---
From: {sender}
Subject: {subject}
Body: {body}
---

Make sure it's on-brand, safe, and solves the user's issue.
"""
