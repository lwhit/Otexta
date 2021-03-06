#!/usr/bin/python
import sys
import socket
import pickle
import hashlib

import RPi.GPIO as GPIO
import time

import urllib2
import urllib
import httplib

from xml.etree import ElementTree as etree
from subprocess import call
from cryptography.fernet import Fernet

class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}
 
    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        return xml
 
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext']:
                    if it.tag=='plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics
 
    def search(self, ip):
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        #return result_dics 
        #print result_dics
        if result_dics == {}:
            return "NULL"
        else:
            return result_dics['Result']
        
def QueryFunction( str ):
	appID = '3TKK6V-3GHPAJA8A6'
	query = str
	w = wolfram(appID)
	theResult = w.search(query)
	if theResult == "NULL":
		return "Not a Quantitative Question"
	else:
		return theResult

host = ""
port = 55555
backlog = 5
size = 1024

serverFD = None

print ("Welcome to Otexta\n")

# Creating server-side socket
serverFD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverFD.bind((host, port))
serverFD.listen(backlog)

# Initalize RPi GPIO
# pin 21 = blue, pin 20 = green, pin 16 = red
GPIO.setmode( GPIO.BCM )
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.output(16, True)
GPIO.output(20, False)
GPIO.output(21, False)

while True:
	print("Awaiting Connection")

	# Begin accepting communications from clients
	clientFD, address = serverFD.accept()
	print("Connection: ", address)

	# Receive client payload
	c_ByteStream = clientFD.recv(size)

	if c_ByteStream:
		# Unpickle payload
		c_payload = pickle.loads(c_ByteStream)
		
		key, question, checksum, s_addr = c_payload
		
		# Check md5 hash
		if hashlib.md5(question).hexdigest() != checksum:
			clientFD.close()

		# Decrypt message
		f = Fernet(key)
		f.decrypt(question)
		
		# Receive payload question and deconstruct
		GPIO.output(20, GPIO.HIGH)
		time.sleep(3)

		# Send question to Wolfram API
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(16, GPIO.LOW)
		time.sleep(3)

		answer = QueryFunction(question)

		# Receive answer payload
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(20, GPIO.LOW)
		time.sleep(3)
		
		# Encrypt answer message
		answer = f.encrypt()
		
		# Create answer payload
		s_payload = (answer, hashlib.md5(answer).hexdigest())
		pickle_payload = dumps(s_payload)
		
		# Send answer payload back to client
		GPIO.output(20, GPIO.HIGH)
		time.sleep(3)
		clientFD.send(pickle_payload)
	
	clientFD.close()
	GPIO.cleanup()

serverFD.close()
