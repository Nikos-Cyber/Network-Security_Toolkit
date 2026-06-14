from idlelib.iomenu import errors
import socket
from scapy.layers.inet import IP,TCP
from scapy.layers.dns import DNS,DNSQR
from scapy.all import Raw,sniff
def sniffing():
    def procces_packet(packet):
        if packet.haslayer(IP) and packet.haslayer(DNS) and packet.haslayer(DNSQR):
            domain = packet[DNSQR].qname.decode()
            ip_address = packet[IP].src
            print(f"DNS {domain} and from  {ip_address}")
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                print(f"Device name :  {hostname}")
            except socket.herror:
                print("no hostname")

        elif packet.haslayer(TCP) and packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors= "ignore")
            if "HTTP" in payload:
                print(f"\nHTTP")
                print(payload)


    sniff(prn=procces_packet,store=0)