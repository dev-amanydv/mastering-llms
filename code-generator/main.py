import subprocess
from IPython.core.display import __builtins__
from IPython.display import Markdown
from IPython.core.display_functions import display
from openai import OpenAI
import os
from dotenv import load_dotenv
from system_info import retrieve_system_info

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

#You can use any of the models for this
anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
grok_url = "https://api.x.ai/v1"

anthropic = OpenAI(api_key="", base_url=anthropic_url)
gemini = OpenAI(api_key="", base_url=gemini_url)
grok = OpenAI(api_key="", base_url=grok_url)

OPENAI_MODEL = "gpt-5-mini"
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
GROK_MODEL = "grok-4"
GEMINI_MODEL = "gemini-2.5-pro"

system_info = retrieve_system_info()

message = f"""
Here is a report of the system information for my computer.
I want to run a C++ compiler to compile a single c++ file called main.cpp and then execute it in the simplest way possible.
Please reply with whether I need to install any c++ compiler to do this. If so, please provide the simplest step by step instructions to do so.

If I'm already set up to compile c++ code, then I'd like to run something like this in Python to compile and execute the code:
```python
compile_command = # something here - to achieve the fastest possible runtime performance
compile_result = subprocess.run(compile_command, check=True, text=True, capture_output=True)
run_command = # something here
run_result = subprocess.run(run_command, check=True, text=True, capture_output=True)
return run_result.stdout
```

Please tell me exactly what I should use for the compile_command and run_command.

System information:
{system_info}
"""

# response = openai.responses.create(
#     model=OPENAI_MODEL,
#     input=[{"role": "user", "content": message}],
#     stream=True
# )

compile_command = ["clang++", "-std=c++20", "-O3", "-flto", "-DNDEBUG", "-o", "main", "main.cpp"]
run_command = ["./main"]

system_prompt = """
Your task is to convert Python code into high performance C++ code/
Respond only with C++ code. Do not provide any explanationother than occasional comments.
The C++ response needs to produce an identical output in the fastest possible time.
"""

def user_prompt_for(python):
    return f"""
    Port this python code to C++ with the fastest possible implementationthat produces identical output in the least time.
    The system information is:
    {system_info}
    Your response will be written to a file called main.cpp and then compiled and executed; You have to be very accurate while writing C++ code, it should not give error while compiling. the compilation command is:
    {compile_command}
    Respond only with the C++ code.
    Python code to port:

    ```python
    {python}
    ```
    """

def messages_for(python):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(python)}
    ]

def write_ouput(cpp):
    with open('main.cpp', 'w', encoding="utf-8") as f:
        f.write(cpp)

def port(client, model, python):
    reasoning_effort = "high" if "gpt" in model else None
    stream = client.responses.create(model=model, input=messages_for(python), reasoning={"effort": reasoning_effort}, stream=True)
    DIM = "\033[2m"
    GRAY = "\033[90m"
    ITALIC = "\033[3m"
    RESET = "\033[0m"
    print(f"{DIM}{ITALIC}Thinking...{GRAY}", end="")
    for event in stream:
        if event.type == 'response.output_text.delta':
            print(event.delta, end="", flush=True)
        if event.type == 'response.completed':
            print(RESET)
            reply = event.response.output_text
            reply = reply.replace('```cpp', '').replace('```', '')
            write_ouput(reply)

pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations + 1):
        j = i * param1 - param2
        result = result - (1/j)
        j = i * param1 + param2
        result = result + (1/j)
    return result

start_time = time.time()
result = calculate(200_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time(Python): {(end_time - start_time):.6f} seconds") 
"""

def run_python(code):
    globals = {"__builtins__": __builtins__}
    exec(code, globals)

print("\n-------PYTHON-----------------\n")
run_python(pi)
print("\n")
port(openai, OPENAI_MODEL, pi)

def compile_and_run():
    subprocess.run(compile_command, check=True, text=True, capture_output=True)
    print(subprocess.run(run_command, check=True, text=True, capture_output=True).stdout)
    print(subprocess.run(run_command, check=True, text=True, capture_output=True).stdout)
    print(subprocess.run(run_command, check=True, text=True, capture_output=True).stdout)

print("------- Optimized C++ ----------\n\n")

compile_and_run()
