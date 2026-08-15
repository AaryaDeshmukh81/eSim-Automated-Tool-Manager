import os

from dependency_checker import check_tool, get_tool_version
from tool_manager import run_ngspice


def main():

    print("=" * 55)
    print("             eSim Automated Tool Manager")
    print("=" * 55)

    # -----------------------------------------
    # STEP 1: Check ngspice
    # -----------------------------------------

    print("\nChecking dependencies...\n")

    ngspice_installed, ngspice_path = check_tool("ngspice")

    if not ngspice_installed:
        print("ngspice: NOT INSTALLED [ERROR]")
        print("Please install ngspice first.")
        return

    print("ngspice: Installed [OK]")
    print("Location:", ngspice_path)
    print("Version:", get_tool_version("ngspice"))

    # -----------------------------------------
    # STEP 2: Find circuit files
    # -----------------------------------------

    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    circuit_files = [
        file for file in os.listdir(project_folder)
        if file.lower().endswith(".cir")
    ]

    if not circuit_files:
        print("\nNo .cir circuit files found.")
        return

    # -----------------------------------------
    # STEP 3: Display circuit files
    # -----------------------------------------

    print("\nAvailable circuit files:")
    print("-" * 40)

    for index, file in enumerate(circuit_files, start=1):
        print(f"{index}. {file}")

    print("-" * 40)

    # -----------------------------------------
    # STEP 4: Ask user to select
    # -----------------------------------------

    while True:

        choice = input(
            f"Enter circuit number (1-{len(circuit_files)}): "
        )

        try:
            choice = int(choice)

            if 1 <= choice <= len(circuit_files):
                break

            print("Please enter a valid number.")

        except ValueError:
            print("Please enter a number.")

    selected_file = circuit_files[choice - 1]

    circuit_path = os.path.join(
        project_folder,
        selected_file
    )

    print()
    print("Selected circuit:", selected_file)
    print("Circuit path:", circuit_path)

    # -----------------------------------------
    # STEP 5: Run simulation
    # -----------------------------------------

    print("\nStarting simulation...")

    success = run_ngspice(circuit_path)

    # -----------------------------------------
    # STEP 6: Final result
    # -----------------------------------------

    print()

    if success:

        print("=" * 55)
        print("       SIMULATION COMPLETED SUCCESSFULLY")
        print("=" * 55)

    else:

        print("=" * 55)
        print("              SIMULATION FAILED")
        print("=" * 55)


if __name__ == "__main__":
    main()