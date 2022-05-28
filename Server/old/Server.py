import socket
import threading as t
from aux_funcs_server import *
from packets_server import *

connections = []

def HandleClient(c, addr):
    global connections
    while True:
        try:
            #Receive the whole raw data and decode it in ascii.
            data = c.recv(2048).decode('ascii')
            print("Data received!")

            #If the data is empty, this means that the client disconnected and sent an empty packet.
            if not data:
                print("{}:{} disconnected.".format(addr[0], addr[1]))

                #Whenever a client disconnects, remove it from the list of active connections...
                for conn in connections:
                    if c == conn[0]:
                        connections.remove(conn)
                        break
                #...print the amount of connected people...
                print('{} people connected now.'.format(len(connections)))
                #...and close the thread.
                break

            #We parse the HTTP request
            #Could add try/except
            reqType, headers, content = ParseHTTPRequest(data)
            isCarriage = '\r' in data

            #We parse the requests here.
            if reqType == "POST":

                #If it is a connection request:
                if headers['myline']=='connect':
                    #Send a "successful connection" response to the client
                    connections.append(tuple([c, isCarriage]))
                    username = content[0]
                    print("Connection Request Received from {} ({}:{})".format(username, addr[0], addr[1]))
                    print('{} people connected now.'.format(len(connections)))
                    c.send(connectResponse(username, isCarriage).encode('ascii'))

                elif headers['myline']=='message to send':
                    #If it is a message to send, send a "message received" response to the client and 
                    #broadcast the message.
                    username = content[0]
                    message = content[1]
                    print("Received Message from {}".format(username))
                    print(messageResponse(isCarriage))
                    c.send(messageResponse(isCarriage).encode('ascii'))
                    broadcastMessage(c, message, connections, username)
                else:
                    #Else, send a "Bad Request" response if it is a POST with no good headers.
                    c.send('HTTP/1.1 400 Bad Request'.encode('ascii'))
            else:
                #If it is a GET, or something else, send a "I'm a teapot" response
                c.send('HTTP/1.1 418 I\'m a teapot'.encode('ascii'))
        except:
            c.close()
    c.close()


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
            #addrList.append(c)
            print('Connected to:', addr[0] + ':' + str(addr[1]))
            #print('{} people connected now.'.format(len(addrList)))
            #Create the thread and start it.
            thread = t.Thread(target=HandleClient, args=(c,addr, ))
            thread.start()

    #On KeyboardInterrupt, close the server and don't throw.
    except KeyboardInterrupt:
        print("Server closing...")        
        s.close()
        exit()



if __name__ == '__main__':
    main()