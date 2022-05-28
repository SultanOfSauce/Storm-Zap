#These are all the packets needed for the server.

def connectResponse(username: str, carriage:bool):
    resp = """HTTP/1.1 200 OK\r
myline:connect\r
\r
HELLO {username}\r
NICE TO MEET YOU""".format(username=username)

    if not carriage:
        resp.replace('\r', '')

    return resp

def messageResponse(carriage: bool):
    resp = """HTTP/1.1 200 OK\r
myline:message to send\r
\r
MESSAGE ACCEPTED FOR DELIVERY"""

    if not carriage:
        resp.replace('\r', '')

    return resp

def messageBroadcast(username, message, carriage):
    resp = """HTTP/1.1 200 OK\r
myline:message to receive\r
\r
FROM {}:\r
{}""".format(username, message)

    if not carriage:
        resp.replace('\r', '')

    return resp