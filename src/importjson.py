from json import load, decoder
from codecs import open as opens
import tkinter.messagebox as messagebox


def importJson(jsonfile: str, target_json: dict, encode: str = "utf-8-sig") -> None:
    try:
        with opens(jsonfile, "r", encoding=encode) as f:
            data = load(f)
            target_json.update(data)
    except decoder.JSONDecodeError:
        messagebox.showerror(title="Error", message=f"{jsonfile} is not properly json formated!")
    except UnicodeDecodeError:
        messagebox.showerror(title="Error", message=f"cannot decode {jsonfile}!")
