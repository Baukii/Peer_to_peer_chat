import socket

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
        print(f"\nFriend: {message}")
        print("You: ", end="")
