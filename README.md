# eSim Automated Tool Manager

A Python-based tool manager prototype for checking NGSpice availability and running circuit simulations for eSim.

## Features

- Checks whether NGSpice is installed and accessible.
- Checks the NGSpice version and executable location.
- Checks required dependencies.
- Lists available NGSpice circuit files.
- Allows the user to select a circuit from the command line.
- Runs the selected circuit using NGSpice.
- Reports simulation success or failure.
- Generates simulation output.

## Project Structure

```text
E-Sim Project/
├── main.py
├── tool_manager.py
├── dependency_checker.py
├── config.py
├── requirements.txt
├── test_circuit.cir
├── test_circuit2.cir
├── manual_output.txt
└── .gitignore
```

## Requirements

- Windows
- Python 3.x
- NGSpice
- Git
- VS Code or another Python-capable editor

## Installation

### 1. Check Python

```powershell
python --version
```

### 2. Install Python dependencies

Open the terminal in the project folder and run:

```powershell
python -m pip install -r requirements.txt
```

### 3. Install NGSpice

Install NGSpice and make sure its executable is accessible to the project.

## Run the Project

From the project folder, run:

```powershell
python main.py
```

The program checks the environment and NGSpice, displays the available circuit files, asks you to select a circuit, runs the simulation, and displays the result.

## Test Files

The project includes:

- `test_circuit.cir`
- `test_circuit2.cir`

A successful NGSpice simulation returns code `0` and generates the expected output.
