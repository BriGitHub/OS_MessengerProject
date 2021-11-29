import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from message import Message

PORT = 2001
# SERVER = "97.81.156.128"
SERVER = "172.18.144.1"
ADDR = SERVER, PORT
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = r"/disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
         
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login,
                       text = "Please login to continue",
                       justify = CENTER,
                       font = "Helvetica 14 bold")
         
        self.pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
         
        self.labelName.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
         
        # create a entry box for
        # typing the message
        self.entryName = Entry(self.login,
                             font = "Helvetica 14")
         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
         
        # set the focus of the cursor
        self.entryName.focus()
         
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE",
                         font = "Helvetica 14 bold",
                         command = lambda: self.goAhead(self.entryName.get()))
         
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()

    # The main layout of the chat
    def layout(self, name):
       
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A",
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
         
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
         
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
         
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
         
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target = self.send(msg))
        snd.start()

    def send(self, msg):
        self.textCons.config(state=DISABLED)
        while True:
            message = Message('server', self.name, '', msg)
            self.textCons.config(state = NORMAL)
            self.textCons.insert(END, self.name+": "+msg+"\n\n") 
            self.textCons.config(state = DISABLED)
            self.textCons.see(END)
            
            #check to see if it is a private message
            if msg.startswith('/'):
                #private message
                split_msg = msg.split()
                message.msg_type = 'private'
                message.dest = split_msg[0][1:]
                if len(split_msg) > 1:
                    message.content = ' '.join(split_msg[1:])
                else:
                    message.content = ''

            client.send(message.encode())
            break

    def goAhead(self, name):
        message =  Message('init', name, '', '')
        enc_message = message.encode()
        client.send(enc_message)

        self.login.destroy()
        self.layout(name)
         
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                msg_header = Message.decode_header(client.recv(Message.HEADER))
                if msg_header['length']:
                    msg_content = Message.decode_content(client.recv(int(msg_header['length'])))

                    #print(f"[SERVER] {msg}")
                    self.textCons.config(state = NORMAL)
                    if msg_header['type'] == 'private':
                        self.textCons.insert(END, msg_header['source']+' (private)'+': '+msg_content+"\n\n")
                    else:
                        self.textCons.insert(END, msg_header['source']+': '+msg_content+"\n\n")
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occured, you are being disconnected now.")
                client.close()
                break

g = GUI()
#threading.Thread(target=receive).start()
#while(True):
    #send(input("Message: "))
