"""
 \ Muhammet ALGAN - BASIC NETDISCOVER /
"""
from scapy.all import *

def scan_ports(target_ip, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port+1):
        packet = IP(dst=target_ip)/TCP(dport=port, flags='S')
        response = sr1(packet, timeout=1, verbose=0)
        if response and response.haslayer(TCP) and response[TCP].flags == 'SA':
            open_ports.append(port)
            print(f"Port {port} is open")

    return open_ports

def detect_os(target_ip):
    packet = IP(dst=target_ip)/ICMP()
    response = sr1(packet, timeout=1, verbose=0)
    if response and response.haslayer(IP):
        print(f"Detected OS: {response[IP].ttl}")

# Get the target IP address and port range from the user
target_ip = input("Enter the target IP address: ")
start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

# Start the port scanning
open_ports = scan_ports(target_ip, start_port, end_port)

# Perform OS detection
detect_os(target_ip)
