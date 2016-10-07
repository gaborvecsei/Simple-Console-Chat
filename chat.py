import thread
import time
import socket
import sys

def receiveMsgServer(socketConnection):
	while True:
		receivedMsg = socketConnection.recv(128)
		receivedString = receivedMsg.decode('utf-8')
		if receivedString == "quit":
			socketConnection.close()
			sys.exit(0)
		print"Received Message: {0}".format(receivedString)

def sendMsgServer(sc):
	while True:
		keyboardInput = raw_input("")
		messageToSend = keyboardInput.encode('utf-8')
		sc.send(messageToSend)
		print "Message sent!"

def receiveMsgClient(socket):
	while True:
		receivedMsg = socket.recv(128)
		receivedString = receivedMsg.decode('utf-8')
		if receivedString == "quit":
			socket.close()
			sys.exit(0)
		print"Received Message: {0}".format(receivedString)

def sendMsgClient(socket):
	while True:
		keyboardInput = raw_input()
		messageToSend = keyboardInput.encode('utf-8')
		socket.send(messageToSend)
		print "Message sent!"

hostOrClient = raw_input("Are you the host or the client (host/client): ")

ipAddr = raw_input("IP: ")
portt = raw_input("Port: ")

if hostOrClient == "host":
	socket = socket.socket()
	socket.bind((ipAddr, eval(portt)))
	socket.listen(1)
	
	print("Connection Waiting...")
	socket_connection, addr = socket.accept()
	print addr
	print("Connection Matched!")
	
	try:
		thread.start_new_thread(receiveMsgServer, (socket_connection, ))
	except:
		print "Unable to start receive thread"
	
	try:
		thread.start_new_thread(sendMsgServer, (socket_connection, ))
	except:
		print "Unable to start send thread"
elif hostOrClient == "client":
	socket = socket.socket()
	print("Connecting to server...")
	while True:
		try:
			socket.connect((ipAddr, eval(portt)))
			break
		except:
			print("Retrying connection to server...")
			time.sleep(1)
	print("Connection Matched!")

	try:
		thread.start_new_thread(receiveMsgClient, (socket, ))
	except:
		print "Unable to start receive thread"

	try:
		thread.start_new_thread(sendMsgClient, (socket, ))
	except:
		print "Unable to start send thread"


while True:
	time.sleep(1)