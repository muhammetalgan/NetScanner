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

# # Get target IP address and port range from user
target_ip = input("Hedef IP adresini girin: ")
start_port = int(input("Başlangıç portunu girin: "))
end_port = int(input("Bitiş portunu girin: "))

# Start port scan
open_ports = scan_ports(target_ip, start_port, end_port)

# Detect operating system
detect_os(target_ip)
