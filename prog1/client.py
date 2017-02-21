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






#====================================================== get command line arguments and validate them


if(len(sys.argv) != 7):
	print "Invalid number of arguments. Invoke the client using: python client.py <server ip> <server port> <password> <filename> <client key filename> <server public key filename>, where <password> is a 16-character alphanumeric string that will act as the AES block cipher's secret key, <filename> is the name of the file that the client is encrypting, signing, and sending to the server, <client key filename> is the name of the file containing the client's private and public RSA keys, <server public key filename> is the name of the file containing the server's public RSA key"
serverIP = sys.argv[1]

if(not sys.argv[2].isdigit()):
	print 'Port number must contain only digits 0-9'
	exit()
serverPort = int(sys.argv[2])
if(serverPort < 1024 or serverPort > 65535): #65535 is the max valid port number
	print 'Port number must be in the inclusive range [1024, 65535]'
	exit()

password = sys.argv[3]
#password must be 16 characters. the specs say that the TA won't try any special chars and will stick to alphanumerics, but i will allow for special chars
if(len(password) != 16):
	print 'password must be exactly 16 characters long'
	exit()


filename = sys.argv[4]
client_key_filename = sys.argv[5]
server_public_key_filename = sys.argv[6]

#read in the file to be sent
try:
	f = open(filename, 'rb')
except IOError as e:
    print "Trying to open file " + filename + " resulted in I/O error({0}): {1}".format(e.errno, e.strerror)
    exit()
file = f.read()
f.close()

#read in client public and private RSA key
try: 
	f = open(client_key_filename, 'rb')
except IOError as e:
	print 'Could not open client key file ' + client_key_filename + ". Got I/O error({0}): {1}".format(e.errno, e.strerror) + '. Perhaps you need to run generate_client_keys.py first to generate client_key.pem?'
	exit()
client_key = RSA.importKey(f.read())
f.close()

#read in server public RSA key
try:
	f = open(server_public_key_filename, 'rb')
except IOError as e:
	print 'Could not open server public key file ' + server_public_key_filename + ". Got I/O error({0}): {1}".format(e.errno, e.strerror) + '. Perhaps you need to run generate_server_keys.py first to generate server_public_key.pem?'
	exit()
server_public_key = RSA.importKey(f.read())
f.close()




#====================================================== helper function

#pads msg so that len(msg) is a multiple of (AES.blocksize=16). If len(msg) is already a multiple of 16,
#the function will add an entire 16-byte padding block
def pad(msg): 
	return msg + (AES.block_size - len(msg) % AES.block_size) * chr(AES.block_size - len(msg) % AES.block_size)

#======================================================



padded_file = pad(file) #we must pad the message so that its length is a multiple of AES.block_size


iv = Random.new().read(AES.block_size)
cipher = AES.new(password, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(padded_file) #encrypt() does not perform padding, so we needed to do the padding ourselves


hasher = SHA256.new()
hasher.update(file)
file_hash = hasher.digest()

#encrypt the hash with client's RSA private key to come up with a signature
signature = client_key.sign(file_hash, '') #according to pycrypto documentation, the second argument doesn't matter (but you're required to pass something)


#encrypt the password with the server's RSA public key
encrypted_password = server_public_key.encrypt(password, '') #according to pycrypto documentation, the second argument doesn't matter (but you're required to pass something)



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

