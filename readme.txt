#Setup
- make sure python is installed


First Time:
    #in the root directory of project:

    ##1. create a new file .env file as in .env.example and add keys

    ##2.
    Create Virtual env
        python -m venv ./venv

    Any one: Activate virtual env
        powershell: venv\Scripts\Activate.ps1
        commandpromp: venv\Scripts\activate

    Install dependencies
        pip install -r requirements.txt

    Run the project
        streamlit run ui.py


From next time onwards:

Any one: Activate virtual env
        powershell: venv\Scripts\Activate.ps1
        commandpromp: venv\Scripts\activate

Run the project
        streamlit run ui.py



##Other Info:
    Can see each API prompt and Response in op.txt in root directory after task is completed.
