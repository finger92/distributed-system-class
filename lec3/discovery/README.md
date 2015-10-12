# Execute
`Notice:`</br>
```
Discovery Server should always start before Conversion servers and proxy server. 
Number of ports should be different.
```

`Discovery Server:`  </br>
```
python discovery.py 5555(Must be this port number). 
```
`Proxy Server:`  </br>
```
python proxyServer.py portnum discovery-host discovery-port
```
`Conversion Server:`: </br>
```
python convServerName.py portnum
```

`For example:`</br>
```
python discovery.py 5555
python proxyServer.py 5556 127.0.0.1 5555
python convServer_b_in.py 5557
python ConvServer_b_lbs.py 5558
```

# Policies For Load Balancing
As to implement load balancing, to reduce the mistakes resulted from crash of servers, there will be multiple conversion servers for each type of conversion. For example, there maybe three conversion servers working for the conversion between banana and inch. Thus if two of them stop working, the system can still give users the result. 
This system uses the strategy of `"Round Robin"`, information of available conversion servers for a certain type of conversion are stored in an array or a dictionary. </br></br>
When there is a request to use a type of conversion server, if it's the first time to ask for conversion between these two units, the system will choose the first server in the array to finish the work. </br></br>
When following requests comes, the system will choose the next server after the last used server in the array. If the last used server is in the end of the array, the system will select the first one in the array. 

  
# Policies For Fault Tolerant

## Case 1: Conversion servers crash: For example conv_a

>### conv_a restart at the same address:
>>When conv_b recieve 'failure entry exists.' in adding operation, it indicate that a former conversion server opened 
on the same ip address and port was crashed without sending removing operation, so it just remove the former info in
tables in discovery server and add new info.

>### conv_b restart at the same address:
>>This situation is similar to the one above.
	
>### conv_a restart at a different address:
>>When proxyServer recieve 'connection refuse' info from a convertion server, this indicate that this convertion server
may be crashed without sending removing msg. So proxyServer will send removing msg to discovery server.


## Case 2: Discovery server crash:
```
Fault tolerant mainly works when the discovery server restarts after crashing.
```

>### There is no operation before the restart:
>>When discovery server recieved a adding operation, it will write this operation to discovFile. When it recieved removing 
operation, it will delete the related adding information in discovFile. When discovery server crashed and restart, it will
read the information in discovFile and readd those information to the server.

>### There are some adding and removing during this period:
>>The adding operation will fail, and the new convertion servers have to wait for the discover restart.

>>The removing operation or the crash of convertion server will not be written in discovFile, so when discovery server restart,it don't know those conversion servers are still alive or not. However, such removing operations will be done through new convertion servers or proxyServer (see Case 1).


