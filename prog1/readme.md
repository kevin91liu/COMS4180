## Synopsis

Documentation for programming assignment #1 of COMS 4180.

## Setup instructions

Starting from a fresh Ubuntu 16.04 VM on GCP:

1. Install pip by running ```sudo apt-get install python-pip```
2. Then install the pycrypto package with ```pip install pycrypto```

Place the following files all in the same directory:
3. server.py
4. client.py
5. generate_server_keys.py
6. generate_client_keys.py

In the terminal, navigate to that directory, and
7. run ```python generate_server_keys.py```. This will generate 2 files in the directory you are in: server_key.pem, which contains the server's private and public RSA keys, and server_public_key.pem, which contains only the server's public RSA key.
8. run ```python generate_client_keys.py```. Does the same thing as in step 5, but for the client instead of the server.

## Invokation

The file that the client sends to the server must reside in the same directory as client.py. 

Port numbers used must be greater than 1024 as an unprivileged user. Something to do with permissioning. 