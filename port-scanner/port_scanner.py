import socket

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # wait max 1 second per port
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

# Common ports and what they're usually used for
common_ports = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3389: "RDP"
}

target = input("Enter an IP or hostname to scan (e.g. 192.168.4.1): ")

print(f"\nScanning {target}...\n")

for port, service in common_ports.items():
    if check_port(target, port):
        print(f"Port {port} ({service}) is OPEN")
    else:
        print(f"Port {port} ({service}) is closed")