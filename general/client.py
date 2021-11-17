#Author: Andrew Whitinger
#Start a client that connects to a server to send messages between

import socket
import threading

HEADER = 64 #size of the header in bytes
PORT = 2001 #router port for the connection
SERVER = "97.81.156.128"
# SERVER = "192.168.109.97"
# SERVER = "xxx.xxx.xxx.xx" #the server's ip to connect to
ADDR = SERVER, PORT
FORMAT = 'utf-8' #encoding strings in utf-8 format to send later
DISCONNECT_MESSAGE = r"/disconnect" #the message to disconnect the client

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the TCP IPV4 server
client.connect(ADDR) #uses the network connection with to connect to the server

#send: sends a message to the given sever
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)

            print(f"[SERVER] {msg}")

threading.Thread(target=receive).start()
while(True):
    send(input("Message: "))
