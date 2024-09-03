import socket
import threading
from messages import *

def handle_client(client_socket, addr, all_connected_sockets):
    print(f"Veza uspostavljena sa {addr}")
    try:
        message = client_socket.send(str(all_connected_sockets).encode("utf-8"))
    except ConnectionResetError:
        print("Neuspešno slanje liste")
    else:
        print("Uspešno slanje liste povezanih")
    client_socket.close()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def InitTCPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def InitUDPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def PovezivanjeNaLogIn():
    # UDPsender = InitUDPSocket()
    # UDPsender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Uzmi lokalnu IP adresu
    # local_ip = socket.gethostbyname(socket.gethostname())
    # msg = local_ip.encode('utf-8')

    # UDPsender.sendto(msg, ("255.255.255.255", 5005))
    # UDPsender.close()

    # Poveži se na server
    TCPSocket = InitTCPSocket()
    TCPSocket.connect(('10.61.1.105', 33433))
    AllConnectedSockets=eval(TCPSocket.recv(64).decode("utf-8")) #
    return AllConnectedSockets
def InitUDPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
def ListeningForConnections(MyConnectedSockets):
    ServerSocket = InitTCPSocket()
    try:
        ServerSocket.bind((get_local_ip(), 22222))
    except:
        pass
    ServerSocket.listen()
    while True:
        ConnectedSocket, addr = ServerSocket.accept()
        MyConnectedSockets.append(ConnectedSocket)
def handle_client_communication(client_socket, all_connected_sockets):
    while True:
        message = recv_from_socket(client_socket)
        if message:
            print(f"Received: {message}")
            broadcast_message(message.encode("utf-8"), client_socket, all_connected_sockets)
        else:
            all_connected_sockets.remove(client_socket)
        
