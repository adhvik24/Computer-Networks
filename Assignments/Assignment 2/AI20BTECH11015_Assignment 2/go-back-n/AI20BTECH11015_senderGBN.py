import socket
import time

senderIP = "10.0.0.1"
senderPort = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024  # Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

win_size = int(input("Enter the window size: "))
timeout = float(input("Enter the timeout in seconds: "))

socket_udp.settimeout(timeout)

f = open('testFile.jpg', "rb")
data = f.read()
size = len(data)
packet_size = bufferSize - 24
f.close()
pkt_cnt = size//packet_size
if(size%packet_size!=0):
    pkt_cnt += 1

packets = []

for i in range(pkt_cnt):
    if(i<pkt_cnt-1):
        packets.append(data[packet_size*i:packet_size*(i+1)])
    else:
        packets.append(data[packet_size*i:])
start = time.time()
print(pkt_cnt)
packet_window = []
a = 1
seqn_num = 1
exp_ack_seqnnum = 1
nextpkt_seqnnum = win_size+1


while (seqn_num<=win_size):
    if(seqn_num==pkt_cnt):
        a = 2
    val = seqn_num.to_bytes(2, 'big')
    mssg = val + bytes('*#%','utf-8') + packets[seqn_num-1] + bytes('*#%','utf-8') + bytes(a)
    socket_udp.sendto(mssg, recieverAddressPort)
    packet_window.append(mssg)
    seqn_num += 1

while(exp_ack_seqnnum!=pkt_cnt+1):
    while(len(packet_window)<win_size and nextpkt_seqnnum < pkt_cnt+1):
        if(nextpkt_seqnnum == pkt_cnt):
            a = 2
        val = nextpkt_seqnnum.to_bytes(2,'big')
        mssg = val + bytes('*#%','utf-8') + packets[nextpkt_seqnnum-1] + bytes('*#%','utf-8') + bytes(a)
        packet_window.append(mssg)
        nextpkt_seqnnum += 1
        # print("REACHED")
    try:
        msgFromServer = socket_udp.recvfrom(bufferSize)
        mssg1 = msgFromServer[0]
        rec_ack_seqnum = int.from_bytes(mssg1[0:2],'big')
        # base = exp_ack_seqnnum.to_bytes(2,'big')
        if(exp_ack_seqnnum<= rec_ack_seqnum):
            base =  rec_ack_seqnum + 1
            while(exp_ack_seqnnum!=base):
                packet_window.pop(0)
                exp_ack_seqnnum += 1
    except socket.timeout:
        print('Timeout')
        for dt in packet_window:
            socket_udp.sendto(dt,recieverAddressPort)

end = time.time()
run_time = end - start
size = size/1024
throughput = size/run_time
print("Throughput is: ", throughput)



# f = open('testFile.jpg', "rb")
# bufferSize = bufferSize - 24
# message = bytes('*','utf-8')

# total = f.read()
# size = len(total)
# data = f.read(bufferSize)
# a = 1
# seqn_num = 1
# while(data):
#     val = seqn_num.to_bytes(2, 'big')
#     if(len(data) < bufferSize):
#         a = 2
#     data = val + bytes('*#%', 'utf-8') + data + bytes('*#%', 'utf-8') + bytes(a)
#     # message = str.encode(data)
#     print(data)
#     socket_udp.sendto(data, recieverAddressPort)
#     data = f.read(bufferSize)
#     seqn_num = seqn_num + 1
    
#     msgFromServer = socket_udp.recvfrom(bufferSize)
#     # f1.write()
#     msgString = "Message from Server {}".format(msgFromServer[0])
#     print(msgString)
#     message = message + msgFromServer[0]
    
# print(message)
# f.close()
# f1 = open("demofile3.jpg", "wb")
# f1.write(message[1:])
# f1.close()

