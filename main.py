import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import utils
import Models.gemini as gemini
from columns_config import COLUMNS

# Paths
question_path = "Data/question.txt"
answer_scheme_path = "Data/answer_scheme.v"
student_solutions_folder_path = "Data/StudentSolutions"
excel_path = "Results/evaluation_results.xlsx"

# Read question and answer scheme
question = utils.read_txt_file(question_path)
answer_scheme = utils.read_txt_file(answer_scheme_path)

# Process each student solution
for filename in os.listdir(student_solutions_folder_path):
    filepath = os.path.join(student_solutions_folder_path, filename)
    if os.path.isfile(filepath):
        student_id = filename.split("-")[0]
        student_solution = utils.read_txt_file(filepath)

        # Evaluate with LLM
        response = gemini.evaluate_verilog(question, answer_scheme, student_solution)
        print(f"Response for {filename}:\n{response}\n")

        # Clean JSON and convert to row
        json_data = utils.clean_json_output(response)
        row = utils.json_to_row(json_data, student_id)

        # Append row to Excel safely
        utils.append_row_to_excel(excel_path, row, COLUMNS)

print(f"Evaluation complete. Results saved to {excel_path}")
