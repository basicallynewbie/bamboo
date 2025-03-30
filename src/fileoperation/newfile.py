from tkinter.filedialog import asksaveasfilename
import tkinter.messagebox as messagebox

class NewFile:
    def __init__(self, source_jsonpath: list) -> None:
        self.source_jsonpath = source_jsonpath
        self.newJsonpath()
        self.createFile()

    def newJsonpath(self) -> str:
        self.jsonpath = asksaveasfilename(defaultextension='json', filetypes=[('Json Files','*.json')])
        if bool(self.jsonpath):
            if self.jsonpath not in self.source_jsonpath:
                self.source_jsonpath.clear()
                self.source_jsonpath.append(self.jsonpath)
        return self.jsonpath
    
    def createFile(self) -> None:
        try:
            with open(self.jsonpath, 'w', encoding='utf-8') as file:
                file.write('')
        except FileNotFoundError:
            self.jsonpath = ''
            pass
        except PermissionError:
            messagebox.showerror(title='Error', message='no permission to create file!')
