import socket
import time

senderIP = "10.0.0.1"
senderPort = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024  # Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

f = open('testFile.jpg', "rb")
message = bytes('*','utf-8')
# total = f.read()
# size = len(total)
data = f.read(bufferSize)
a = 1
seqn_num = 1
while(data):
    val = seqn_num.to_bytes(2, 'big')
    if(len(data) < bufferSize):
        a = 2
    data = val + bytes('*#%', 'utf-8') + data + bytes('*#%', 'utf-8') + bytes(a)
    # message = str.encode(data)
    print(data)
    socket_udp.sendto(data, recieverAddressPort)
    data = f.read(bufferSize)
    seqn_num = seqn_num + 1
    
    msgFromServer = socket_udp.recvfrom(bufferSize)
    # f1.write()
    msgString = "Message from Server {}".format(msgFromServer[0])
    print(msgString)
    message = message + msgFromServer[0]
    

# msgString = "Message from Server {}".format(msgFromServer[0])
    # time.sleep(0.01)  # Give receiver a bit time to save

# msgFromServer = socket_udp.recvfrom(1024)

# msgString = "Message from Server {}".format(msgFromServer[0])
# print(msgString)
# f1 = open("demofile3.jpg", "wb")
# m = str(msgFromServer[0],'UTF-16')
print(message)
f.close()
f1 = open("demofile3.jpg", "wb")
f1.write(message[1:])
f1.close()

# while True:

#     # Send to server using created UDP socket
#     msg = input("Please enter message to send: ")
#     message = str.encode(msg)
#     socket_udp.sendto(message, recieverAddressPort)

#     # wait for reply message from reciever
#     msgFromServer = socket_udp.recvfrom(bufferSize)

#     msgString = "Message from Server {}".format(msgFromServer[0])
#     print(msgString)