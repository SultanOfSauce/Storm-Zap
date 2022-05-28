import socket
from typing import List, Tuple
from packets_server import *

def ObtainPort(defaultport:str="8081"):
    '''
    ObtainPort asks the user for a valid port. It continues to ask until a valid port is given
    '''
    while True:
        serverPort = input("Insert Server Port: [{}] ".format(defaultport))

        if serverPort == "":
            serverPort = defaultport

        print("The server will be open on {}".format(serverPort))
        confirm = input("Is that right?: [Y/n] ")

        if not ((confirm.lower() == 'y') | (confirm == '')):
            print("Try again.\n")
            continue
        
        try:
            retVal = int(serverPort)
            assert retVal <= 65535
            break
        except (ValueError, AssertionError):
            print("Non valid value. Please Try Again.")
    return retVal


def ParseHTTPRequest(data: str):
    '''
    Parse an HTTP request sent from the client. User input Protection/Cleaning could be added.
    '''
    data = data.replace("\r", "")

    lines = data.split('\n')
        
    headerEnd = 0
    body_ok = False
    for i in range(len(lines)):
        if lines[i] == '':
            headerEnd = i
            body_ok=True
            break
    firstline = lines[0]
    requestType = firstline.split(" ")[0]
    if body_ok:
        headers = lines[1:headerEnd]
        content = lines[headerEnd+1:]
    else:
        headers = lines[1:]
        content = []

    headers_dict = {}
    for line in headers:
        key,value = line.split(': ')
        headers_dict[key] = value

    return requestType, headers_dict, content


def broadcastMessage(conn: socket.socket, message: str, a_list, username: str):
    '''
    Small function to send a message to all the people connected to the server, except the client who is sending the message.
    '''
    for c in a_list:
        if c[0] != conn:
            c[0].sendall(messageBroadcast(username, message, c[1]).encode('ascii'))
    return
