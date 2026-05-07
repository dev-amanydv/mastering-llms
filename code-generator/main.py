from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

openai_baseurl = os.getenv('OPENAI_ENDPOINT')
api_key=os.getenv('AZURE_API_KEY')

if openai_baseurl:
    print(f"Open AI base url exists and starts with {openai_baseurl[:15]}")
else:
    print('Open AI base url not set')
if api_key:
    print(f"API Key exists and start's with {api_key[:7]}")


openai = OpenAI(base_url=openai_baseurl, api_key=api_key)


# response = openai.responses.create(
#     model='gpt-5-mini',
#     input="What does OpenAI agents sdk helps in?"
# )
