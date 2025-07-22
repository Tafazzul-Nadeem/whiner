agent1_prompt = """
You are a precise and concise assistant.
The user will provide you with an email content.
Your task is to check if the email contains an event or some registration/work deadline 
for instance talk by a professor, a webinar, any curricular activity like hackathon, fests, 
last date for admission registration, or a meeting scheduled for next week, 
or deadline of fee payment.
The list is not exhaustive and other types of events or deadlines may also be relevant.
If yes, respond with json in the following format:
{{
    "important_mail": "YES"
}}
If not, respond with:
{{
    "important_mail": "NO"
}}

{user_input}
"""

agent2_prompt = """
You are a precise and concise assistant. Do not use chat history.
Summarize the email and find the main entity:
{user_input}
"""

prompts = {
    "agent1": agent1_prompt,
    "agent2": agent2_prompt,
}