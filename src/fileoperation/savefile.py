from tkinter.filedialog import asksaveasfilename
from json import dump

def saveFile(instance, jsonpath: str, target_dict: dict) -> None:
    if bool(instance.check()):
        if not bool(jsonpath):
            jsonpath = asksaveasfilename(defaultextension='.json', filetypes=[('Json Files','*.json')])
        try:
            with open(jsonpath, 'w', encoding='UTF-8') as file:
                dump(target_dict, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            pass
    else:
        instance.alert('can only save when no error exist')

def saveFileAs(instance, jsonpath: str, target_dict: dict) -> None:
    if bool(instance.check()):
        try:
            with open(asksaveasfilename(defaultextension='.json', filetypes=[('Json Files','*.json')]), 'w', encoding='UTF-8') as file:
                dump(target_dict, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            pass
    else:
        instance.alert('can only save when no error exist')