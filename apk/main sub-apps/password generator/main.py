import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import secrets
import re
import math

class SimplePasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Password Generator")
        self.root.geometry("600x400")
        
        # Create widgets
        tk.Label(root, text="Password Generator", font=("Arial", 20)).pack(pady=20)
        
        # Length
        tk.Label(root, text="Length:").pack()
        self.length_var = tk.IntVar(value=16)
        tk.Scale(root, from_=8, to=32, variable=self.length_var, orient="horizontal").pack()
        
        # Generate button
        tk.Button(root, text="Generate Password", command=self.generate, bg="blue", fg="white").pack(pady=20)
        
        # Password display
        self.password_var = tk.StringVar()
        tk.Entry(root, textvariable=self.password_var, font=("Courier", 14), width=40).pack(pady=10)
        
        # Copy button
        tk.Button(root, text="Copy to Clipboard", command=self.copy).pack()
        
        # Generate first password
        self.generate()
    
    def generate(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(self.length_var.get()))
        self.password_var.set(password)
    
    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_var.get())
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Run the app
root = tk.Tk()
app = SimplePasswordGenerator(root)
root.mainloop()
