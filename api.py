from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
import serial
import arduino_services
# Prefixes for query parameters
prefixes = {
    "m1": "motor1",
    "m2": "motor2",
    "m3": "motor3",
    "m4": "motor4",
}
# route one
app = FastAPI()

@app.put("/rotate/")
def rotate_motor(
        device: str,  # m1, m2...etc
        direction: str = "clockwise",  # or "counterclockwise"
        angle: int = 90  # in degrees
) -> dict:
    if device not in prefixes:
        raise HTTPException(status_code=400, detail="Invalid motor selected.")

    if direction not in ["clockwise", "counterclockwise"]:
        raise HTTPException(status_code=400, detail="Invalid direction. Use 'clockwise' or 'counterclockwise'.")

    # Placeholder for actual Arduino communication
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    arduino.write(f"{prefixes[device]}:{direction}:{angle}\n".encode())

    return {
        "device": device,
        "motor": prefixes[device],
        "action": "rotate",
        "direction": direction,
        "angle": angle
    }
