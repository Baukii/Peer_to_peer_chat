import socket
import threading
from other import send_messages, receive_messages

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind(('10.61.1.105', 33433))
ServerSocket.listen()

ConnectedSocket, addr = ServerSocket.accept()
print("Accepted connection from " + str(addr))

threading.Thread(target=send_messages, args=(ConnectedSocket,)).start()
threading.Thread(target=receive_messages, args=(ConnectedSocket,)).start()

