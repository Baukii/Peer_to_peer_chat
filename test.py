import socket
import threading
from other import send_messages, receive_messages

MySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MySocket.connect(('10.61.1.105', 33433))
print("connected")
threading.Thread(target=send_messages, args=(MySocket,)).start()
threading.Thread(target=receive_messages, args=(MySocket,)).start()

