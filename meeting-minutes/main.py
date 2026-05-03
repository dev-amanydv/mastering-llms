from transformers import AutoModelForCausalLM
from transformers import TextStreamer
from transformers import AutoTokenizer
from safetensors import torch
from transformers import BitsAndBytesConfig
from networkx import display
import os
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import pipeline
import torch
from IPython.display import Markdown, display, update_display

load_dotenv()

LLAMA = "meta-llama/Llama-3.2-3B-Instruct"

hf_token = os.getenv('HF_TOKEN')
print(f"HF_TOKEN: {hf_token}")

login(hf_token, add_to_git_credential=True)

audio_file = open('denver_extract.mp3', 'rb')

pipe = pipeline(task="automatic-speech-recognition", model="openai/whisper-medium", device='cuda', dtype=torch.float16, return_timestamps=True)

result = pipe(audio_file)
print(f"result: {result}")
transcription=result["text"]

open_source_transcription=transcription
display(Markdown(open_source_transcription))

system_message = """
You produce minutes of meetings from transcripts, with summary, key discussion points,
takeaways and action items with owners, in markdown format without code blocks.
"""

user_prompt=f"""
Below is an extract transcript of a Denver council meeting.
Please write minutes in markdown without code blocks, including:
- a summary with attendees, location and date
- discussion points
- takeaways
- action items with owners

Transcription:
{transcription}
"""

messages = [{
    "role": "system", "content": system_message
}, {
    "role": "user", "content": user_prompt
}]

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)

tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.add_eos_token
inputs = tokenizer.apply_chat_template(messages, return_tensors='pt').to('cuda')
streamer = TextStreamer(tokenizer)
model = AutoModelForCausalLM.from_pretrained(LLAMA, device_map="auto", quantization_config=quant_config)
outputs = model.generate(inputs, max_new_tokens=2000, streamer=streamer)

response = tokenizer.decode(outputs[0])

display(Markdown(response))


