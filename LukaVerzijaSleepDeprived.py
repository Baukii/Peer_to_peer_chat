import socket
import threading
import os
import time


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.peer_usernames = {}  # Map peer addresses to usernames
        self.username = None
        self.server_socket = self.bind_socket()
        self.listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        self.listen_thread.start()
        self.discovery_thread = threading.Thread(target=self.discovery_loop, daemon=True)
        self.discovery_thread.start()

    def bind_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind((self.host, self.port))
        print(f"Bound to {self.host}:{self.port}")
        return server_socket

    def listen_for_messages(self):
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                decoded_message = message.decode()

                if addr not in self.peers and addr != (self.host, self.port):
                    self.peers.append(addr)  # Add new peer

                if decoded_message.startswith('<username>'):
                    _, username = decoded_message.split(':', 1)
                    self.peer_usernames[addr] = username.strip()
                elif decoded_message == 'ping':
                    self.server_socket.sendto(b'pong', addr)
                elif decoded_message == 'pong':
                    pass  # Suppress pong messages
                elif decoded_message.startswith('<discovery>'):
                    # Handle discovery message without printing
                    self.server_socket.sendto(f"<username>{self.username}".encode(), addr)
                else:
                    print(f"\n{decoded_message}\n")
            except Exception as e:
                pass

    def send_message(self, message):
        if not self.username:
            print("Error: You must be logged in to send messages.")
            return

        if message.lower() == "<list>":
            self.list_peers()
            return
        elif message.lower().startswith("<whisper>"):
            self.handle_whisper(message)
            return
        elif message.lower() == "<ping>":
            self.handle_ping()
            return
        elif message.lower() == "<status>":
            self.show_status()
            return
        elif message.lower() == "<clear>":
            self.clear_console()
            return
        elif message.lower() == "<help>":
            self.show_help()
            return
        elif message.lower() == "<stop>":
            self.handle_stop()
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
                # Broadcast discovery message
                broadcast_message = "<discovery>"
                self.server_socket.sendto(broadcast_message.encode(), ('<broadcast>', self.port))
                
                # Wait to receive discovery messages
                time.sleep(10)
            except Exception as e:
                pass

    def list_peers(self):
        if self.peer_usernames:
            print("\nList of peers:")
            for addr, username in self.peer_usernames.items():
                print(f"{addr}: {username}")
        else:
            print("No peers found.")

    def handle_whisper(self, message):
        try:
            _, rest = message.split(maxsplit=2)
            target_username, text = rest.split(':', 1)
            target_username = target_username.strip()
            text = text.strip()

            target_peer = None
            for addr, username in self.peer_usernames.items():
                if username == target_username:
                    target_peer = addr
                    break

            if target_peer:
                full_message = f"Whisper from {self.username}: {text}"
                self.server_socket.sendto(full_message.encode(), target_peer)
                print("Message sent successfully.")
            else:
                print(f"Error: User '{target_username}' not found.")

        except ValueError:
            print("Error: Invalid whisper format. Use '<whisper> <username>: <message>'.")

    def handle_ping(self):
        print("Sending ping to all peers...")
        for peer in self.peers:
            try:
                self.server_socket.sendto(b'ping', peer)
            except OSError:
                print(f"Failed to send ping to {peer}")

    def show_status(self):
        print(f"Connected peers: {len(self.peers)}")
        print("List of connected peers:")
        for peer in self.peers:
            print(peer)

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_help(self):
        help_text = """
Available commands:
<list>       - List all usernames of peers.
<whisper>    - Send a private message to a specific user (e.g., <whisper> username: message).
<ping>       - Send a ping to check if a peer is online.
<status>     - Show the number of connected peers and their addresses.
<clear>      - Clear the chat history from the console.
<help>       - Show this help message.
<stop>       - End the chat and exit the chatroom.
        """
        print(help_text)

    def handle_stop(self):
        if self.username:
            disconnect_message = f"{self.username} has left the chatroom."
            for peer in self.peers:
                try:
                    self.server_socket.sendto(disconnect_message.encode(), peer)
                except OSError:
                    print(f"Failed to send disconnect message to {peer}")

            self.peers.clear()
            self.server_socket.close()
            print("You have been disconnected from the chatroom.")
            self.username = None

    def start(self):
        self.clear_console()
        print("Welcome to the peer-to-peer messaging system.")
        self.username = input("Enter your username: ").strip()
        print("Please wait, this might take a moment")
        time.sleep(2)

        print("You can now start chatting with peers.")
        print("Type '<help>' to show available commands.")

        while True:
            message = input(f"{self.username}: ").strip()
            self.send_message(message)
            if message.lower() == "<stop>":
                self.handle_stop()
                break

        print("Exiting chatroom...")

if __name__ == "__main__":
    host = '0.0.0.0'  # Use 0.0.0.0 to bind to all network interfaces
    port = 15012  # Initial port number; it will change if already in use

    peer = Peer(host, port)
    peer.start()
