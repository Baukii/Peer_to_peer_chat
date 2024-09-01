import socket
from other import InputBezInterupcije

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind(('10.61.1.100', 33433))
ServerSocket.listen()

ConnectedSocket, addr = ServerSocket.accept()
print("Accepted connection from " + str(addr))

output = ConnectedSocket.recv(1024)
print(output.decode('utf-8'))

InputBezInterupcije()