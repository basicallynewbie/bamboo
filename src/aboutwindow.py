import tkinter as tk
import tkinter.font as tkFont

class About:
    def __init__(self, font_dict: dict) -> None:
        about_window = tk.Toplevel()
        about_window.title('about')
        self.font = tkFont.Font(family=font_dict['font'], size=font_dict['size'])

        about_text = tk.Text(about_window, font=self.font)
        about_text.pack()

        with open('LICENSE', 'r', encoding='UTF-8') as file:
            content = file.read()
            about_text.config(state='normal')
            about_text.delete(1.0, tk.END)
            about_text.insert(tk.END, content)
            about_text.config(state='disabled')
