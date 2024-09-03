import threading
from connection import *
from other import *
AllConnectedSockets = PovezivanjeNaLogIn()
MyConnectedSockets=[]
for i in AllConnectedSockets:
    ConnectFromSocket=InitTCPSocket()
    try:    
        ConnectFromSocket.connect((i[0],22222))
    except:
        pass
    else:
        MyConnectedSockets.append(ConnectFromSocket)
listening_thread = threading.Thread(target=ListeningForConnections, args=(MyConnectedSockets,))
listening_thread.start()

    # Pokretanje threada za slanje poruka
send_thread = threading.Thread(target=SendAllConnected, args=(MyConnectedSockets,))
send_thread.start()
while True:
    if MyConnectedSockets:
        for client_socket in MyConnectedSockets:
            communication_thread = threading.Thread(target=handle_client_communication, args=(client_socket, MyConnectedSockets))
            communication_thread.start()