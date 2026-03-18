from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env", override=True)
print("Key loaded:", os.getenv("OPENROUTER_API_KEY")[:100])

qwen=OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
nemotron=OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
# We're using open-source models which are free to use
qwen_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

nemotron_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

qwen_messages=["Hi there"]
nemotron_messages=["Hi"]

def call_qwen():
    messages=[{"role": "system", "content": qwen_system}]
    for q_message, n_message in zip(qwen_messages, nemotron_messages):
        messages.append({"role": "assistant", "content": q_message})
        messages.append({"role": "user", "content": n_message})
    response=qwen.chat.completions.create(model="qwen2.5-coder:7b", messages=messages)
    return response.choices[0].message.content

def call_nemotron():
    messages=[{"role": "system", "content": nemotron_system}]
    for q_message, n_message in zip(qwen_messages, nemotron_messages):
        messages.append({ "role": "assistant", "content": n_message})
        messages.append({ "role": "user", "content": q_message})
    response=nemotron.chat.completions.create(model="nvidia/nemotron-3-super-120b-a12b:free", messages=messages)
    return response.choices[0].message.content

def main():
    for i in range(2):
        qwen_response = call_qwen()
        qwen_messages.append(qwen_response)
        nemotron_response = call_nemotron()
        nemotron_messages.append(nemotron_response)

        print(f"Qwen response: {qwen_response}")
        print(f"Nemotron response: {nemotron_response}")


if __name__ == "__main__":
    main()
    call_nemotron