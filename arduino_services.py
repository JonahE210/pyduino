import serial.tools.list_ports, platform
from arduino_mp import MultiprocessingArduinoCLI
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

def get_os() -> str:
    """Detects the current operating system."""
    return platform.system()

# Moved this block of code into a function for the purpose of multiprocessing

def list_ports():
    """Lists available serial ports."""
    ports = serial.tools.list_ports.comports()
    # changed str(port) -> str(port.device)
    ports_list = [str(port.device) for port in ports]

    for port in ports_list:
        print(port)

    return ports_list

# There was a weird bug with the 'filterPorts' function
# where ports_list[i] wouldn't loop through filterPorts
# SIDENOTE: Changed 'filterPorts' to 'filter_ports' to stay in line with snake_case
def filter_ports(ports_list, os_system, com):
    """Finds the correct Arduino port based on OS."""
    prefixes = {"Windows": "COM",
                "Darwin": "/dev/cu.usbmodem",
                "Linux": "/dev/tty"}

    prefix = prefixes.get(os_system, None)

    if not prefix:
        print(f"Unsupported OS: {os_system}")
        return None

    for port in ports_list:
        if port.startswith(prefix + str(com)):
            return port

    print(f"No matching port found for {prefix}{com}")
    return None


def main() -> Optional[None]:
    """Main function"""
    ports_list = list_ports()
    os_system = get_os()
    com = input("Choose a Com port for Arduino (last 5 characters after 'usbmodem' on Mac): ")
    portIndex = filter_ports(ports_list, os_system, com)

    if not portIndex:
        print("Invalid port selection. Exiting.")
        return

    arduino_cli = MultiprocessingArduinoCLI()

    while True:
        print("\nAvailable Commands: board_list | compile | upload | q (quit)")
        order = input("Arduino Command: ").strip().upper()

        if order == "Q":
            break
        elif order == "BOARD_LIST":
            task = {"type": "board_list"}
        elif order == "COMPILE":
            fqbn = input("Enter FQBN (e.g., arduino:avr:uno): ").strip()
            sketch = input("Enter sketch path (e.g. MyFirstSketch): ").strip()
            task = {"type": "compile", "fqbn": fqbn, "sketch": sketch}
        elif order == "UPLOAD":
            fqbn = input("Enter FQBN: ").strip()
            sketch = input("Enter sketch path: ").strip()
            task = {"type": "upload", "port": portIndex, "fqbn": fqbn, "sketch": sketch}
        else:

            task = {"type": "serial", "port": portIndex, "command": order}

        stdout, stderr = arduino_cli.run_arduino_task(task)

        print(f"\nArduino CLI Output:\n{stdout}")
        if stderr:
            print(f"Error:\n{stderr}")

    arduino_cli.terminate_subprocess()


if __name__ == "__main__":
    main()
