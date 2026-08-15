import subprocess
from pathlib import Path
import shutil
import sys


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

NGSPICE_PATH = Path(
    r"C:\Users\Lenovo\Downloads\ngspice-47_64\Spice64\bin\ngspice.exe"
)


# ============================================================
# CHECK NGSPICE
# ============================================================

def check_ngspice():

    print()
    print("=" * 60)
    print("CHECKING NGSPICE")
    print("=" * 60)

    if NGSPICE_PATH.exists():

        print("ngspice: Installed [OK]")
        print(f"Location: {NGSPICE_PATH}")
        print("Version: ngspice-47")

        return True

    system_path = shutil.which("ngspice")

    if system_path:

        print("ngspice: Installed [OK]")
        print(f"Location: {system_path}")

        return True

    print("ngspice: NOT FOUND [ERROR]")

    return False


# ============================================================
# GET NGSPICE EXECUTABLE
# ============================================================

def get_ngspice():

    if NGSPICE_PATH.exists():

        return str(NGSPICE_PATH)

    system_path = shutil.which("ngspice")

    if system_path:

        return system_path

    return None


# ============================================================
# FIND CIRCUIT FILES
# ============================================================

def get_circuit_files():

    files = []

    for file in PROJECT_DIR.iterdir():

        if file.is_file() and file.suffix.lower() == ".cir":

            files.append(file)

    files.sort(
        key=lambda x: x.name.lower()
    )

    return files


# ============================================================
# DISPLAY CIRCUIT FILES
# ============================================================

def display_circuit_files(files):

    print()
    print("=" * 60)
    print("AVAILABLE CIRCUIT FILES")
    print("=" * 60)

    for i, file in enumerate(files, start=1):

        print(
            f"{i}. {file.name}"
        )


# ============================================================
# RUN NGSPICE
# ============================================================

def run_ngspice(circuit_file):

    ngspice = get_ngspice()

    if ngspice is None:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)

        print(
            "NGSpice executable was not found."
        )

        return False


    # --------------------------------------------------------
    # Make sure circuit exists
    # --------------------------------------------------------

    if not circuit_file.exists():

        print()
        print(
            f"ERROR: Circuit file not found:"
        )

        print(
            circuit_file
        )

        return False


    # --------------------------------------------------------
    # Use RELATIVE paths
    #
    # This matches the command that worked manually.
    # --------------------------------------------------------

    circuit_name = circuit_file.name

    output_name = (
        f"{circuit_file.stem}_ngspice_output.txt"
    )


    output_file = (
        PROJECT_DIR / output_name
    )


    # --------------------------------------------------------
    # Delete old output
    # --------------------------------------------------------

    if output_file.exists():

        try:

            output_file.unlink()

        except Exception as e:

            print()
            print(
                f"Warning: Could not delete old output: {e}"
            )


    print()
    print("=" * 60)
    print("STARTING NGSPICE SIMULATION")
    print("=" * 60)

    print(
        f"Circuit: {circuit_file}"
    )

    print(
        f"Output:  {output_file}"
    )


    # ========================================================
    # EXACT COMMAND STYLE THAT WORKED MANUALLY
    #
    # ngspice.exe -b ".\test_circuit2.cir"
    #             -o ".\test_circuit2_ngspice_output.txt"
    # ========================================================

    command = [
        ngspice,
        "-b",
        f".\\{circuit_name}",
        "-o",
        f".\\{output_name}"
    ]


    print()
    print("Running command:")

    print(
        " ".join(
            f'"{x}"' if " " in x else x
            for x in command
        )
    )

    print()


    # ========================================================
    # RUN NGSPICE
    # ========================================================

    try:

        result = subprocess.run(
            command,
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60
        )


    except subprocess.TimeoutExpired:

        print()
        print("=" * 60)
        print("ERROR: NGSPICE TIMED OUT")
        print("=" * 60)

        return False


    except Exception as e:

        print()
        print("=" * 60)
        print("ERROR STARTING NGSPICE")
        print("=" * 60)

        print(
            str(e)
        )

        return False


    # ========================================================
    # PROCESS RESULT
    # ========================================================

    print("=" * 60)
    print("NGSPICE PROCESS COMPLETED")
    print("=" * 60)

    print(
        f"NGSpice return code: {result.returncode}"
    )


    # --------------------------------------------------------
    # Print Python-captured stdout
    # --------------------------------------------------------

    if result.stdout:

        print()
        print("NGSPICE STDOUT")
        print("-" * 60)

        print(
            result.stdout
        )


    # --------------------------------------------------------
    # Print Python-captured stderr
    # --------------------------------------------------------

    if result.stderr:

        print()
        print("NGSPICE STDERR")
        print("-" * 60)

        print(
            result.stderr
        )


    # ========================================================
    # CHECK OUTPUT FILE
    # ========================================================

    if not output_file.exists():

        print()
        print("=" * 60)
        print("ERROR: NGSPICE OUTPUT FILE WAS NOT CREATED")
        print("=" * 60)

        print(
            f"Expected file:"
        )

        print(
            output_file
        )

        print()
        print(
            "Checking project directory..."
        )

        for item in PROJECT_DIR.iterdir():

            print(
                f"  {item.name}"
            )

        return False


    # ========================================================
    # OUTPUT FILE SUCCESS
    # ========================================================

    print()
    print("=" * 60)
    print("NGSPICE OUTPUT FILE CREATED")
    print("=" * 60)

    print(
        f"Saved to: {output_file}"
    )

    print(
        f"File size: {output_file.stat().st_size} bytes"
    )


    # ========================================================
    # READ OUTPUT
    # ========================================================

    try:

        with open(
            output_file,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:

            output = file.read()

    except Exception as e:

        print()
        print(
            f"ERROR reading output file: {e}"
        )

        return False


    # ========================================================
    # DISPLAY OUTPUT
    # ========================================================

    print()
    print("=" * 60)
    print("NGSPICE OUTPUT")
    print("=" * 60)

    print(
        output
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    if result.returncode == 0:

        print()
        print("=" * 60)
        print("SIMULATION COMPLETED SUCCESSFULLY")
        print("=" * 60)

        return True


    # ========================================================
    # FAILURE
    # ========================================================

    print()
    print("=" * 60)
    print("SIMULATION FAILED")
    print("=" * 60)

    print(
        f"Return code: {result.returncode}"
    )

    return False


# ============================================================
# RUN SELECTED CIRCUIT
# ============================================================

def run_selected_circuit(circuit_file):

    print()
    print(
        f"Selected circuit: {circuit_file.name}"
    )

    print(
        f"Circuit path: {circuit_file}"
    )

    print()
    print(
        "Starting simulation..."
    )

    success = run_ngspice(
        circuit_file
    )

    print()

    if success:

        print("=" * 60)
        print("SIMULATION COMPLETED SUCCESSFULLY")
        print("=" * 60)

    else:

        print("=" * 60)
        print("SIMULATION FAILED")
        print("=" * 60)

    return success


# ============================================================
# TOOL MANAGER
# ============================================================

def tool_manager():

    print()
    print("=" * 60)
    print("        E-SIM AUTOMATED TOOL MANAGER")
    print("=" * 60)


    # --------------------------------------------------------
    # CHECK DEPENDENCIES
    # --------------------------------------------------------

    print()
    print(
        "Checking dependencies..."
    )

    if not check_ngspice():

        print()
        print("=" * 60)
        print("DEPENDENCY CHECK FAILED")
        print("=" * 60)

        return False


    # --------------------------------------------------------
    # GET CIRCUIT FILES
    # --------------------------------------------------------

    circuit_files = get_circuit_files()


    if len(circuit_files) == 0:

        print()
        print("=" * 60)
        print("NO CIRCUIT FILES FOUND")
        print("=" * 60)

        print(
            f"Project folder:"
        )

        print(
            PROJECT_DIR
        )

        return False


    # --------------------------------------------------------
    # DISPLAY CIRCUITS
    # --------------------------------------------------------

    display_circuit_files(
        circuit_files
    )


    # --------------------------------------------------------
    # SELECT CIRCUIT
    # --------------------------------------------------------

    while True:

        try:

            choice = int(
                input(
                    f"\nEnter circuit number "
                    f"(1-{len(circuit_files)}): "
                )
            )

            if (
                choice >= 1
                and
                choice <= len(circuit_files)
            ):

                break

            print(
                "Please enter a valid circuit number."
            )

        except ValueError:

            print(
                "Please enter a number."
            )


    selected_circuit = (
        circuit_files[choice - 1]
    )


    print()
    print(
        f"Selected circuit: {selected_circuit.name}"
    )

    print(
        f"Circuit path: {selected_circuit}"
    )


    # --------------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------------

    success = run_selected_circuit(
        selected_circuit
    )


    return success


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    success = tool_manager()

    if success:

        sys.exit(0)

    else:

        sys.exit(1)