#These are all the packets needed for the server.

def connectResponse(username: str):
    return """HTTP/1.1 200 OK\r
myline:connect\r
\r
HELLO {username}\r
NICE TO MEET YOU""".format(username=username)

def messageResponse():
    return """HTTP/1.1 200 OK\r
myline:message to send\r
\r
MESSAGE ACCEPTED FOR DELIVERY"""

def messageBroadcast(username, message):
    return """HTTP/1.1 200 OK\r
myline:message to receive\r
\r
FROM {}:\r
{}""".format(username, message)