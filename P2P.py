import socket
import threading
import os
import time
import sys

def write_to_file(message, file_name="chat_log.txt"):
    with open(file_name, "a") as f:
        f.write(message)
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
                message, addr = self.server_socket.recvfrom(1)
                decoded_message = message.decode()
                if addr not in self.peers and addr != (self.host, self.port):
                    self.peers.append(addr)  # Add new peer
                write_to_file(decoded_message)
                if decoded_message.startswith('<username>'):
                    _, username = decoded_message.split(':', 1)
                    self.peer_usernames.update({username:addr})
                    self.send_message(open('chat_log.txt',"rb").read())
                elif decoded_message.startswith('<discovery>'):
                    self.server_socket.sendto(f"<username>:{self.username}".encode(), addr)
                else:
                    self.handle_message(decoded_message)
            except Exception as e:
                pass

    def handle_message(self, message):
        sys.stdout.write("\033[F")  # Move the cursor up one line
        print(f"\n{message}")
        write_to_file(f"\n{message}")

    def send_message(self, message):
        if not self.username or not message:
            print("Error: Username and message cannot be empty.")
            return

        if message.lower() == "<list>":
            self.list_peers()
            return
        elif message.lower().startswith("<whisper>"):
            self.handle_whisper(message)
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
        for peer in self.peers[1:]:
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
                print(f"Error in discovery loop: {e}")

    def list_peers(self):
        if self.peer_usernames:
            print("\nList of peers:")
            for username, addr in self.peer_usernames.items():
                if username != "None":
                    print(f"{username}")
        else:
            print("No peers found.")
        print()

    def handle_whisper(self, message):
        try:
            _, rest = message.split(" ", 1)
            target_username, text = rest.split(":", maxsplit=2)
            target_username = target_username.strip()
            text = text.strip()
            target_ip = self.peer_usernames[target_username]
            if target_ip:
                full_message = f"Whisper from {self.username}: {text}"
                self.server_socket.sendto(full_message.encode(), target_ip)
                # Save the whisper to file
                print(f"Whisper sent to {target_username}: {text}")
                print("Message sent successfully.")
            else:
                print(f"Error: User '{target_username}' not found.")
        except ValueError:
            print("Error: Invalid whisper format. Use '<whisper> username:message'.")

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
<whisper>    - Send a private message to a specific user (e.g., <whisper> username:message).
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
            # Save the disconnection message to file
            self.write_to_file(disconnect_message)
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
    port = 15013  # Initial port number; it will change if already in use

    peer = Peer(host, port)
    peer.start()