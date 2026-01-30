import nmap
import threading
import datetime

scanner = nmap.PortScanner()
# This will make the output look much more organized
lock = threading.Lock()  
print("=== Nmap Port Scanner ===")

target = input("Enter IP or hostname: ")
ports = input("Enter port or port range ")

log_file = "scan_results.txt"

def scan_port(port):
    try:
        scanner.scan(target, str(port))

        state = scanner[target]['tcp'][port]['state']

        with lock:
            if state == "open":
                print(f"[+] Port {port} is OPEN")
            else:
                print(f"[-] Port {port} is CLOSED")

            with open(log_file, "a") as file:
                file.write(f"Port {port}: {state}\n")

    except:
        with lock:
            print(f"[!] Port {port} caused an error")

with open(log_file, "a") as file:
    file.write("\n=========================\n")
    file.write(f"Scan Time: {datetime.datetime.now()}\n")
    file.write(f"Target: {target}\n")
    file.write(f"Ports: {ports}\n")

print("\nScanning... please wait\n")

threads = []

# All port ranges wll be handled here (e.g. 20-80)
if "-" in ports:
    start_port, end_port = ports.split("-")
    port_list = range(int(start_port), int(end_port) + 1)
else:
    port_list = [int(ports)]

# This creates the threads
for port in port_list:
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("\nScan complete. Results saved to scan_results.txt")