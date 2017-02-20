#author: kevin liu
#COMS 4180 programming assignment 1
#client
#
# Command line arguments:
# -server ip address
# -server port number
# -password: 16 character password, contains alphanumerics
# -filename of the file to sign, encrypt, and send
# -necessary RSA key components (filenames containing RSA data)
#



from socket import *
import sys
import signal
import threading
import time
import datetime

#======================================================

#code to handle ctrl+C for exiting
def signal_handler(signal, frame):
	print('\nYou pressed Ctrl+C! Exiting the client.')
	clientSocket.close()
	#both the listenerThread and commandThread are daemons, so they'll close once the main thread exits.
	#no need to .join() the listener and command threads -- in fact .join() would not work on 
	#those threads because they have while true loops, and .join() would wait forever for 
	#those threads to finish.
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#======================================================



#======================================================


if(len(sys.argv) < 3):
	print "You must specify the IP address and port of the server. Invoke the client using: python client.py <ip> <port>"
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])



