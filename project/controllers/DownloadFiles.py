import customtkinter
import tkinter as tk
from dataclasses import dataclass
import numpy as np
import tkinter.filedialog as fd
import tkinter.messagebox
from project.models.DataFile import SimpleCSV, SimpleCSV2
import datetime

# MODELS
@dataclass 
class DataframeTable2D:
    ax_x: np.ndarray
    ax_y: np.ndarray
    name: str
    state: bool = False

@dataclass
class DataframeTable3D:
    ax_x: np.ndarray
    ax_y: np.ndarray
    ax_z: np.ndarray
    name: str
    state: bool = False

@dataclass
class HeaderInfo:
    date: str
    reference_electrode: str
    initial_data: dict

    def structure_header(self) -> str:
        return f'Date: {self.date}\nReference Electrode: {self.reference_electrode}\nInitial Data: {self.initial_data}'

@dataclass 
class File:
    info: list[DataframeTable2D or DataframeTable3D]
    header: HeaderInfo

# CONTROLLER
class ControllerDownloads:
    def __init__(self, info: list[SimpleCSV or SimpleCSV2], path: str, list_of_checks: list[int]):
        self.info = info
        self.path = path
        self.list_of_checks = list_of_checks
        self.date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.header = HeaderInfo(self.date, 'Ag/AgCl', {'Masa Activa': 1, 'Area Activa': 2}).structure_header()
        self.data: list[File] = list()
        self.convert_info()

    def convert_info(self):
        """
        Convertir la informacion de entrada en tablas para su posterior descarga.
        """
        print('FROM CONTROLLER DOWNLOADS ')
        print(self.list_of_checks)
        # Aqui es un bucle for para cada archivo
        for i in range(len(self.info)):
            x = 0
            # Get interpolation data
            interpolate = DataframeTable2D(
            self.info[i].UExppos,
            self.info[i].IExppos,
            'Interpolate',
            self.list_of_checks[x]
            )
            x += 1
            # Get K data
            Ks = DataframeTable2D(
            self.info[i].IKpos,
            self.info[i].UKpos,
            'K',
            self.list_of_checks[x]                        
            )
            x += 1            
            # Get VOLTAMPEROGRAM data
            volt = DataframeTable2D(
            self.info[i].Imodelpos,
            self.info[i].Imodelneg,
            'VOLTAMPEROGRAM',
            self.list_of_checks[x]
            )
            x += 1            
            # Get Total Q data
            Qs = DataframeTable3D(
            self.info[i].pandasdt['Capacitiva'],
            self.info[i].pandasdt['Difusiva'],
            self.info[i].pandasdt['Doble layer'],
            'Total-Q',
            self.list_of_checks[x]
            )
            x += 1            
            # Get Q% data
            Qp = DataframeTable3D(
            self.info[i].pandasdt['Capacitiva'],
            self.info[i].pandasdt['Difusiva'],
            self.info[i].pandasdt['Doble layer'],
            'Q%',
            self.list_of_checks[x]
            )
            x += 1                        
            # Get MASOGRAMA data
            Mas = DataframeTable2D(
            self.info[i].masapos,
            self.info[i].masaneg,
            'MASOGRAM',
            self.list_of_checks[x]
            )
            x += 1                        
            # Get ACTIVE THICKNESS data
            ActThc = DataframeTable2D(
            self.info[i].inserneg,
            self.info[i].insert,
            'ACTIVE-THICKNESS',
            self.list_of_checks[x]
            )
            self.data.append(File([interpolate, Ks, volt, Qs, Qp, Mas, ActThc], self.header))
            
    def download(self):
        """
        Descargar los archivos
        """
        for i in range(len(self.data)):
            # Un codigo que descarga los archivos mediante np.savetxt con el header en el path seleccionado
            if self.data[i].info[0].state:
                np.savetxt(f'{self.path}/{self.data[i].info[0].name}_{self.info[i].velocidad}.txt', np.column_stack((self.data[i].info[0].ax_x, self.data[i].info[0].ax_y)), header=self.header)

# VIEWS
class Checkboxes:
    """
    Clase que contiene un checkbox y su respectiva informacion
    """
    def __init__(self, parent, name: str, id: int):
        self.parent = parent
        self.id = id
        self.isActive = tk.BooleanVar(name=name, value=False)
        self.checkbox = customtkinter.CTkCheckBox(parent, text=name, fg_color='#2CC985', variable=self.isActive)
    

# MAIN VIEW
class DownloadFiles(tk.Toplevel):
    """
    Ventana que permite seleccionar los archivos a descargar
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Download Files")
        self.resizable(False, False)
        self.parent = parent
        self.list_of_checkboxes: list[Checkboxes] = list()
        self.checkboxes = ['Interpolation', 'Obtaining of K', 'VOLTAMPEROGRAM', 'Total Q', 'Q%', 'MASOGRAMA', 'ACTIVE THICKNESS']
        self.list_of_checks: list[bool] = list()
        self.path: str = ''

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
        self.path = fd.askdirectory(initialdir='/', title='Select Folder')
        print(self.path)

    def handler_submit(self):
        if(self.path != ''):
            for i in range(len(self.list_of_checkboxes)):
                if self.list_of_checkboxes[i].isActive.get():
                    self.list_of_checks.append(True)
                else:
                    self.list_of_checks.append(False)
            self.parent.download_files_path = self.path
            self.parent.list_of_checks = self.list_of_checks
            print('FROM DOWNLOAD FILES TOP LEVEL')
            print(self.parent.download_files_path)
            print(self.parent.list_of_checks)
            print(self.parent)
            print(self.list_of_checks)
        else:
            tkinter.messagebox.showinfo('Error', 'Select a folder')


            # ControllerDownloads(self.info_to_donwload, HeaderInfo('01/01/2021', 'Ag/AgCl', {'Masa Activa': 1, 'Area Activa': 2})).download()
            # self.destroy()
         