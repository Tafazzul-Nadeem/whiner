import google.generativeai as genai
from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
# from PIL import Image
from dotenv import load_dotenv

from agents.langgraph_agents import call_agents
# Load environment variables from .env file
load_dotenv()

def get_events(new_mail, secrets):
    # Start the agentic call flow
    result = call_agents(new_mail, secrets)
    return result

# ---- Run it ----
if __name__ == "__main__":
    event = get_events("Sample email content to extract events from.")
    