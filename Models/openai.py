import os
from openai import OpenAI

# Load OpenAI API key
openai_api_key = os.getenv("openai_api_key")
if openai_api_key is None:
    raise ValueError("openap_api_key environment variable not set.")

# Initialize client
client = OpenAI(api_key=openai_api_key)

def evaluate_verilog(prompts):
    response = client.chat.completions.create(
        model="gpt-4.1",  # or gpt-4o / gpt-4.1 depending on your needs
        messages=[
            {"role": "system", "content": prompts["system"]},
            {"role": "user", "content": prompts["content"]}
        ],
        temperature=0.0  # deterministic output
    )
    
    return response.choices[0].message.content
