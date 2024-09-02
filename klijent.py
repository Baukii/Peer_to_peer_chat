import threading
from connection import PovezivanjeNaLogIn
from other import send_messages, receive_messages
ConnectedSockets = PovezivanjeNaLogIn()
if ConnectedSockets:
    client_socket = ConnectedSockets[0]
    print("Connected to the server. You can start chatting.")
    threading.Thread(target=send_messages, args=(client_socket,)).start()
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

