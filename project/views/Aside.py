import customtkinter
import tkinter as tk
from tkinter import ttk 

from tkinter import StringVar
from project.views.SelectableFileSection import SelectableFilesSection
from project.views.MainInput import MainInput
from project.interfaces.IModelosInputs import IModelosInputs
import project.utils.contstans as CONST
from project.controllers.DownloadFiles import DownloadFiles

class ModeloUnoFormulario(IModelosInputs):
    def __init__(self, master: tk.Frame, id: str, diccionario: dict):
        super().__init__(diccionario)
        self.id = id
        self.frame = customtkinter.CTkFrame(master=master, fg_color='#CFCFCF')
        self.lista_variables_asig = self.set_variables()    
        self.list_inputs: list[MainInput] = list()
        self.crear_widgets()

    def crear_widgets(self):
        for i,( c, v) in enumerate(self.dict_var.items()):
            self.list_inputs.append(MainInput(self.frame,i, c, v, self.lista_variables_asig[i]))         

    def return_data_inputs(self):
        lista_data = list()
        for i in range(len(self.list_inputs)):
            # Si es el ultimo valor de lista, que sea un string
            if i == len(self.list_inputs) - 1:
                lista_data.append(self.list_inputs[i].entrie_din.get())
            else:
                lista_data.append(float(self.list_inputs[i].entrie_din.get()))

        return lista_data


class NavigationFrameModelo1:
    def __init__(self, master) -> None:
        
        self.master = master
        self.modelo_actual = None

        self.dict_modelo_masa_activa = CONST.modelo1_masa_activa
        self.dict_modelo_area_activa = CONST.modelo1_area_activa

        self.navigation_frame = customtkinter.CTkFrame(self.master, corner_radius=0,  fg_color='#CFCFCF')
        self.navigation_frame.grid_rowconfigure(10, weight=1)
        self.navigation_frame.grid(row=3, column=0, sticky="nsew",  columnspan=4, padx=5)

        self.introduccion_dato = StringVar(value='')
        self.formulario_actual: ModeloUnoFormulario = None

        self.input_1 = customtkinter.CTkRadioButton(self.navigation_frame, text='Masa Activa', 
                                            variable=self.introduccion_dato, 
                                            value="Masa Activa",
                                            )
        
        self.input_1.grid( row=0, column=0, padx=10, pady=10  )

        self.input_2 = customtkinter.CTkRadioButton(self.navigation_frame, text='Area Activa', 
                                            variable=self.introduccion_dato, 
                                            value="Area Activa", 
                                            )
        
        self.input_2.grid( row=0, column=1, padx=10, pady=10  )


    def render_form(self, into: dict):

        if self.formulario_actual is not None:
            self.formulario_actual.frame.grid_forget()

        if(into == 'Masa Activa'):
            self.modelo_actual = 1
            self.formulario_actual = ModeloUnoFormulario(self.master,1, self.dict_modelo_masa_activa )
        else:         
            self.modelo_actual = 2
            self.formulario_actual = ModeloUnoFormulario(self.master,2, self.dict_modelo_area_activa )

        self.formulario_actual.frame.grid(row=2, column=0)        
         
    def get_data_from_form(self):
        print(self.formulario_actual.return_data_inputs())


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title("Download Files")
        self.resizable(False, False)
        self.parent = parent
        self.geometry("400x400")
        self.withdraw()
        t = ToggledFrame(self, text='Rotate', relief="raised", borderwidth=1)
        t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

        ttk.Label(t.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
        ttk.Entry(t.sub_frame).pack(side="left")


class Aside:
    def __init__(self, root) -> None:
        self.root = root
        self.aside = customtkinter.CTkFrame(self.root, width=100,height=500, fg_color='#CFCFCF', border_color='#1D3F60', border_width=3)
        self.aside.grid_columnconfigure(0, weight=0)
        self.aside.grid_rowconfigure(0, weight=0)
        self.aside.grid( row=1, column=1, rowspan=10, sticky= 'nswe', padx=(0))
        self.download_files_path: str = ''
        self.list_of_checks: list[bool] = list()
        self.cosa = DownloadFiles(self.root)
        self.cosa.withdraw()
        self.settings = SettingsWindow(self.root)

        self.selectable_files = SelectableFilesSection(self.aside)
        self.navigation_frame = NavigationFrameModelo1(self.aside)

        self.btn_downloadfiles = customtkinter.CTkButton(self.aside, text='Download Files', fg_color='#2CC985', command=lambda: self.open_download_files())
        self.btn_downloadfiles.grid(row=2, column=0, sticky='nswe', padx=10, pady=10)

        self.btn_settings = customtkinter.CTkButton(self.aside, text='Settings', fg_color='#2CC985', command=lambda: self.open_settings())
        self.btn_settings.grid(row=2, column=1, sticky='nswe', padx=10, pady=10)

    def open_download_files(self):
        self.cosa.deiconify()

    def open_settings(self):
        self.settings.deiconify()

