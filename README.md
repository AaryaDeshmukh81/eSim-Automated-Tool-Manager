
**eSim Automated Tool Manager**

A Python-based prototype for managing external tools and dependencies used with eSim.

**Features :**
- Checks NGSpice availability.
- Checks NGSpice version information.
- Checks required dependencies.
- Detects available NGSpice circuit files.
- Allows the user to select a circuit file.
- Runs the selected circuit using NGSpice.
- Reports simulation status and output.

**Project Structure :**
```text
eSim-Automated-Tool-manager/
├── main.py
├── tool_manager.py
├── dependency_checker.py
├── config.py
├── requirements.txt
├── test_circuit.cir
├── test_circuit2.cir
├── manual_output.txt
└── .gitignore

**Requirements :**
* Windows
* Python 3.x
* NGSpice
* Git
* VS Code or another Python-capable editor

**Installation :**

Check Python:
python --version
Install the required Python dependencies:
python -m pip install -r requirements.txt
Install NGSpice and ensure that its executable is accessible to the project.

**Execution :**

Run the tool manager from the project directory:
python main.py
The tool manager checks the required environment and NGSpice availability, displays the available circuit files, and allows the user to select a circuit for simulation.

**Testing :**

The project includes:
* test_circuit.cir
* test_circuit2.cir

The testing process checks NGSpice availability, version information, dependency status, circuit selection, and circuit simulation execution.

