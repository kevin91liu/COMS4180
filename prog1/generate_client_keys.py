#creates 2 files: client_key.pem, which contains public and private RSA keys, and client_public_key.pem, which contains only the public RSA key

from Crypto.PublicKey import RSA


client_key = RSA.generate(2048)
f = open('client_key.pem', 'w')
f.write(client_key.exportKey('PEM'))
f.close()

client_public_key = client_key.publickey()
f = open('client_public_key.pem', 'w')
f.write(client_public_key.exportKey('PEM'))
f.close()