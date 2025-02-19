import serial.tools.list_ports
import serial, platform
from typing import Optional

def get_os() -> Optional[str]:
    os_system = platform.system()
    return str(os_system)

"""instantiating ports and serial instances"""
ports = serial.tools.list_ports.comports()
serial_instance = serial.Serial()
ports_list = []

for port in ports:
    ports_list.append(str(port))
    print(str(port))

com = input(f"Choose a Com port for Arduino number # (last 5 characters after 'usbmodem' if you're on mac): ")

for i in range(0, len(ports_list)):
    """This for-loop is what runs the OS detection"""

    if get_os() == "Windows":
        print(f"OS detected: {get_os()}")
        if ports_list[i].startswith("COM" + str(com)):
            portIndex = "COM" + str(com)
            print(portIndex)
    elif get_os() == "Darwin":
        print(f"OS detected: {get_os()} (macOS)")
        if ports_list[i].startswith("/dev/cu.usbmodem" + str(com)):
            portIndex = "/dev/cu.usbmodem" + str(com)
            print(portIndex)
    elif get_os() == "Linux":
        print(f"OS detected: {get_os()}")
        if ports_list[i].startswith("/dev/cu.usbmodem" + str(com)):
            portIndex = "/dev/cu.usbmodem" + str(com)
            print(portIndex)
    else:
        print(f"OS not detected: {get_os()}")

serial_instance.baudrate = 9600
serial_instance.port = portIndex

try:
    serial_instance.open()
    print(f"Connected to {portIndex}")
except Exception as e:
    print(f"Not connecting to {portIndex}")
    exit()

order = ""
while order != "eXIT":
    order = input(f"Arduino Command -> (ON/OFF/BLINK/eXIT): ")
    serial_instance.write(order.encode('utf-8'))