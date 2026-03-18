import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from litellm import completion

load_dotenv(override=True);

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
grok_api_key = os.getenv('GROK_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

openai = OpenAI()

anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
deepseek_url = "https://api.deepseek.com"
groq_url = "https://api.groq.com/openai/v1"
grok_url = "https://api.x.ai/v1"
openrouter_url = "https://openrouter.ai/api/v1"
ollama_url = "http://localhost:11434/v1"

anthropic = OpenAI(api_key=anthropic_api_key, base_url=anthropic_url)
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)
deepseek = OpenAI(api_key=deepseek_api_key, base_url=deepseek_url)
groq = OpenAI(api_key=groq_api_key, base_url=groq_url)
grok = OpenAI(api_key=grok_api_key, base_url=grok_url)
openrouter = OpenAI(base_url=openrouter_url, api_key=openrouter_api_key)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)

os.environ["OPENROUTER_API_KEY"] = "openrouter_api_key"

with open(mode="r", file="hamlet.txt") as file:
    hamlet_text = file.read()

loc = hamlet_text.find("Speak, man")
print(hamlet_text[loc:loc+100])

question=[{
    "role": "user", "content": "In Hamlet, when Laertes asks 'Where is my father?' what is the reply?"
}]

# response = completion(model="ollama/qwen2.5-coder:7b", messages=question, api_base="http://localhost:11434")
# print(response.choices[0].message.content)


# Keep the prompt exactly same as much as you can to enable the prompt caching implicitly
question[0]["content"]= question[0]["content"] + "\n\n For context, here is the entire text of Hamlet:\n\n"+hamlet_text

response = completion(model="ollama/qwen2.5-coder:7b", messages=question, api_base="http://localhost:11434")

print(response.choices[0].message.content)
print(f"Input tokensxx: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
# Local models don't support caching, fronteir models like claude, gemini and gpt supports.
# print(f"Cached tokens: {response.usage.prompt_tokens_details.cached_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")


def main():
    return 1

if __name__ == "__main__":
    main()
