#!/usr/bin/env python3
import socket
import struct

DNS_SERVER = "8.8.8.8"
DNS_PORT = 53
transaction_id = 0x1a2b
flags = 0x0100  # standard query
dns_header = struct.pack("!6H", transaction_id, flags, 1, 0, 0, 0)
dns_bytes = dns_header

#question = "www.uniza.sk"
question = input("Enter domain name to resolve: ")
labels = question.split(".")
labels_bytes = bytes()
for label in labels:
    labels_bytes += struct.pack("B", len(label)) 
    labels_bytes += label.encode()
labels_bytes += struct.pack("B", 0)  # end of QNAME
qestion_type = 1
question_bytes = labels_bytes + struct.pack("!2H", qestion_type, 0x001)  # QTYPE A, QCLASS IN
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(dns_bytes + question_bytes, (DNS_SERVER, DNS_PORT))

(recieved_bytes, addr) = sock.recvfrom(512)
print("Received {} bytes from {}".format(len(recieved_bytes), addr))

if int.from_bytes(recieved_bytes[0:2], "big") == socket.htons(transaction_id):
    ip_addr = socket.inet_ntoa(recieved_bytes[-4:])
    print("Ip response: {}".format(ip_addr))
sock.close()