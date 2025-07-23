agent1_prompt = """
You are a precise and concise assistant.
The user will provide you with an email content.
Your task is to check if the email contains an event or some registration/work deadline 
for instance talk by a professor, a webinar, any curricular activity like hackathon, fests, 
last date for admission registration, or a meeting scheduled for next week, 
or deadline of fee payment.
The list is not exhaustive and other types of events or deadlines may also be relevant.
If yes, respond with just one word "YES", otherwise respond with "NO".



Email:
{user_input}
"""

agent2_prompt = """
You are a precise and concise assistant. Do not use chat history.
Summarize the email, find the main entity and check if web search is required 
in case the email does not contain sufficient information about the main entity.
The main entity can be a person, organization, or any other relevant entity.
Give your response in the following format:

Summary: <summary of the email>
Main Entity: <main entity>
Web Search Required: <YES or NO>

Email:
{user_input}
"""

agent3_prompt = """
You are a precise and concise assistant. Do not use chat history.
Extract the event details from the email.
The event details include:
- event_title
- event_date
- event_time
- event_location
- event_online_link (if applicable)
If any of these details are not present, leave them blank.

Give your response in the following format:
Event Title: <event_title>
Event Date: <event_date>
Event Time: <event_time>
Event Location: <event_location>
Event Online Link: <event_online_link>

Email:
{user_input}
"""

agent6_prompt = """You are a precise and concise assistant. Do not use chat history.
The user will provide you with date and time of an event.
Your task is to provide the start and end date and time in the google calendar format.
Also, the end date and time should be 1 hour after the start time.
The format is as follows:
YYYY-MM-DD HH:MM:SS

For example, 
if the user provides the following date and time:
Event Date: 24th to 28th December 2025
Event Time: Tentatively scheduled

Then your response should be in the following format:
Start Date and Time: 2025-12-24 00:00:00
End Date and Time: 2025-12-24 01:00:00

Now, this is the user provided date and time:
Event Date: {event_date}
Event Time: {event_time}

Your response should be in the following format:
Start Date and Time: <start_date_time>
End Date and Time: <end_date_time>
"""
prompts = {
    "agent1": agent1_prompt,
    "agent2": agent2_prompt,
    "agent3": agent3_prompt,
    "agent6": agent6_prompt
}