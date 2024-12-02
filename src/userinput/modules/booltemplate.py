from src.userinput.modules.inputtemplate import *

class BoolTemplate(Template):
    def packing(self, master: tk.Frame) -> None:
        self.string = tk.StringVar(value=self.language[self.item])
        self.variable = tk.IntVar()
        self.button = tk.Checkbutton(
            master=master,
            textvariable=self.string, 
            variable=self.variable, 
            onvalue=1,
            offvalue=0,
            ).pack(side='left')

    def getVar(self) -> bool:
        if self.variable.get() == 1:
            return True
        else:
            return False

    def toggle(self) -> None:
        if self.getVar() and self.variable.get() == 1:
            pass
        elif not self.getVar() and self.variable.get() == 0:
            pass
        else:
            self.button.toggle()