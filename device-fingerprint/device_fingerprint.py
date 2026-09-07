import subprocess
import time
import sys

def ping(ip):
    # "-c 1" means send just 1 ping packet (Linux/Mac syntax)
    # We check the return code: 0 means success (device responds with a ping basically)
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def get_mac(ip):
    try:
        result = subprocess.run(
            ["ip", "neigh", "show", ip],
            capture_output=True, text=True
        )
        output = result.stdout
        if "lladdr" in output:
            parts = output.split()
            mac_index = parts.index("lladdr") + 1
            return parts[mac_index]
        else:
            return "Unknown"
    except Exception:
        return "Unknown"

# Sweeping a range of IPs on the local network
if len(sys.argv) > 1:
    base_ip = sys.argv[1]
else:
    base_ip = "192.168.4"
    print(f"No network specified, defaulting to {base_ip}.x")

alive_devices = []  # empty list to collect (ip, mac) pairs as we find them
start_time = time.time()

for i in range(1, 255):
    ip = f"{base_ip}.{i}"
    print(f"Scanning {ip}...", end="\r")
    if ping(ip):
        mac = get_mac(ip)
        print(f"{ip} is alive (MAC: {mac})" + " " * 10)
        alive_devices.append((ip, mac))

# After the loop finishes, save results and show a summary
with open("scan_results.txt", "w") as f:
    for ip, mac in alive_devices:
        f.write(f"{ip}\t{mac}\n")

elapsed = time.time() - start_time
print(f"\nScan complete. {len(alive_devices)} devices found in {elapsed:.1f} seconds.")
print("Results saved to scan_results.txt")