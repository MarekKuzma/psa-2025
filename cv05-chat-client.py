#!/usr/bin/env python3

from cv05_chat_protocol import Chat_proto, Ctrl_value
import socket as s 
IP = "127.0.0.1"
PORT = 1111

def chat_client():
    nick = input("Enter your nick for chat client: ")
    chat_proto = Chat_proto(nick)
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((IP, PORT))
    msg_bytes = chat_proto.login().encode()
    sock.send(msg_bytes)
    #client = sock.accept()
    #client_sock = client[0]
    #client_addr = client[1]
    while True:
        print ("Menu:")
        print ("1 - Send message.")
        print ("2 - list users.")
        print ("3 - Exit.")
        choice = input("Select choice: ")
        print()
        if choice[0] == "1":
            text_msg = input("Enter message: ")
            msg_bytes = chat_proto.msg(text_msg).encode()
            sock.send(msg_bytes)
        elif choice[0] == "2":
            msg_bytes = chat_proto.users().encode()
            sock.send(msg_bytes)

            msg_bytes = sock.recv(1000)
            print("Logged in users")
            print(msg_bytes.decode())
            input("Press enter to continue...")
        elif choice[0] == "3":
            msg_bytes = chat_proto.logout().encode()
            sock.send(msg_bytes)
            sock.close()
            return

if __name__ == "__main__":
    chat_client()
