import socket
import time

senderIP = "10.0.0.1"
senderPort = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024  # Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

f = open('testFile.jpg', "rb")
data = f.read(bufferSize)
a = 1
seqn_num = 0
while(data):
    val = seqn_num.to_bytes(2, 'big')
    data = val + bytes('@', 'utf-8') + data + bytes('@', 'utf-8') + bytes(a)
    message = str.encode(data)
    socket_udp.sendto(message, recieverAddressPort)
    data = f.read(bufferSize)
    seqn_num = seqn_num + 1
    if(len(data) < bufferSize):
        a = 2
    time.sleep(0.01)  # Give receiver a bit time to save

msgFromServer = socket_udp.recvfrom()

msgString = "Message from Server {}".format(msgFromServer[0])
print(msgString)
f1 = open("demofile3.txt", "w")
f1.write(msgFromServer[0])
f1.close()
f.close()

# while True:

#     # Send to server using created UDP socket
#     msg = input("Please enter message to send: ")
#     message = str.encode(msg)
#     socket_udp.sendto(message, recieverAddressPort)

#     # wait for reply message from reciever
#     msgFromServer = socket_udp.recvfrom(bufferSize)

#     msgString = "Message from Server {}".format(msgFromServer[0])
#     print(msgString)
