from connection import SocketSetup
from connection import ConnectSockets


MySocket=SocketSetup()
port = 33433
ip = '10.61.1.100'
while True:
    try:
        ConnectSockets(MySocket,(ip,port))
        print("connected")
        break
    except:
        print("not connected")
        pass
        