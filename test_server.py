import socket
import threading
from other import send_messages, receive_messages
from connection import get_local_ip,handle_client

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind((get_local_ip(), 33433))
ServerSocket.listen()

AllConnectedSockets = []
while True:
    ConnectedSocket, addr = ServerSocket.accept()
    AllConnectedSockets.append(ConnectedSocket)
    threading.Thread(target=handle_client, args=(ConnectedSocket, addr, AllConnectedSockets)).start()
