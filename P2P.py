import socket
import threading
import time

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = self.bind_socket()
        self.peers = []
        self.peer_usernames = {}
        self.username = None

        self.lock = threading.Lock()
        self.message_queue = []

        # Start threads for listening and discovery
        self.listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        self.listen_thread.start()
        self.discovery_thread = threading.Thread(target=self.discovery_loop, daemon=True)
        self.discovery_thread.start()

    def bind_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind((self.host, self.port))
        return server_socket

    def listen_for_messages(self):
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                decoded_message = message.decode()

                if addr not in self.peers and addr != (self.host, self.port):
                    self.peers.append(addr)

                if decoded_message.startswith('<username>'):
                    _, username = decoded_message.split(':', maxsplit=1)
                    self.peer_usernames[username] = addr

                elif decoded_message == 'ping':
                    self.server_socket.sendto(b'pong', addr)

                elif decoded_message == 'pong':
                    pass

                elif decoded_message.startswith('<discovery>'):
                    if self.username:
                        self.server_socket.sendto(f"<username>:{self.username}".encode(), addr)

                else:
                    with self.lock:
                        self.message_queue.append(decoded_message)

            except Exception as e:
                print(f"Error in message reception: {e}")

    def receive_message(self):
        with self.lock:
            if self.message_queue:
                return self.message_queue.pop(0)
        return None

    def send_message(self, message):
        if not self.username:
            print("Error: You must be logged in to send messages.")
            return

        full_message = f"{self.username}: {message}"
        for peer in self.peers:
            try:
                self.server_socket.sendto(full_message.encode(), peer)
            except OSError:
                print(f"Failed to send message to {peer}")

    def discovery_loop(self):
        while True:
            try:
                broadcast_message = "<discovery>"
                self.server_socket.sendto(broadcast_message.encode(), ('<broadcast>', self.port))
                time.sleep(10)
            except Exception as e:
                print(f"Error in discovery loop: {e}")

    def start(self):
        self.username = input("Enter your username: ").strip()
        print("Please wait, this might take a moment")
        time.sleep(2)
        print("You can now start chatting with peers.")

        while True:
            message = input(f"{self.username}: ").strip()
            self.send_message(message)
            if message.lower() == "<stop>":
                break

        print("Exiting chatroom...")
        self.server_socket.close()

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 15013
    peer = Peer(host, port)
    peer.start()
