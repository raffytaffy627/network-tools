import csv
import platform
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

# --- Settings: change these to monitor different hosts ---
HOSTS = ["8.8.8.8", "1.1.1.1", "github.com"]
INTERVAL = 10  # seconds between each round of pings
LOG_FILE = Path(__file__).parent / "uptime_log.csv"

IS_WINDOWS = platform.system() == "Windows"


def ping(host):
    """Ping a host once. Returns the latency in ms, or None if it's down."""
    # Windows and Linux use different ping flags for "send 1 packet, wait 1 second"
    if IS_WINDOWS:
        command = ["ping", "-n", "1", "-w", "1000", host]
    else:
        command = ["ping", "-c", "1", "-W", "1", host]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        return None

    # Look for the reply time in ping's output, e.g. "time=14ms" or "time<1ms"
    match = re.search(r"time[=<]\s*([\d.]+)\s*ms", result.stdout)

    if result.returncode == 0 and match:
        return float(match.group(1))
    return None


def log_result(timestamp, host, status, latency):
    """Append one result to the CSV log, adding a header row if the file is new."""
    is_new_file = not LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(["timestamp", "host", "status", "latency_ms"])
        writer.writerow([timestamp, host, status, latency if latency is not None else ""])


def main():
    print(f"Uptime Monitor - pinging {len(HOSTS)} hosts every {INTERVAL}s")
    print(f"Logging to {LOG_FILE.name}. Press Ctrl+C to stop.\n")

    # Keep a running count of replies for each host
    stats = {host: {"up": 0, "total": 0} for host in HOSTS}

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}]")

            for host in HOSTS:
                latency = ping(host)
                stats[host]["total"] += 1

                if latency is not None:
                    stats[host]["up"] += 1
                    print(f"  UP    {host:<15} {latency:.0f} ms")
                    log_result(timestamp, host, "UP", latency)
                else:
                    print(f"  DOWN  {host:<15} no reply")
                    log_result(timestamp, host, "DOWN", None)

            print()
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        # Ctrl+C lands here instead of crashing with a traceback
        print("\nStopped. Uptime this session:")
        for host, s in stats.items():
            percent = s["up"] / s["total"] * 100 if s["total"] else 0
            print(f"  {host:<15} {percent:5.1f}%  ({s['up']}/{s['total']} replies)")


if __name__ == "__main__":
    main()