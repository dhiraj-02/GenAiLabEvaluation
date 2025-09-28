import json
import os
import pandas as pd
import csv

def read_json(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
    
def read_txt_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()
    

def append_to_file(filepath: str, text: str):
    with open(filepath, "a") as f:
        f.write(text + "\n")


def clean_json_output(raw_output: str) -> dict:
    """Remove ```json ... ``` wrappers and parse into Python dict."""
    clean = raw_output.strip()
    if clean.startswith("```json"):
        clean = clean.removeprefix("```json").removesuffix("```").strip()
    return json.loads(clean)


def json_to_row(json_data, student_id, modules, total_marks):
    """
    Converts LLM JSON evaluation output into a row dict suitable for Excel.
    Marks and feedback are placed side by side for each module.
    """
    row = {"student_id": student_id}
    
    for module, max_marks in modules.items():
        key = f"{module} ({max_marks}m)"
        row[f"{key} marks"] = json_data.get(key, {}).get("marks", 0)
        row[f"{key} feedback"] = json_data.get(key, {}).get("feedback", "Not implemented.")
    
    # Add total
    row[f"total ({total_marks}m)"] = json_data.get(f"total ({total_marks}m)", 0)
    
    return row



def append_row_to_excel(excel_path, row, columns):
    """
    Append a row to an Excel file.
    If the file doesn't exist, create it with headers.
    """
    # Convert row to DataFrame
    df_row = pd.DataFrame([row], columns=columns)

    if not os.path.exists(excel_path):
        # File doesn't exist → create with headers
        df_row.to_excel(excel_path, index=False)
    else:
        # File exists → append
        try:
            existing_df = pd.read_excel(excel_path)
        except Exception:
            existing_df = pd.DataFrame(columns=columns)

        # Append new row
        updated_df = pd.concat([existing_df, df_row], ignore_index=True)

        # Save back to Excel
        updated_df.to_excel(excel_path, index=False)


def read_module_csv(file_path):
    module_dict = {}
    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 2:
                continue  # skip malformed rows
            module, marks = row[0].strip(), row[1].strip()
            try:
                module_dict[module] = float(marks)
            except ValueError:
                # if not an integer, skip or store as-is
                continue
    return module_dict