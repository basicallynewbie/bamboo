import tkinter as tk
import tkinter.font as tkFont


class Help:
    def __init__(self, help_file: str, font_dict: dict) -> None:
        help_window = tk.Toplevel()
        help_window.title("Help")
        self.font = tkFont.Font(family=font_dict['font'], size=font_dict['size'])

        help_text = tk.Text(help_window, font=self.font)
        help_text.pack()

        try:
            with open(help_file, "r", encoding="UTF-8") as file:
                content = file.read()
            help_text.config(state="normal")
            help_text.delete(1.0, tk.END)
            help_text.insert(tk.END, content)
            help_text.config(state="disabled")
        except FileNotFoundError:
            help_file = "help/english.txt"
            with open(help_file, "r", encoding="UTF-8") as file:
                content = file.read()
            help_text.config(state="normal")
            help_text.delete(1.0, tk.END)
            help_text.insert(tk.END, content)
            help_text.config(state="disabled")
