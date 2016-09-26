import sys
import cryptography
import hashlib
import socket
import pickle
#import time

from cryptography.fernet import Fernet

# Getting values from the arguments
question = sys.argv[1]
serv_addr = sys.argv[2]

# Generating the Fernet key
key = Fernet.generate_key()
fer = Fernet(key)

# Encrypting the question string for the payload
# Encrytpion can only be done on byte arrays so
# the string is converted to a byte array first
token = fer.encrypt(str.encode(question))

# Decryption results in a byte array which is then
# converted to a string for printing out
#print(fer.decrypt(token).decode("utf-8"))

# Getting the MD5 hash of the question to be used
# to make sure it sends correctly to the server
q_hash = hashlib.new("md5")
q_hash.update(str.encode(question))
q_md_hash = q_hash.hexdigest()

# Creating the payload to be sent to the server
q_payload = (key, token, q_md_hash, serv_addr)

host = ''
port = 50000
size = 1024
s = None

def openClient():
    global host
    host = '192.168.0.112'
    global port
    port = 50000
    global size
    size = 1024
    global s
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #use AF_INET so we can connect to a client on another machine
                                                             #SOCK_STREAM - Use TCP/IP transmission protocol for
                                                               #reliability
        s.connect((host, port)) #connect to remote address given by (host, port) Tuple
    except socket.error(value, message): #If we have an issue connecting to the remote socket..
        if s:
            s.close() #socket is closed
        print('Could not open socket: ' + str(message))
        sys.exit(1)
    print('--')

openClient()

messageToSend = q_payload  #Question payload, Tuple

#s.send(str.encode(messageToSend)) #send byte data to server
s.send(pickle.dumps(messageToSend))

data = s.recv(size) #receive byte data from server
#print('Received: ', str(data,encoding='utf-8', errors='strict'))
print('Received: ', str(pickle.loads(data)))

s.close()

a_payload = data
ans_bytes = a_payload[0]
ans_hash = a_payload[1]
a_hash = hashlib.new("md5")
a_hash.update(ans_bytes)
a_md_hash = a_hash.hexdigest()

if ans_hash == a_md_hash:
     answer = fer.decrypt(ans_bytes).decode("utf-8")
     print(answer)

else:
    print("Answer data was corrupted")


