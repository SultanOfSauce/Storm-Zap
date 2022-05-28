import socket
import threading as t
from aux_funcs_server import *
from packets_server import *

addrList = []

def HandleClient(c, addr):
    while True:
        try:
            #Receive the whole raw data and decode it in ascii.
            data = c.recv(2048).decode('ascii')

            #If the data is empty, this means that the client disconnected and sent an empty packet.
            if not data:
                print("{}:{} disconnected.".format(addr[0], addr[1]))

                #Whenever a client disconnects, remove it from the list of active connections...
                addrList.remove(c)
                #...print the amount of connected people...
                print('{} people connected now.'.format(len(addrList)))
                #...and close the thread.
                c.close()
                return

            '''
            carriage tries to send data according to the data that the client sent.
            if there was a carriage return in the data received, the data is sent
            with a carriage return, and viceversa.
            This is NOT true for broadcasted messages, where the burden of "translating"
            is left to the client.
            '''
            carriage = '\r' in data

            #We parse the HTTP request
            #Could add try/except
            reqType, headers, content = ParseHTTPRequest(data)

            #We parse the requests here.
            if reqType == "POST":

                #If it is a connection request:
                if headers['myline']=='connect':
                    #Send a "successful connection" response to the client
                    username = content[0]
                    print("Connection Request Received from {} ({}:{})".format(username, addr[0], addr[1]))
                    c.send(connectResponse(username, carriage).encode('ascii'))

                elif headers['myline']=='message to send':
                    #If it is a message to send, send a "message received" response to the client and 
                    #broadcast the message.
                    username = content[0]
                    message = content[1]
                    print("Received Message from {}".format(username))
                    c.send(messageResponse(carriage).encode('ascii'))
                    broadcastMessage(c, message, addrList, username)
                else:
                    #Else, send a "Bad Request" response if it is a POST with no good headers.
                    c.send('HTTP/1.1 400 Bad Request'.encode('ascii'))
            else:
                #If it is a GET, or something else, send a "I'm a teapot" response
                c.send('HTTP/1.1 418 I\'m a teapot'.encode('ascii'))
        except ConnectionResetError:
            print("{}:{} disconnected.".format(addr[0], addr[1]))

            #Whenever a client disconnects, remove it from the list of active connections...
            addrList.remove(c)
            #...print the amount of connected people...
            print('{} people connected now.'.format(len(addrList)))
            #...and close the thread.
            c.close()
            return
        except KeyboardInterrupt:
            c.close()
            return


def main():
    #Get from the User the Listening Port
    port = ObtainPort("8081")

    #Let's open the socket for a TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #And bind it to the right port
    s.bind(("", port))
    print("Socket bound to port:", port)

    #How many people do we want to listen to the same time?
    listenN = 5
    s.listen(listenN)
    print("Socket is listening ({} people max)".format(listenN))


    try:
        while True:
            '''
            The server always listens for new clients. Whenever a new client connects, 
            a new Thread is started to handle a single client.
            '''
            #Connection is accepted
            c, addr = s.accept()
            #and the connection added to the list of all the open connections
            addrList.append(c)
            print('Connected to:', addr[0] + ':' + str(addr[1]))
            print('{} people connected now.'.format(len(addrList)))
            #Create the thread and start it.
            thread = t.Thread(target=HandleClient, args=(c,addr, ))
            thread.start()
    #On KeyboardInterrupt, close the server and don't throw.
    except KeyboardInterrupt:
        print("Server closing...")  
        for c in addrList:
            c.close()      
        s.close()

    


if __name__ == '__main__':
    main()