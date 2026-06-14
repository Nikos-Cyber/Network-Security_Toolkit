import socket

def port_scanner():
    def scan_ports(ip):
        open_ports = []
        for port in range(1,1000):
            with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as scan:
                scan.settimeout(0.1)
                result = scan.connect_ex((ip,port))

            if result == 0:
                    open_ports.append(port)
        if len(open_ports)>50:
            print("-----DANGER------")
            print(open_ports)
        else:
            print("-"*50)
            print("ALL GOOD")
            print(f"open ports = {open_ports}")
            print("-" *50)
    port_scanning = input("\nPut target ip :")
    scan_ports(port_scanning)
