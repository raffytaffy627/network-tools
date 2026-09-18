import ipaddress

print("Subnet Calculator - type 'quit' to exit\n")

while True:
    user_input = input("Enter an IPv4 address with CIDR (e.g. 192.168.1.0/24): ").strip()

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    try:
        # strict=False lets you enter ANY IP in the network (like 192.168.1.57/24)
        # Also Python works out which network it belongs to
        network = ipaddress.IPv4Network(user_input, strict=False)
    except ValueError:
        print("Invalid input. Use a format like 192.168.1.0/24 or 10.0.0.5/8.\n")
        continue

    prefix = network.prefixlen       # the number after the slash, e.g. 24
    total = network.num_addresses     # every address in the subnet

    # Normal subnets reserve 2 addresses: the network address and the broadcast.
    # /31 and /32 are special cases with no reserved addresses.
    if prefix == 32:
        first_host = last_host = network.network_address
        usable = 1
        broadcast = "N/A (single host)"
    elif prefix == 31:
        first_host = network.network_address
        last_host = network.broadcast_address
        usable = 2
        broadcast = "N/A (point-to-point)"
    else:
        first_host = network.network_address + 1
        last_host = network.broadcast_address - 1
        usable = total - 2
        broadcast = network.broadcast_address

    scope = "Private" if network.is_private else "Public"

    print(f"\n  Network address:   {network.network_address}/{prefix}")
    print(f"  Subnet mask:       {network.netmask}")
    print(f"  Wildcard mask:     {network.hostmask}")
    print(f"  Broadcast address: {broadcast}")
    print(f"  Usable host range: {first_host} - {last_host}")
    print(f"  Total addresses:   {total:,}")
    print(f"  Usable hosts:      {usable:,}")
    print(f"  Type:              {scope}\n")