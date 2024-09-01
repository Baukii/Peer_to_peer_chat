import socket
MySocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
MySocket.connect(('10.61.1.100',33433))
print("connected")
MySocket.sendto(b'Hello!',('10.61.1.100',33433))
