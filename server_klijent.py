import socket
import threading

# Port i IP adresa
PORT = 33434
SERVER_IP = '0.0.0.0'  # Slušaj na svim dostupnim mrežnim interfejsima

# Server funkcija
def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen()
    print("TCP server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
            client_socket.sendall(f"Echo: {message}".encode('utf-8'))
        except ConnectionResetError:
            break
    client_socket.close()

# Klijent funkcija
def start_tcp_client(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, PORT))
    
    while True:
        message = input("You: ")
        client_socket.sendall(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server: {response}")

        if message.lower() == "stop!":
            break

    client_socket.close()

# Funkcija za pokretanje servera i klijenta
def run_server_and_client():
    # Pokreće server u pozadini
    threading.Thread(target=start_tcp_server, daemon=True).start()
    
    # Pita korisnika da unese IP servera za klijent
    server_ip = input("Enter server IP (or 'localhost' if running on the same machine): ").strip()
    print("You can start chatting now.")
    
    # Pokreće klijent
    start_tcp_client(server_ip)

if __name__ == "__main__":
    run_server_and_client()
