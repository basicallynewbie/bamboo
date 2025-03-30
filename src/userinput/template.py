import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from re import search

class Template:
    def __init__(
            self, 
            language: dict, 
            item: str, 
            masters: ttk.Frame,
            pool: list,
            font: tkFont.Font,
            string_cmd_name: str = None,
            **kwargs
            ) -> None:
        self.language = language
        self.item = item
        self.pool = pool
        self.font = font
        self.kwargs = kwargs
        if self.item in self.language.keys():
            name = self.language[self.item]
        else:
            name = self.item
        self.frame = ttk.Frame(masters)
        self.frame.pack(expand=True, fill='x', padx=1, pady=1)
        self.frame.rowconfigure(0, weight=1, uniform="fred")
        self.frame.columnconfigure(1, weight=1, uniform="fred")

        self.string = tk.StringVar(value=name)
        ttk.Entry(
            master=self.frame,
            textvariable=self.string, 
            font=self.font,
            validate='key', 
            validatecommand=(string_cmd_name, '%P')
            ).grid(column=0, row=0, sticky="nsew", padx=1)
        ttk.Button(
            master=self.frame,
            command=self.selfDestroy,
            text=' - ').grid(column=3, row=0, sticky="nsew", padx=1)
    
    def destroy(self):
            self.frame.destroy()

    def selfDestroy(self):
            self.destroy()
            for i in self.pool:
                if i.item == self.item:
                    self.pool.remove(i)

    def __del__(self):
        ...

    def packing(self, *args, **kwargs) -> None:
        self.variable = None

    def updateStr(self) -> None:
        if self.item in self.language.keys():
            self.string.set(self.language[self.item])

    def getStr(self) -> str:
        if self.item in self.language:
            return self.item
        else:
            return self.string.get()

    def getVar(self) -> any:
        return self.variable.get()
    
    def setVar(self, value) -> None:
        self.variable.set(value)

class BoolTemplate(Template):
    def packing(self, default: bool = False, *args, **kwargs) -> None:
        self.variable = tk.BooleanVar(value=default)
        radio = ttk.Frame(self.frame)
        radio.grid(column=1, row=0, sticky="nsew", padx=1)
        ttk.Radiobutton(
            radio, 
            text="true", 
            variable=self.variable, 
            value=True, 
            ).pack(side='left')
        ttk.Radiobutton(
            radio, 
            text="false", 
            variable=self.variable, 
            value=False, 
            ).pack(side='left')

class StrTemplate(Template):
    def packing(
            self,
            default: str = '',
            variable_cmd_name: str = None
            ) -> None:
        self.variable = tk.StringVar(value=default)
        self.input = ttk.Entry(
            master=self.frame,
            font=self.font,
            textvariable=self.variable,
            validate='key', 
            validatecommand=(variable_cmd_name, '%P')
            )
        self.input.grid(column=1, row=0, sticky="nsew", padx=1)
    
    def setStr(self, value: str) -> None:
        self.string.set(value)

class IntTemplate(Template):
    def packing(
            self, 
            default: str = '',
            variable_cmd_name: str = None
            ) -> None:
        self.variable = tk.IntVar(value=default)
        tk.Spinbox(
            master=self.frame,
            font=self.font,
            textvariable=self.variable, 
            from_=-999999,
            to=999999,
            validate='key', 
            validatecommand=(variable_cmd_name, '%P'),
            width=12
            ).grid(column=1, row=0, sticky="nsew", padx=1)

class FloatTemplate(Template):
    def packing(
            self, 
            default: float = 0.5,
            variable_cmd_name: str = None
            ) -> None:
        self.variable = tk.DoubleVar(value=default)
        self.after = tk.IntVar(value=int(str(self.variable.get()).split('.')[-1]))
        frame = ttk.Frame(self.frame)
        frame.grid(column=1, row=0, sticky="nsew", padx=1)
        frame.columnconfigure(1, weight=1, uniform="fred")
        ttk.Label(frame, text='0.', font=self.font).grid(column=0, row=0, sticky="nsew")
        tk.Spinbox(
            master=frame,
            font=self.font,
            textvariable=self.after, 
            from_=0,
            to=999999,
            validate='key', 
            validatecommand=(variable_cmd_name, '%P'),
            width=10
            ).grid(column=1, row=0, sticky="nsew")
    
    def getVar(self) -> float:
        after = 0
        if bool(self.after.get()):
            after = self.after.get()
        self.variable.set(float(f'0.{after}'))
        return self.variable.get()
    
    def setVar(self, value) -> None:
        self.variable.set(value)
        if bool(search(r'\.', str(self.variable.get()))):
            self.after.set(int(str(self.variable.get()).split('.')[-1]))
        else:
            self.after.set(0)

class ListTemplate(Template):
    def packing(
            self, 
            default: str = '',
            variable_cmd_name: str = None) -> None:
        self.variable_cmd_name = variable_cmd_name
        self.variable = default
        self.list = []
        ttk.Button(master=self.frame, command=self.subWindow, text='edit'
                    ).grid(column=1, row=0, sticky="nsew", padx=1)
    
    def getVar(self) -> any:
        return self.variable

    def setVar(self, value) -> None:
        self.variable.clear()
        self.variable = value
    
    def subWindow(self):
        def add(input = ''):
            temp = tk.StringVar(value=input)
            ttk.Entry(
            master=str_frame,
            font=self.font,
            textvariable=temp,
            validate="key",
            validatecommand=(self.variable_cmd_name, "%P"),
            ).pack(pady=3)
            self.list.append(temp)

        def save():
            self.variable.clear()
            self.variable.extend([i.get() for i in self.list])

        self.list.clear()
        window = tk.Toplevel(self.kwargs['root'], takefocus=True)
        window.title(self.item)
        window.geometry('500x500+300+200')
        frame = ttk.Frame(window)
        frame.pack(expand=True, fill='both', padx=1, pady=1)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(padx=1, pady=1)
        ttk.Button(
            master=btn_frame,
            command=add,
            text=' + ').pack(padx=2, side='left')
        ttk.Button(
            master=btn_frame,
            command=save,
            text='save').pack(padx=2, side='left')
        str_frame = ttk.Frame(frame)
        str_frame.pack(padx=1, pady=1, fill='x')
        for i in self.variable:
            add(i)

class DictTemplate(Template):
    def packing(self, default, *args, **kwargs) -> None:
        self.variable = default
        self.list = []
        ttk.Button(master=self.frame, command=self.subWindow, text='edit'
                    ).grid(column=1, row=0, sticky="nsew", padx=1)
    
    def getVar(self) -> any:
        return self.variable

    def setVar(self, value) -> None:
        self.variable.clear()
        self.variable.update(value)

    def subWindow(self):
        def add(key = '', value = ''):
            temp = StrTemplate(
                language={}, 
                item=f'custom_{self.counter}',
                masters=str_frame,
                pool=self.list,
                font=self.font
                )
            temp.packing()
            if bool(key):
                temp.setStr(key)
            if bool(value):
                temp.setVar(value)
            self.list.append(temp)
            self.counter += 1

        def save():
            self.variable.clear()
            self.variable.update({x.getStr(): x.getVar() for x in self.list})

        self.list.clear()      
        self.counter = 0
        window = tk.Toplevel(self.kwargs['root'], takefocus=True)
        window.title(self.item)
        window.geometry('600x500+300+200')
        frame = ttk.Frame(window)
        frame.pack(expand=True, fill='both', padx=1, pady=1)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(padx=1, pady=1)
        ttk.Button(
            master=btn_frame,
            command=add,
            text=' + ').pack(padx=2, side='left')
        ttk.Button(
            master=btn_frame,
            command=save,
            text='save').pack(padx=2, side='left')
        str_frame = ttk.Frame(frame)
        str_frame.pack(padx=1, pady=1, fill='x')
        for key, value in self.variable.items():
            add(key, value)
