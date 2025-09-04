from pydantic import BaseModel

class EmailRequest(BaseModel):
    id: str
    from_email: str
    subject: str
    body: str

class EmailResponse(BaseModel):
    category: str
    urgency: str
    reply: str
