from src.userinput.modules.inputtemplate import *

class StrTemplate(Template):
    def packing(
            self, 
            masters: tk.Canvas, 
            counter: int,
            name: str, 
            name_cmd_name: str = None, 
            str_cmd_name: str = None,  
            default: str = '', 
            states: str = 'normal'
            ) -> None:
        self.masters = masters
        self.name = name
        self.string = tk.StringVar(value=self.name)
        self.stringbox = tk.Entry(
            master=self.masters,
            textvariable=self.string, 
            validate='key', 
            validatecommand=(name_cmd_name, '%P'),
            state = states,
            width=20
            )
        self.masters.create_window(
            10, 10+25*(counter), 
            window=self.stringbox, 
            anchor='nw', 
            tags=self.name
            )
        
        self.variable = tk.StringVar(value=default)
        self.variablebox = tk.Entry(
            master=self.masters,
            textvariable=self.variable,
            validate='key', 
            validatecommand=(str_cmd_name, '%P'),
            width=77
            )
        self.masters.create_window(
            161, 10+25*(counter), 
            window=self.variablebox, 
            anchor='nw', 
            tags=self.name+'v'
            )

    def remove(self) -> None:
        self.masters.delete(self.name)
        self.masters.delete(self.name+'v')