import socket
from scapy.layers.inet import IP,TCP
from scapy.layers.inet6 import IPv6
from scapy.layers.dns import DNS,DNSQR
from scapy.all import Raw,sniff
from mac_vendor_lookup import MacLookup , VendorNotFoundError
import subprocess
import re

lookup = MacLookup()
lookup.update_vendors()
def vendor(ip_addres):
    def is_random_mac(mac):
        first_byte = int(mac.split("-")[0], 16)
        return (first_byte & 0b00000010) != 0
    mac_finder = subprocess.check_output("arp -a", shell = True , text=True)
    macs = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})\s+dynamic"
    star = "*"
    for ip , mac in re.findall(macs,mac_finder):
        if ip == ip_addres:
            if is_random_mac(mac):
                Vendor = "Random\Private Mac"
            else:
                try:
                    Vendor = lookup.lookup(mac)
                except VendorNotFoundError:
                    Vendor = "Unknown"

            with open("report.txt", "a") as file:
                file.write(f"{star * 20}\nTYPE : IP :{ip}\nTYPE : MAC : {mac}\nTYPE : VENDOR : {Vendor}\n{star * 20}")


def procces_packet(packet):
    if packet.haslayer(IP) and packet.haslayer(DNS) and packet.haslayer(DNSQR):
        domain = packet[DNSQR].qname.decode()
        ip_address = packet[IP].src
        if len(domain) >= 50:
            vendor(ip_address)
            print("aha")
    elif packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors= "ignore")
        if "HTTP" in payload :
            if packet.haslayer[IP]:
                ipaddres2 = packet[IP].src
            elif packet.haslayer(IPv6):
                ipaddres2 = packet[IPv6].src

            danger_keywords = ["password", "passwd", "username", "login", "admin", "secret"]
            if any(keyword in payload.lower() for keyword in danger_keywords):
                vendor(ipaddres2)
                print("aha")

sniff(iface= "Wi-Fi",prn=procces_packet, store=0)

