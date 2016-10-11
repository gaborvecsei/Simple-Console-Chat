"""
*****************************************************
*
*              Gabor Vecsei
* Email:       vecseigabor.x@gmail.com
* Blog:        https://gaborvecsei.wordpress.com/
* LinkedIn:    www.linkedin.com/in/vecsei-gabor
* Github:      https://github.com/gaborvecsei
*
* Simple chat program which runs in the console
*****************************************************
"""

import threading
import time
import socket
import sys

class Server():

	def __init__(self, ipAddr, port):
		self.ipAddr = ipAddr
		self.port = port
		self.socket = None
		self.socketConnection = None
		self.connectionAddress = None

	def createConnection(self):
		self.socket = socket.socket()
		self.socket.bind((self.ipAddr, self.port))
		self.socket.listen(1)
		print "[*] Waiting for connection..."
		try:
			self.socketConnection, self.connectionAddress = self.socket.accept()
			print "[*] Connection created!"
			return True
		except socket.error as e:
			print "[*] Could not connect!"
			print e
			self.socket.close()
			return False

	def sendMsg(self):
		while True:
			keyboardInput = raw_input("")
			messageToSend = keyboardInput.encode('utf-8')
			try:
				self.socketConnection.send(messageToSend)
				print "Message sent: {0}".format(messageToSend)
			except socket.error as e:
				print "[*] Couldn't send the message!"
				print e

	def receiveMsg(self):
		while True:
			receivedMsg = self.socketConnection.recv(128)
			receivedString = receivedMsg.decode('utf-8')
			print"Received Message: {0}".format(receivedString)

	def runServer(self):
		sendThread = threading.Thread(target=self.sendMsg)
		receiveThread = threading.Thread(target=self.receiveMsg)

		sendThread.start()
		receiveThread.start()

		sendThread.join()
		receiveThread.join()

	def closeConnection(self):
		self.socketConnection.close()
		self.socket.close()
		self.connectionAddress = None



class Client():

	def __init__(self, ipAddr, port, maxConnectionTries = 5):
		self.ipAddr = ipAddr
		self.port = port
		self.socket = None
		self.maxConnectionTries = maxConnectionTries

	def createConnection(self):
		self.socket = socket.socket()
		print "Connection to the server"
		tries = 0
		while True:
			try:
				self.socket.connect((self.ipAddr, self.port))
				break
			except socket.error as e:
				print "[*] Retrying connection... " + str(tries)
				tries += 1
				if tries > self.maxConnectionTries:
					self.socket.close()
					return False
				time.sleep(1)
		print "[*] Connection matched!"
		return True


	def sendMsg(self):
		while True:
			keyboardInput = raw_input()
			messageToSend = keyboardInput.encode('utf-8')
			try:
				self.socket.send(messageToSend)
				print "Message sent: {0}".format(messageToSend)
			except socket.error as e:
				print "[*] Couldn't send the message!"
				print e

	def receiveMsg(self):
		while True:
			receivedMsg = self.socket.recv(128)
			receivedString = receivedMsg.decode('utf-8')
			print"Received Message: {0}".format(receivedString)

	def runClient(self):
		sendThread = threading.Thread(target=self.sendMsg)
		receiveThread = threading.Thread(target=self.receiveMsg)

		sendThread.start()
		receiveThread.start()

		sendThread.join()
		receiveThread.join()

	def closeConnection(self):
		self.socket.close()

def main():
	ipAddr = "localhost"
	port = 1200

	serverOrClient = raw_input("Server or client (server/client): ")
	if serverOrClient == "server":
		server = Server(ipAddr, port)
		isConnected = server.createConnection()
		if isConnected:
			server.runServer()
		else:
			print "Connection timed out"
			sys.exit(1)
	elif serverOrClient == "client":
		client = Client(ipAddr, port)
		isConnected = client.createConnection()
		if isConnected:
			client.runClient()
		else:
			print "Connection timed out"
			sys.exit(1)
	elif serverOrClient == "exit":
		sys.exit(0)
	else:
		main()

	while True:
		time.sleep(1)


if __name__ == "__main__":
	main()