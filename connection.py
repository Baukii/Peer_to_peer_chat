import socket

def SocketSetup():
    MySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    MySocket.bind(('localhost', 33433))
    MySocket.listen(1)
    return MySocket
def ConnectSockets(MySocket, GuestSocket):
    MySocket.connect(GuestSocket.getsockname())
def CheckOpenSockets():
    return 0
