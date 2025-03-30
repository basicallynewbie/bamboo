from tkinter.filedialog import askopenfilename
import tkinter as tk
from src.importjson import importJson

class OpenFile:
    def __init__(self, instance, target_dict: dict, source_jsonpath: list) -> None:
        self.instance = instance
        self.target_dict = target_dict
        self.source_jsonpath = source_jsonpath
        self.window()
    
    def update(self) -> None:
        jsonpath = askopenfilename(defaultextension='json',filetypes=[('Json Files','*.json')])
        try:
            if bool(jsonpath):
                if jsonpath not in self.source_jsonpath:
                    self.source_jsonpath.clear()
                    self.source_jsonpath.append(jsonpath)
                    self.target_dict.clear()
                    importJson(jsonpath, self.target_dict, self.encode.get())
                    self.instance.newVar()
                    self.toplevel.destroy()
        except FileNotFoundError:
            pass
    
    def window(self) -> None:
        self.toplevel = tk.Toplevel()
        self.toplevel.title("open file")
        self.toplevel.geometry('240x120+400+300')
        self.toplevel.maxsize(240, 120)
        self.toplevel.grid_columnconfigure(0, weight=1, uniform="fred")
        tk.Label(self.toplevel, text='  ').grid(column=0, row=0, sticky='NW')
        tk.Label(self.toplevel, text=' encode ').grid(column=0, row=1, sticky='SENW')
        self.encode = tk.StringVar(value='utf-8')
        tk.Entry(master=self.toplevel, textvariable=self.encode).grid(column=1, row=1, sticky='NW')
        tk.Label(self.toplevel, text='  ').grid(column=0, row=2, sticky='NW')
        tk.Button(
            self.toplevel, 
            text='open', 
            width=20, 
            command=self.update
            ).grid(column=0, row=3, columnspan=2, sticky='SENW')
