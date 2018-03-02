#!/usr/bin/env python3

import tkinter as tk

class AddressBookApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        pass

# Main entry point
root = tk.Tk()
app = AddressBookApp(master=root)
app.mainloop()