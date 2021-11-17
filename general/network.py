#Author: Andrew Whitinger
#purpose: create a network to send messages back and forth (combination of server.py and client.py)
#note: only works for one client
#import network

import socket

class Network():
    PORT = 2001         #port used for network communication
    HEADER = 64         #length of message header in bytes
    FORMAT = 'utf-8'    #message format
    LOG = True          #true if log messages are to be printed

    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())      #local ip address
        self.sock = socket.socket(socket.AF.INET, socket.SOCK_STREAM)   #socket used for connections
        self.connection = None                                          #connection to client (None if client)
        self.client_addr = None                                         #client address (None if client)

    def start_server(self):
        # Initialize server and bind to local ip and port
        sock.bind((LOCAL_IP, PORT))

        # Allow connections and get a connection from a single client
        sock.listen()
        print(LOG * f"[LISTENING] Server is listening on {local_ip}")

        self.connection, self.client_addr = server.accept()
        print(LOG * f"[NEW CONNECTION] {addr} connected.")

    def connect(self, ip):
        # Connect socket to a given host ip
        sock.connect((ip, port))

    def send(self, message):
        # Encode message and determine length
        formatted_msg = message.encode(FORMAT)              #formatted message
        message_length = str(len(message)).encode(FORMAT)   #length of message to send
        message_length += b' ' * (HEADER - len(message_length)) #pad right with blank space

        # Send message length, followed by message
        target = connection if connection else sock         #target to send message to
            target.send(message_length)
            target.send(formatted_msg)

        print(LOG * f"[MESSAGE SENT] {message}")

    def receive(self):
        # Receive message length followed by message, and return message
        sender = connection if connection else sock         #sender that will send message
        message_length = sender.recv(HEADER).decode(FORMAT)
        if message_length:
            message = sender.recv(int(message_length)).decode(FORMAT)
            print(LOG * f"[MESSAGE RECEIVED] {message})

            return message
        else:
            return None     #message of length 0 received
