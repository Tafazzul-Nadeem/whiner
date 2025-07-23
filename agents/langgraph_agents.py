import google.generativeai as genai
from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
import re
from tavily import TavilyClient

# from PIL import Image
from dotenv import load_dotenv

from agents.prompts import prompts

# Load environment variables from .env file
load_dotenv()

def call_agents(new_mail, secrets):
    """Agent1: Check if mail contains an event or some registration/work 
    deadline.

    Agent2: Summarize the email and find the main entity

    Agent3: Extract the event details from the email
    (event_title, event_date, event_time, event_location, event_online_link)
    
    Agent4: Make a toolcall (tavily) to find something about the main entity
            if required
    """

    # ---- Stateless wrapper for Gemini ----
    class AgentState(TypedDict):
        user_input: str
        email_reception_date: str
        important_mail: str
        web_search_required: str
        email_summary: str
        main_entity: str
        main_event_search: str
        event_title: str
        event_date: str
        event_time: str
        event_location: str
        event_online_link: str
        start_date_time: str
        end_date_time: str


    def agent1(state: AgentState) -> AgentState:
        """Check if mail contains an event or some 
        registration/work deadline."""
        print("Agent1: Checking if the email is important...")
        custom_prompt = prompts["agent1"].format(user_input=state['user_input'])
        model = genai.GenerativeModel("gemma-3-4b-it")
        response = model.generate_content(custom_prompt)
        # response = model.generate_content([custom_prompt, image])
        print("Agent1 Response:", response.text.strip())
        return {"important_mail": response.text.strip()}

    def router_node(state: AgentState) -> dict:
        print("Router: Checking if the email is important...")
        imp_mail = state["important_mail"].upper()
        if "YES" in imp_mail:
            return {"next_node": ["run_agent2", "run_agent3"]}  # Proceed to Agent2 and Agent3
        else:
            return {"next_node": "end_flow"}  

    def agent2(state: AgentState) -> AgentState:
        """Summarize the email and find the main entity."""
        print("Agent2: Summarizing the email and finding the main entity...")
        custom_prompt = prompts["agent2"].format(user_input=state['user_input'])
        model = genai.GenerativeModel("gemma-3-4b-it")
        response = model.generate_content(custom_prompt)
        # Extract summary and main entity from the response
        match = re.search(r"Summary:\s*(.*?)\s*Main Entity:\s*(.*?)\s*Web Search Required:\s*(.*)", 
                          response.text, re.DOTALL)

        if match:
            summary = match.group(1).strip()
            main_entity = match.group(2).strip()
            web_search_required = match.group(3).strip()
            return {"email_summary": summary, "main_entity": main_entity, "web_search_required": web_search_required}
        else:
            return {"email_summary": response.text, "main_entity": response.text, "web_search_required": "NO"}

    def agent3(state: AgentState) -> AgentState:
        """Extract event details from the email."""
        print("Agent3: Extracting event details from the email...")
        custom_prompt = prompts["agent3"].format(user_input=state['user_input'])
        model = genai.GenerativeModel("gemma-3-4b-it")
        response = model.generate_content(custom_prompt)
        match = re.search(r"Event Title:\s*(.*?)\s*Event Date:\s*(.*?)\s*Event Time:\s*(.*?)\s*Event Location:\s*(.*?)\s*Event Online Link:\s*(.*)", 
                          response.text, re.DOTALL)
        if match:
            event_title = (match.group(1) or "").strip()
            event_date = (match.group(2) or "").strip()
            event_time = (match.group(3) or "").strip()
            event_location = (match.group(4) or "").strip()
            event_online_link = (match.group(5) or "").strip()
            return {
                "event_title": event_title,
                "event_date": event_date,
                "event_time": event_time,
                "event_location": event_location,
                "event_online_link": event_online_link
            }
        else:
            # If no match, return the original response
            return {
                "event_title": response.text,
                "event_date": response.text,
                "event_time": response.text,
                "event_location": response.text,
                "event_online_link": response.text
            }
    def agent4(state: AgentState) -> AgentState:
        """Replace all secrets and make a toolcall to find 
        more about the main entity."""
        restored_state = {}
        # Flatten all entity_map values into one replacement dict
        replacement_map = {}
        for category in secrets.values():
            replacement_map.update(category)

        for key, value in state.items():
            if isinstance(value, str):
                for placeholder, original in replacement_map.items():
                    value = value.replace(placeholder, original)
            restored_state[key] = value

        return restored_state


    def agent5(state: dict) -> dict:
        """Make a toolcall to TAVILY to find more about the main entity."""
        if state["web_search_required"] == "YES":
            tavily_client = TavilyClient()
            query = state["main_entity"]

            result = tavily_client.search(
                query=query,
                search_depth="advanced",  # or "basic"
                max_results=5,
                include_answer=True  # This gives a summarized answer
            )
            state["main_event_search"] = result.get("answer", "No summary found.")
            return state
        else:
            return state

    def agent6(state: AgentState) -> AgentState:
        """Clean the date and time formats."""
        custom_prompt = prompts["agent6"].format(event_title=state['event_title'],
                                                  event_date=state['event_date'],
                                                  event_time=state['event_time'])
        model = genai.GenerativeModel("gemma-3-4b-it")
        response = model.generate_content(custom_prompt)
        # Extract start and end date and time from the response
        match = re.search(r"Start Date and Time:\s*(.*?)\s*End Date and Time:\s*(.*)", 
                          response.text, re.DOTALL)
        if match:
            start_date_time = (match.group(1) or "").strip()
            end_date_time = (match.group(2) or "").strip()
            return {
                "start_date_time": start_date_time,
                "end_date_time": end_date_time
            }
        else:
            # If no match, return the original response
            return {
                "start_date_time": response.text,
                "end_date_time": response.text
            }

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # ---- Build the LangGraph ----
    builder = StateGraph(AgentState)
    builder.add_node("Agent1", agent1)
    builder.add_node("Router", router_node)
    builder.add_node("Agent2", agent2)
    builder.add_node("Agent3", agent3)
    builder.add_node("Agent4", agent4)
    builder.add_node("Agent5", agent5)
    builder.add_node("Agent6", agent6)

    # builder.add_node("Join", join_state)

    builder.add_edge("Agent1", "Router")
    builder.add_conditional_edges(
        source="Router",
        path=lambda state: state["next_node"],  # Use the "next" key returned above
        path_map={
            "run_agent2": "Agent2",
            "run_agent3": "Agent3",
            "end_flow": END
        }
    )
    builder.add_edge("Agent2", "Agent4")
    builder.add_edge("Agent3", "Agent4")
    builder.add_edge("Agent4", "Agent5")  
    builder.add_edge("Agent5", "Agent6")  
    builder.add_edge("Agent6", END) 

    builder.set_entry_point("Agent1")

    graph = builder.compile()

    subject = new_mail.subject
    date = new_mail.date
    body = new_mail.body
    user_message = f"Email Subject: {subject}\n\nEmail Date: {date}\n\nEmail Body: {body}"
    state = {
        "user_input": user_message,
        "email_reception_date": date,
        "important_mail": "",
        "web_search_required": "NO",
        "email_summary": "",
        "main_entity": "",
        "main_event_search": "",
        "event_title": "",
        "event_date": "",
        "event_time": "",
        "event_location": "",
        "event_online_link": "",
        "start_date_time": "",
        "end_date_time": ""
    }
    final_state = graph.invoke(state)
    print("\nGemini Agent:", final_state["email_summary"])

    return final_state

# ---- Run it ----
if __name__ == "__main__":
    event = call_agents("Sample email content to extract events from.")
