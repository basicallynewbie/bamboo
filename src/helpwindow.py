import tkinter as tk

class Help:
    def __init__(self, help_file: str) -> None:
        help_window = tk.Toplevel()
        help_window.title('Help')

        help_text = tk.Text(help_window, width= 140)
        help_text.pack()

        with open(help_file, 'r', encoding='UTF-8') as file:
            content = file.read()
            help_text.config(state='normal')
            help_text.delete(1.0, tk.END)
            help_text.insert(tk.END, content)
            help_text.config(state='disabled')