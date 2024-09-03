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
"""def SendingUDPMessages():
    UDPsender = InitUDPSocket()
    local_ip = get_local_ip()
    msg = local_ip.encode('utf-8')
    #i=1
    #while True:
    #    try:
    
    UDPsender.sendto(msg, ("255.255.255.255", 15476))
    UDPsender.close()
    #    except:
    #        i+=1
    #        print(i)
"""
def SendingUDPMessages():
    UDPsender = InitUDPSocket()
    local_ip = get_local_ip()
    msg = local_ip.encode('utf-8')
    try:
        UDPsender.sendto(msg, (local_ip, 15476)) 
        print("adresa poslata") # Promeni na lokalnu adresu
    except Exception as e:
        print(f"Greška u slanju UDP poruka: {e}")
    finally:
        UDPsender.close()

def PovezivanjeNaLogIn():
    TCPSocket = InitTCPSocket()
    TCPSocket.connect(('10.61.1.105', 33433))
    AllConnectedSockets=eval(TCPSocket.recv(64).decode("utf-8")) #
    return AllConnectedSockets
def InitUDPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
def ListeningForConnections(MyConnectedSockets):
    ServerSocket = InitTCPSocket()
    ServerSocket.bind((get_local_ip(), 22222))
    ServerSocket.listen()
    while True:
        ConnectedSocket, addr = ServerSocket.accept()
        MyConnectedSockets.append(ConnectedSocket)
def ListeningForUDPMessages():
    ListeningSocket = InitUDPSocket()
    port=15476
    ListeningSocket.bind((get_local_ip(), 15476))
    ConnectTo=ListeningSocket.recvfrom(1024)
    RequestingTCPConnection((ConnectTo,15476))
def RequestingTCPConnection(addr):
    PeerSocket=InitTCPSocket()
    PeerSocket.connect((addr,22222))
def AcceptingTCPConnection():
    AcceptingSocket=InitTCPSocket()
    AcceptingSocket.bind((get_local_ip(),22222))
    AcceptingSocket.listen()
    AllConnectedSockets=[]
    while True:
        ConnectedSocket, addr = AcceptingSocket.accept()
        AllConnectedSockets.append(ConnectedSocket)
def handle_client_communication(client_socket, all_connected_sockets):
    while True:
        message = recv_from_socket(client_socket)
        if message:
            print(f"Received: {message}")