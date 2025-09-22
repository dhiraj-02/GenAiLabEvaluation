import os
from google import genai
from google.genai import types
import utils as utils
from Models.prompt import get_verilog_prompt_json

GEMINI_API_KEY = os.getenv("gemini_api_key")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_verilog(question, answer_scheme, student_answer):
    prompts = get_verilog_prompt_json(question, answer_scheme, student_answer)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompts["system"],
            temperature=0.0   # deterministic output
        ),
        contents=prompts["content"]
    )
    
    return response.text


