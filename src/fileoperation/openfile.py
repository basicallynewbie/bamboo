from tkinter.filedialog import askopenfilename
from src.importjson import importJson

def openFile(instance, jsonpath: str, target_dict: dict):
    newjsonpath = askopenfilename(defaultextension='json',filetypes=[('Json Files','*.json')])
    try:
        if bool(newjsonpath):
            if newjsonpath != jsonpath:
                jsonpath = newjsonpath
                target_dict.clear()
                importJson(newjsonpath, target_dict)
                instance.newVar()
    except FileNotFoundError:
        pass