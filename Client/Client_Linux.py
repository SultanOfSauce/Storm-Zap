from platform import system
import socket as s
import sys
import select

from aux_funcs_client import *
from packets_client import *

#The program first checks if the OS is the right one.
if (system() != "Linux") & (system() != "Darwin"):
	print("You have accidentally used the UNIX Client on a non-Linux platform.")
	print("Closing...")
	exit()

#The user chooses the IP, port and Username
serverName, serverPort = ObtainConnectionInfo()
username = ChooseUsername()

#The program tries to connect...
clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
clientSocket.connect((serverName,int(serverPort)))

#...and sends a connection request.
clientSocket.sendall(connectRequest(username).encode('ascii'))
resp = clientSocket.recv(2048).decode('ascii')
code, _, _  = ParseHTTPResponse(resp)
if code != "200":
	print("Something went wrong with your connection attempt.")
	exit()
else:
	print("Connected.")

#Here a socket list is created to be used with select.
sockets_list = [sys.stdin, clientSocket]

while True:

	try:
		#Select lets us get input from both the socket and stdin from UNIX OSes.
		read_sockets, _, _ = select.select(sockets_list, [], [])

		for socks in read_sockets:
			#If we receive a response packet from the server, parse it and display if needed.
			if socks == clientSocket:
				response = clientSocket.recv(2048)
				code, headers, content = ParseHTTPResponse(response.decode('ascii'))
				if code != '200':
					print("Something went wrong with your message.")
				elif headers['myline'] == "message to send":
					continue
				elif headers['myline'] == "message to receive":
					print('From:', content[0].removeprefix('FROM: '))
					print(content[1])

			#Else, send the message in stdin. If the message is "%exit", get out.	
			else:
				message = sys.stdin.readline().removesuffix('\n')
				#print("Messaggio:",message)
				if message == "%exit":
					print("Closing...")
					clientSocket.close()
					exit()
				clientSocket.send(messageRequest(username, message).encode('ascii'))
				sys.stdout.flush()

	#We can also get out with a KeyboardInterrupt in a more "elegant" way (not that much actually...)
	except KeyboardInterrupt:
		clientSocket.close()
		exit()

