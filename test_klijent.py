import socket
import threading
from other import send_messages, receive_messages
from connection import PovezivanjeNaLogIn
ConnectedSockets=PovezivanjeNaLogIn()
threading.Thread(target=send_messages, args=(ConnectedSockets[0],)).start()
threading.Thread(target=receive_messages, args=(ConnectedSockets[0],)).start()
