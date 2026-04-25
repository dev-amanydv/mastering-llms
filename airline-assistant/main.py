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
You are a helpful airline assistant.

Rules:
1. If the query is about flights → use available flight tools.
2. If the query is NOT about flights → DO NOT call flight tools.
3. If the query requires real-world or general knowledge → you MUST use the web_search tool.
4. Never guess unknown information.
5. If no tool applies, answer normally.

Give short, courteous answers (max 1 sentence).
"""

messages = [
    {
        "role": "system",
        "content": system_message
    },
    {
        "role": "assistant",
        "content": "Hey, how can I help you regarding airlines today??"
    }
]

ticket_prices = { "mumbai": "6899", "delhi": "3499", 'himachal': "5999", "rajasthan": "2999"}
expected_duration = { "mumbai": "6 hours 30 minutes", "delhi": "4 hours 40 minutes", "himachal": "4 hours 10 minutes", "rajasthan": "3 hours 20 minutes"}

def get_ticket_price(destination_city):
    print(f"--------Tool (get_ticket_price) called for city {destination_city}-------")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return price

def get_travel_duration(destination_city):
    print(f"--------Tool (caluclate_time) called for city {destination_city}-------")
    time = expected_duration.get(destination_city.lower(), "Unknown time")
    return time
    

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
    },
    {
        "type": "function",
        "name": "get_travel_duration",
        "description": "Get the travel duration to reach destination city",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The city customer wants to go"
                }
            },
            "required": ["destination_city"]
        }
    },
    {
        "type": "web_search"
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
        tools=tools,
        tool_choice="auto"
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
            if item.name == "get_travel_duration":
                destination_city = json.loads(item.arguments)["destination_city"]
                time = get_travel_duration(destination_city)
                messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": time
                })

    response = openai.responses.create(
        model=model,
        tools=tools,
        input=messages,
        tool_choice='auto'
    )

    print(f"\nAssistant: {response.output_text}\n")
    print(f"\n\n\n*************************\n{response.model_dump_json(indent=2)}\n")


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