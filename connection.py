import socket
import threading
from other import receive_messages, send_messages,broadcast_message
<<<<<<< HEAD

def handle_client(client_socket, addr, all_connected_sockets):
    print(f"Veza uspostavljena sa {addr}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast_message(message, client_socket, all_connected_sockets)
        except ConnectionResetError:
            break
    
    print(f"Klijent {addr} je prekinuo vezu.")
    client_socket.close()
    all_connected_sockets.remove(client_socket)

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
=======
>>>>>>> UDPkojiradi

def handle_client(client_socket, addr, all_connected_sockets):
    print(f"Veza uspostavljena sa {addr}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast_message(message, client_socket, all_connected_sockets)
        except ConnectionResetError:
            break
    
    print(f"Klijent {addr} je prekinuo vezu.")
    client_socket.close()
    all_connected_sockets.remove(client_socket)

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
<<<<<<< HEAD
    ConnectedSockets = []
    threads = []
    print("Pokušaj povezivanja na uređaje u mreži")
    def connect_to_ip(ip):
        MySocket = InitSocket()
        try:
            MySocket.connect((ip, 33433))
        except:
            pass
        else:
            ConnectedSockets.append(MySocket)
            print(f"Povezano na {ip}")
            breakk=True
=======
    UDPsender = InitUDPSocket()
    UDPsender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
>>>>>>> UDPkojiradi

    # Uzmi lokalnu IP adresu
    local_ip = socket.gethostbyname(socket.gethostname())
    msg = local_ip.encode('utf-8')
    UDPsender.sendto(msg, ("255.255.255.255", 5005))
    UDPsender.close()

<<<<<<< HEAD
    for i in range(256):
        ip = f'10.61.1.{i}'
        thread = threading.Thread(target=connect_to_ip, args=(ip,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return ConnectedSockets
=======
    # Poveži se na TCP port
    TCPSocket = InitTCPSocket()
    TCPSocket.connect(('10.61.1.105', 33433))  # IP adresa servera treba da bude ovde
    return [TCPSocket]
>>>>>>> UDPkojiradi
