import tkinter as tk
from tkinter import messagebox, scrolledtext
from threading import Thread
import asyncio
import socket
from P2P import Peer

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.geometry("450x650")

        # Create frames
        self.login_frame = tk.Frame(self, bg="#1e1e1e")
        self.login_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_frame = tk.Frame(self, bg="#1e1e1e")

        # Initialize frames
        self.init_login_frame()
        self.init_chat_frame()

        self.username = None
        self.peer = None

        # Display the login frame initially
        self.show_frame(self.login_frame)
    
    def init_login_frame(self):
        tk.Label(self.login_frame, text="Username:", bg="#000000", fg="#FFFFFF").pack(pady=10)
        self.username_entry = tk.Entry(self.login_frame, bg="#000000", fg="#FFFFFF")
        self.username_entry.pack(pady=5)
        send_button = tk.Button(self.login_frame, text="Send", bg="blue", fg="#FFFFFF", command=self.switch_to_chat)
        send_button.pack(pady=10)
    
    def init_chat_frame(self):
        self.frame = tk.Frame(self.chat_frame, bg="#1e1e1e")
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, state='disabled', bg="#1e1e1e", fg="#ffffff", font=("Arial", 12))
        self.text_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.entry_frame = tk.Frame(self.chat_frame, bg="#000000")
        self.entry_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry = tk.Entry(self.entry_frame, bg="#333333", fg="#ffffff", font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.handle_return)
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg="#007acc", fg="#ffffff", font=("Arial", 12, "bold"))
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def show_frame(self, frame):
        frame.pack(fill='both', expand=True)
        if frame == self.login_frame:
            self.chat_frame.pack_forget()
        else:
            self.login_frame.pack_forget()
    
    def switch_to_chat(self):
        username = self.username_entry.get()
        Peer.username=username
        if username:
            self.username = username
            self.show_frame(self.chat_frame)
            self.text_area.insert('end', f"{username} has joined the chat.\n")
            self.text_area.yview('end')

            # Start peer communication
            self.start_network()
        else:
            messagebox.showwarning("Input Error", "Please enter a username.")


    def start_network(self):
        self.loop = asyncio.get_event_loop()
        self.peer = Peer('0.0.0.0', 15013)
        self.network_thread = Thread(target=self.network_loop, daemon=True)
        self.network_thread.start()

    def network_loop(self):
        try:
            self.loop.run_until_complete(self.peer.listen_for_messages())
        except Exception as e:
            print(f"Network error: {e}")

    def send_message(self):
        message = self.entry.get()
        if message:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"{self.username}: {message}\n")
            self.text_area.config(state='disabled')
            self.text_area.yview(tk.END)
            self.entry.delete(0, tk.END)

            if self.peer:
                self.peer.send_message(message)

    def save_chat_history(self):
        try:
            with open("message_file.txt", 'a') as file:
                file.write(self.text_area.get("1.0", tk.END))
        except Exception as e:
            print(f"Error saving chat history to file: {e}")

    def on_closing(self):
        self.save_chat_history()
        self.destroy()

    def handle_return(self, event):
        self.send_message()

if __name__ == "__main__":
    app = Application()
    app.mainloop()