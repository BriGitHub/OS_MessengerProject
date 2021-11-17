import socket

class Network():
    PORT = 2001         #port used for network communication
    HEADER = 256        #length of message header in bytes
    FORMAT = 'utf-8'    #message format
    LOG = True          #true if log messages are to be printed

    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())      #local ip address
        self.sock = socket.socket(socket.AF.INET, socket.SOCK_STREAM)   #socket used for connections
        self.connection = None                                          #connection to client (None if client)
        self.client_addr = None                                         #client address (None if client)

    def start_server(self):
        # Initialize server and bind to local ip and port
        self.sock.bind((self.LOCAL_IP, self.PORT))

        # Allow connections and get a connection from a single client
        self.sock.listen()
        print(self.LOG * f"[LISTENING] Server is listening on {self.local_ip}")

        self.connection, self.client_addr = self.server.accept()
        print(self.LOG * f"[NEW CONNECTION] {self.addr} connected.")

    def connect(self, ip):
        # Connect socket to a given host ip
        self.sock.connect((ip, self.port))
        
    def send(self, message):
        # Encode message and determine length
        formatted_msg = message.encode(self.FORMAT)              #formatted message
        message_length = str(len(message)).encode(self.FORMAT)   #length of message to send
        message_length += b' ' * (self.HEADER - len(message_length)) #pad right with blank space

        # Send message length, followed by message
        target = self.connection if self.connection else self.sock         #target to send message to
        target.send(message_length)
        target.send(formatted_msg)

        print(self.LOG * f"[MESSAGE SENT] {message}")

    def receive(self):
        # Receive message length followed by message, and return message
        sender = self.connection if self.connection else self.sock         #sender that will send message
        message_length = sender.recv(self.HEADER).decode(self.FORMAT)
        if message_length:
            message = sender.recv(int(message_length)).decode(self.FORMAT)
            print(self.LOG * f"[MESSAGE RECEIVED] {message}")

            return message
        else:
            return None     #message of length 0 received