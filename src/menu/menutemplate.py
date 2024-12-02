import tkinter as tk

class MenuTemplate:
    def __init__(self, master: tk.Menu, menu_object: tk.Menu) -> None:
        self.master = master
        self.menu_object = menu_object

    def menuModule(self, command_list) -> None:
        for labels, commands, accelerators in command_list:
            self.menu_object.add_command(label=labels, command=commands, accelerator=accelerators)

    def addMenu(self, menu_label) -> None:
        self.master.add_cascade(label=menu_label, menu=self.menu_object)

    def __call__(self, menu_label, command_list) -> None:
        self.menuModule(command_list)
        self.addMenu(menu_label)