#!/usr/bin/env python

#******************************************************************************
#
#  CS 6421 - Simple Conversation
#  implement convertion between bananas and inches of bananas
#  Execution:    python client.py proxy_host proxy_port
#
#******************************************************************************

import socket
import sys
DISCOV_IP = '127.0.0.1'
DISCOV_PORT = 5555
BUFFER_SIZE = 1024

## Function to send msg to discover server
def send_to_proxy(commond, host, port): 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))   #get connetion
        m = commond + '\n'
        sock.send(m.encode('UTF-8'))
        greeting = sock.recv(BUFFER_SIZE)
        converted = sock.recv(BUFFER_SIZE)
        if not converted:
            return greeting.splitlines()[1]
        return converted
        sock.close()
    except socket.error, arg:
        sock.close()   #close socket
        return 'operations failed. More info:', arg
    

### Main code run when program is started
BUFFER_SIZE = 1024
interface = ""

# if input arguments are wrong, print out usage
if len(sys.argv) != 3:
    print >> sys.stderr, "usage: python {0} proxy_host proxy_port\n".format(sys.argv[0])
    sys.exit(1)

proxy_host = sys.argv[1]
proxy_port = int(sys.argv[2])

exit_flag = False
try:
    print("Started client.")
    while not exit_flag:
        print ("input your commond. info: unit_a unit_b amount")
        commond = raw_input()
        print ('Accepted commond :' + commond)
        msg = send_to_proxy(commond, proxy_host, proxy_port)
        m = msg.decode('UTF-8')
        if "Failed" in m:
            print ("Failed to process request from client. Info: "+ m)
        else:
            print("Proxy request returning: %s" % m)
        print ("continue.")
except KeyboardInterrupt:
    exit_flag = True

print("Exiting...")
sys.exit(0)
