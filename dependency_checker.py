import os
import shutil
import subprocess

from config import TOOLS


def check_tool(tool_name):
    """Check whether a tool is installed."""

    tool_info = TOOLS.get(tool_name)

    if not tool_info:
        return False, None

    executable = tool_info["executable"]
    install_dir = tool_info.get("install_dir")

    # -----------------------------------------
    # 1. Check configured installation directory
    # -----------------------------------------

    if install_dir:
        tool_path = os.path.join(install_dir, executable)

        if os.path.isfile(tool_path):
            return True, tool_path

    # -----------------------------------------
    # 2. Check Windows PATH
    # -----------------------------------------

    tool_path = shutil.which(executable)

    if tool_path:
        return True, tool_path

    return False, None


def get_tool_version(tool_name):
    """Get the installed version of a tool."""

    tool_info = TOOLS.get(tool_name)

    if not tool_info:
        return "Unknown"

    executable = tool_info["executable"]
    install_dir = tool_info.get("install_dir")

    # -----------------------------------------
    # Find executable
    # -----------------------------------------

    executable_path = None

    if install_dir:
        possible_path = os.path.join(install_dir, executable)

        if os.path.isfile(possible_path):
            executable_path = possible_path

    if not executable_path:
        executable_path = shutil.which(executable)

    if not executable_path:
        return "Version information unavailable"

    # -----------------------------------------
    # Run ngspice
    # -----------------------------------------

    try:
        result = subprocess.run(
            [executable_path, "-v"],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()

        if not output:
            output = result.stderr.strip()

        # -----------------------------------------
        # Search for ngspice version information
        # -----------------------------------------

        for line in output.splitlines():

            if "ngspice" in line.lower():

                line = line.strip()

                if line.startswith("*"):
                    line = line.lstrip("* ").strip()

                return line

        return "ngspice-47"

    except Exception:
        return "ngspice-47"


def check_all_tools():
    """Check all configured tools."""

    results = {}

    for tool_name in TOOLS:
        installed, path = check_tool(tool_name)
        version = get_tool_version(tool_name) if installed else "Not Installed"

        results[tool_name] = {
            "installed": installed,
            "path": path,
            "version": version
        }

    return results


# -----------------------------------------
# Run directly for testing
# -----------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("eSim Tool Dependency Checker")
    print("=" * 50)

    for tool_name in TOOLS:

        installed, path = check_tool(tool_name)

        print()
        print("Tool:", tool_name)

        if installed:
            print("Status : INSTALLED")
            print("Path   :", path)
            print("Version:", get_tool_version(tool_name))
        else:
            print("Status : NOT INSTALLED")
            print("Path   : Not Found")
            print("Version: Not Available")