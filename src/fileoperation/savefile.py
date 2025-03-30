from tkinter.filedialog import asksaveasfilename
from json import dump

class SaveFileAs:
    def __init__(self, instance, target_dict: dict, source_jsonpath: list) -> None:
        self.instance = instance
        self.target_dict = target_dict
        self.source_jsonpath = source_jsonpath
        self.action()

    def askPath(self) -> str:
        self.jsonpath = asksaveasfilename(defaultextension='.json', filetypes=[('Json Files','*.json')])
        if bool(self.jsonpath):
                if self.jsonpath not in self.source_jsonpath:
                    self.source_jsonpath.clear()
                    self.source_jsonpath.append(self.jsonpath)

    def save(self) -> None:
        if bool(self.instance.check()):
            try:
                with open(self.jsonpath, 'w', encoding='utf-8') as file:
                    dump(self.target_dict, file, indent=4, ensure_ascii=False)
            except FileNotFoundError:
                pass
        else:
            self.instance.alert('can only save when no error exist')

    def action(self) -> None:
        self.askPath()
        self.save()

class SaveFile(SaveFileAs):
    def action(self) -> None:
        if not bool(self.source_jsonpath):
            self.askPath()
        else:
            self.jsonpath = self.source_jsonpath[0]
        self.save()
