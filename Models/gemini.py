import os
from google import genai
from google.genai import types
import utils as utils

gemini_api_key = os.getenv("gemini_api_key")
if gemini_api_key is None:
    raise ValueError("gemini_api_key environment variable not set.")


client = genai.Client(api_key=gemini_api_key)


def evaluate_verilog(prompts):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompts["system"],
            temperature=0.0   # deterministic output
        ),
        contents=prompts["content"]
    )
    
    return response.text


