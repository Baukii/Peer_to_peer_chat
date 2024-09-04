import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import asyncio
from threading import Thread

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Upisi username")
        self.geometry("400x300")
        
        # Create frames
        self.login_frame = tk.Frame(self, bg="#1e1e1e")
        self.login_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_frame = tk.Frame(self, bg="#1e1e1e")
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Initialize frames
        self.init_login_frame()
        self.init_chat_frame()
        
        self.username = None
        
        # Display the login frame initially
        self.show_frame(self.login_frame)
    
    def init_login_frame(self):
        # Username Label
        tk.Label(self.login_frame, text="Username:",bg="#000000", fg="#FFFFFF").pack(pady=10)
        
        # Username Entry
        self.username_entry = tk.Entry(self.login_frame, bg="#000000", fg="#FFFFFF")
        self.username_entry.pack(pady=5)
        
        # Send Button
        send_button = tk.Button(self.login_frame, text="Send", bg="blue",fg="#FFFFFF", command=self.switch_to_chat)
        send_button.pack(pady=10)
    
    def init_chat_frame(self):
        # Chatbox (Text widget)
        self.chatbox = tk.Text(self.chat_frame, wrap='word', bg='#000000', fg='#FFFFFF')
        self.chatbox.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Send Message Entry
        self.message_entry = tk.Entry(self.chat_frame, bg="#000000", fg="#FFFFFF")
        self.message_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.message_entry.bind() #popuni
    
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
            self.show_frame(self.chat_frame)
            self.chatbox.insert('end', f"{username} has joined the chat.\n")
            self.chatbox.yview('end')
        else:
            messagebox.showwarning("Input Error", "Please enter a username.")
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
                if self.username:  # Ensure username is set
                    display_message = f"{self.username}: {message}"
                else:
                    display_message = f"Unknown: {message}"

                self.chatbox.insert('end', f"{display_message}\n")
                self.chatbox.yview('end')
                
                with open("messages.txt", mode="wt") as file:
                    file.write(f"{display_message}\n")
                    
                self.message_entry.delete(0, 'end')

        else:
            messagebox.showwarning("Input Error", "Please enter a message.")

    def append_message(self, message):
        self.chatbox.config(state='normal')
        self.chatbox.insert('end', f"{message}\n")
        self.chatbox.config(state='disabled')
        self.chatbox.yview('end')  # Scroll to the end to show the new message

if __name__ == "__main__":
    app = Application()
    app.mainloop()

