from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient()

def tavily_summary_agent(query) -> str:

    result = client.search(
        query=query,
        search_depth="advanced",  # or "basic"
        max_results=20,
        include_answer=True  # This gives a summarized answer
    )
    
    result = result.get("answer", "No summary found.")
    return result

print(tavily_summary_agent("Inter-IIT Cultural Meet 2025"))