#creates 2 files: server_key.pem, which contains public and private RSA keys, and server_public_key.pem, which contains only the public RSA key

from Crypto.PublicKey import RSA

server_key = RSA.generate(2048)
f = open('server_key.pem', 'w')
f.write(server_key.exportKey('PEM'))
f.close()

server_public_key = server_key.publickey()
f = open('server_public_key.pem', 'w')
f.write(server_public_key.exportKey('PEM'))
f.close()