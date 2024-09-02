import socket
import threading
from connection import listen_for_client_ip, handle_client_connection,PovezivanjeNaLogIn
from other import send_messages, receive_messages

def start_tcp_server():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('10.61.1.105', 33433)) 
    tcp_server_socket.listen()
    
    print("TCP server is listening for incoming connections...")

    while True:
        client_socket, client_address = tcp_server_socket.accept()
        print(f"Accepted connection from {client_address}")

        threading.Thread(target=handle_client_connection, args=(client_socket, client_address)).start()


threading.Thread(target=listen_for_client_ip, daemon=True).start()
start_tcp_server()

ConnectedSockets = PovezivanjeNaLogIn()
if ConnectedSockets:
    client_socket = ConnectedSockets[0]
    print("Connected to the server. You can start chatting.")
    threading.Thread(target=send_messages, args=(client_socket,)).start()
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

