import os
from concurrent.futures import  ThreadPoolExecutor

def device_scanner():
    online_devices = []
    def ping_ip(ip):
            response = os.system(f"ping -n 4 -w 300 {ip}>nul")
            if response == 0:
                online_devices.append(ip)

            return None

    with ThreadPoolExecutor(max_workers=25) as executor:
        ips = [f"192.168.1.{str(i)}"for i in range(1,255)]
        results = executor.map(ping_ip,ips)



    for device in online_devices:
        print(f"{device} is online")


