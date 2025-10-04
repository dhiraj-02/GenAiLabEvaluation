
def get_verilog_prompt_json(question: str, answer_scheme: str, student_answer: str, compilation_and_execution_output: str, modules: dict, total_marks: float) -> dict:
    """
    Returns a dict in the format:
    {
        "system": "<system message>",
        "content": "<content message>"
    }
    using modules from main
    """

    # Construct JSON keys with marks for the system message
    module_keys = ",\n  ".join([
        f'"{name} ({marks}m)": {{"marks": <float>, "feedback": "<short>"}}'
        for name, marks in modules.items()
    ])

    system_message = f"""You are an expert at evaluating Verilog. You will be given a Verilog programming question, an answer scheme, and a student answer. You must assign marks according to the answer scheme. STRICTLY follow this output format:

    {{
    {module_keys},
    "total ({total_marks}m)": <int>
    }}

    Notes:
    - Always include all module keys above, even if the student has not implemented them (then give marks=0 with feedback "Not implemented").
    - "marks" must be an float only 0.5 no other fraction is allowed.
    - "feedback" must be a single short and to the point phrase (<= 5 words), if correct then give "".
    - Do NOT add extra fields, text, or explanation outside JSON."""

    content_message = f"""question:
{question}

answer scheme:
{answer_scheme}

student answer:
{student_answer}

{compilation_and_execution_output}

Only return what is asked in the system prompt."""

    return {
        "system": system_message,
        "content": content_message
    }
