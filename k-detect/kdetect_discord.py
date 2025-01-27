from scapy.all import sniff
from scapy.layers.inet import IP, TCP
import socket
import time

# Define the Discord webhook hostname
discord_webhook_host = 'discord.com'

# Resolve the Discord webhook hostname to IP addresses
try:
    discord_ips = socket.gethostbyname_ex(discord_webhook_host)[2]
    print(f"\033[92mResolved Discord IP addresses: {discord_ips}\033[0m")
except socket.gaierror:
    discord_ips = []


def packet_callback(packet):
    # Check if the packet has IP and TCP layers
    if packet.haslayer(IP) and packet.haslayer(TCP):
        ip_layer = packet[IP]
        # Check if the destination IP is a known Discord IP address
        if ip_layer.dst in discord_ips and packet[TCP].dport == 443:
            print(f"\033[91m!!! ALERT: Detected network traffic to DiscordWebhook to IP: {ip_layer.dst}")


def start_sniffing(interface='wlp2s0'):
    while True:
        try:
            sniff(iface=interface, filter="tcp port 443", prn=packet_callback, store=0, timeout=60)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)


if __name__ == "__main__":
    # Todo: Automatically detect active network interface
    start_sniffing(interface='wlp2s0')
