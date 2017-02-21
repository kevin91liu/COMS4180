#author: kevin liu
#COMS 4180 programming assignment 1
#server
#
# Command line arguments:
# -port number on which server will listen for connections
# -mode: either "u" or "t". untrusted and trusted.
# -server key filename (contains both public and private keys)
# -client public key filename (contains only public key)
#

from socket import *
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pickle
import signal
import sys


#====================================================== get command line arguments and validate them

if(len(sys.argv) != 5):
	print "Invalid number of arguments. Invoke the server using: python server.py <port> <mode> <server key filename> <client public key filename>, where <mode> is either u or t, <server key filename> is the name of the file containing the server's private and public RSA keys, <client public key filename> is the name of the file containing the client's public RSA key"

if(not sys.argv[1].isdigit()):
	print 'Port number must contain only digits 0-9'
	exit()
serverPort = int(sys.argv[1])
if(serverPort < 1024 or serverPort > 65535): #65535 is the max valid port number
	print 'Port number must be in the inclusive range [1024, 65535]'
	exit()

mode = sys.argv[2]
if(mode != 't' and mode != 'u'):
	print 'mode must be either u or t'
	exit()

server_key_filename = sys.argv[3]
client_public_key_filename = sys.argv[4]

#====================================================== read keys

try: 
	f = open(server_key_filename, 'rb')
except IOError as e:
	print 'Could not open server key file ' + server_key_filename + ". Got I/O error({0}): {1}".format(e.errno, e.strerror) + '. Perhaps you need to run generate_server_keys.py first to generate server_key.pem?'
	exit()
server_key = RSA.importKey(f.read())
f.close()

try:
	f = open(client_public_key_filename, 'rb')
except IOError as e:
	print 'Could not open client public key file ' + client_public_key_filename + ". Got I/O error({0}): {1}".format(e.errno, e.strerror) + '. Perhaps you need to run generate_client_keys.py first to generate client_public_key.pem?'
	exit()
client_public_key = RSA.importKey(f.read())
f.close()



#====================================================== CTRL+C handler

def signal_handler(signal, frame):
	print('\nYou pressed Ctrl+C! Exiting...')
	listenerSocket.close()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#====================================================== helper function

#removes padding from padded_msg, and returns the unpadded message
def unpad(padded_msg):
	num_padding_bytes = ord(padded_msg[len(padded_msg)-1:])
	return padded_msg[:-num_padding_bytes]



#====================================================== the main code


listenerSocket = socket(AF_INET, SOCK_STREAM)
listenerSocket.bind(("", serverPort))
listenerSocket.listen(1)
#wait until the receiver connects with the sender
#receive back ACKs from the ackSenderTCPSocket
receivingSocket, addr = listenerSocket.accept()
print 'Received incoming connection from ' + addr[0] + ':' + str(addr[1])

received_str = '';

while 1:
    data = receivingSocket.recv(4096)
    if not data: break #this will happen once the client side calls clientSocket.close()
    received_str = received_str + data

unpickled_dict = pickle.loads(received_str)

iv = unpickled_dict['iv']
encrypted_password = unpickled_dict['encrypted_password']
ciphertext = unpickled_dict['ciphertext']
signature = unpickled_dict['signature']


password = server_key.decrypt(encrypted_password)


cipher = AES.new(password, AES.MODE_CBC, iv)
padded_file = cipher.decrypt(ciphertext)

file = unpad(padded_file)

#write the received file to disk
f = open('decryptedfile', 'wb')
f.write(file)
f.close()


#if running in trusted mode, use decryptedfile for verification. if running in untrusted mode, use fakefile for verification
if mode == 't':
	f = open('decryptedfile', 'rb')
else: #then mode must be 'u' since we already validated above that mode is either 't' or 'u'
	f = open('fakefile', 'rb')
file = f.read()
f.close()

#come up with SHA256 hash of the file
hasher = SHA256.new()
hasher.update(file)
file_hash = hasher.digest()


if client_public_key.verify(file_hash, signature):
	print 'Verification Passed'
else:
	print 'Verification Failed'




