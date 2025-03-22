from fastapi import FastAPI, Depends
from typing import Optional
app = FastAPI()

# Prefixes for query parameters
prefixes = {
    "m1": "motor1",
    "m2": "motor2",
    "m3": "motor3",
    "m4": "motor4",
}
# route one
@app.get("/get/")
def get_data(device: str, file: Optional[str] = None) -> dict:
    """Grabs data from web interface"""
    file_prefix = prefixes[device]
    file = f"test{file_prefix}.ino"
    return {
        "device": device,
        "file": file
    }
@app.put("/upload/")
def update_data(device: str, file: Optional[str] = None) -> dict:
    """Puts data to the web-interface"""
    file_prefix = prefixes[device]
    file = f"test{file_prefix}.ino"
    return {
        "device": device,
        "file": file,
    }
    pass

# route three