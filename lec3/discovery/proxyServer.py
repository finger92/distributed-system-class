#!/usr/bin/env python

#  CS 6421 - Python-based proxy conversion server. 
#  Queries a specified discovery server to query for a conversion path.
#
#  Execution:    python proxy_conv_server.py portnum discovery-host discovery-port
#


import sys, socket
import traceback

BUFFER_SIZE = 1024
    
# Issue a request to a conversion server and return the result
def proxy_request(src_unit, dst_unit, amount, host, port):
    msg = '%s %s %s\n' % (src_unit, dst_unit, amount)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.sendall(msg.encode('UTF-8'))
    except Exception as e:
        # if a server crashed without sending removing operation 
        # then proxy server send it to discovery server
        if "Connection refused" in e:
            s.connect((discovery_host, int(discovery_port)))
            msg = "remove " + host + " " + port + "\n" 
            s.sendall(msg.encode('UTF-8'))
            s.recv(BUFFER_SIZE)
            return "Failed, one of the convertion server was crashed, please try it later."
    greeting = s.recv(BUFFER_SIZE)
    converted = s.recv(BUFFER_SIZE)
    print greeting, converted
    try:
        # handle an unknown bug happend in the every first query
        if not converted:
            value = float(greeting.splitlines()[1])
        else:
            value = float(converted.decode('UTF-8'))
        print("Proxy request returning %s" % value)
    except:
        return "Result converted failed, please check the convertion server or try it again.\n"
    return value

# Issue a path request to a discovery server and return the result
def discovery_path_request(src_unit, dst_unit, host, port):
    msg = 'path %s %s\n' % (src_unit, dst_unit)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(msg.encode('UTF-8'))
    greeting = s.recv(BUFFER_SIZE)
    msg = s.recv(BUFFER_SIZE).decode('UTF-8')
    print("Path request returning: %s" % (msg))
    if not msg:
        # handle a strange bug
        return greeting.splitlines()[1]
    return msg



def process(conn, next):
    greeting = "Welcome, you are connected to a Python-based proxy unit conversion server\n"
    conn.send(greeting.encode('UTF-8'))
    userInput = conn.recv(BUFFER_SIZE).decode('UTF-8')
    if not userInput:
        print("Error reading message")
        return

    print("Received message: %s" % (userInput))
    tokens = userInput.split()
    if len(tokens)!=3:
        err = "Need to input three arguements\n"
        conn.send(err.encode('UTF-8'))
        return 
    input_unit,output_unit,amount = tokens
    c = float(amount)

    path = discovery_path_request(input_unit, output_unit, discovery_host, discovery_port)

    P = path.lower().splitlines()

    if P[0].startswith('failure'):
        msg = "Failed, discovery server returned: " + path + "\n"
        conn.send(msg.encode('UTF-8'))
        return 
    else:
        # Parse the path response
        # Format is "Query ft m to server at localhost 5570"
        for i in P:
            s,d,host,port = (i.split()[j] for j in [1, 2, 6, 7])
            print ('Query %s %s %s to server at %s %s.' % (s, d, c, host, port))
            c = proxy_request(s, d, c, host, port)

    conn.send(("%s\n" % c).encode('UTF-8'))


if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.stderr.write("usage: python {0} port discovery-host discovery-port\n".format(sys.argv[0]))
        sys.exit(1)

    server_port = int(sys.argv[1])
    discovery_host = sys.argv[2]
    discovery_port = sys.argv[3]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", server_port))
    s.listen(5)
    exit_flag = False
    try:
        print ("Proxy server listening on port %s" % (server_port))
        while not exit_flag:
            conn, addr = s.accept()
            print ('Accepted connection from client %s' % str(addr))
            try:
                process(conn, next)
            except:
                traceback.print_exc(file=sys.stdout)
                print ('Failed to process request from client. Continuing.')

            conn.close()
    except KeyboardInterrupt:
        exit_flag = True

    print("Exiting...")
    s.close()
    sys.exit(0)