# Network Tools

Small Python networking utilities I'm building while studying networking and working toward a career in data center and network engineering. Each tool is a single script that uses only Python's standard library, so there's nothing extra to install.

## Tools

| Tool | What it does | Runs on |
|------|--------------|---------|
| [dns-lookup](dns-lookup/) | Resolves a domain name to its IPv4 address | Windows, Linux, macOS |
| [port-scanner](port-scanner/) | Checks whether common ports (FTP, SSH, HTTP, HTTPS, RDP) are open on a host | Windows, Linux, macOS |
| [subnet-calculator](subnet-calculator/) | Breaks down any IPv4 subnet: network, broadcast, masks, host range, and host count | Windows, Linux, macOS |
| [uptime-monitor](uptime-monitor/) | Pings hosts on a schedule, shows live UP/DOWN status and latency, and logs results to CSV | Windows, Linux |
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
github.com resolves to 140.82.114.4

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

## Subnet Calculator

Enter any IPv4 address with a CIDR prefix. It doesn't have to be the network address; the tool works out which subnet the IP belongs to.

```bash
python3 subnet-calculator/subnet_calculator.py
```

Example output:

```
Enter an IPv4 address with CIDR (e.g. 192.168.1.0/24): 192.168.1.57/26

  Network address:   192.168.1.0/26
  Subnet mask:       255.255.255.192
  Wildcard mask:     0.0.0.63
  Broadcast address: 192.168.1.63
  Usable host range: 192.168.1.1 - 192.168.1.62
  Total addresses:   64
  Usable hosts:      62
  Type:              Private
```

It also handles the edge cases correctly: a `/31` is treated as a point-to-point link (both addresses usable, no broadcast), and a `/32` as a single host.

## Uptime Monitor

```bash
python3 uptime-monitor/uptime_monitor.py
```

Example output:

```
[2026-09-18 03:42:12]
  UP    8.8.8.8         11 ms
  UP    1.1.1.1         11 ms
  UP    github.com      46 ms
  DOWN  10.255.255.1    no reply
```

Press Ctrl+C to stop and get an uptime percentage for each host. Every result is logged to `uptime_log.csv`.

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
- Subnetting math, including why `/31` and `/32` break the "subtract 2" rule (`ipaddress`)
- Running system commands cross-platform, parsing output with regular expressions, and logging to CSV (`subprocess`, `re`, `csv`)
- Ping sweeps, the ARP/neighbor table, and running system commands from Python (`subprocess`)

## Roadmap

- [x] Subnet calculator
- [x] Uptime / latency monitor
- [ ] Windows support for device-fingerprint