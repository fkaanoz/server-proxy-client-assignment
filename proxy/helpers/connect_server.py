import socket

def connect_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host,port))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    client_socket.sendall(bytes("AUTH SECRET_123;", 'utf-8'))

    dataReceived = client_socket.recv(1024)
    dataReceived = dataReceived.decode('utf-8')

    if dataReceived == "AUTH OK;":
        print("Connected to SERVER")
    else:
        print("Authentication failed")
        client_socket.close()
        return None

    return client_socket

