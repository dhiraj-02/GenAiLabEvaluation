import os
from dotenv import load_dotenv
load_dotenv()

import utils
import Models.gemini as gemini
import Models.openai as openai
import run_v
from Models.prompt import get_verilog_prompt_json



def main(question, solutions, progress_callback=None):

    # Paths
    question_path = f"QuestionBank/{question}/question.txt"
    answer_scheme_path = f"QuestionBank/{question}/answer_scheme.v"
    student_solutions_folder_path = f"SolutionBank/{solutions}"
    excel_path = f"Results/{question}-{solutions}.xlsx"

    os.makedirs("Results", exist_ok=True)  

    # Modules
    modules = utils.read_module_csv(f"QuestionBank/{question}/modules.csv")
    total_marks = sum(modules.values())

    # Generate Excel columns: marks and feedback side by side
    columns = ["student_id"]
    for module, marks in modules.items():
        columns.append(f"{module} ({marks}m) marks")
        columns.append(f"{module} ({marks}m) feedback")
    columns.append(f"total ({total_marks}m)")

    # Read question and answer scheme
    question_txt = utils.read_txt_file(question_path)
    answer_scheme = utils.read_txt_file(answer_scheme_path)

    student_files = [f for f in os.listdir(student_solutions_folder_path) 
                     if os.path.isfile(os.path.join(student_solutions_folder_path, f))]
    total_students = len(student_files)

    # Process each student solution
    for idx, filename in enumerate(student_files, start=1):
        # --- Call callback with current index and total ---
        if progress_callback:
            progress_callback(idx, total_students)

        filepath = os.path.join(student_solutions_folder_path, filename)
        student_id = filename.split("-")[0]

        student_solution = utils.read_txt_file(filepath)
        compilation_and_execution_output = run_v.compile_and_run(filepath)
        prompts = get_verilog_prompt_json(question_txt, answer_scheme, student_solution, compilation_and_execution_output, modules, total_marks)

        # Evaluate with LLM
        response = openai.evaluate_verilog(prompts)

        utils.append_to_file("op.txt", f"Student ID: {student_id}\n Prompt: {prompts}\n Response: {response}\n\n")

        # Clean JSON and convert to row
        json_data = utils.clean_json_output(response)
        row = utils.json_to_row(json_data, student_id, modules, total_marks)

        # Append row to Excel safely
        utils.append_row_to_excel(excel_path, row, columns)
