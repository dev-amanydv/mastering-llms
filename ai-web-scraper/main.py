from scraper import fetch_website_content, fetch_website_links
from openai import OpenAI
import itertools
import threading
import time
import sys

OLLAMA_MODEL = "qwen2.5-coder:3b"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key=API_KEY)

system_prompt = """You are a professional content summarizer. Your task is to analyze website content and create clear, accurate, and concise summaries.

Guidelines:
- Extract the main topic and key points from the content
- Ignore navigation menus, advertisements, footers, and boilerplate text
- Focus only on the core informational content
- Write in clear, professional language
- Organize information logically with proper structure
- Preserve important facts, statistics, and quotes accurately
- Keep the summary between 150-300 words unless the content is very brief
- Use bullet points for lists when appropriate
- Do not add information that isn't in the source content
- Do not include your own opinions or interpretations

Output format:
1. Title/Main Topic (one line)
2. Brief Overview (2-3 sentences)
3. Key Points (bullet points if multiple topics)
4. Conclusion/Takeaway (1-2 sentences if applicable)"""

user_prompt_prefix = """Please read and summarize the following website content. Focus on extracting the main message and key information while filtering out irrelevant elements like navigation, ads, or boilerplate text.

Website content:
---
"""

class LoadingSpinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.done = False
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        
    def spin(self):
        while not self.done:
            sys.stdout.write(f'\r{self.message} {next(self.spinner)} ')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def __enter__(self):
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done = True
        self.thread.join()

def messages_content(website_data):
    return [
        {
            "role": "system", "content": system_prompt
        }, {
            "role": "user", "content": user_prompt_prefix + website_data + "\n---\n\nProvide a clear and structured summary:"
        }
    ]

def summarise(url):
    with LoadingSpinner(" Fetching website content"):
        website_data = fetch_website_content(url)
    print(" Website content fetched successfully\n")
    
    with LoadingSpinner(" AI is analyzing and summarizing"):
        messages = messages_content(website_data)
        response = ollama.chat.completions.create(
            model=OLLAMA_MODEL, 
            messages=messages, 
            temperature=0.3, 
            max_tokens=3000
        )
    print(" Summary generated successfully\n")
    
    return response.choices[0].message.content

def main():
    print("=" * 60)
    print("         WEBSITE CONTENT SUMMARIZER")
    print("=" * 60)
    print()
    
    url = input(" Enter the URL to summarise: ")
    print()
    
    try:
        summary = summarise(url)
        
        print('=' * 60)
        print('                    SUMMARY')
        print('=' * 60)
        print()
        print(summary)
        print()
        print('=' * 60)
        
    except Exception as e:
        print(f"\n Error: {str(e)}")
        print("Please check the URL and try again.")

if __name__ == "__main__":
    main()