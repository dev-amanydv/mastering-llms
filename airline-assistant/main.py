import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)

openai_endpoint=os.getenv('OPENAI_ENDPOINT')
azure_api_key=os.getenv('AZURE_API_KEY')

if openai_endpoint:
    print(f"OpenAI endpoint exist & starts with {openai_endpoint[:5]}")
else:
    print("OpenAI Endpoint not set")
if azure_api_key:
    print(f"Azure api key exist & starts with {azure_api_key[:5]}\n\n")
else:
    print("Azure api key not set\n\n\n")

model="gpt-5-mini"

openai = OpenAI(base_url=f"{openai_endpoint}", api_key=azure_api_key)

system_message="""
You are a helpful assistant for an Airlines called FlightAI.
Give short, courteous answers, not more than 1 sentence.
Always be accurate. If you don't know the answer just say not available.
"""

messages = [
    {
        "role": "system",
        "content": system_message
    },
    {
        "role": "assistant",
        "content": "Hey, how can I help you today??"
    }
]

ticket_prices = { "mumbai": "6899", "delhi": "3499", 'himachal': "5999", "rajasthan": "2999"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return price

tools = [
    {
        "type": "function",
        "name": "get_ticket_price",
        "description": "Get the ticket prices for the flights",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The city that customer wants to go"
                }
            },
            "required": ["destination_city"]
        }
    }
]

def sendPrompt(messages, input):
    messages += [{
        "role": "user",
        "content": input
    }]

    response = openai.responses.create(
        model=f"{model}",
        input=messages,
        tools=tools
    )

    messages += response.output

    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_ticket_price":
                destination_city = json.loads(item.arguments)["destination_city"]
                price = get_ticket_price(destination_city)
                messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": price
                })

    response = openai.responses.create(
        model=model,
        tools=tools,
        input=messages
    )

    print(f"\nAssistant: {response.output_text}\n")
    return

def main():
    for m in messages:
        if m['role'] == "assistant":
            print(f"Assistant: {m['content']}\n")
        if m['role'] == "user":
            print(f"User: {m['content']}\n")

    while True:
        query = input("User: ")
        if query == '/exit':
            break
        sendPrompt(messages, query)
main()