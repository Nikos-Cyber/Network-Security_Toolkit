from mac_vendor_lookup import MacLookup , VendorNotFoundError
import subprocess
import re


def vendor():
    lookup = MacLookup()
    lookup.update_vendors()
    def is_random_mac(mac):
        first_byte = int(mac.split("-")[0], 16)
        return (first_byte & 0b00000010) != 0
    mac_finder = subprocess.check_output("arp -a", shell = True , text=True)
    macs = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})\s+dynamic"
    star = "*"
    for ip , mac in re.findall(macs,mac_finder):

        if is_random_mac(mac):
            Vendor = "Random\Private Mac"
        else:
            try:
                Vendor = lookup.lookup(mac)
            except VendorNotFoundError:
                Vendor = "Unknown"

    print(f"{star * 20}\nTYPE : IP :{ip}\nTYPE : MAC : {mac}\nTYPE : VENDOR : {Vendor}\n{star * 20}")


