# Echo server program
import socket
import time

from helpers.get_destination import get_destination
from helpers.get_input import get_input

#Loopback IP address
HOST = '127.0.0.1'
PROXY_PORT = 3000
SERVER_PORT = 8080

PORT = 0

#Create a sockets
dest = get_destination()
if dest == "0":
    PORT = PROXY_PORT
else:
    PORT = SERVER_PORT


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))


while 1:
    s_text = get_input()

    client_socket.sendall(bytes(s_text,'utf-8'))
    time.sleep(0.5)

    dataReceived=client_socket.recv(1024)
    dataReceived = dataReceived.decode('utf-8')
    print(" RESPONSE: ")
    print(dataReceived , "\n")

