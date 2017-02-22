## Synopsis

Documentation for programming assignment #1 of COMS 4180. You can also view this README doc at https://github.com/kevin91liu/COMS4180/tree/master/prog1


## Setup instructions

Starting from a fresh Ubuntu 16.04 VM on GCP:

1. Install pip by running ```sudo apt-get install python-pip```
2. Then install the pycrypto package with ```pip install pycrypto```

Place the following files all in the same directory:

 * server.py
 * client.py
 * generate_server_keys.py
 * generate_client_keys.py

In the terminal, navigate to that directory, and

3. run ```python generate_server_keys.py```. This will generate 2 files in the directory you are in: server_key.pem, which contains the server's private and public RSA keys, and server_public_key.pem, which contains only the server's public RSA key.

4. run ```python generate_client_keys.py```. This will generate 2 files in the directory you are in: client_key.pem, which contains the client's private and public RSA keys, and client_public_key.pem, which contains only the client's public RSA key.


## Invokation

5. start the server by running ```python server.py <port> <mode> <server key filename> <client public key filename>```. The arguments must be given in this order.
   
   * ```port``` values must be in the range [1024, 65535] inclusive. Port numbers under 1024 won't work (will result in an error) because of permissioning -- something to do with being an unprivileged user. 
  
   * ```mode``` must be either ```u``` or ```t```, standing for "untrusted" and "trusted". If running in untrusted mode, then there must be a file named ```fakefile``` in the same directory as server.py
  
   * ```server key filename``` should be a file that contains the server's public and private RSA keys. You can use ```server_key.pem```, generated above, or another file of your choosing as long as it contains a public/private RSA key pair in .PEM format.
   * ```client public key filename``` should be a file that contains the client's public RSA key. You can use ```client_public_key.pem```, generated above, or another file of your choosing as long as it contains a public RSA key in .PEM format.

   Example: ```python server.py 2000 t server_key.pem client_public_key.pem```


6. run the client by running ```python client.py <server ip> <server port> <password> <filename> <client key filename> <server public key filename>```. The arguments must be given in this order.

   * ```server ip``` should be the IPv4 address where server.py (from step 5) is running. If both the server and client are running on the same machine, you can instead use ```localhost```
   * ```server port``` should be the same port value you specified in step 5.
   * ```password``` must be a 16-character alphanumeric string. It will act as the AES block cipher's secret key
   * ```filename``` is the name of the file that the client is encrypting, signing, and sending to the server. It must be in the same directory as client.py.
   * ```client key filename``` should be a file that contains the client's public and private RSA keys. You can use ```client_key.pem```, generated above, or another file of your choosing as long as it contains a public/private RSA key pair in .PEM format
   * ```server public key filename``` should be a file that contains the server's public RSA key. You can use ```server_public_key.pem```, generated above, or another file of your choosing as long as it contains a public RSA key in .PEM format.

   Example: ```python client.py localhost 2000 aaaabbbbccccdddd img.png client_key.pem server_public_key.pem```

#

If you wish to run the server and client on separate machines, you can do that. On the server machine, you would want the following files all in the same directory:
* server.py
* server_key.pem
* client_public_key.pem
* fakefile (needed if you run server in untrusted mode)

On the client machine, you would want all the following files in the same directory:
* client.py
* client_key.pem
* server_public_key.pem
* whatever file the client is sending. For example, img.png


## Additional notes

When you start the server, the server waits for an incoming connection (while it's waiting, you can kill the server by pressing CTRL+C). When you run the client code, the client forms a TCP connection with the server and transmits the ciphertext (padded file, encrypted with AES in CBC mode), the IV, the symmetric private key used to encrypt the file (the private key is encrypted with the server's RSA public key, rather than being sent in the clear), and the signature of the file. When the client finishes transmitting the data, the client closes the socket and exits. On the server side, it accepts the connection and prints that it is receiving a connection from the client's IP:port. The server receives the data, decrypts, and verifies, printing whether verification succeeds or not. The server then exits. Therefore, the server will only ever accept 1 connection during a single run of the server. 

The pycrypto library's ```encrypt()``` and ```decrypt``` functions do not handle padding. Therefore, I implemented padding myself according to PKCS #7. 
