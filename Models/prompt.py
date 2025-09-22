from columns_config import MODULES, TOTAL_MARKS

# Construct JSON keys with marks for the system message
module_keys = ",\n  ".join([
    f'"{name} ({marks}m)": {{"marks": <int>, "feedback": "<short>"}}'
    for name, marks in MODULES.items()
])

system_message = f"""You are an expert at evaluating Verilog. You will be given a Verilog programming question, an answer scheme, and a student answer. You must assign marks according to the answer scheme. STRICTLY follow this output format:

{{
  {module_keys},
  "total ({TOTAL_MARKS}m)": <int>
}}

Notes:
- Always include all module keys above, even if the student has not implemented them (then give marks=0 with feedback "Not implemented").
- "marks" must be an integer (partial marks allowed).
- "feedback" must be a single short phrase (< 12 words).
- Do NOT add extra fields, text, or explanation outside JSON."""

def get_verilog_prompt_json(question: str, answer_scheme: str, student_answer: str) -> dict:
    """
    Returns a dict in the format:
    {
        "system": "<system message>",
        "content": "<content message>"
    }
    using MODULES from columns_config.py
    """

    content_message = f"""question:
{question}

answer scheme:
{answer_scheme}

student answer:
{student_answer}

Only return what is asked in the system prompt."""

    return {
        "system": system_message,
        "content": content_message
    }
