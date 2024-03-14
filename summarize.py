import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "openai key"

client = OpenAI()

def get_page_contents(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.get_text()
        return contents
    else:
        return None

def summarize(url):
    contents = get_page_contents(url)
    if contents:
        messages = [{"role": "system", "content":  
                    "You are an intelligent assistant."}]
        message = f"Summarize this page: {contents}"
        if message: 
            messages.append({"role": "user", "content": message}) 
            chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat.choices[0].message.content 
            print(f"ChatGPT: {reply}") 
            messages.append({"role": "assistant", "content": reply})
            return {reply: url}
    else:
        return {"Error": "Failed to fetch page contents."}