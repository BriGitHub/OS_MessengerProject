import socket
import threading

HEADER = 64
PORT = 2001
# SERVER = "97.81.156.128"
SERVER = "172.18.144.1"
ADDR = SERVER, PORT
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = r"/disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

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
