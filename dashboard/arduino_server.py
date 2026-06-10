import serial
import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# ── Configuration ──────────────────────────────────────────
SERIAL_PORT = "COM7"
BAUD_RATE   = 115200
HOST        = "localhost"
PORT        = 5000
# ───────────────────────────────────────────────────────────

latest_data = {
    "temperature": "--",
    "humidity":    "--",
    "pressure":    "--",
    "noise":       "--",
    "model":       "--",
    "confidence":  "--",
    "environment": "Waiting...",
    "reason":      "Connecting to Arduino...",
    "status":      "waiting"   # good | bad | moderate | waiting
}
data_lock = threading.Lock()


def read_serial():
    global latest_data
    buf = {}
    print(f"[Server] Connecting to {SERIAL_PORT} at {BAUD_RATE} baud…")
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
                print("[Server] Connected to Arduino ✓")
                while True:
                    raw = ser.readline().decode("utf-8", errors="ignore").strip()
                    if not raw:
                        continue

                    # Parse sensor lines
                    m = re.match(r"Temp:\s+([\d.]+)", raw)
                    if m: buf["temperature"] = m.group(1)

                    m = re.match(r"Humidity:\s+([\d.]+)", raw)
                    if m: buf["humidity"] = m.group(1)

                    m = re.match(r"Pressure:\s+([\d.]+)", raw)
                    if m: buf["pressure"] = m.group(1)

                    m = re.match(r"Noise:\s+([\d.]+)", raw)
                    if m: buf["noise"] = m.group(1)

                    m = re.match(r"Model:\s+(\w+)", raw)
                    if m: buf["model"] = m.group(1)

                    m = re.match(r"Confidence:\s+([\d.]+)", raw)
                    if m: buf["confidence"] = m.group(1)

                    # Parse result lines
                    if "Environment:" in raw:
                        env_text = raw.replace("Environment:", "").strip()
                        buf["environment"] = env_text
                        if "GOOD" in raw:
                            buf["status"] = "good"
                        elif "BAD" in raw:
                            buf["status"] = "bad"
                        elif "MODERATE" in raw:
                            buf["status"] = "moderate"

                    if "Reason:" in raw:
                        buf["reason"] = raw.replace("Reason:", "").strip()

                    # Flush on separator
                    if "==============" in raw and "environment" in buf:
                        with data_lock:
                            latest_data.update(buf)
                        buf = {}

        except serial.SerialException as e:
            print(f"[Server] Serial error: {e}  — retrying in 3 s…")
            with data_lock:
                latest_data["environment"] = "Disconnected"
                latest_data["reason"]      = "Arduino not found. Check USB cable."
                latest_data["status"]      = "waiting"
            time.sleep(3)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silence request logs

    def do_GET(self):
        if self.path == "/data":
            with data_lock:
                payload = json.dumps(latest_data).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        elif self.path == "/" or self.path == "/index.html":
            try:
                with open("dashboard.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"dashboard.html not found - place it next to this script.")
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    # Install pyserial if missing
    try:
        import serial
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])
        import serial

    threading.Thread(target=read_serial, daemon=True).start()
    print(f"[Server] Dashboard → http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
