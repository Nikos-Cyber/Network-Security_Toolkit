import time
import socket
import os
from concurrent.futures import  ThreadPoolExecutor
from Vendor import vendor
from Device_Scanner import device_scanner
from Port_Scanner import port_scanner
from sniffer import sniffing

while True:
    user_choice = input(f"\n1) Port Scanner\n2) Check internet activity\n3) Device Scanner\n4) Scheduled Port Scanning\n5) Scheduled Device Scanning\n6) Vendor Finder(Device Scan Recommended First)\n\nPut answer :")
    if int(user_choice) == 1:
        port_scanner()
    elif int(user_choice) == 2:
        sniffing()
    elif int(user_choice) == 3:
        device_scanner()
    elif int(user_choice) == 4:
        timing = input("How often do you need a port scan (More than 2 minutes):")
        timing2 = int(timing)*60
        ip = input("Put target ip :")
        while True:
            time.sleep(timing2 - 105)
            open_ports = []
            for port in range(1, 1000):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scan:
                    scan.settimeout(0.1)
                    result = scan.connect_ex((ip, port))

                if result == 0:
                    open_ports.append(port)
            if len(open_ports) > 50:
                print("-----DANGER------")
                print(open_ports)
            else:
                print("-" * 50)
                print("ALL GOOD")
                print(f"open ports = {open_ports}")
                print("-" * 50)
    elif int(user_choice) == 5:
        timing3 = input("How often do you need a device scan (More then 2 minutes) :")
        timing4 = int(timing3)*60
        while True:
            time.sleep(timing4 - 55)
            online_devices = []
            def ping_ip(ip):
                response = os.system(f"ping -n 4 -w 300 {ip}>nul")
                if response == 0:
                    online_devices.append(ip)



            with ThreadPoolExecutor(max_workers=25) as executor:
                ips = [f"192.168.1.{str(i)}" for i in range(1, 255)]
                results = executor.map(ping_ip, ips)
            print("*" * 25)
            for device in online_devices:
                print(f"{device} is online")
            print("*" * 25)
    elif int(user_choice) == 6:
        vendor()