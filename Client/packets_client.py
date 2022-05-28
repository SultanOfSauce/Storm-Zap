#These are all the packets needed for the client.

def connectRequest(username: str):
    return """POST / HTTP/1.1\r
myline: connect\r
\r
{username}\r
HELLO I WANT TO CONNECT WITH YOU""".format(username=username)

def messageRequest(username: str, message: str):
    return """POST / HTTP/1.1\r
myline: message to send\r
\r
{username}\r
{message}""".format(username=username, message=message) #clean input