#Librerias
import tkinter as tk
from tkinter import StringVar
import customtkinter
import tkinter.filedialog as fd
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from PIL import Image
import os
import sys
from dataclasses import dataclass
from tkinter import messagebox

#constantes
import project.utils.contstans as CONST
from tkinter.constants import *

#Classes

## MODELOS
from project.models.DataFile import SimpleCSV

## DATACLASSES
from project.models.DataClasses import EntradaModelo1

## VIEWS
from project.views.MainInput import MainInput
from project.views.VelocitiesList import VelocitiesList, InputSpeed
from project.views.FrameOptionsOutputs import FrameOptionsOutputs
from project.views.VerticalScrolledFrame import VerticalScrolledFrame
from project.views.SelectableFileSection import SelectableFilesSection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

## INTERFACES 
from project.interfaces.IModelosInputs import IModelosInputs

from project.utils.split_str import split_str

#Controllers
from project.controllers.ControllerModelo1 import ControllerModelo1



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
            try:
                lista_data.append(float(self.list_inputs[i].entrie_din.get()))
            except ValueError:
                lista_data.append(None)
            
        return lista_data

class NavigationFrameModelo1:
    def __init__(self, master) -> None:
        
        self.master = master

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
            self.formulario_actual = ModeloUnoFormulario(self.master,1, self.dict_modelo_masa_activa )
        else:         
            self.formulario_actual = ModeloUnoFormulario(self.master,2, self.dict_modelo_area_activa )
        
        self.formulario_actual.frame.grid(row=2, column=0)        
         
    def get_data_from_form(self):
        print(self.formulario_actual.return_data_inputs())

class WindowInput(tk.Toplevel):
    """
    Clase que se encarga de abrir el formulario en una ventana emergente.
    :param: ventana_inicial: es la ventana de la que emerge.
    """
    def __init__(self, ventana_inicial: any, formulario: str):
        super().__init__(ventana_inicial)
        self.resizable(False, False)
        self.dict_modelo_masa_activa = CONST.modelo1_masa_activa
        self.dict_modelo_area_activa = CONST.modelo1_area_activa
        self.title(formulario)
        
        

        if(formulario == 'Masa Activa'):
            self.formulario_actual = ModeloUnoFormulario(self,1, self.dict_modelo_masa_activa )
        else:         
            self.formulario_actual = ModeloUnoFormulario(self,2, self.dict_modelo_area_activa )
        
        self.formulario_actual.frame.grid(row=2, column=0)        
        
        self.frame_btn = customtkinter.CTkFrame(self, fg_color='#CFCFCF' )
        self.frame_btn.grid_rowconfigure(0, weight=1)
        self.frame_btn.grid_columnconfigure(0, weight=1)
        self.frame_btn.grid( sticky= 'nswe' )

        self.message_frame = customtkinter.CTkFrame(self, fg_color='#CFCFCF')
        self.message_frame.grid_rowconfigure(0, weight=1)
        self.message_frame.grid_columnconfigure(0, weight=1)
        
        self.btn = customtkinter.CTkButton(self.frame_btn, 
                                           text='Accept', 
                                           fg_color='#2CC985',
                                           command=lambda: self.handlerData())
        self.btn.grid(sticky='nswe', padx=50, pady=10)

    def handlerData(self) -> None:
        print('HANDLER DATA')
        array = self.formulario_actual.return_data_inputs()
        if all(isinstance(valor, float) for valor in array):
            print(array)
        else: 
            if self.message_frame.winfo_ismapped():
                self.message_frame.grid_forget()
                self.label.grid_forget()
                
            else:    
                self.message_frame.grid( sticky= 'nswe' )
                self.label = customtkinter.CTkLabel(self.message_frame, text='Introduce correctamente los datos: Algun dato no es numerico', text_color='#B71C1C')
                self.label.grid()
                
class Aside:
    def __init__(self, root) -> None:
        self.root = root
        self.aside = customtkinter.CTkFrame(self.root, width=100,height=500, fg_color='#CFCFCF', border_color='#1D3F60', border_width=3)
        self.aside.grid_columnconfigure(0, weight=0)
        self.aside.grid_rowconfigure(0, weight=0)
        self.aside.grid( row=1, column=1, rowspan=10, sticky= 'nswe', padx=(0))
    
        self.selectable_files = SelectableFilesSection(self.aside)
        self.navigation_frame = NavigationFrameModelo1(self.aside)


class Navbar:
    def __init__(self, root) -> None:
        self.root = root
        nav = customtkinter.CTkFrame(self.root, height=100, fg_color='#1d3f60')
        nav.grid(row=0, column=1, columnspan=10, sticky= 'we')

class TabView:
    def __init__(self, root) -> None:
        self.root = root
        self.TabTree = customtkinter.CTkTabview(root, state=DISABLED, fg_color='#1D3F60')
        self.TabTree.grid( row=2, column=3, rowspan=8, columnspan=7, sticky= 'nswe')
        self.TabTree.add('Interpolation')  ## EJES I/cm-2 or I/g^-1
        self.TabTree.add('Obtaining of K')  ## Y m*V^1/2 miliamper mA*Vs-1/2 X   ##OBTENCION DE K
        self.TabTree.add('VOLTAMPEROGRAM')  ## VOLTAMPEROGRAMAS ESTIMADA VOLTAPEROGRAM
        self.TabTree.add('Total Q')  ##  TOTAL 
        self.TabTree.add('Q%')  ## Q%
        self.TabTree.add('MASOGRAMA')  ## MASOGRAMA 
        self.TabTree.add('ACTIVE THICKNESS')  ## ACTIVE THICKNESS



         #  pyinstaller -F main.py  --collect-all customtkinter -w

class MainScreeen:
    def __init__(self) -> None:
        self.root = customtkinter.CTk()
        self.inizialize_window()      

        self.nav = Navbar(self.root)
        self.aside = Aside(self.root)
        self.tabview = TabView(self.root)

        self.tipo_de_modelo = None

    #TREE PARA CAMBIAR DE PESTANA

        self.main_container = VerticalScrolledFrame( self.tabview.TabTree.tab('Interpolation'))
        self.main_container.pack(fill=BOTH, expand=True)


        self.conntent2 = VerticalScrolledFrame( self.tabview.TabTree.tab('Obtaining of K'))
        self.conntent2.pack(fill=BOTH, expand=True)

        self.content3 = VerticalScrolledFrame( self.tabview.TabTree.tab('VOLTAMPEROGRAM'))
        self.content3.pack(fill=BOTH, expand=True)


        self.content4 = VerticalScrolledFrame( self.tabview.TabTree.tab('Total Q'))
        self.content4.pack(fill=BOTH, expand=True)


        self.content5 = VerticalScrolledFrame( self.tabview.TabTree.tab('Q%'))
        self.content5.pack(fill=BOTH, expand=True)    


        self.content6 = VerticalScrolledFrame( self.tabview.TabTree.tab('MASOGRAMA'))
        self.content6.pack(fill=BOTH, expand=True)        

        self.content7 = VerticalScrolledFrame( self.tabview.TabTree.tab('ACTIVE THICKNESS'))
        self.content7.pack(fill=BOTH, expand=True)       




       
        self.btn_next = customtkinter.CTkButton(self.aside.aside ,text='Continue', 
                                            fg_color='#2ECC71',
                                            command=lambda: self.get_data_from_form())
        self.btn_next.grid(row=10, column=0)        


       
        self.open_form = customtkinter.CTkButton(self.aside.aside ,text='Open form', 
                                            fg_color='#2ECC71',
                                            command=lambda: self.abrir_formulario())
        self.open_form.grid(row=10, column=1)  

        self.root.mainloop()

    def get_data_from_form(self) -> None:
        data: list[float] = (self.aside.navigation_frame.formulario_actual.return_data_inputs())
        self.tipo_de_modelo = self.aside.navigation_frame.formulario_actual.id
        self.generate_response(data, self.tipo_de_modelo)

    def generate_response(self,data, id) -> None:
        """
        Genera una respuesta para pasarla al Controller para este modelo.
        """
        if(id==1):
            inputdict = CONST.modelo1_masa_activa_respuestas
                  
        if(id == 2):
            inputdict = CONST.modelo1_area_activa_respuestas

        for i,( k, v) in enumerate(inputdict.items()):
            if(i<len(data)):
                inputdict[k] = data[i]


        paths, values = self.get_velocities_info()
        print(paths, values)

        inputdict['velocidades'] = values

        response = EntradaModelo1(inputdict, values, paths)
        
        self.call_controller(response, id)


    def get_velocities_info(self) -> tuple[list[str], list[int]]:
        """
        Toma los datos de los archivos y las velocidades de las entradas.
        """
        paths: list[str] = list()
        values: list[int] = list()

        #Recibir los datos del path del archivo.
        for i in range(len(self.aside.selectable_files.list_of_velocities)):
            paths.append(self.aside.selectable_files.list_of_velocities[i].get_path())

        #Recibe los datos del entrie del formulario de velocidades.
        for i in range(len(self.aside.selectable_files.list_of_velocities)):
            values.append(float(self.aside.selectable_files.list_of_velocities[i].return_info()))            

        return paths, values

    def call_controller(self, response: EntradaModelo1, id: int) -> None:
        """
        Llama al controlador para manejar todos los datos.
        """
        if(self.tipo_de_modelo == 1 or 2):
            controller = ControllerModelo1(response, self.tipo_de_modelo)
            interpolacion, oxidacion, corriente_total, bars, porcentaje, masograma, insertograma, outputs = controller.manage_data()

        print(interpolacion)

        self.render_modelo1(interpolacion, oxidacion, corriente_total, bars, porcentaje, masograma, insertograma, outputs)

    def render_modelo1(self,interpolacion, oxidacion, corriente_total, bars, porcentaje, masograma, insertograma, outputs):
        
        #Renderizar grafica de oxidacion
        canvasOxidacion = FigureCanvasTkAgg(oxidacion, self.conntent2.interior)
        canvasOxidacion.draw()
        canvasOxidacion.get_tk_widget().pack(fill='both', pady=20, padx=20)

        navbar_tool_bar2 = NavigationToolbar2Tk(canvasOxidacion, self.conntent2.interior, pack_toolbar=False)
        navbar_tool_bar2.update()
        navbar_tool_bar2.pack(fill='both' )  

        bars_canvas = FigureCanvasTkAgg(bars, self.content4.interior)
        bars_canvas.draw()
        bars_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
        navbar_tool_bar = NavigationToolbar2Tk(bars_canvas, self.content4.interior, pack_toolbar=False)
        navbar_tool_bar.update()
        navbar_tool_bar.pack(fill='both' )      


        #Este for se encarga de plotear y renderizar las graficas en las diferentes ramas del arbol 
        for i in range(len(interpolacion)): 
            canvas = FigureCanvasTkAgg(interpolacion[i], self.main_container.interior)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
            navbar_tool_bar = NavigationToolbar2Tk(canvas, self.main_container.interior, pack_toolbar=False)
            navbar_tool_bar.update()
            navbar_tool_bar.pack(fill='both' )

            corriente_canvas = FigureCanvasTkAgg(corriente_total[i], self.content3.interior)
            corriente_canvas.draw()
            corriente_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
            navbar_tool_bar = NavigationToolbar2Tk(corriente_canvas, self.content3.interior, pack_toolbar=False)
            navbar_tool_bar.update()
            navbar_tool_bar.pack(fill='both' )
    
            porcentaje_canvas = FigureCanvasTkAgg(porcentaje[i], self.content5.interior)
            porcentaje_canvas.draw()
            porcentaje_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
            porcentaje_canvas = NavigationToolbar2Tk(porcentaje_canvas, self.content5.interior, pack_toolbar=False)
            porcentaje_canvas.update()
            porcentaje_canvas.pack(fill='both' )              

            masograna_canvas = FigureCanvasTkAgg(masograma[i], self.content6.interior)
            masograna_canvas.draw()
            masograna_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
            masograna_canvas = NavigationToolbar2Tk(masograna_canvas, self.content6.interior, pack_toolbar=False)
            masograna_canvas.update()
            masograna_canvas.pack(fill='both' )          

            insertograma_canvas = FigureCanvasTkAgg(insertograma[i], self.content7.interior)
            insertograma_canvas.draw()
            insertograma_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
            insertograma_canvas = NavigationToolbar2Tk(insertograma_canvas, self.content7.interior, pack_toolbar=False)
            insertograma_canvas.update()
            insertograma_canvas.pack(fill='both' )

            self.tabview.TabTree.configure(state='Activate')
    
    def inizialize_window(self) -> None:
            self.root.title( 'SuperCapacitoresSoftware' )
            width= self.root.winfo_screenwidth()
            height= self.root.winfo_screenheight()    
            self.root.minsize( width= width, height= height)
            self.root.state('zoomed')
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_columnconfigure(2, weight=1)
            self.root.grid_columnconfigure(3, weight=1)
            self.root.grid_columnconfigure(4, weight=1)
            self.root.grid_columnconfigure(5, weight=1)
            self.root.grid_columnconfigure(6, weight=1)
            self.root.grid_columnconfigure(7, weight=1)
            self.root.grid_columnconfigure(8, weight=1)
            self.root.grid_columnconfigure(9, weight=1)
            self.root.grid_columnconfigure(10, weight=1)
                
            self.root.grid_rowconfigure(1, weight=1)
            self.root.grid_rowconfigure(2, weight=1)
            self.root.grid_rowconfigure(3, weight=1)
            self.root.grid_rowconfigure(4, weight=1)
            self.root.grid_rowconfigure(5, weight=1)
            self.root.grid_rowconfigure(6, weight=1)
            self.root.grid_rowconfigure(7, weight=1)
            self.root.grid_rowconfigure(8, weight=1)
            self.root.grid_rowconfigure(9, weight=1)
            self.root.grid_rowconfigure(10, weight=1)          

    def abrir_formulario(self):
        opcion = self.aside.navigation_frame.introduccion_dato.get()
        print(opcion)
        if opcion == "Masa Activa":
            formulario1 = WindowInput(self.root, opcion)
        elif opcion == "Area Activa":
            formulario2 = WindowInput(self.root, opcion)

        # self.root.withdraw()  # Ocultar la ventana inicial    

if __name__ == '__main__':
    M = MainScreeen()


# Molecular Mass of active ion
# Active material density 
# Geometrical superficial area
# Potencial steps
# Electric doblue layer capacitance (Trassati)
# Number of electrons
# Mass of Active Material

# cambio
# DLC
# densidad activa
# peso mol
# num electrones
# ventana
