import tkinter as tk
from pathlib import Path
from src.importjson import importJson
from src.fileoperation.newfile import newFile
from src.fileoperation.openfile import openFile
from src.fileoperation.savefile import saveFile, saveFileAs
from src.menu.menutemplate import MenuTemplate
from src.menu.rootmenu import RootMenu
from src.menu.popmenu import PopMenu
from src.userinput.userinput import UserInput
from src.helpwindow import Help
from src.aboutwindow import About

class Start:
    def __init__(self, language: str) -> None:
        self.language = {}
        try:
            importJson(f"language/{language}.json", self.language)
        except:
            exit(f"cannot find language/{language}.json")
        self.help_file = f'help/{language}.txt'
        self.target_dict = {'reference':{}, 'metadata':{}}
        self.jsonpath = ''

    def rootWindow(self) -> None:
        self.window = tk.Tk()
        self.window.title('Bamboo')
        self.window.geometry('750x500+300+200')
        self.window.maxsize(width='750', height='1080')

    def rootManu(self) -> None:
        self.mainmenu = RootMenu(self.window, self.language, self.target_dict)
        self.mainmenu.startMenu()

    def languagemenu(self) -> None:
        languagepath = Path('language')
        self.language_list = []
        for i in languagepath.iterdir():
            if i.is_file:
                self.language_list.append([
                    i.stem, 
                    lambda path=str(i):self.updateLanguage(path), 
                    None
                    ])
    
    def submenu(self) -> None:
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.filemenu)(self.language['file'], [
            [self.language['new'], self.bindNew, 'Ctrl+n'],
            [self.language['open'], self.bindOpen, 'Ctrl+o'],
            [self.language['save'], self.bindSave, 'Ctrl+s'],
            [self.language['save as'], self.bindSaveAs, 'Ctrl+Shift+S'],
            [self.language['exit'], self.window.quit, None]
            ])
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.editmenu)(self.language['eidt'], [
            [self.language['cut'], self.bindCut, 'Ctrl+x'],
            [self.language['copy'], self.bindCopy, 'Ctrl+c'],
            [self.language['paste'], self.bindPaste, 'Ctrl+v'],
            [self.language['delete'], None, 'Delete']
            ])
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.languagemenu)\
                        (self.language['language'], self.language_list)
        MenuTemplate(self.mainmenu.rootmenu, self.mainmenu.helpmenu)(self.language['help'], [
            [self.language['help'], self.bindHelp, 'Ctrl+h'],
            [self.language['about'], About, None]
            ])

    def popManu(self) -> None:
        self.pop = PopMenu()
        self.pop.startMenu(self.window, self.language)

    def inputs(self) -> None:
        self.user_input = UserInput(self.window, self.language ,self.target_dict)
        self.user_input.startInput()

    def updateLanguage(self, jsonfile) -> None:
        self.mainmenu.delMenu()
        self.pop.delMenu()
        importJson(jsonfile, self.language)
        self.help_file = jsonfile.replace('language', 'help')
        self.help_file = self.help_file.replace('json', 'txt')
        self.mainmenu.addMenu()
        self.submenu()
        self.pop.addMenu()
        self.user_input.update()

    def loop(self) -> None:
        self.rootWindow()
        self.rootManu()
        self.languagemenu()
        self.submenu()
        self.binding()
        self.popManu()
        self.inputs()
        self.window.mainloop()

    def bindNew(self, event = None) -> None:
        newFile(self.jsonpath)

    def bindOpen(self, event = None) -> None:
        openFile(self.user_input, self.jsonpath, self.target_dict)

    def bindSave(self, event = None) -> None:
        saveFile(self.user_input, self.jsonpath, self.target_dict)

    def bindSaveAs(self, event = None) -> None:
        saveFileAs(self.user_input, self.jsonpath, self.target_dict)

    def bindHelp(self, event = None) -> None:
        Help(self.help_file)

    def bindCut(self, event = None) -> None:
        self.window.focus_get().event_generate('<<Cut>>')

    def bindCopy(self, event = None) -> None:
        self.window.focus_get().event_generate('<<Copy>>')

    def bindPaste(self, event = None) -> None:
        self.window.focus_get().event_generate('<<Paste>>')

    def binding(self) -> None:
        self.window.bind('<Control-n>', func=self.bindNew)
        self.window.bind('<Control-o>', func=self.bindOpen)
        self.window.bind('<Control-s>', func=self.bindSave)
        self.window.bind('<Control-Shift-S>', func=self.bindSaveAs)
        self.window.bind('<Control-h>', func=self.bindHelp)
