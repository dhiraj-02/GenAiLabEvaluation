import subprocess

def compile_and_run(verilog_file, top_module=None):
    compile_cmd = ["iverilog", "-o", "sim.out", verilog_file]
    if top_module:
        compile_cmd.extend(["-s", top_module])

    result_str = "compilation result:\n"
    stdout_str = "stdout:\n"

    try:
        # Compile
        compile_process = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:
            # Compilation error → put error in compilation result, stdout empty
            result_str += compile_process.stderr.strip()
            return f"{result_str}\n\n{stdout_str}"

        result_str += "Compilation successful"

        # Run simulation
        run_process = subprocess.run(
            ["vvp", "sim.out"],
            capture_output=True,
            text=True
        )

        if run_process.returncode != 0:
            # Execution error → put in stdout
            stdout_str += run_process.stderr.strip()
        else:
            # Execution success → put normal stdout
            stdout_str += run_process.stdout.strip()

        return f"{result_str}\n\n{stdout_str}"

    except FileNotFoundError as e:
        result_str += f"Error: {e}"
        return f"{result_str}\n\n{stdout_str}"
