import tkinter as tk

class About:
    def __init__(self) -> None:
        about_window = tk.Toplevel()
        about_window.title('about')

        about_text = tk.Text(about_window, width= 80)
        about_text.pack()

        with open('LICENSE', 'r', encoding='UTF-8') as file:
            content = file.read()
            about_text.config(state='normal')
            about_text.delete(1.0, tk.END)
            about_text.insert(tk.END, content)
            about_text.config(state='disabled')