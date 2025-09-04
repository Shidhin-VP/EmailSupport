from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4", temperature=0)

def classify_email(input_text: str) -> str:
    from langchain.schema import HumanMessage, SystemMessage

    messages = [
        SystemMessage(content="You are an email classifier. Classify the email into one of: billing, bug, how-to, abuse/spam, other."),
        HumanMessage(content=input_text),
    ]

    response = llm.invoke(messages)
    return response.content.strip()


def assess_urgency(input_text: str) -> str:
    from langchain.schema import HumanMessage, SystemMessage

    messages = [
        SystemMessage(content="Determine the urgency of this email: low, medium, or high."),
        HumanMessage(content=input_text),
    ]

    response = llm.invoke(messages)
    return response.content.strip()


def generate_reply(input_text: str) -> str:
    from langchain.schema import HumanMessage, SystemMessage

    messages = [
        SystemMessage(content="You are a helpful support agent. Draft a safe and on-brand reply to the customer."),
        HumanMessage(content=input_text),
    ]

    response = llm.invoke(messages)
    return response.content.strip()
