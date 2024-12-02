import tkinter as tk

class RootMenu:
    def __init__(self, master: tk.Tk, language: dict, target_dict: dict) -> None:
        self.master = master
        self.language = language
        self.target_dict = target_dict
        self.rootmenu = tk.Menu(self.master)

    def startMenu(self) -> None:
        self.addMenu()
        self.master.config(menu=self.rootmenu)

    def delMenu(self) -> None:
        self.rootmenu.delete(0, 'end')

    def addMenu(self) -> None:
        self.filemenu = tk.Menu(self.rootmenu, tearoff=False)
        self.editmenu = tk.Menu(self.rootmenu, tearoff=False)
        self.languagemenu = tk.Menu(self.rootmenu, tearoff=False)
        self.helpmenu = tk.Menu(self.rootmenu, tearoff=False)
