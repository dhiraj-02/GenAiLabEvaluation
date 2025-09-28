import streamlit as st
import os
import zipfile
import shutil
import uuid
import main
import pandas as pd

# --- App Config ---
st.set_page_config(page_title="QnA App", layout="wide")

# --- Initialize session state ---
if "task_submitted" not in st.session_state:
    st.session_state.task_submitted = False
if "task_processed" not in st.session_state:
    st.session_state.task_processed = False
if "task_form_uuid" not in st.session_state:
    st.session_state.task_form_uuid = str(uuid.uuid4())
if "form_id" not in st.session_state:
    st.session_state.form_id = str(uuid.uuid4())
if "question_created" not in st.session_state:
    st.session_state.question_created = False


# --- Sidebar navigation ---
st.sidebar.markdown("## Navigation")

if "menu" not in st.session_state:
    st.session_state.menu = "📤 Submit Task"  # default

menu = st.sidebar.radio(
    "Go to:",
    ["📤 Submit Task", "➕ Create Question", "🔍 View Results"],
    index=0,
    key="sidebar_menu",
    disabled=st.session_state.task_submitted and not st.session_state.task_processed
)

st.session_state.menu = menu



# ------------------ CREATE QUESTION ------------------
def create_question_ui():
    st.title("📝 Create Question")

    prefix = st.session_state.form_id
    disabled = st.session_state.question_created  # disable after creation

    # --- Inputs ---
    question_name = st.text_input("Question Name", key=f"{prefix}_question_name", disabled=disabled, width=300)

    col1, col2 = st.columns(2)
    with col1:
        question_txt = st.text_area("Question Text", height=300, key=f"{prefix}_question_txt", disabled=disabled)
    with col2:
        answer_scheme = st.text_area("Answer Scheme", height=300, key=f"{prefix}_answer_scheme", disabled=disabled)
    num_modules = st.number_input("Number of Modules", min_value=0, step=1, key=f"{prefix}_num_modules", disabled=disabled, width=200)

    modules = []
    if num_modules > 0:
        st.subheader("Modules")
        for i in range(int(num_modules)):
            c1, c2 = st.columns([2, 1])
            with c1:
                modname = st.text_input(f"Module Name {i+1}", key=f"{prefix}_mod_{i}", disabled=disabled, width=300)
            with c2:
                marks = st.number_input(f"Max Marks {i+1}", min_value=0.0, step=0.5, key=f"{prefix}_marks_{i}", disabled=disabled, width=200)
            modules.append((modname, marks))

    # --- Create Question ---
    if not st.session_state.question_created and st.button("✅ Create Question"):
        # Basic checks
        if not question_name or not question_txt or not answer_scheme or not modules:
            st.error("Please fill all the required fields!")
        elif any(not mod or marks <= 0 for mod, marks in modules):
            st.error("Each module must have a name and marks greater than 0!")
        else:
            # Save files
            os.makedirs(f"QuestionBank/{question_name}", exist_ok=True)
            with open(f"QuestionBank/{question_name}/question.txt", "w") as f:
                f.write(question_txt)
            with open(f"QuestionBank/{question_name}/answer_scheme.v", "w") as f:
                f.write(answer_scheme)
            with open(f"QuestionBank/{question_name}/modules.csv", "w") as f:
                for mod, marks in modules:
                    f.write(f"{mod},{marks}\n")

            st.session_state.question_created = True
            st.rerun()  # refresh to lock fields

    # --- Clear / New Question ---
    if st.session_state.question_created:
        st.success(f"Files for question '{question_name}' created successfully!")
        if st.button("🔄 Clear / New Question"):
            st.session_state.form_id = str(uuid.uuid4())  # new prefix -> new blank fields
            st.session_state.question_created = False
            st.rerun()  # rerun with cleared inputs


# ------------------ SUBMIT TASK ------------------
def submit_task_ui():
    st.title("📤 Submit Task")

    prefix = st.session_state.task_form_uuid
    disabled = st.session_state.task_submitted

    # --- Directories ---
    q_dirs = [d for d in os.listdir("QuestionBank") if os.path.isdir(os.path.join("QuestionBank", d))]
    if not q_dirs:
        st.warning("No questions available. Please create a question first.")
        return

    # --- Dropdown ---
    selected_q = st.selectbox("Select Question", q_dirs, key=f"selq_{prefix}", disabled=disabled, width=300)

    # --- Paths ---
    question_file = os.path.join("QuestionBank", selected_q, "question.txt")
    answer_file = os.path.join("QuestionBank", selected_q, "answer_scheme.v")
    modules_file = os.path.join("QuestionBank", selected_q, "modules.csv")

    # --- Preview / Warnings ---
    col1, col2 = st.columns(2)
    files_exist = True

    with col1:
        if os.path.exists(question_file):
            with open(question_file, "r") as f:
                st.text_area("Question Text Preview", f.read(), height=300, disabled=True, key=f"qprev_{prefix}")
        else:
            st.warning("No question.txt found!")
            files_exist = False

    with col2:
        if os.path.exists(answer_file):
            with open(answer_file, "r") as f:
                st.text_area("Answer Scheme Preview", f.read(), height=300, disabled=True, key=f"aprev_{prefix}")
        else:
            st.warning("No answer_scheme.v found!")
            files_exist = False

    if os.path.exists(modules_file):
        with open(modules_file, "r") as f:
            st.text_area("Modules CSV Preview", f.read(), width=300, height=250, disabled=True, key=f"mprev_{prefix}")
    else:
        st.warning("No modules.csv found!")
        files_exist = False

    # --- Inputs ---
    task_name = st.text_input("Task Name", key=f"taskname_{prefix}", disabled=disabled, width=300)
    uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"], key=f"zip_{prefix}", disabled=disabled, width=400)

    # --- Placeholder for status ---
    status_placeholder = st.empty()

    # --- Submit button ---
    if not st.session_state.task_submitted:
        submit_clicked = st.button("📥 Submit Task")
        if submit_clicked:
            if not files_exist:
                st.error("Cannot submit: One or more required files are missing!\nPlease create new question.")
            elif not task_name or not uploaded_zip:
                st.error("Please provide a task name and upload a ZIP file.")
            else:
                st.session_state.task_submitted = True
                st.session_state.task_processed = False
                st.rerun()
    else:
        st.info("Task submitted. Processing...")

    # --- Processing block (runs only once per submission) ---
    if st.session_state.task_submitted and not st.session_state.task_processed and uploaded_zip is not None:
        st.session_state.task_processed = True  # mark as processed immediately

        status_placeholder.info("Task received. Processing... Please wait.")

        # Ensure directories
        os.makedirs("SolutionBank", exist_ok=True)
        os.makedirs("trash", exist_ok=True)

        # Save ZIP
        task_path = os.path.join("trash", f"{task_name}.zip")
        with open(task_path, "wb") as f:
            f.write(uploaded_zip.getbuffer())

        # Extract ZIP
        extract_dir = os.path.join("trash", f"{task_name}_extracted")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(task_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Copy files from deepest folder
        def get_deepest_folder_with_files(path):
            deepest_folder = path
            max_depth = -1
            for root, dirs, files in os.walk(path):
                if files:
                    depth = root.count(os.sep)
                    if depth > max_depth:
                        max_depth = depth
                        deepest_folder = root
            return deepest_folder

        deepest = get_deepest_folder_with_files(extract_dir)

        # Ensure SolutionBank folder for this task exists
        dest_folder = f"SolutionBank/{task_name}"
        os.makedirs(dest_folder, exist_ok=True)

        # Copy files
        for f in os.listdir(deepest):
            src_file = os.path.join(deepest, f)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_folder)

        # Progress callback
        def progress_callback(current, total):
            status_placeholder.info(f"Processing file {current}/{total}")

        # Run main evaluation
        try:
            with st.spinner("Processing task... Please wait."):
                main.main(selected_q, task_name, progress_callback=progress_callback)
            st.success(f"Evaluation complete. Results saved to Results/{selected_q}-{task_name}.xlsx")
        except Exception as e:
            st.error(f"Error during evaluation: {e}")

    # --- Clear / New Task button ---
    if st.session_state.task_processed and st.button("🔄 Clear / New Task"):
        st.session_state.task_form_uuid = str(uuid.uuid4())  # new keys for widgets
        st.session_state.task_submitted = False
        st.session_state.task_processed = False
        st.rerun()


# ------------------ VIEW RESULTS ------------------
def view_results():
    st.title("🔍 View Results")
    RESULTS_DIR = "Results"
    # Ensure the directory exists
    if not os.path.exists(RESULTS_DIR):
        st.warning(f"Directory '{RESULTS_DIR}' does not exist.")
        return

    # Get all Excel files in the directory
    files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".xlsx")]
    
    if not files:
        st.info("No Excel files found in the results directory.")
        return

    # Dropdown to select a file
    selected_file = st.selectbox("Select a results file:", files)

    if selected_file:
        file_path = os.path.join(RESULTS_DIR, selected_file)
        try:
            df = pd.read_excel(file_path)
            st.write(f"Showing contents of **{selected_file}**")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to read file: {e}")


# Render page
if st.session_state.menu == "➕ Create Question":
    create_question_ui()
elif st.session_state.menu == "📤 Submit Task":
    submit_task_ui()
elif st.session_state.menu == "🔍 View Results":
    view_results()



