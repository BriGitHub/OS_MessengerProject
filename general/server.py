#Author: Andrew Whitinger
#Start and host a server that a client can connect to and send messages (literal strings) back and forth

from collections import deque
import socket
import threading

from message import Message

HEADER = 64 #size of the header in bytes
PORT = 2001 #router port for the connection
SERVER = socket.gethostbyname(socket.gethostname()) #gets the user's machine local ip
ADDR = SERVER, PORT
FORMAT = 'utf-8' #encoding strings in utf-8 format to send later
DISCONNECT_MESSAGE = r"/disconnect" #the message to disconnect the client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the TCP IPV4 server
client_inboxes = dict()

#init_client: handle incoming connection, register client if not already, and start handling messages
def init_client(conn, addr):
    conn.recv(Message.)

#handle_client: prints out there was a new connection to the server and gives the host the ip
#the loop works by using the header for the length of the message and it sends the message over
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #gets the encoded message from the client
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}") #print the ip and the message

#send: sends a message to the given sever
def send(conn, msg):
    message = msg.encode(FORMAT) #encode the message
    msg_length = len(message) #get the header
    send_length = str(msg_length).encode(FORMAT) #encode the header
    send_length += b' ' * (HEADER - len(send_length)) #make the header be the expected length (pad with spaces if needed)
    conn.send(send_length) #send header
    conn.send(message) #send message

#handle_incoming_connections: accept clients as they join
def handle_incoming_connections():
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=init_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#start: tell the server to listen and start the thread for the client
def start():
    server.bind(ADDR) #uses the network connection with the server
    server.listen() #start the server
    print(f"[LISTENING] Server is listening on {SERVER}")
    handle_incoming_connections()

#main: run the server
def main():
    print("[STARTING] server is starting...")
    start()

if __name__ == "__main__":
    main()
