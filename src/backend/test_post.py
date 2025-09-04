import requests

url = "http://127.0.0.1:8000/process-email"

email_data = {
    "id": "e1",
    "from_email": "jordan@example.com",
    "subject": "Charged twice on my invoice",
    "body": "Hi, I was billed twice for May. Invoice #12877. Can you refund the duplicate? Thanks."
}


response = requests.post(url, json=email_data)

if response.status_code == 200:
    result = response.json()
    print("✅ Response received:")
    print(f"Category: {result['category']}")
    print(f"Urgency: {result['urgency']}")
    print(f"Reply:\n{result['reply']}")
else:
    print("❌ Failed to get response:", response.status_code)
    print(response.text)
