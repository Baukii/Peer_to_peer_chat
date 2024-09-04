import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import threading
from P2P import Peer  # Ensure this import matches the location and name of your Peer class file

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Upisi username")
        self.width = 450
        self.height = 650
        self.geometry(f"{self.width}x{self.height}")

        self.backend = None  # Backend instance
        self.username = None
        
        # Create frames
        self.login_frame = tk.Frame(self, bg="#1e1e1e")
        self.login_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_frame = tk.Frame(self, bg="#1e1e1e")
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Initialize frames
        self.init_login_frame()
        self.init_chat_frame()
        
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
        if username:
            self.username = username
            self.backend = Peer('0.0.0.0', 15013)
            self.backend.username = self.username
            
            # Start a thread to handle incoming messages
            self.backend_thread = threading.Thread(target=self.listen_for_backend_messages, daemon=True)
            self.backend_thread.start()
            
            self.show_frame(self.chat_frame)
            self.text_area.insert('end', f"{username} has joined the chat.\n")
            self.text_area.yview('end')
        else:
            messagebox.showwarning("Input Error", "Please enter a username.")
    
    def listen_for_backend_messages(self):
        while True:
            message = self.backend.receive_message()
            if message:
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, f"{message}\n")
                self.text_area.config(state='disabled')
                self.text_area.yview(tk.END)
    
    def send_message(self):
        message = self.entry.get()
        if message:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"{self.username}: {message}\n")
            self.text_area.config(state='disabled')
            self.text_area.yview(tk.END)
            self.entry.delete(0, tk.END)
            
            if self.backend:
                self.backend.send_message(message)
    
    def handle_return(self, event):
        self.send_message()

    def save_chat_history(self):
        try:
            with open("message_file.txt", 'a') as file:
                file.write(self.text_area.get("1.0", tk.END))
        except Exception as e:
            print(f"Error saving chat history to file: {e}")

    def on_closing(self):
        self.save_chat_history()
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
