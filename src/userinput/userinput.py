from src.userinput.template import *
from src.userinput.validate import Validate
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import tkinter.font as tkFont
from time import strftime, localtime


class UserInput:
    ESCAPE_CHAR = r'\\|/|:|\*|\?|"|<|>|\|'

    def __init__(
        self, master: tk.Tk, language: dict, target_dict: dict, font_dict: dict
    ) -> None:
        self.master = master
        self.language = language
        self.target_dict = target_dict
        self.reference = {
            "target_folder": "",
            "template": "",
            "episode_symbol": "E",
            "separator": ".",
            "index": 0,
            "length": 2,
            "offset": 0,
            "ratio": 0.5,
            "series": False,
            "subfolder": False,
            "no_extra": False,
            "match_ratio": False,
            "escape": [],
            "ignore": [],
            "replace": {},
            "manual": {},
        }
        self.metadata = {"title": "", "original_title": "", "season": "01"}
        self.font = tkFont.Font(family=font_dict["font"], size=font_dict["size"])
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

    def _on_mousewheel(self, canvas: tk.Canvas, event) -> None:
        def delta(event):
            if (event.num == 5) or (event.delta < 0):
                return 1
            if (event.num == 4) or (event.delta > 0):
                return -1
            else:
                return 0

        canvas.yview_scroll(delta(event), "units")

    def metadataView(self) -> None:
        def update_scroll_region(event):
            self.metadata_canvas.configure(
                scrollregion=self.metadata_canvas.bbox("all")
            )

        def metadata_on_mousewheel(event):
            self._on_mousewheel(self.metadata_canvas, event)

        def set_frame_size(event):
            self.metadata_canvas.itemconfig(
                "frame", width=self.metadata_canvas.winfo_width()
            )

        metadata_frame = ttk.Frame(self.notebook)
        self.notebook.add(metadata_frame, text="matadata", padding=(2, 2, 2, 2))
        self.metadata_bar = ttk.Scrollbar(metadata_frame)
        self.metadata_bar.pack(fill="y", side="left")
        self.metadata_canvas = tk.Canvas(metadata_frame, background="green")
        self.metadata_canvas.pack(expand=True, fill="both")
        self.metadata_frame = ttk.Frame(self.metadata_canvas)
        self.metadata_canvas.create_window(
            0, 0, window=self.metadata_frame, anchor="nw", tags="frame"
        )
        self.metadata_bar.configure(command=self.metadata_canvas.yview)
        self.metadata_bar.bind("<MouseWheel>", metadata_on_mousewheel)
        self.metadata_canvas.configure(yscrollcommand=self.metadata_bar.set)
        self.metadata_canvas.bind("<Configure>", set_frame_size)
        self.metadata_canvas.bind("<MouseWheel>", metadata_on_mousewheel)
        self.metadata_frame.bind("<Configure>", update_scroll_region)
        self.metadata_frame.bind("<MouseWheel>", metadata_on_mousewheel)

    def referenceView(self) -> None:
        def update_scroll_region(event):
            self.reference_canvas.configure(
                scrollregion=self.reference_canvas.bbox("all")
            )

        def reference_on_mousewheel(event):
            self._on_mousewheel(self.reference_canvas, event)

        def set_frame_size(event):
            self.reference_canvas.itemconfig(
                "frame", width=self.reference_canvas.winfo_width()
            )

        reference_frame = ttk.Frame(self.notebook)
        self.notebook.add(reference_frame, text="reference", padding=(2, 2, 2, 2))
        self.reference_bar = ttk.Scrollbar(reference_frame)
        self.reference_bar.pack(fill="y", side="left")
        self.reference_canvas = tk.Canvas(reference_frame, background="green")
        self.reference_canvas.pack(expand=True, fill="both")
        self.reference_frame = ttk.Frame(self.reference_canvas)
        self.reference_canvas.create_window(
            0, 0, window=self.reference_frame, anchor="nw", tags="frame"
        )
        self.reference_bar.configure(command=self.reference_canvas.yview)
        self.reference_bar.bind("<MouseWheel>", reference_on_mousewheel)
        self.reference_canvas.configure(yscrollcommand=self.reference_bar.set)
        self.reference_canvas.bind("<Configure>", set_frame_size)
        self.reference_canvas.bind("<MouseWheel>", reference_on_mousewheel)
        self.reference_frame.bind("<Configure>", update_scroll_region)
        self.reference_frame.bind("<MouseWheel>", reference_on_mousewheel)

    def startInput(self) -> None:
        self.metadataView()
        self.referenceView()
        validate = Validate()

        self.strInput = self.notebook.register(validate.strValidate)
        self.folderInput = self.notebook.register(validate.folderValidate)
        self.separatorInput = self.notebook.register(validate.separatorValidate)
        self.intInput = self.notebook.register(validate.intValidate)
        self.floatInput = self.notebook.register(validate.floatValidate)
        self.master.bind("<Control-k>", self.check)

        self.metadataInput()
        self.referenceInput()

    def metadataInput(self) -> None:
        button_frame = ttk.Frame(self.metadata_frame)
        button_frame.pack()
        add_button = ttk.Button(
            master=button_frame, command=self.metadataAdd, text=" + "
        )
        add_button.pack(padx=1, side="left")
        ttk.Button(button_frame, text="check", command=self.check).pack(
            padx=1, side="right"
        )
        self.metadata_list = []
        for metadata in self.metadata.keys():
            self.metadataAdd(metadata, self.metadata[metadata])

    def metadataAdd(self, names="", defaults=""):
        if not bool(names):
            names = strftime("%H_%M_%S", localtime())
        temp = StrTemplate(
            language=self.language,
            item=names,
            masters=self.metadata_frame,
            pool=self.metadata_list,
            string_cmd_name=self.strInput,
            font=self.font,
        )
        temp.packing(variable_cmd_name=self.strInput, default=defaults)
        self.metadata_list.append(temp)

    def referenceInput(self) -> None:
        self.reference_list = []
        button_frame = ttk.Frame(self.reference_frame)
        button_frame.pack()
        ttk.Button(master=button_frame, command=self.subwindow, text=" + ").pack(
            padx=1, side="left"
        )
        ttk.Button(button_frame, text="check", command=self.check).pack(
            padx=1, side="right"
        )
        self.referenceLooping(self.reference, default=True)

    def referenceAdd(
        self,
        template,
        name: str = None,
        cmd=None,
        default: bool = False,
        source: dict = {},
    ) -> None:
        temp = template(
            language=self.language,
            item=name,
            masters=self.reference_frame,
            pool=self.reference_list,
            string_cmd_name=self.strInput,
            root=self.master,
            font=self.font,
        )
        if default:
            temp.packing(variable_cmd_name=cmd, default=source[name])
        else:
            temp.packing(variable_cmd_name=cmd)
        self.reference_list.append(temp)

    def referenceLooping(self, source_dict: dict, default=False):
        for reference in source_dict.keys():
            if type(source_dict[reference]) == str:
                if reference == "target_folder":
                    self.referenceAdd(
                        StrTemplate,
                        reference,
                        self.folderInput,
                        default=default,
                        source=source_dict,
                    )
                elif reference == "separator":
                    self.referenceAdd(
                        StrTemplate,
                        reference,
                        self.separatorInput,
                        default=default,
                        source=source_dict,
                    )
                else:
                    self.referenceAdd(
                        StrTemplate,
                        reference,
                        self.strInput,
                        default=default,
                        source=source_dict,
                    )
            elif type(source_dict[reference]) == int:
                self.referenceAdd(
                    IntTemplate,
                    reference,
                    self.intInput,
                    default=default,
                    source=source_dict,
                )
            elif type(source_dict[reference]) == float:
                self.referenceAdd(
                    FloatTemplate,
                    reference,
                    self.floatInput,
                    default=default,
                    source=source_dict,
                )
            elif type(source_dict[reference]) == bool:
                self.referenceAdd(
                    BoolTemplate, reference, default=default, source=source_dict
                )
            elif type(source_dict[reference]) == list:
                self.referenceAdd(
                    ListTemplate,
                    reference,
                    self.folderInput,
                    default=default,
                    source=source_dict,
                )
            elif type(source_dict[reference]) == dict:
                self.referenceAdd(
                    DictTemplate, reference, default=default, source=source_dict
                )

    def subwindow(self) -> None:
        def create():
            if types.get() == "str":
                self.referenceAdd(StrTemplate, name.get())
            if types.get() == "int":
                self.referenceAdd(IntTemplate, name.get())
            if types.get() == "float":
                self.referenceAdd(FloatTemplate, name.get())
            if types.get() == "bool":
                self.referenceAdd(BoolTemplate, name.get())
            if types.get() == "list":
                self.referenceAdd(ListTemplate, name.get())
            if types.get() == "dict":
                self.referenceAdd(DictTemplate, name.get())
            window.destroy()

        window = tk.Toplevel(self.master, takefocus=True)
        window.title("add reference")
        window.geometry("300x200+400+300")
        name_frame = ttk.Frame(window)
        name_frame.pack()
        ttk.Label(name_frame, text="name:", font=self.font).pack(side="left", pady=3)
        name = tk.StringVar(value=strftime("%H_%M_%S", localtime()))
        ttk.Entry(
            master=name_frame,
            font=self.font,
            textvariable=name,
            validate="key",
            validatecommand=(self.strInput, "%P"),
        ).pack(pady=3)
        type_frame = ttk.Frame(window)
        type_frame.pack()
        ttk.Label(type_frame, text="type:", font=self.font).pack(side="left")
        types = tk.StringVar(value="str")
        btn_frame = ttk.Frame(type_frame)
        btn_frame.pack()
        for i in ["str", "int", "float", "bool", "list", "dict"]:
            ttk.Radiobutton(btn_frame, text=i, variable=types, value=i).pack(
                side="bottom", anchor="nw"
            )
        ttk.Button(master=window, command=create, text="confirm").pack()

    def update(self) -> None:
        for i in self.metadata_list:
            i.updateStr()
        for l in self.reference_list:
            l.updateStr()

    def getAnswer(self) -> dict:
        self.target_dict.update(
            {"reference": {x.getStr(): x.getVar() for x in self.reference_list}}
        )
        self.target_dict.update(
            {"metadata": {x.getStr(): x.getVar() for x in self.metadata_list}}
        )
        return self.target_dict

    def newVar(self) -> None:
        def alert():
            messagebox.showerror(
                title="Error", message=self.language["import_alert"]
            )

        try:
            for metadata in self.target_dict["metadata"]:
                if not isinstance(self.target_dict["metadata"][metadata], str):
                    alert()
                    return
                if bool(
                    search(self.ESCAPE_CHAR, self.target_dict["metadata"][metadata])
                ):
                    alert()
                    return
            for reference in self.target_dict["reference"]:
                if reference in ["series", "subfolder", "no_extra", "match_ratio"]:
                    if not isinstance(self.target_dict["reference"][reference], bool):
                        alert()
                        return
                elif reference in [
                    "target_folder",
                    "template",
                    "episode_symbol",
                    "separator",
                ]:
                    if not isinstance(self.target_dict["reference"][reference], str):
                        alert()
                        return
                elif reference in ["index", "length", "offset"]:
                    if not isinstance(self.target_dict["reference"][reference], int):
                        alert()
                        return
                elif reference in ["escape", "ignore"]:
                    if not isinstance(self.target_dict["reference"][reference], list):
                        alert()
                        return
                elif reference in ["replace", "manual"]:
                    if not isinstance(self.target_dict["reference"][reference], dict):
                        alert()
                        return
        except:
            alert()
            return

        for i in self.metadata_list:
            i.destroy()
            del i
        for l in self.reference_list:
            l.destroy()
            del l
        self.metadata_list.clear()
        self.reference_list.clear()
        for metadata in self.target_dict["metadata"].keys():
            self.metadataAdd(metadata, self.target_dict["metadata"][metadata])
        self.referenceLooping(self.target_dict["reference"], default=True)
        self.update()

    def alert(self, messages: str) -> None:
        messagebox.showerror(title="Error", message=messages)

    def check(self, event=None) -> bool:
        self.getAnswer()
        alert = ""
        if "title" not in self.target_dict["metadata"].keys():
            alert += f"{self.language['title']}(str){self.language['exist_alert']}\n"
        for metadata in self.target_dict["metadata"].keys():
            if metadata == "title":
                if not bool(self.target_dict["metadata"][metadata]):
                    alert += f"{self.language['title_alert']}\n"
                try:
                    if bool(
                        search(self.ESCAPE_CHAR, self.target_dict["metadata"][metadata])
                    ):
                        alert += f"metadata: {metadata}{self.language['str_alert']}\n"
                except TypeError:
                    alert += (
                        f"{self.language[metadata]}{self.language['type_alert']}str\n"
                    )
            else:
                try:
                    if bool(
                        search(self.ESCAPE_CHAR, self.target_dict["metadata"][metadata])
                    ):
                        alert += f"metadata: {metadata}{self.language['str_alert']}\n"
                except TypeError:
                    alert += f"metadata: {metadata}{self.language['type_alert']}str\n"
        if "target_folder" not in self.target_dict["reference"].keys():
            alert += f"reference: {self.language['target_folder']}(str){self.language['exist_alert']}\n"
        for reference in self.target_dict["reference"].keys():
            if reference == "target_folder":
                try:
                    if bool(
                        search(
                            self.ESCAPE_CHAR[7:],
                            self.target_dict["reference"][reference],
                        )
                    ) or (not bool(self.target_dict["reference"][reference])):
                        alert += f"{self.language['target_folder_alert']}\n"
                except TypeError:
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}str\n"
            elif reference == "template":
                try:
                    if self.target_dict["reference"]["series"]:
                        if not bool(self.target_dict["reference"][reference]):
                            alert += f"{self.language['template_alert']}\n"
                        if bool(
                            search(
                                self.ESCAPE_CHAR,
                                self.target_dict["reference"][reference],
                            )
                        ):
                            alert += f"reference: {self.language[reference]}{self.language['str_alert']}\n"
                except KeyError:
                    alert += f"reference: {self.language['series']}(bool){self.language['exist_alert']}\n"
                except TypeError:
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}str\n"
            elif reference == "separator":
                try:
                    if len(self.target_dict["reference"][reference]) > 1 or bool(
                        search(
                            self.ESCAPE_CHAR, self.target_dict["reference"][reference]
                        )
                    ):
                        alert += f"reference: {self.language['separator_alert']}\n"
                except TypeError:
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}str\n"
            elif reference == "ratio":
                try:
                    if not 0 < self.target_dict["reference"][reference] < 1:
                        alert += f"{self.language['ratio_alert']}\n"
                except TypeError:
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}float\n"
            elif reference in ["series", "subfolder"]:
                if not isinstance(self.target_dict["reference"][reference], bool):
                    alert += f"reference: {self.language[reference]}{self.language['bool_alert']}\n"
            elif reference == "offset":
                if not isinstance(self.target_dict["reference"][reference], int):
                    alert += f"reference: {self.language[reference]}{self.language['int_alert']}\n"
            elif reference in ["index", "length"]:
                try:
                    if self.target_dict["reference"][reference] < 0:
                        alert += f"reference: {self.language[reference]}{self.language['zero_alert']}\n"
                except TypeError:
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}int\n"
            elif reference in ["escape", "ignore"]:
                try:
                    for i in self.target_dict["reference"][reference]:
                        if bool(search(self.ESCAPE_CHAR[7:], i)):
                            alert += f"{self.language[reference]} {self.language['list_alert']}\n"
                except TypeError:
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}list\n"
            elif reference in ['replace', 'manual']:
                if not isinstance(self.target_dict["reference"][reference], dict):
                    alert += f"reference: {self.language[reference]}{self.language['type_alert']}dict\n"
            else:
                if isinstance(self.target_dict["reference"][reference], str):
                    if bool(
                        search(
                            self.ESCAPE_CHAR, self.target_dict["reference"][reference]
                        )
                    ):
                        try:
                            alert += f"{self.language[reference]} {self.language['str_alert']}\n"
                        except KeyError:
                            alert += f"{reference} {self.language['str_alert']}\n"

        if len(alert) > 0 and not alert.isspace():
            self.alert(alert)
            return False
        else:
            return True
