# Uptime Monitor

Pings a list of hosts on a schedule, shows live UP/DOWN status with latency, and logs every result to a CSV file. A small-scale version of how data centers monitor their equipment.

## Usage

```bash
python3 uptime_monitor.py
```

Press **Ctrl+C** to stop and see an uptime summary for the session.

To monitor different hosts or change how often it checks, edit the settings at the top of the script:

```python
HOSTS = ["8.8.8.8", "1.1.1.1", "github.com"]
INTERVAL = 10  # seconds between each round of pings
```

## Example

```
Uptime Monitor - pinging 4 hosts every 10s
Logging to uptime_log.csv. Press Ctrl+C to stop.

[2026-09-18 03:42:12]
  UP    8.8.8.8         11 ms
  UP    1.1.1.1         11 ms
  UP    github.com      46 ms
  DOWN  10.255.255.1    no reply

Stopped. Uptime this session:
  8.8.8.8         100.0%  (1/1 replies)
  1.1.1.1         100.0%  (1/1 replies)
  github.com      100.0%  (1/1 replies)
  10.255.255.1      0.0%  (0/1 replies)
```

## CSV log

Every result is appended to `uptime_log.csv` (next to the script), which opens directly in Excel or Google Sheets:

```
timestamp,host,status,latency_ms
2026-09-18 03:40:24,8.8.8.8,UP,11.0
2026-09-18 03:40:24,1.1.1.1,UP,11.0
2026-09-18 03:40:24,github.com,UP,46.0
```

The log is in `.gitignore` since it's generated data.

## How it works

- Runs the system's `ping` command with `subprocess`, using the right flags for Windows (`-n 1 -w 1000`) or Linux (`-c 1 -W 1`), so it works on both.
- Pulls the reply time out of ping's output with a regular expression.
- **Windows gotcha:** Windows `ping` reports success even when a router replies "Destination host unreachable." The script only counts a host as UP if there's an actual reply time, which filters out that false positive.
- Catches **Ctrl+C** to print a clean summary instead of crashing with a traceback.