import socket
import threading

def receive_data(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # Koristite recvfrom za UDP
        print(f"Primljeno od {addr}: {data.decode('utf-8')}")
        if data.decode('utf-8') == "stop":
            print("Prekinuto primanje podataka.")
            break

def send_data(sock, address):
    while True:
        user_input = input("Unesite poruku (ili 'stop' za prekid): ")
        sock.sendto(user_input.encode('utf-8'), address)  # Sendto za UDP
        if user_input == "stop":
            print("Prekinuto slanje podataka.")
            break

def InputBezInterupcije():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('10.61.1.100', 33433)

    recv_thread = threading.Thread(target=receive_data, args=(sock,))
    recv_thread.start()

    send_data(sock, server_address)

    recv_thread.join()
