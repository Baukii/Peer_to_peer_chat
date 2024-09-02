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
            message = socket_obj.recv(1024).decode('utf-8')
            if message.lower() == "stop!":
                print("\nFriend has left the chat")
                break
            sys.stdout.write("\033[F") #move the cursor up one line
            print("\n"f"Friend: {message}")
            print("You: ",end="")
        except ConnectionResetError:
            print("\nConnection closed by the other side.")
            break
def broadcast_message(message, sender_socket, all_connected_sockets):
    for client_socket in all_connected_sockets:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message)
            except Exception as e:
                print(f"Error sending message to {client_socket}: {e}")
                all_connected_sockets.remove(client_socket)