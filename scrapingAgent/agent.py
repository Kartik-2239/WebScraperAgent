import requests
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import Agent
import logging
import os
from bs4 import BeautifulSoup


def get_content_for_prediction(url:str, start: int, end: int) -> str:
    """
    start is starting index and end is ending index of the html content to be fetched.
    Fetches the HTML content from the given URL and returns the first 1000 characters as a string.
    This helps the AI analyze the structure of the web page and identify which HTML tags are present,
    so it can decide which tags to use for extracting specific types of data (like links, headings, etc.).
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text[start:end]
        return html_content
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return e
get_content_for_prediction_tool = FunctionTool(get_content_for_prediction)

from typing import Optional
def get_data(url: str, tag: str, attribute: Optional[str]= None) -> str:
    """
    Fetches the HTML content from the given URL and extracts all elements matching the specified HTML tag.
    For example, if the tag is 'a', it will return all the links on the webpage as a list of strings.
    This helps the AI retrieve specific types of data (like links, headings, images, etc.) from the page.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        data_full = soup.find_all(tag)
        if attribute is not None:
            data_full = [str(data.get(attribute)) for data in data_full]
        else:
            data_full = [str(data.text) for data in data_full]
        return "\n".join(data_full)
    except requests.exceptions.RequestException as e:
        return f"Error fetching data from {url}: {e}"
get_data_tool = FunctionTool(get_data)


def save_img(link_of_img:str, name_of_img:str, name_of_file:str) -> str:
    requests.get(link_of_img)
    try:
        os.mkdir(name_of_file)
    except:
        pass
    with open(f'{name_of_file}/{name_of_img}.jpg', 'wb') as f:
        f.write(requests.get(link_of_img).content)
    return f"Image saved as {name_of_img}"
save_img_tool = FunctionTool(save_img)

def save_text(name_of_img:str, name_of_file:str, text:str) -> str:
    try:
        os.mkdir(name_of_file)
    except:
        pass
    with open(f'{name_of_file}/{name_of_img}.txt', 'w') as f:
        f.write(text)
    return f"Text saved as {name_of_img}"



save_text_tool = FunctionTool(save_text)

model = 'gemini-2.5-flash-preview-04-17'

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="This agent is used to get the data from the given URL and tag. The data is returned as a list of strings.",
    instruction="""
    -Get the data from the given URL and figure out the tag names and attribute for links, be it link or text, from the data html content from using the tool `get_content_for_prediction_tool`(put start = 0 and end = 1000 and then change it if necessary) and pass that tag and attribute with the url in `get_data_tool` and process the data by removing useless things and adds." \
    -If the data according to the tag and attribute is not found change the start and finish variables in `get_content_for_prediction_tool`  to search the html content which has not been searched yet.
    -If user is asking for text data then set attribute as `None`.
    -If the user asks for images then by default search the block for the image with the best, original, or high resolution by removing thumb or any other limiters on the resolution.
    -Save the image one by one in the images folder, pass the link of the image and name of the image to `save_img_tool` and save it in the images folder.
    -save text by converting whatever the user is asking into str and save it in the text file and save it in the text folder, pass the content in text in `save_text_tool`.
    -DO NOT SAVE THE IMAGE IF NOT ASKED BY THE USER.
    -DO NOT SAVE THE TEXT IF NOT ASKED BY THE USER.
    """,
    tools=[get_content_for_prediction_tool, get_data_tool, save_img_tool, save_text_tool],
)

