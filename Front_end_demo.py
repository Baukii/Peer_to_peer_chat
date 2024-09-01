import tkinter as tk
from tkinter import scrolledtext
import asyncio
from threading import Thread


#mozda bude menjano 1
class PeerNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.peers = []
        self.reader = None
        self.writer = None
        self.message_callback = None

    async def start(self):
        # Create and start a server
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f'Serving on {self.host}:{self.port}')

    async def connect_to_peer(self, peer_host, peer_port):
        # Connect to a peer
        self.reader, self.writer = await asyncio.open_connection(peer_host, peer_port)
        print(f'Connected to peer at {peer_host}:{peer_port}')

    async def handle_client(self, reader, writer):
        # Handle incoming client connections
        self.peers.append((reader, writer))
        addr = writer.get_extra_info('peername')
        print(f'Connected to {addr}')

        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            # Call the message callback method to handle the received message
            if self.message_callback:
                await self.message_callback(message)

        print(f'Connection closed to {addr}')
        self.peers.remove((reader, writer))

    async def broadcast(self, message):
        # Send a message to all connected peers
        for reader, writer in self.peers:
            writer.write(message.encode())
            await writer.drain()


class P2PApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P Chat")
        self.root.geometry("450x650")
        self.root.configure(bg="#000000")  # Black background for the main window

        # Frame for chat area
        self.frame = tk.Frame(root, bg="#1e1e1e")  # Dark gray background for the chat frame
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # ScrolledText widget for displaying messages
        self.text_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, state='disabled', bg="#1e1e1e", fg="#ffffff", font=("Arial", 12))
        self.text_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Entry widget for typing messages
        self.entry_frame = tk.Frame(root, bg="#000000")  # Black background for the entry frame
        self.entry_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, bg="#333333", fg="#ffffff", font=("Arial", 12))  # Dark background with white text
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.send_message)

        # Send button
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg="#007acc", fg="#ffffff", font=("Arial", 12, "bold"))
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.start_network()

    def start_network(self):
        self.loop = asyncio.get_event_loop()
        self.network_thread = Thread(target=self.network_loop, daemon=True)
        self.network_thread.start()

    def network_loop(self):
        self.loop.run_until_complete(self.run())

    async def run(self):
        # Replace with your network node implementation
        self.node = PeerNode('127.0.0.1', 8888)
        asyncio.create_task(self.node.start())
        await self.node.connect_to_peer('127.0.0.1', 8889)
        
        while True:
            await asyncio.sleep(1)

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"You: {message}\n")
            self.text_area.config(state='disabled')
            self.entry.delete(0, tk.END)
            asyncio.run_coroutine_threadsafe(self.node.broadcast(message), self.loop)

    # mozda bude menjano 2
    async def receive_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, f"Peer: {message}\n")
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = P2PApp(root)
    root.mainloop()
