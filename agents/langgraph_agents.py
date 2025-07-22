import google.generativeai as genai
from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
# from PIL import Image
from dotenv import load_dotenv

from agents.prompts import prompts

# Load environment variables from .env file
load_dotenv()

def call_agents(new_mail):
    """Agent1: Check if mail contains an event or some registration/work deadline.

    Agent2: Summarize the email and find the main entity

    Agent3: Extract the event details from the email
            (event_title, event_date, event_time, event_location, event_online_link)
    
    Agent4: Make a toolcall (tavily) to find something about the main entity
            if required
    """

    # ---- Stateless wrapper for Gemini ----
    class AgentState(TypedDict):
        user_input: str
        agent_output: str

    def agent1(state: AgentState) -> AgentState:
        """Check if mail contains an event or some registration/work deadline."""

        custom_prompt = prompts["agent1"].format(user_input=state['user_input'])
        model = genai.GenerativeModel("gemma-3-4b-it")
        response = model.generate_content(custom_prompt)
        # response = model.generate_content([custom_prompt, image])
        return {"user_input": state["user_input"], "agent_output": response.text}

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # ---- Build the LangGraph ----
    builder = StateGraph(AgentState)
    builder.add_node("GeminiAgent", agent1)
    # builder.add_edge("GeminiAgent", "END") # can also be used to end the graph
    builder.set_entry_point("GeminiAgent")
    builder.set_finish_point("GeminiAgent")  # Single-step, no loops

    graph = builder.compile()

    subject = new_mail.subject
    date = new_mail.date
    body = new_mail.body
    user_message = f"Email Subject: {subject}\n\nEmail Date: {date}\n\nEmail Body: {body}"
    
    result = graph.invoke({"user_input": user_message})
    print("\nGemini Agent:", result["agent_output"])

    return result["agent_output"]

# ---- Run it ----
if __name__ == "__main__":
    event = call_agents("Sample email content to extract events from.")
