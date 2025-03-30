import tkinter as tk

class PopMenu:
    def __init__(self) -> None:
        pass
    
    def on_right_click(self, event) -> None:
        self.popmenu.post(event.x_root, event.y_root)
    
    def startMenu(self, master: tk.Tk, language: dict) -> None:
        self.master = master
        self.language = language
        self.popmenu = tk.Menu(self.master, tearoff=False)
        self.addMenu()
        self.master.bind("<Button-3>", func=self.on_right_click)

    def delMenu(self) -> None:
        self.popmenu.delete(0, 'end')
    
    def addMenu(self) -> None:
        self.popmenu.add_command(label=self.language['cut'],
            command=lambda:self.master.focus_get().event_generate('<<Cut>>'),
            accelerator='Ctrl+x'
            )
        self.popmenu.add_command(label=self.language['copy'],
            command=lambda:self.master.focus_get().event_generate('<<Copy>>'),
            accelerator='Ctrl+c'
            )
        self.popmenu.add_command(label=self.language['paste'],
            command=lambda:self.master.focus_get().event_generate('<<Paste>>'),
            accelerator='Ctrl+v'
            )
