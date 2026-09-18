# Network Tools

Small Python networking utilities I'm building while studying networking and working toward a career in data center and network engineering. Each tool is a single script that uses only Python's standard library, so there's nothing extra to install.

## Tools

| Tool | What it does | Runs on |
|------|--------------|---------|
| [dns-lookup](dns-lookup/) | Resolves a domain name to its IPv4 address | Windows, Linux, macOS |
| [port-scanner](port-scanner/) | Checks whether common ports (FTP, SSH, HTTP, HTTPS, RDP) are open on a host | Windows, Linux, macOS |
| [device-fingerprint](device-fingerprint/) | Ping-sweeps a /24 subnet, grabs the MAC address of every live device, and saves the results to a file | Linux |

## Getting started

Requires Python 3.

```bash
git clone https://github.com/raffytaffy627/network-tools.git
cd network-tools
```

On Windows, use `python` instead of `python3` in the commands below.

## DNS Lookup

```bash
python3 dns-lookup/dns_lookup.py
```

Example output:

```
DNS Lookup Tool — type 'quit' to exit

Enter a website (e.g. google.com): github.com
github.com resolves to 140.82.113.4

Enter a website (e.g. google.com): quit
Goodbye!
```

## Port Scanner

```bash
python3 port-scanner/port_scanner.py
```

Example output:

```
Enter an IP or hostname to scan (e.g. 192.168.4.1): 192.168.4.1

Scanning 192.168.4.1...

Port 21 (FTP) is closed
Port 22 (SSH) is closed
Port 80 (HTTP) is OPEN
Port 443 (HTTPS) is OPEN
Port 3389 (RDP) is closed
```

> Only scan devices and networks you own or have permission to test.

## Device Fingerprint (Linux)

Pass the first three parts of your network's IP range. If you leave it out, it defaults to `192.168.4`.

```bash
python3 device-fingerprint/device_fingerprint.py 192.168.1
```

Example output:

```
192.168.1.1 is alive (MAC: aa:bb:cc:11:22:33)
192.168.1.25 is alive (MAC: aa:bb:cc:44:55:66)
192.168.1.40 is alive (MAC: aa:bb:cc:77:88:99)

Scan complete. 3 devices found in 42.7 seconds.
Results saved to scan_results.txt
```

**How it works:** it pings each address from `.1` to `.254` once with a 1-second timeout. For every device that replies, it looks up the MAC address in the system's neighbor (ARP) table with `ip neigh`.

## What I learned

- How DNS turns a domain name into an IP address (`socket.gethostbyname`)
- How a TCP connect scan works, and why timeouts matter (`socket.connect_ex`)
- Ping sweeps, the ARP/neighbor table, and running system commands from Python (`subprocess`)

## Roadmap

- [ ] Subnet calculator
- [ ] Uptime / latency monitor
- [ ] Windows support for device-fingerprint