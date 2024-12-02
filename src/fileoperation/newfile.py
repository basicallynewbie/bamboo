from tkinter.filedialog import asksaveasfilename

def newFile(jsonpath: str) -> None:
    jsonpath = asksaveasfilename(defaultextension='json', filetypes=[('Json Files','*.json')])
    try:
        with open(jsonpath, 'w') as file:
            file.write('')
    except FileNotFoundError:
        pass