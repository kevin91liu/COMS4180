#author: kevin liu
#COMS 4180 programming assignment 1
#server
#
# Command line arguments:
# -port number on which server will listen for connections
# -mode: either "u" or "t". untrusted and trusted.
# -filenames with RSA stuff
#

from socket import *
import sys
import os
import signal
import threading
import time
import datetime
import Queue


if(len(sys.argv) < 2):
	print "You must specify a port number to use. Invoke the server using: python server.py <port>"
serverPort = int(sys.argv[1])



#======================================================
#===CTRL+C handler===

def signal_handler(signal, frame):
	print('You pressed Ctrl+C! Closing the server.')
	for username in dict_Users:
		if(dict_Users[username].connectionSocket != None):
			dict_Users[username].connectionSocket.send("Server is closing. Goodbye.")
			dict_Users[username].connectionSocket.close()
	#all threads are daemons, so we don't need to join() them. they'll close once the 
	#main thread exits. in fact, .join() wouldn't work since the threads have while true
	#loops, so .join() would wait forever for them to finish
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)







	

