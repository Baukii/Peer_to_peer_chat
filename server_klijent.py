import threading
from connection import *
from messages import *

SendingUDPMessages()
MyConnectedSockets=AcceptingTCPConnection()
accepting_thread = threading.Thread(target=AcceptingTCPConnection, args=(MyConnectedSockets,))
accepting_thread.start()
listening_thread = threading.Thread(target=ListeningForUDPMessages, args=(MyConnectedSockets,))
listening_thread.start()

send_thread = threading.Thread(target=SendAllConnected, args=(MyConnectedSockets,))
send_thread.start()

while True:
    if MyConnectedSockets:
        for client_socket in MyConnectedSockets:
            communication_thread = threading.Thread(target=handle_client_communication, args=(client_socket, MyConnectedSockets))
            communication_thread.start()
    