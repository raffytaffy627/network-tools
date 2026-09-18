import socket

print("DNS Lookup Tool — type 'quit' to exit\n")

while True:
    # .strip() removes accidental spaces before/after what the user typed
    domain = input("Enter a website (e.g. google.com): ").strip()

    if domain.lower() == "quit":
        print("Goodbye!")
        break

    # If the user just hits Enter with nothing typed, ask again
    if not domain:
        continue

    try:
        # Ask the system's DNS resolver for the domain's IPv4 address
        ip_address = socket.gethostbyname(domain)
        print(f"{domain} resolves to {ip_address}\n")
    except socket.gaierror:
        # gaierror = "get address info error": the name couldn't be resolved
        print(f"Could not resolve {domain}. Check the spelling or your internet connection.\n")