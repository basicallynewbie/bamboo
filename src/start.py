import tkinter as tk
import tkinter.messagebox as messagebox
from pathlib import Path
from src.importjson import importJson
from src.fileoperation.newfile import NewFile
from src.fileoperation.openfile import OpenFile
from src.fileoperation.savefile import SaveFile, SaveFileAs
from src.menu.menutemplate import MenuTemplate
from src.menu.rootmenu import RootMenu
from src.menu.popmenu import PopMenu
from src.userinput.userinput import UserInput
from src.helpwindow import Help
from src.aboutwindow import About
from sys import exit as exits


class Start:
    def __init__(self, config: dict) -> None:
        language = config["language"]
        config.pop("language")
        self.font_dict = config
        self.language = {}
        if Path(f"language/{language}.json").exists():
            importJson(f"language/{language}.json", self.language)
        elif Path("language/english.json").exists():
            messagebox.showerror(
                title="Error", 
                message=f"cannot find language/{language}.json, using language/english.json"
            )
            importJson("language/english.json", self.language)
        else:
            messagebox.showerror(
                title="Error", message=f"cannot find language/{language}.json"
            )
            exits(f"cannot find language/{language}.json")

        if Path(f"help/{language}.txt").exists():
            self.help_file = f"help/{language}.txt"
        elif Path("language/english.json").exists():
            self.help_file = f"help/english.txt"
        else:
            messagebox.showerror(
                title="Error",
                message=f"cannot find help/{language}.txt, Help is disabled",
            )
            self.bindHelp = self.disable

        self.target_dict = {"reference": {}, "metadata": {}}
        self.jsonpath = []

    def rootWindow(self) -> None:
        self.window = tk.Tk()
        self.window.title("Bamboo")
        self.window.geometry("800x600+200+100")

    def rootManu(self) -> None:
        self.mainmenu = RootMenu(self.window, self.language, self.target_dict)
        self.mainmenu.startMenu()

    def languagemenu(self) -> None:
        languagepath = Path("language")
        self.language_list = []
        for i in languagepath.iterdir():
            if i.is_file:
                self.language_list.append(
                    [i.stem, lambda path=str(i): self.updateLanguage(path), None]
                )

    def packMenu(self) -> None:
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.filemenu)(
            self.language["file"],
            [
                [self.language["new"], self.bindNew, "Ctrl+n"],
                [self.language["open"], self.bindOpen, "Ctrl+o"],
                [self.language["save"], self.bindSave, "Ctrl+s"],
                [self.language["save as"], self.bindSaveAs, "Ctrl+Shift+S"],
                [self.language["exit"], self.window.quit, None],
            ],
        )
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.editmenu)(
            self.language["eidt"],
            [
                [self.language["cut"], self.bindCut, "Ctrl+x"],
                [self.language["copy"], self.bindCopy, "Ctrl+c"],
                [self.language["paste"], self.bindPaste, "Ctrl+v"],
                [self.language["delete"], None, "Delete"],
            ],
        )
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.languagemenu)(
            self.language["language"], self.language_list
        )
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.helpmenu)(
            self.language["help"],
            [
                [self.language["help"], self.bindHelp, "Ctrl+h"],
                [self.language["about"], lambda: About(self.font_dict), None],
            ],
        )

    def popManu(self) -> None:
        self.pop = PopMenu()
        self.pop.startMenu(self.window, self.language)

    def inputs(self) -> None:
        self.user_input = UserInput(
            self.window, self.language, self.target_dict, self.font_dict
        )
        self.user_input.startInput()

    def updateLanguage(self, jsonfile: str) -> None:
        self.mainmenu.delMenu()
        self.pop.delMenu()
        try:
            importJson(jsonfile, self.language)
        except:
            messagebox.showerror(
                title="Error", 
                message=f"cannot load {jsonfile}, using language/english.json"
            )
            importJson("language/english.json", self.language)
        self.help_file = jsonfile.replace("language", "help")
        self.help_file = self.help_file.replace("json", "txt")
        if not Path(self.help_file).exists():
            self.help_file = f"help/english.txt"
        self.mainmenu.addMenu()
        self.packMenu()
        self.pop.addMenu()
        self.user_input.update()

    def loop(self) -> None:
        self.rootWindow()
        self.rootManu()
        self.languagemenu()
        self.packMenu()
        self.binding()
        self.popManu()
        self.inputs()
        self.window.mainloop()

    def bindNew(self, event=None) -> None:
        NewFile(self.jsonpath)

    def bindOpen(self, event=None) -> None:
        OpenFile(self.user_input, self.target_dict, self.jsonpath)

    def bindSave(self, event=None) -> None:
        SaveFile(self.user_input, self.target_dict, self.jsonpath)

    def bindSaveAs(self, event=None) -> None:
        SaveFileAs(self.user_input, self.target_dict, self.jsonpath)

    def bindHelp(self, event=None) -> None:
        Help(self.help_file, self.font_dict)

    def bindCut(self, event=None) -> None:
        self.window.focus_get().event_generate("<<Cut>>")

    def bindCopy(self, event=None) -> None:
        self.window.focus_get().event_generate("<<Copy>>")

    def bindPaste(self, event=None) -> None:
        self.window.focus_get().event_generate("<<Paste>>")

    def binding(self) -> None:
        self.window.bind("<Control-n>", func=self.bindNew)
        self.window.bind("<Control-o>", func=self.bindOpen)
        self.window.bind("<Control-s>", func=self.bindSave)
        self.window.bind("<Control-Shift-S>", func=self.bindSaveAs)
        self.window.bind("<Control-h>", func=self.bindHelp)

    def disable(self) -> None:
        pass
