from platform import system
import socket as s
import sys
import threading

from aux_funcs_client import *
from packets_client import *

#The user chooses the IP, port and Username
serverName, serverPort = ObtainConnectionInfo()
username = ChooseUsername()

#The program tries to connect...
clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
clientSocket.connect((serverName,int(serverPort)))

#...and sends a connection request.
clientSocket.sendall(connectRequest(username).encode('ascii'))
resp = clientSocket.recv(4096).decode('ascii')
code, _, _  = ParseHTTPResponse(resp)
if code != "200":
	print("Something went wrong with your connection attempt.")
	exit()
else:
	print("Successfully connected.")

#Here we create both handlers for stdin and the responses to be used with multithreading.

#If we receive a response packet from the server, parse it and display if needed.
def handle_messages():
	try:
		while 1:
			response = clientSocket.recv(4096).decode('ascii')

			if response == '':
				exit()

			code, headers, content = ParseHTTPResponse(response)
			if code != '200':
				print("Something went wrong with your message.")
			elif headers['myline'] == "message to send":
				continue
			elif headers['myline'] == "message to receive":
				print('From', content[0].removeprefix('FROM ') + ' ' + content[1])
	except ConnectionAbortedError:
		exit()


#Start the thread for handling the socket
receivingThread = threading.Thread(target=handle_messages)
receivingThread.start()

#Else, send the message in stdin. If the message is "%exit", get out.
def handle_input():

	try:
		while 1:
			message = input()

			if message == "%exit":
				print("Closing...")
				return
			if message == '':
				continue

			clientSocket.send(messageRequest(username, message).encode('ascii'))
			sys.stdout.flush()
	#Unicodeencodeerror
	except KeyboardInterrupt:
		print("Closing...")
		return

#Start the funcion to handle the input.
handle_input()

#When out of handle_input, close the connection and exit.
clientSocket.close()
print("Connection Closed.")
exit()

