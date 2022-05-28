def ObtainConnectionInfo(defaultserver:str="localhost", defaultport:str="8081"):
    '''
    ObtainConnectionInfo asks the user for a valid port and Ip address. It continues to ask until a valid port is given
    '''
    while True:
        serverName = input("Insert Server Name: [{}] ".format(defaultserver) )
        serverPort = input("Insert Server Port: [{}] ".format(defaultport))

        if serverName == "":
            serverName = defaultserver

        if serverPort == "":
            serverPort = defaultport

        print("A connection will be done on {}:{}".format(serverName, serverPort))
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
    return serverName, serverPort

def ChooseUsername():
    '''
    ChooseUsername asks the user for a Username. It continues to ask until a non-empty username is given.
    '''
    while True:
        username = input("Insert Username: ")
        
        if username == "":
            print("Username can't be empty. Try Again.")
            continue

        print("You username will be \"{}\".".format(username))
        confirm = input("Is that right? [Y/n]:")

        if (confirm.lower() == 'y') | (confirm == ''):
            break
        else:
            print("Try again.\n")
    return username


def ParseHTTPResponse(data: str):
    '''
    Parse an HTTP request sent from the client. User input Protection/Cleaning could be added.
    '''
    data = data.replace('\r', '')

    lines = data.splitlines()

    
    headerEnd = 0
    for i in range(len(lines)):
        if lines[i] == '':
            headerEnd = i
            break
    try:
        response = lines[0].split(' ')[1]
    except:
        response = lines
    headers = lines[1:headerEnd]
    content = lines[headerEnd+1:]

    headers_dict = {}
    for line in headers:
        key,value = line.split(':')#split each line by http field name and value
        headers_dict[key] = value

    return response, headers_dict, content

