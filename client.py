#testing the round trip time it takes the network
import time
import socket


def send_get_request(host):

    #Before it gets sent out in MS
    before = time.time() * 1000

    #create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect socket to host
    client_socket.connect((host,80))


    #create the request
    request =('''
        
        GET / HTTP/1.1
        User-Agent: PostmanRuntime/7.43.0
        Accept: */*
        Host: localhost:80
        Accept-Encoding: gzip, deflate, br
        Connection: keep-alive
        '''
    )
    #send the request
    client_socket.sendall(request.encode('UTF-8'))

    #Receive the response in chunks
    response = b''

    while True:
        chunk = client_socket.recv(4096)

        if not chunk:
            break
        response += chunk


    #close the connection
    client_socket.close()


    #after it gets sent out
    after = time.time() * 1000

    print('success')

    rtt = after - before
    #decode and return the response
    return (f'{response.decode()}\r\n\r\n'
            # f'Time it took to send in MS:{before}\r\n'
            # f'Time it took to return in MS {after}\r\n'
            f'Total Round-Trip Time {rtt:.2f} MS\r\n')



print(send_get_request('192.168.x.x'))

