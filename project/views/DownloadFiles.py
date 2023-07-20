import customtkinter
import tkinter as tk
from dataclasses import dataclass
import numpy as np
import tkinter.filedialog as fd
import tkinter.messagebox

@dataclass 
class InfoFile:     
    state: bool
    name: str
    info: np.ndarray 

@dataclass
class InfoFiles:
    files: list[InfoFile]
    path: str

@dataclass
class HeaderInfo:
    date: str
    reference_electrode: str
    initial_data: dict

    def structure_header(self) -> str:
        return f'Date: {self.date}\nReference Electrode: {self.reference_electrode}\nInitial Data: {self.initial_data}'

class ControllerDownloads:
    def __init__(self, info: InfoFiles, header: HeaderInfo):
        self.info = info
        self.path = info.path
        self.header = header.structure_header()

    def download(self):
        for i in range(len(self.info.files)):
            if self.info.files[i].state:    
                np.savetxt( f'{self.path}/{self.info.files[i].name}', self.info.files[i].info, delimiter=',', header=self.header)
        

class Checkboxes:
    def __init__(self, parent, name: str, id: int):
        self.parent = parent
        self.id = id
        self.isActive = tk.BooleanVar(name=name, value=False)
        self.checkbox = customtkinter.CTkCheckBox(parent, text=name, fg_color='#2CC985', variable=self.isActive, command=lambda: self.print_isActive())
    
    def print_isActive(self):
        print(self.isActive.get(), self.id)

class DownloadFiles(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Download Files")
        self.resizable(False, False)
        self.parent = parent
        self.info_to_donwload = InfoFiles([], '')
        self.list_of_checkboxes: list[Checkboxes] = []
        self.checkboxes = ['Interpolation', 'Obtaining of K', 'VOLTAMPEROGRAM', 'Total Q', 'Q%', 'MASOGRAMA', 'ACTIVE THICKNESS']
        
        # Frame que contiene informacion 
        self.frame_info = customtkinter.CTkFrame(self, fg_color='#CFCFCF')
        self.frame_info.grid_rowconfigure(0, weight=1)
        self.frame_info.grid_columnconfigure(0, weight=1)
        self.frame_info.grid(sticky='nswe', padx=10, pady=10)

        # Checkbox para seleccionar los archivos dentro de frame_info
        for i in range(len(self.checkboxes)):
            if (i % 2 == 0):
                actual_checkbox = Checkboxes(self.frame_info, self.checkboxes[i], i)
                actual_checkbox.checkbox.grid(row=i, column=0, sticky='nswe', padx=10, pady=10)
                self.list_of_checkboxes.append(actual_checkbox)
            else:
                actual_checkbox = Checkboxes(self.frame_info, self.checkboxes[i], i)
                actual_checkbox.checkbox.grid(row=i-1, column=1, sticky='nswe', padx=10, pady=10)
                self.list_of_checkboxes.append(actual_checkbox)                

        # Boton para seleccionar la carpeta donde se guardaran los archivos
        self.btn_select_folder = customtkinter.CTkButton(self, text='Select Folder', fg_color='#2CC985', command=lambda: self.select_folder())
        self.btn_select_folder.grid(row=1, column=0, sticky='nswe', padx=10, pady=10)

        # Boton para cancelar la seleccion de archivos
        self.btn_cancel = customtkinter.CTkButton(self, text='Cancel', fg_color='#B71C1C', command=lambda: self.destroy())
        self.btn_cancel.grid(row=2, column=0, sticky='nswe', padx=10, pady=10)
        
        # Boton para aceptar los archivos seleccionados
        self.btn_accept = customtkinter.CTkButton(self, text='Accept', fg_color='#2CC985', command=lambda: self.handler_submit())
        self.btn_accept.grid(row=2, column=1, sticky='nswe', padx=10, pady=10)



    def select_folder(self):
        """
        Selecciona la carpeta donde se guardaran los archivos
        """
        self.info_to_donwload.path = fd.askdirectory(initialdir='/', title='Select Folder')
        print(self.info_to_donwload.path)

    def add_file(self, file: InfoFile):
        """
        Añade un archivo a la lista de archivos seleccionados
        :param: file: es la informacion del archivo seleccionado
        """
        self.info_to_donwload.files.append(file)

    def handler_submit(self):
        if(self.info_to_donwload.path != ''):
            for i in range(len(self.list_of_checkboxes)):
                if self.list_of_checkboxes[i].isActive.get():
                    self.add_file(InfoFile(True, self.checkboxes[i], np.array([1,2,3])))
                else:
                    self.add_file(InfoFile(False, self.checkboxes[i], np.array([1,2,3])))
            print(self.info_to_donwload)
        else:
            tkinter.messagebox.showinfo('Error', 'Select a folder')


            # ControllerDownloads(self.info_to_donwload, HeaderInfo('01/01/2021', 'Ag/AgCl', {'Masa Activa': 1, 'Area Activa': 2})).download()
            # self.destroy()
         