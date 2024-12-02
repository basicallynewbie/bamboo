from src.userinput.modules.booltemplate import BoolTemplate
from src.userinput.modules.inttemplate import IntTemplate
from src.userinput.modules.strtemplate import StrTemplate
from re import search
import tkinter as tk
import tkinter.messagebox as messagebox

class UserInput:
    ESCAPE_CHAR = r'\\|/|:|\*|\?|"|<|>|\|'

    def __init__(self, master: tk.Tk, language: dict, target_dict: dict) -> None:
        self.master = master
        self.language = language
        self.target_dict = target_dict
        self.reference = {
            'target_folder': '', 'template': '', 'escape': [],
            'index': 0, 'length': 2, 'offset': 0, 
            'subfolder': False,  'series': False, 'separator': '.'
            }
        self.metadata = {'title': '', 'original_title': '', 'season': '01'}

    def startInput(self):
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(fill='x', padx='4px')

        self.reference_frame = tk.Frame(self.master)
        self.reference_frame.pack(fill='x', padx='4px')

        self.metadata_frame = tk.Frame(self.master)
        self.metadata_frame.pack(fill='x', padx='4px')

        self.scrollbar = tk.Scrollbar(self.metadata_frame, cursor='')
        self.scrollbar.pack(side='right', fill='y')

        self.metadata_canvas = tk.Canvas(
            self.metadata_frame, 
            width=800 ,
            height=1200, 
            scrollregion=(0,0,800,1450), 
            yscrollcommand=self.scrollbar.set
            )
        self.metadata_canvas.pack(expand=True)

        self.scrollbar.config(command=self.metadata_canvas.yview)

        self.master.bind('<MouseWheel>', self._on_mousewheel)
        self.master.bind('<Control-k>', self.check)

        self.boolBox()
        self.intBox()
        self.strBox()

    def _on_mousewheel(self, event):
        def delta(event):
            if event.num == 5 or event.delta < 0:
                return 1 
            if event.num == 4 or event.delta > 0:
                return -1 
            else:
                return 0

        self.metadata_canvas.yview_scroll(delta(event), "units")

    def separatorValidate(self, user_input: str) -> bool:
        # %P = value of the entry if the edit is allowed
        if len(user_input) < 2 and not bool(search(self.ESCAPE_CHAR, user_input)):
            return True
        return False

    def intValidate(self, user_input: str) -> bool:
        # %P = value of the entry if the edit is allowed
        if user_input.isdigit():
            if user_input == '0':
                return True
            elif user_input != '0' and user_input[0] != '0' \
                and 0<=int(user_input)<=999999:
                return True
        return False
    
    def strValidate(self, user_input: str) -> bool:
        # %P = value of the entry if the edit is allowed
        if not bool(search(self.ESCAPE_CHAR, user_input)):
            return True
        return False
    
    def escapeValidate(self, user_input: str) -> bool:
        # %P = value of the entry if the edit is allowed
        if not bool(search(self.ESCAPE_CHAR[:18], user_input)):
            return True
        return False
    
    def folderValidate(self, user_input: str) -> bool:
        # %P = value of the entry if the edit is allowed
        if not bool(search(self.ESCAPE_CHAR[7:], user_input)):
            return True
        return False
    
    def nameValidate(self, user_input: str) -> bool:
        # %P = value of the entry if the edit is allowed
        if not bool(search(r'[ \[\]\.,`@\-=+!#$%^&*()<>?/\\\|}{~:;\'"\n\r\t\f]',
                            user_input)):
            return True
        return False

    def boolBox(self) -> None:
        self.series = BoolTemplate(self.language, 'series')
        self.series.packing(self.reference_frame)

        self.subfolder = BoolTemplate(self.language, 'subfolder')
        self.subfolder.packing(self.reference_frame)

        separatorInput = self.reference_frame.register(self.separatorValidate)
        separator_frame = tk.Frame(self.reference_frame)
        self.separator_string = tk.StringVar(value=self.language['separator'])
        tk.Label(separator_frame, textvariable=self.separator_string)\
            .grid(row=0, column=0)
        self.separator_variable = tk.StringVar(value='.')
        separator_stringbox = tk.Entry(
            master=separator_frame,
            textvariable=self.separator_variable, 
            validate='key', 
            validatecommand=(separatorInput, '%P'),
            width=12
            )
        separator_stringbox.grid(row=0, column=1)
        separator_frame.pack(side='left')

    def intBox(self) -> None:
        intInput = self.reference_frame.register(self.intValidate)
        
        self.index = IntTemplate(self.language, 'index')
        self.index.packing(self.reference_frame, intInput, 0)

        self.length = IntTemplate(self.language, 'length')
        self.length.packing(self.reference_frame, intInput, 2)

        self.offset = IntTemplate(self.language, 'offset')
        self.offset.packing(self.reference_frame, intInput, 0)

    def strBox(self) -> None:
        self.strInput = self.metadata_frame.register(self.strValidate)
        self.folderInput = self.metadata_frame.register(self.folderValidate)
        self.nameInput = self.metadata_frame.register(self.nameValidate)
        self.escapeInput = self.metadata_frame.register(self.escapeValidate)
        self.counter = 0

        self.target_folder = StrTemplate(self.language, 'target_folder')
        self.target_folder.packing(
            self.metadata_canvas, 
            self.counter, 
            self.language['target_folder'], 
            self.strInput, 
            self.folderInput, 
            states='readonly'
            )
        self.counter += 1

        self.escape = StrTemplate(self.language, 'escape')
        self.escape.packing(
            self.metadata_canvas, 
            self.counter, 
            self.language['escape'], 
            self.strInput, 
            self.escapeInput, 
            states='readonly'
            )
        self.counter += 1

        self.template = StrTemplate(self.language, 'template')
        self.template.packing(
            self.metadata_canvas, 
            self.counter, 
            self.language['template'], 
            self.strInput, 
            self.strInput, 
            states='readonly'
            )
        self.counter += 1

        self.title = StrTemplate(self.language, 'title')
        self.title.packing(
            self.metadata_canvas, 
            self.counter, 
            self.language['title'], 
            self.strInput, 
            self.strInput, 
            states='readonly'
            )
        self.counter += 1

        self.original_title = StrTemplate(self.language, 'original_title')
        self.original_title.packing(
            self.metadata_canvas, 
            self.counter, 
            self.language['original_title'], 
            self.strInput, 
            self.strInput, 
            states='readonly'
            )
        self.counter += 1

        self.season = StrTemplate(self.language, 'season')
        self.season.packing(
            self.metadata_canvas, 
            self.counter, 
            self.language['season'], 
            self.strInput, 
            self.strInput, 
            default='01', 
            states='readonly'
            )
        self.counter += 1

        self.str_list = []
        self.addcounter = 1

        self.addbutton = tk.Button(
            self.metadata_canvas, text='+', width=20, command=self.addLine)
        
        self.delbutton = tk.Button(
            self.metadata_canvas, text='-', width=20, command=self.delLine)
        
        self.check_string = tk.StringVar(value=self.language['check'])
        self.checkbutton = tk.Button(
            self.metadata_canvas, 
            textvariable=self.check_string, 
            width=20, 
            command=self.check)
        
        self.addbuttoncreate()
        self.delbuttoncreate()
        self.checkbuttoncreate()

    def addLine(self):
        if self.addcounter < 50:
            self.metadata_canvas.delete('addbutton')
            self.metadata_canvas.delete('delbutton')
            self.metadata_canvas.delete('check')
            doublestr = StrTemplate(self.language, f"Custom{str(self.addcounter)}")
            doublestr.packing(
                self.metadata_canvas, 
                self.counter, 
                f"Custom{str(self.addcounter)}", 
                self.nameInput, 
                self.strInput)
            self.addcounter += 1
            self.counter += 1
            self.str_list.append(doublestr)
            self.addbuttoncreate()
            self.delbuttoncreate()
            self.checkbuttoncreate()
        else:
            pass

    def delLine(self):
        if self.addcounter > 1:
            self.metadata_canvas.delete('addbutton')
            self.metadata_canvas.delete('delbutton')
            self.metadata_canvas.delete('check')
            self.str_list[-1].remove()
            self.str_list.pop()
            self.addcounter -= 1
            self.counter -= 1
            self.addbuttoncreate()
            self.delbuttoncreate()
            self.checkbuttoncreate()
        else:
            pass
    
    def addbuttoncreate(self):
        self.metadata_canvas.create_window(
            125, 10+25*self.counter, 
            window=self.addbutton, 
            anchor='n', 
            tags='addbutton')
    
    def delbuttoncreate(self):
        self.metadata_canvas.create_window(
            375, 10+25*self.counter, 
            window=self.delbutton, 
            anchor='n', 
            tags='delbutton')
    
    def checkbuttoncreate(self):
        self.metadata_canvas.create_window(
            625, 10+25*self.counter, 
            window=self.checkbutton, 
            anchor='n', 
            tags='check')

    def update(self) -> None:
        self.separator_string.set(self.language['separator'])
        self.series.updateStr()
        self.subfolder.updateStr()
        self.index.updateStr()
        self.length.updateStr()
        self.offset.updateStr()
        self.title.updateStr()
        self.original_title.updateStr()
        self.season.updateStr()
        self.template.updateStr()
        self.target_folder.updateStr()
        self.escape.updateStr()
        self.check_string.set(self.language['check'])

    def getAnswer(self) -> dict:
        self.reference.update({'target_folder': self.target_folder.getVar()})
        self.reference.update({'template': self.template.getVar()})
        self.reference.update({'index': self.index.getVar()})
        self.reference.update({'length': self.length.getVar()})
        self.reference.update({'offset': self.offset.getVar()})
        self.reference.update({'subfolder': self.subfolder.getVar()})
        self.reference.update({'series': self.series.getVar()})
        self.reference.update({'separator': self.separator_variable.get()})
        try:
            self.escape_var = self.escape.getVar()
            if bool(search(r'\|', self.escape_var)):
                self.escape_list = self.escape_var.split('|')
                for i in self.escape_list:
                    if not bool(i):
                        self.escape_list.pop(i)
            else:
                self.escape_list = [self.escape_var]
            self.reference.update({'escape': self.escape_list})
        except:
            pass
        
        self.metadata.update({'title': self.title.getVar()})
        self.metadata.update({'original_title': self.original_title.getVar()})
        self.metadata.update({'season': self.season.getVar()})
        str_name_list = ['title', 'original_title', 'season']
        for i in self.str_list:
            str_name_list.append(i.getStr())
        for l in self.str_list:
                self.metadata.update({l.getStr(): l.getVar()})
        try:
            for j in self.metadata.keys():
                if j not in str_name_list:
                    self.metadata.pop(j)
        except:
            pass

        self.target_dict.update({'reference': self.reference})
        self.target_dict.update({'metadata': self.metadata})

    def alert(self, messages: str):
        messagebox.showerror(title='Error', message=messages)

    def check(self, event = None) -> bool:
        self.getAnswer()
        alert = ''
        try:
            if not bool(self.metadata['title']):
                alert += self.language['title_alert']
                alert += '\n'
        except:
            pass
        try:
            if not bool(self.reference['target_folder']) \
                    or bool(search(self.ESCAPE_CHAR[7:], 
                                self.reference['target_folder'])):
                alert += self.language['target_folder_alert']
                alert += '\n'
        except:
            pass
        try:
            if self.reference['series']:
                if not bool(self.reference['template']):
                    alert += self.language['template_alert']
                    alert += '\n'
        except:
            pass
        try:
            if len(self.reference['separator']) > 1 \
                    or bool(search(self.ESCAPE_CHAR, 
                                self.reference['separator'])):
                alert += self.language['separator_alert']
                alert += '\n'
        except:
            pass
        try:
            for j in ['series', 'subfolder']:
                if not isinstance(self.reference[j], bool):
                    alert += self.language['bool_alert']
                    alert += '\n'
        except:
            pass
        try:
            for l in ['index', 'length', 'offset']:
                if not isinstance(self.reference[l], int):
                    alert += self.language['int_alert']
                    alert += '\n'
        except:
            pass
        try:
            alert_count = 0
            for k in self.reference.keys():
                if k == 'target_folder':
                    continue
                if isinstance(self.reference[k], str):
                    if bool(search(self.ESCAPE_CHAR, self.reference[k])):
                        alert_count += 1
            for i in self.metadata.values():
                if bool(search(self.ESCAPE_CHAR, i)):
                    alert_count += 1
            if alert_count > 0:
                alert += self.language['str_alert']
                alert += '\n'
        except:
            pass
        finally:
            if len(alert) > 0 and not alert.isspace():
                self.alert(alert)
                return False
            else:
                return True

    def newVar(self) -> None:
        self.reference.clear()
        self.metadata.clear()
        self.reference.update({
            'target_folder': '', 'template': '', 'escape': [],
            'index': 0, 'length': 2, 'offset': 0, 
            'subfolder': False,  'series': False, 'separator': '.'
            })
        self.metadata.update({'title': '', 'original_title': '', 'season': ''})
        if ('reference' and 'metadata') in self.target_dict.keys():
            self.reference.update(self.target_dict['reference'])
            self.metadata.update(self.target_dict['metadata'])
        else:
            reference_list = ['target_folder', 'template', 'index', 
                'length', 'offset', 'subfolder', 'series']
            for i in reference_list:
                try:
                    self.reference.update({i: self.target_dict[i]})
                except:
                    pass
            for l in self.target_dict.keys():
                if l not in reference_list:
                    self.metadata.update({l: self.target_dict[l]})
        self.target_dict.clear()

        self.target_folder.setVar(self.reference['target_folder'])
        self.template.setVar(self.reference['template'])
        self.index.setVar(self.reference['index'])
        self.length.setVar(self.reference['length'])
        self.offset.setVar(self.reference['offset'])
        self.subfolder.setVar(self.reference['subfolder'])
        self.series.setVar(self.reference['series'])
        self.separator_variable.set(self.reference['separator'])
        self.title.setVar(self.metadata['title'])
        self.original_title.setVar(self.metadata['original_title'])
        self.season.setVar(self.metadata['season'])
        escape_str = ''
        for k in self.reference['escape']:
            k += '|'
            escape_str += k
        self.escape.setVar(escape_str)
        
        if len(self.str_list) > 0:
            for i in self.str_list:
                i.remove()
                self.addcounter -= 1
                self.counter -= 1
            self.str_list.clear()
        for l in self.metadata.keys():
            if l not in ['title', 'original_title', 'season']:
                self.metadata_canvas.delete('addbutton')
                self.metadata_canvas.delete('delbutton')
                self.metadata_canvas.delete('check')
                doublestr = StrTemplate(self.language, l)
                doublestr.packing(
                    self.metadata_canvas, 
                    self.counter, 
                    l,
                    self.nameInput, 
                    self.strInput,
                    self.metadata[l]
                    )
                self.addcounter += 1
                self.counter += 1
                self.str_list.append(doublestr)
                self.addbuttoncreate()
                self.delbuttoncreate()
                self.checkbuttoncreate()
