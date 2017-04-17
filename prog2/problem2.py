#author kevin liu
#programming assignment 2

import sys
from scapy.all import *


f = open('inpartb.txt', 'rb')

src_ip = f.readline()[:-1] #[:-1] removes the last character, which is a newline \n
dst_ip = f.readline()[:-1]
src_port = int(f.readline()[:-1])
dst_port = int(f.readline()[:-1])
body = f.readline()[:-1]

iplayer = IP(src = src_ip, dst = dst_ip)
transportlayer = TCP(sport = src_port, dport = dst_port)
packet = iplayer/transportlayer/Raw(load=body)

packet.show()
print str(packet)

send(packet)