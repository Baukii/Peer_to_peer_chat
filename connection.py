import socket
import threading
from other import send_messages, receive_messages

def InitTCPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def InitUDPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 

def PovezivanjeNaLogIn():
    UDPsender = InitUDPSocket()
    UDPsender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    msg = get_local_ip().encode('utf-8')
    
    # Broadcast IP adresu na UDP portu
    UDPsender.sendto(msg, ("255.255.255.255", 5005))
    UDPsender.close()

    # Poveži se na TCP port
    TCPSocket = InitTCPSocket()
    TCPSocket.connect((get_local_ip(), 33533))  # IP adresa servera treba da bude ovde
    return [TCPSocket]

def listen_for_client_ip():
    UDP_PORT = 5005
    TCP_PORT = 33433
    UDP_IP = "0.0.0.0"  # Sluša na svim IP adresama

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind((UDP_IP, UDP_PORT))

    while True:
        msg, addr = udp_socket.recvfrom(1024)  # Pretpostavljamo da je poruka manja od 1024 bajta
        client_ip = msg.decode('utf-8')
        print(f"Received IP address from client: {client_ip}")

        # Poveži se sa klijentom preko TCP
        client_tcp_socket = InitTCPSocket()
        try:
            client_tcp_socket.connect((client_ip, TCP_PORT))
            handle_client_connection(client_tcp_socket, (client_ip, TCP_PORT))
        except Exception as e:
            print(f"Failed to connect to client at {client_ip}: {e}")

def handle_client_connection(client_socket, addr):
    print(f"Accepted connection from {addr}")
    threading.Thread(target=send_messages, args=(client_socket,)).start()
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

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