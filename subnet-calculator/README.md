# Subnet Calculator

Enter any IPv4 address with a CIDR prefix and get a full breakdown of the subnet it belongs to. Built while studying subnetting for CompTIA Network+.

## Usage

```bash
python3 subnet_calculator.py
```

Type `quit` to exit.

## Example

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

## What each field means

| Field | Meaning |
|-------|---------|
| Network address | The first address in the subnet; identifies the network itself |
| Subnet mask | Which part of the address is the network vs. the host |
| Wildcard mask | The inverse of the subnet mask, used in Cisco ACLs and OSPF (Open Shortest Path First) |
| Broadcast address | The last address; sends to every host on the subnet |
| Usable host range | Addresses you can actually assign to devices |
| Type | Private (RFC 1918 ranges like 10.x, 172.16–31.x, 192.168.x) or Public |

## Edge cases :/

Most subnets lose 2 addresses (network and broadcast), but two prefixes break that rule:

- **/31**: a point-to-point link between two routers (RFC 3021). Both addresses are usable and there's no broadcast.
- **/32**: a single host. One usable address, no broadcast.

The calculator handles both instead of reporting negative or incorrect host counts.

## How it works!! :D

Uses Python's built-in `ipaddress` module. `strict=False` lets you enter any IP inside the subnet (like `.57`), and the module works out which network it belongs to. Invalid input like `300.1.1.1/24` is caught and you're asked again.

## Bugs I hit while building this

- **`prefix` is not defined:** a line was indented one level too far, which put it inside the `except` block after `continue`, so it never ran. Fixed the indentation.
- **Wrong broadcast for /31 and /32:** the tool printed a broadcast address for subnets that don't have one. Added a `broadcast` variable set in each branch of the if/elif/else.