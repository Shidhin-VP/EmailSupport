from fastapi import FastAPI
from models import EmailRequest, EmailResponse
from agent import analyze_email
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")
def root():
    return {"Message":"Hello from EmailApp"}

@app.post("/process-email", response_model=EmailResponse)
def process_email(email: EmailRequest):
    combined_email = f"From: {email.from_email}\nSubject: {email.subject}\n\n{email.body}"
    
    result = analyze_email(combined_email)
    
    return EmailResponse(
        category=result["category"],
        urgency=result["urgency"],
        reply=result["reply"]
    )
