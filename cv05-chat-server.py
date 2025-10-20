#!/usr/bin/env python3

from cv05_chat_protocol import Chat_proto, Ctrl_value
import socket as s 
IP = "0.0.0.0"
PORT = 1111

def hanlde_client(client_sock, chat_proto):
    msg_bytes = client_sock.recv(1000)
    msg_text  = msg_bytes.decode()

    chat_proto.parse_proto_msg(msg_text)

def chat_server():
    chat_proto = Chat_proto("server")
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind(IP, PORT)
    sock.listen(5)
    #client = sock.accept()
    #client_sock = client[0]
    #cleint_addr = client[1]
    while True:
        (client_sock, client_addr) = sock.accept()
        print("Connected client [{}:{}]".format(client_addr[0], client_sock[0]))
        handle_client(client_sock, chat_proto)

if __name__ == "__main__":
    chat_server()
