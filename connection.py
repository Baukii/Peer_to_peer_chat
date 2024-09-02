import socket
import threading

def InitSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def PovezivanjeNaLogIn():
    ConnectedSockets = []
    threads = []
    print("Pokušaj povezivanja na uređaje u mreži")
    def connect_to_ip(ip):
        MySocket = InitSocket()
        try:
            MySocket.connect((ip, 33433))
        except:
            pass
        else:
            ConnectedSockets.append(MySocket)
            print(f"Povezano na {ip} \nPokušaj povezivanje na ostale uređaje u mreži")


    for i in range(105, 256):
        ip = f'10.61.1.{i}'
        thread = threading.Thread(target=connect_to_ip, args=(ip,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return ConnectedSockets
