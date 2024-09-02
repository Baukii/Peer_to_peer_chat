import socket
import threading
from other import receive_messages, send_messages,broadcast_message

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

def InitSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def PovezivanjeNaLogIn():
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


    for i in range(256):
        ip = f'10.61.1.{i}'
        thread = threading.Thread(target=connect_to_ip, args=(ip,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return ConnectedSockets