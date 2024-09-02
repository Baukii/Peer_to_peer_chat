import socket
import threading
from other import send_messages, receive_messages

def InitSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def MyIP():
    MyName = socket.gethostname()
    MyIPAddress = socket.gethostbyname(MyName)
    return MyIPAddress

def handle_client(client_socket):
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket)

def start_server(my_ip):
    server_socket = InitSocket()
    server_socket.bind((my_ip, 33433))
    server_socket.listen()
    print("Server started. Waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        handle_client(client_socket)

def connect_to_server(ip):
    client_socket = InitSocket()
    try:
        client_socket.connect((ip, 33433))
        print(f"Connected to server {ip}")
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
        send_messages(client_socket)
    except Exception as e:
        print(f"Cannot connect to {ip}: {e}")

def listen_for_broadcast():
    broadcast_socket = InitSocket()
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_socket.bind(('', 33433))
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.settimeout(5)

    try:
        while True:
            try:
                message, addr = broadcast_socket.recvfrom(1024)
                if message.decode('utf-8').startswith("BROADCAST"):
                    print(f"Broadcast message received from {addr}")
                    connect_to_server(addr[0])
            except socket.timeout:
                pass
    finally:
        broadcast_socket.close()
