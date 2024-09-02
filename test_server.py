import socket
import threading
from other import send_messages, receive_messages
from connection import get_local_ip, handle_client

def main():
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.bind((get_local_ip(), 33433))
    ServerSocket.listen()
    print(f"Server is listening on {get_local_ip()}:33433")

    AllConnectedSockets = []

    while True:
        ConnectedSocket, addr = ServerSocket.accept()
        AllConnectedSockets.append(ConnectedSocket)
        # Proslijedi sve potrebne argumente funkciji handle_client
        threading.Thread(target=handle_client, args=(ConnectedSocket, addr, AllConnectedSockets)).start()

if __name__ == "__main__":
    main()
