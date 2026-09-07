import socket

# Ask the user for a website name
domain = input("Enter a website (e.g. google.com): ")

try:
    ip_address = socket.gethostbyname(domain)
    print(f"{domain} resolves to {ip_address}")
except socket.gaierror:
    print(f"Could not resolve {domain}. Check the spelling or your internet connection.")
    import socket

print("DNS Lookup Tool — type 'quit' to exit\n")

while True:
    domain = input("Enter a website (e.g. google.com): ")
    
    if domain.lower() == "quit":
        print("Goodbye!")
        break
    
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"{domain} resolves to {ip_address}\n")
    except socket.gaierror:
        print(f"Could not resolve {domain}. Check the spelling or your internet connection.\n")