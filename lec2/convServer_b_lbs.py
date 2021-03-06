#!/usr/bin/env python

#******************************************************************************
#
#  CS 6421 - Simple Conversation
#  implement convertion between bananas and pounds of bananas
#  Execution:    python convServer_1.py portnum
#
#******************************************************************************

import socket
import sys

## Function to process requests
def process(conn):
    conn.send("Welcome to the Bananas (b) to Pounds (lbs) conversion server!\n")

    # read userInput from client
    userInput = conn.recv(BUFFER_SIZE)
    if not userInput:
        print "Error reading message"
        sys.exit(1)

    print "Received message: ", userInput
    # TODO: add convertion function here, reply = func(userInput)
    mylist = userInput.split(" ")
    # excption handler
    if len(mylist) != 3:
        conn.send('pls input 3 arguements. Usage: eg. b lbs 2 or lbs b 2\n')
    elif mylist[0] == mylist[1] or mylist[0] != 'b' and mylist[0] != 'lbs' or mylist[1] != 'b' and mylist[1] != 'lbs':
        conn.send('Wrong input. Usage: eg. b lbs 2 or lbs b 2\n');
    else:
        # send convertion result
        if mylist[0] == 'b':
            conn.send(str(float(mylist[2]) * 0.2646)+'\n');
        elif mylist[0] == 'lbs':
            conn.send(str(float(mylist[2]) / 0.2646)+'\n');
    conn.close()    


### Main code run when program is started
BUFFER_SIZE = 1024
interface = ""

# if input arguments are wrong, print out usage
if len(sys.argv) != 2:
    print >> sys.stderr, "usage: python {0} portnum\n".format(sys.argv[0])
    sys.exit(1)

portnum = int(sys.argv[1])

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((interface, portnum))
s.listen(5)

while True:
    # accept connection and print out info of client
    conn, addr = s.accept()
    print 'Accepted connection from client', addr
    process(conn)
s.close()
