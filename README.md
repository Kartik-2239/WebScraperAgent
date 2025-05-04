#Web Scraping Agent
A powerful web scraping tool built with Google's ADK (Agent Development Kit) that enables intelligent extraction of data from websites.

# Features
Intelligent HTML Content Analysis: Dynamically analyzes webpage structure to determine optimal extraction strategies
Targeted Data Extraction: Extract specific elements like links, text, images, and more
Data Persistence: Save extracted images and text to local storage
AI-Powered Decision Making: Leverages Gemini models to intelligently process web content

# Requirements
Python 3.7+
Google ADK
BeautifulSoup4
Requests

# Installation

# Clone the repository
```
git clone https://github.com/Kartik-2239/WebScraperAgent.git
cd WebScraperAgent

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install google-adk bs4 requests
```

# Usage
1.) You can use the terminal
```
cd WebScraperAgent
adk run scrapingAgent
```
then you can give it a link and the query

2.) You can define an agent calling function (it is an google adk thing)
```
APP_NAME = "scrapingAgent"
USER_ID = "user_1"
SESSION_ID = "session_001" 

session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
runner = Runner(
    agent=weather_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)

from google.genai import types 
async def call_agent_async(query: str, runner, user_id, session_id):
  print(f"\n>>> User Query: {query}")
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

      if event.is_final_response():
          if event.content and event.content.parts:
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          break 

  print(f"<<< Agent Response: {final_response_text}")

call_agent_async(query, user_id, session_id):
```

# Available Tools
The agent provides several tools:

1.) get_content_for_prediction: Fetches a sample of HTML to analyze page structure
    pythonhtml_sample = get_content_for_prediction("https://example.com", 0, 1000)

2.) get_data: Extracts specific elements from a webpage
    Get all links
    links = get_data("https://example.com", "a", "href")
    Get all headings
    headings = get_data("https://example.com", "h1", None)

3.) save_img: Downloads and saves images
    pythonsave_img("https://example.com/image.jpg", "example_image", "images")

4.) save_text: Saves extracted text to file  
    pythonsave_text("example_text", "texts", "This is the extracted content")

You have to enable the last two by uncomenting the tools in agents.py



# Example Tasks

Extract all links from a webpage
Download all images from a webpage
Extract and save all headings
Analyze webpage structure to determine optimal extraction strategy

# Notes

The agent uses a realistic user agent to avoid being blocked by websites
Directory creation is handled automatically when saving files
The agent intelligently searches for high-resolution images when requested

# Disclaimer
This tool is for educational purposes only. Always respect website terms of service, robots.txt files, and rate limits when scraping. Ensure you have permission to scrape content from websites.





