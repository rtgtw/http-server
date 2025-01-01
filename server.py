#import socket (built in python library)
import socket


#define socket host(IP) and port (Server will have a known port #)
SERVER_HOST = '192.168.x.x'
SERVER_PORT = 8888


#Create TCP Socket

#The actual socket, AF_INET represents the IPv4 address family
#Sock Stream represents TCP
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Setting up the socket
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#Binding the TCP socket object to a host's port
serverSocket.bind((SERVER_HOST,SERVER_PORT))
#Listetns for active connections and you can also specify a backlog
serverSocket.listen(10)
print(f'TCP Socket is listening on port {SERVER_PORT}... ')



#Forever loop to listen forever
while True:
    #Wait for a client connection
    #.accept() waits for a client to connect and returns a new tcp socket + their address
    clientConnection, clientAddress = serverSocket.accept()

    print(f'Accepted Client: {clientConnection}, {clientAddress}')
    #read the information sent by the client, this is an HTTP server so the client
    #will send an HTTP Get request, Read that info using .recv and specify the buffer

    #create a empty byte variable to store the chunks of inbound data
    data = b''
    numberOfChunks = 0

    #loop through the recv until data has everything from the buffer
    while True:

        chunk = clientConnection.recv(1024)

        #if nothing is left inside of the chunk, break the loop
        if not chunk:
            break

        #append to data variable
        data += chunk
        numberOfChunks += 1

        #double carriage return marks the end of an HTTP request
        #recv is just a tcp with a buffer listening for if any data passes through
        #it will do this forever, so we will forever be in the loop, we'll know that the client (Get Request)
        #is finished with its request after a double carriage return, this is what a User Agent (Web Browser)
        #sends AFTER its finished with its headers, then it continues on with its message, the continuation
        #would be the body, but a get request doesnt have a body, a POST or PUT can / does
        #a GET response from the Server (aka this custom server) is the one that would have a response, because
        #its responding with some data, which in this case would be an HTML file
        if b'\r\n\r\n' in data:
            print('Double carriage return: End of HTTP request \n')
            break



    print(f'Total bytes: {len(data)}\n'
          f'Number of Chunks: {numberOfChunks}\n\n'
          f'{data.decode()}')


    while True:

        #send the http response based on the request
        #response body is where the HTML/Response be for this request
        #this is where frameworks come into play, reading a file and using i/o (database reads) can be costly
        #the more users are calling this, so frameworks can enhance this process by possibly storing a cache
        #or some elaborate system to make this process faster and less costly
        with open('index.html','r',encoding='UTF-8') as file:
            responseBody = file.read()


        #HTTP header which the client's user agent understands since this is the HTTP protocol
        responseHeader = ('HTTP/1.0 200 OK\r\n'
                          'Content-Type: text/html\r\n'
                          'Content-Length: {}\r\n'
                          'Connection: keeclearp-alive\r\n\r\n'
                          '{}').format(len(responseBody),responseBody)


        #send the full response
        clientConnection.sendall(responseHeader.encode('UTF-8'))


        #close the connection
        clientConnection.close()
        break

#close the socket connection
# serverSocket.close()






