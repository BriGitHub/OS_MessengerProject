#Author: Andrew Whitinger
#Start and host a server that a client can connect to and send messages (literal strings) back and forth

from queue import Queue
import socket
import threading

from message import Message

PORT = 2001 #router port for the connection
SERVER = socket.gethostbyname(socket.gethostname()) #gets the user's machine local ip
ADDR = SERVER, PORT
FORMAT = 'utf-8' #encoding strings in utf-8 format to send later
WELCOME_MESSAGE = "Welcome to the server, %s!"
DISCONNECT_MESSAGE = r"/disconnect" #the message to disconnect the client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the TCP IPV4 server
client_inboxes = dict()

#init_client: handle incoming connection, register client if not already, and start handling messages
def init_client(conn, addr):
    init_message = Message.decode_message(conn.recv(Message.HEADER))
    if init_message.msg_type != 'init':
        return
    
    name = init_message.source
    if name not in client_inboxes:
        print(f"[NEW CONNECTION] {addr} connected.")
        client_inboxes[name] = Queue()
        client_inboxes[name].put(Message('private', 'SERVER', name, WELCOME_MESSAGE % name))
    else:
        print(f"[NEW CONNECTION] {addr} reconnected.")
        
    threading.Thread(target=handle_messages_from_client, args=(conn, addr, name)).start()
    threading.Thread(target=handle_messages_to_client, args=(conn, addr, name)).start()

#handle_client: prints out there was a new connection to the server and gives the host the ip
#the loop works by using the header for the length of the message and it sends the message over
def handle_messages_from_client(conn, addr, name):
    connected = True
    while connected:
        try:
            msg_header = Message.decode_header(conn.recv(Message.HEADER)) #gets the encoded message from the client
            if msg_header['length']:
                msg_content = Message.decode_content(conn.recv(int(msg_header['length'])))
                if msg_content == DISCONNECT_MESSAGE:
                    connected = False
                    break
                
                message = Message(msg_header['type'], msg_header['source'], msg_header['dest'], msg_content)
                if message.msg_type == 'private':
                    if message.dest not in client_inboxes:
                        client_inboxes[message.dest] = Queue()
                        client_inboxes[message.dest].put(Message('private', name, message.dest, WELCOME_MESSAGE % message.dest))
                    client_inboxes[message.dest].put(message)
                elif message.msg_type == 'server':
                    for client in client_inboxes:
                        if client != name:
                            client_inboxes[client].put(message)
        except Exception as e:
            print(e)
            connected = False

# handle_messages_to_client: sends queued messages to client
def handle_messages_to_client(conn, addr, name):
    connected = True
    client_inboxes[name].put(Message('private', 'admin', name, 'test'))
    while connected:
        message = client_inboxes[name].get()
        conn.send(message.encode())

#handle_incoming_connections: accept clients as they join
def handle_incoming_connections():
    while True:
        conn, addr = server.accept()
        init_client(conn, addr)
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
