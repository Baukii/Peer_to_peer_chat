import socket
import sys
import threading

def send_messages(socket_obj):
    while True:
        message = input("You: ")
        socket_obj.sendall(message.encode('utf-8'))
        if message.lower() == "stop!":
            break

def receive_messages(socket_obj):
    while True:
        try:   
            message = socket_obj.recv(32).decode('utf-8')
            if message.lower() == "stop!":
                print("\nFriend has left the chat")
                break
            sys.stdout.write("\033[F") #move the cursor up one line
            print("\n"f"Friend: {message}")
            print("You: ",end="")
        except ConnectionResetError:
            print("\nConnection closed by the other side.")
            break
def broadcast_message(message, sender_socket, all_connected_sockets, exclude_sender=True):
    for client_socket in all_connected_sockets:
        if not exclude_sender or client_socket != sender_socket:
            try:
                client_socket.sendall(message)
            except Exception as e:
                print(f"Error sending message to {client_socket}: {e}")

def recv_from_socket(client_socket, buffer_size=1024):
    try:
        return client_socket.recv(buffer_size).decode("utf-8")
    except Exception as e:
        print(f"Error receiving message: {e}")
        return False

def SendAllConnected(all_connected_sockets):
    while True:
        message = input("You: ").encode("utf-8")
        broadcast_message(message, None, all_connected_sockets, exclude_sender=True)
