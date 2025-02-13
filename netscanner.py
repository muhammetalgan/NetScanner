"""
 \ Muhammet ALGAN - AdvancedNetScanner-With-AutoExploitCheck-CVE-ExploitDB /
                    https://github.com/muhammetalgan
"""
import subprocess
import requests
from scapy.all import

def check_exploits(application, version):
    url = f"https://www.exploit-db.com/search?platform=&type=&searchtext={application} {version}"
    response = requests.get(url)

    if "No results" in response.text:
        print(f"No known exploits found for {application} {version}")
    else:
        print(f"Potential exploits found for {application} {version}")
        # You can further process the response here if needed

def get_installed_applications():
    command = "dpkg-query -f '${Package} ${Version}\n' -W"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    applications = output.strip().split('\n')
    return [app.split(' ') for app in applications]

def scan_ports(target_ip, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port+1):
        packet = IP(dst=target_ip)/TCP(dport=port, flags='S')
        response = sr1(packet, timeout=1, verbose=0)
        if response and response.haslayer(TCP) and response[TCP].flags == 'SA':
            open_ports.append(port)
            print(f"Port {port} is open")
            # Perform Service Banner Grabbing
            packet = IP(dst=target_ip)/TCP(dport=port, flags='S')
            response = sr1(packet, timeout=1, verbose=0)
            if response and response.haslayer(TCP) and response[TCP].flags == 'SA':
                print(f"Service banner: {response[TCP].payload}")

    return open_ports

def detect_os(target_ip):
    packet = IP(dst=target_ip)/ICMP()
    response = sr1(packet, timeout=1, verbose=0)
    if response and response.haslayer(IP):
        print(f"Detected OS: {response[IP].ttl}")

def perform_vulnerability_scan(target_ip):
    # Perform vulnerability scanning logic here
    # You can implement various checks and tests to identify vulnerabilities
    # Examples include weak configurations, default credentials, insecure protocols, etc.
    # This function can print or store the results of the vulnerability scan

    print("Performing vulnerability scan...")

    # Example: CVE Database Integration
    cve_url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={target_ip}"
    response = requests.get(cve_url)

    if response.status_code == 200:
        print("Vulnerabilities found in CVE database:")
        # Parse and extract relevant information from the response
        # Display or store the results
    else:
        print("Failed to retrieve CVE information.")

# Get the target IP address and port range from the user
target_ip = input("Enter the target IP address: ")
start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

# Get the versions of installed applications
installed_applications = get_installed_applications()

# Check for exploits for each installed application
exploitable_apps = []
for app in installed_applications:
    application = app[0]
    version = app[1]
    check_exploits(application, version)
    exploitable_apps.append((application, version))

# Start the port scanning
open_ports = scan_ports(target_ip, start_port, end_port)

# Perform OS detection
detect_os(target_ip)

# Perform vulnerability scanning
perform_vulnerability_scan(target_ip)

# Print the versions of installed applications
for app in installed_applications:
    print(f"Application: {app[0]}\tVersion: {app[1]}")

# Automation and Reporting
if open_ports:
    print("Open ports found:")
    for port in open_ports:
        print(f"Port {port} is open")

if exploitable_apps:
    print("Exploitable applications found:")
    for app in exploitable_apps:
        print(f"Application: {app[0]}\tVersion: {app[1]}")

# You can further customize the automation and reporting logic based on your requirements
# For example, you can save the results to a file, send an email report, or integrate with other tools.
