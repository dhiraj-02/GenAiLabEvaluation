# Define modules and their max marks
MODULES = {
    "REG_8BIT": 3,
    "EXPANSION_BOX": 3,
    "XOR_8BIT": 1,
    "XOR_4BIT": 1,
    "CSA_4BIT": 6,
    "CONCAT": 1,
    "ENCRYPT": 4,
    "TESTBENCH": 3,
    "Final O/P": 6
}

TOTAL_MARKS = sum(MODULES.values())

# Generate Excel columns: marks and feedback side by side
COLUMNS = ["student_id"]
for module, marks in MODULES.items():
    COLUMNS.append(f"{module} ({marks}m) marks")
    COLUMNS.append(f"{module} ({marks}m) feedback")
COLUMNS.append(f"total ({TOTAL_MARKS}m)")

