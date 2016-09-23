import sys
import cryptography
import hashlib
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

###### Sockets part inserted here to communicate with server ######
#
#
#
###### Receive answer payload from server ######

# Answer payload will be a tuple from the server
# a_payload =
# ans_bytes = a_payload[0]
# ans_hash = a_payload[1]
# a_hash = hashlib.new("md5")
# a_hash.update(ans_bytes)
# a_md_hash = a_hash.hexdigest()
#
# if ans_hash == a_md_hash:
#     answer = fer.decrypt(ans_bytes).decode("utf-8")
#     print(answer)
#
# else:
#     print("Answer data was corrupted")


