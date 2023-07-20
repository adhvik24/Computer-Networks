import socket
import time

senderIP = "10.0.0.1"
senderPort = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024  # Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

f = open('testFile.jpg', "rb")
data = f.read()
size = len(data)
packet_size = bufferSize - 24
f.close()
f = open('testFile.jpg', "rb")
bufferSize = bufferSize - 24
message = bytes('*','utf-8')
data = f.read(bufferSize)
a = 1
retrans_cnt = 0
seqn_num = 1
timeout = float(input("Enter the timeout:"))
start = time.time()
while(data):
    val = seqn_num.to_bytes(2, 'big')
    if(len(data) < bufferSize):
        a = 2
    data = val + bytes('*#%', 'utf-8') + data + bytes('*#%', 'utf-8') + bytes(a)
    socket_udp.sendto(data, recieverAddressPort)
    maxtime = time.time()+timeout

    acked = False

    while not acked:
        try:
            socket_udp.settimeout(maxtime-time.time())
            msgFromServer = socket_udp.recvfrom(bufferSize)
            ack = msgFromServer[0]
            ack_sqn = ack[0:2]

            while ack_sqn != val:
                remsgFromServer = socket_udp.recvfrom(bufferSize)
                reack = msgFromServer[0]
                ack_sqn = reack[0:2]

            acked = True

        except socket.timeout:
            # Timeout occured
            print("timeout occurred")
            retrans_cnt +=1
            socket_udp.sendto(data, recieverAddressPort)
            maxtime = time.time() + timeout



    data = f.read(bufferSize)
    seqn_num = seqn_num + 1
    
end = time.time()
f.close()

timeutilised = end - start
size = size/1024
print("Number of retransmissions: ", retrans_cnt)
print("Throughput: ", size/(timeutilised))