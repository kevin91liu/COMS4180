#author: kevin liu
#COMS 4180 programming assignment 1
#client
#
# Command line arguments:
# -server ip address
# -server port number
# -password: 16 character password, contains alphanumerics, that acts as AES private key
# -filename of the file to sign, encrypt, and send. Must be in the same directory as this executable
# -client key filename (contains both private and public key)
# -server public key filename (contains only public key)
#



from socket import *
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import pickle


import sys
import signal



#======================================================

# #code to handle ctrl+C for exiting
# def signal_handler(signal, frame):
# 	print('\nYou pressed Ctrl+C! Exiting the client.')
# 	clientSocket.close()
# 	#both the listenerThread and commandThread are daemons, so they'll close once the main thread exits.
# 	#no need to .join() the listener and command threads -- in fact .join() would not work on 
# 	#those threads because they have while true loops, and .join() would wait forever for 
# 	#those threads to finish.
# 	sys.exit(0)
# signal.signal(signal.SIGINT, signal_handler)

#======================================================

#pads msg so that len(msg) is a multiple of (AES.blocksize=16). If len(msg) is already a multiple of 16,
#the function will add an entire 16-byte padding block
def pad(msg): 
	return msg + (AES.block_size - len(msg) % AES.block_size) * chr(AES.block_size - len(msg) % AES.block_size)


#======================================================


##**TODO: validate inputs
if(len(sys.argv) != 7):
	print "Invalid number of arguments. Invoke the client using: python client.py <server ip> <server port> <password> <filename> <client key filename> <server public key filename>, where <password> is a 16-character alphanumeric string that will act as the AES block cipher's secret key, <filename> is the name of the file that the client is encrypting, signing, and sending to the server, <client key filename> is the name of the file containing the client's private and public RSA keys, <server public key filename> is the name of the file containing the server's public RSA key"
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
password = sys.argv[3]
filename = sys.argv[4]
client_key_filename = sys.argv[5]
server_public_key_filename = sys.argv[6]





try:
	f = open(filename, 'rb')
except IOError as e:
    print "Trying to open file " + filename + " resulted in I/O error({0}): {1}".format(e.errno, e.strerror)

message = f.read()
f.close()
padded_msg = pad(message) #we must pad the message so that its length is a multiple of AES.block_size

iv = Random.new().read(AES.block_size)
cipher = AES.new(password, AES.MODE_CBC, iv)


ciphertext = cipher.encrypt(padded_msg) #encrypt() does not perform padding, so we need to do the padding ourselves


hasher = SHA256.new()
hasher.update(message)
message_hash = hasher.digest()

#encrypt the hash with client's RSA private key to come up with a signature
f = open(client_key_filename, 'rb')
client_key = RSA.importKey(f.read())
f.close()

signature = client_key.sign(message_hash, '') #according to pycrypto documentation, the second argument doesn't matter (but you're required to pass something)

#encrypt the password with the server's RSA public key
f = open(server_public_key_filename, 'rb')
server_public_key = RSA.importKey(f.read())
f.close()

encrypted_password = server_public_key.encrypt(password, '') #according to pycrypto documentation, the second argument doesn't matter (but you're required to pass something)

##**TODO: send through the socket to the server: IV, ciphertext, AES private key password (encrypted with server's RSA public key), signature of file

#open a socket with the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort)) #open TCP connection to server

#use pickle to store the 4 variables into a structured format, so that the server can unpickle and
#easily tell the 4 variables apart.
pickled_string = pickle.dumps({
	'iv': iv,
	'encrypted_password': encrypted_password, 
	'ciphertext': ciphertext, 
	'signature': signature
	})

clientSocket.send(pickled_string)

clientSocket.close()

