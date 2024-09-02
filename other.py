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
        message = socket_obj.recv(1024).decode('utf-8')
        if message.lower() == "stop!":
            break
        print("\n"f"Friend: {message}")
        print("You: ",end="")

def broadcast_message(message, sender_socket, all_connected_sockets):
    for client_socket in all_connected_sockets:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message)
            except Exception as e:
                print(f"Error sending message to {client_socket}: {e}")
                all_connected_sockets.remove(client_socket)
