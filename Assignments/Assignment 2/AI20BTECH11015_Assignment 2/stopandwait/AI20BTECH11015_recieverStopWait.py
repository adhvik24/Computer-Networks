import socket
import time

recieverIP = "10.0.0.2"
recieverPort = 20002
bufferSize = 1024  # Message Buffer Size

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully.....")
f = open("Receivedimg.jpg","wb")
a = bytes(1)
seqn_num_exp = 1
message = bytes('*', 'utf-8')
while(a == bytes(1)):

    # wait to recieve message from the server
    bytesAddressPair = socket_udp.recvfrom(bufferSize)
    print(bytesAddressPair)  # print recieved message

    # split the recieved tuple into variables
    recievedMessage = bytesAddressPair[0]
    senderAddress = bytesAddressPair[1]
    x = recievedMessage.split(bytes('*#%', 'utf-8'))
    seqn_num = x[0]
    data = x[1]
    a = x[2]
    if(seqn_num == seqn_num_exp.to_bytes(2,"big")):
        message = message + data
        seqn_num_exp += 1
    ack = seqn_num + b"Packet Received"
    socket_udp.sendto(ack, senderAddress)
    if(a==bytes(2)):
        break
f.write(message[1:])
f.close()