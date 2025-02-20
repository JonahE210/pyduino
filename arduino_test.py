import serial.tools.list_ports
import serial, platform
from typing import Optional

def get_os() -> Optional[str]:
    os_system = platform.system()
    return str(os_system)

# filters ports using operating system
# ex: for Linux the prefix is "/dev/tty"
def filterPorts(operating_sys, prefix):

    print(f"OS detected: {operating_sys}")

    if ports_list[i].startswith(prefix + str(com)):

        portIndex = prefix + str(com)
        print(portIndex)

        return portIndex

# instantiating ports and serial instances
ports = serial.tools.list_ports.comports()
serial_instance = serial.Serial()
ports_list = []

# prints all available/applicable ports
# NOTE: it may be possible to move this to the filterPorts() function to save on the slightest bit of efficiency, but don't worry about it
for port in ports:
    ports_list.append(str(port))
    print(str(port))

com = input(f"Choose a Com port for Arduino number # (last 5 characters after 'usbmodem' if you're on mac): ")

# This for-loop is what runs the OS detection
for i in range(0, len(ports_list)):

    # NOTE: I added a variable here to prevent the program from running the function multiple times
    # All get_os() calls have been replaced
    os = get_os()

    if os == "Windows":

        portIndex = filterPorts(os, "COM")

        # NOTE: I moved the below code to a function

        # print(f"OS detected: {os}")
        # if ports_list[i].startswith("COM" + str(com)):
        #     portIndex = "COM" + str(com)
        #     print(portIndex)

    elif os == "Darwin":

        portIndex = filterPorts(os, "/dev/cu.usbmodem")

    elif os == "Linux":

        portIndex = filterPorts(os, "/dev/tty")

    else:
        print(f"OS not detected: {os}")

serial_instance.baudrate = 9600
serial_instance.port = portIndex

# Since we are looking for a certain amount of bytes, if the desired amount has not been reached
# the absence of a timeout will block the entire program
serial_instance.timeout = 2

# NOTE: I didn't even know Python had try-catch lol
try:
    serial_instance.open()
    print(f"Connected to {portIndex}")
except Exception as e:
    print(f"Not connecting to {portIndex}")
    exit()

order = ""

# NOTE: I changed "eXIT" to "q" just for unified structure purposes (essentially because the interface uses q)
while order.lower != "q":
    order = input(f"Arduino Command -> (ON/OFF/BLINK/q): ")
    serial_instance.write(order.encode('utf-8'))

    # Reads the serial instance for 35 bytes and converts it from 'byte' data type to 'str' data type
    # TODO: allocate a dynamic amount of bytes
    # NOTE: Check byte-by-byte until we reach \r\n (since this is what it seems to end with)
    
    test = serial_instance.read(35).decode()
    

    print(test)