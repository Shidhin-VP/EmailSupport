from langchain.agents import initialize_agent, AgentType,Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from .tools import classify_email, assess_urgency, generate_reply

def get_email_agent():
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4", temperature=0)
    
    # tools = [classify_email, assess_urgency, generate_reply]

    tools = [
    Tool(
        name="classify_email",
        func=classify_email,
        description="Classify the email into categories like billing, bug, how-to, abuse/spam, or other."
    ),
    Tool(
        name="assess_urgency",
        func=assess_urgency,
        description="Assess the urgency level of the email: low, medium, or high."
    ),
    Tool(
        name="generate_reply",
        func=generate_reply,
        description="Generate a helpful, on-brand reply to the email."
    )
]
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    
    return agent

def analyze_email(email: str) -> dict:
    agent = get_email_agent()
    
    category = agent.run(f"Classify this email:\n{email}")
    urgency = agent.run(f"How urgent is this email?\n{email}")
    reply = agent.run(f"Draft a reply to this email:\n{email}")
    
    return {
        "category": category,
        "urgency": urgency,
        "reply": reply
    }
