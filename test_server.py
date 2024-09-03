import socket
import threading
from messages import *
from connection import *

ServerSocket = InitTCPSocket()
ServerSocket.bind((get_local_ip(), 33433))
ServerSocket.listen()

AllConnectedSockets = []
while True:
    ConnectedSocket, addr = ServerSocket.accept()
    print(ConnectedSocket,addr)
    AllConnectedSockets.append(addr)
    handle_client(ConnectedSocket, addr, AllConnectedSockets[:-1])