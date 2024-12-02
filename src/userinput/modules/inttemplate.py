from src.userinput.modules.inputtemplate import *

class IntTemplate(Template):
    def packing(self, masters: tk.Frame , cmd_name: str, default: int = 0) -> None:
        integer_frame = tk.Frame(masters)
        self.string = tk.StringVar(value=self.language[self.item])
        tk.Label(integer_frame, textvariable=self.string).grid(row=0, column=0)
        self.variable = tk.IntVar(value=default)
        integer = tk.Spinbox(
            master=integer_frame,
            textvariable=self.variable, 
            from_=0,
            to=999999,
            validate='key', 
            validatecommand=(cmd_name, '%P'),
            width=12
            )
        integer.grid(row=0, column=1)
        integer_frame.pack(side='left')