import socket

recieverIP = "10.0.0.2"
recieverPort = 20002
bufferSize = 1024  # Message Buffer Size

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully.....")
a = bytes(1)
message = bytes('@', 'utf-8')
while(a == bytes(1)):

    # wait to recieve message from the server
    bytesAddressPair = socket_udp.recvfrom(bufferSize)
    print(bytesAddressPair)  # print recieved message

    # split the recieved tuple into variables
    recievedMessage = bytesAddressPair[0]
    senderAddress = bytesAddressPair[1]
    x = recievedMessage.split(bytes('@', 'utf-8'))
    seqn_num = x[0]
    data = x[1]
    a = x[2]
    message = message + data
    # print them just for understanding
    # msgString = "Message from Client:{}".format(data)
    # detailString = "Client IP Address:{}".format(senderAddress)
    # print(msgString)
    # print(detailString)

# Sending a reply to client
message = str.encode(message[1:])
socket_udp.sendto(message, senderAddress)
