#author kevin liu
#programming assignment 2
from scapy.all import *
import random
import string

src_port = int(sys.argv[1])
dst_port = int(sys.argv[2])


def random_word(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))



#part 1)
for i in range(3000, 3021):
	iplayer = IP(src = '127.0.0.1', dst = '127.0.0.1')
	transportlayer = TCP(sport = src_port, dport = i)
	packet = iplayer/transportlayer
	send(packet)


#part 2)
for i in range(0, 5):
	iplayer = IP(src = '127.0.0.1', dst = '127.0.0.1')
	transportlayer = TCP(sport = src_port, dport = dst_port)
	packet = iplayer/transportlayer/Raw(load=random_word(10))
	send(packet)