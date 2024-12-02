import tkinter as tk

class Template:
    def __init__(self, language: dict, item: str) -> None:
        self.language = language
        self.item = item

    def packing(self, *args, **kwargs) -> None:
        self.string = None
        self.variable = None

    def updateStr(self) -> None:
        self.string.set(self.language[self.item])

    def getVar(self) -> any:
        return self.variable.get()
    
    def getStr(self) -> str:
        return self.string.get()
    
    def setVar(self, value) -> None:
        return self.variable.set(value)
