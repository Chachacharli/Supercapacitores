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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

## INTERFACES 
from project.interfaces.IModelosInputs import IModelosInputs

from project.utils.split_str import split_str

#Controllers
from project.controllers.ControllerModelo1 import ControllerModelo1



class ModeloUnoFormulario(IModelosInputs):
    def __init__(self, master, id, diccionario):
        super().__init__(diccionario)
        self.id = id
        self.frame = customtkinter.CTkFrame(master=master, fg_color='#CFCFCF')
        self.lista_variables_asig = self.set_variables()    
        self.list_inputs: list[MainInput] = list()
        self.crear_widgets()

    def crear_widgets(self):
        self.etiqueta = customtkinter.CTkLabel(self.frame)
        for i,( c, v) in enumerate(self.dict_var.items()):
            self.list_inputs.append(MainInput(self.frame,i, c, v, self.lista_variables_asig[i]))         
        self.etiqueta.grid()

    def return_data_inputs(self):
        lista_data = list()
        for i in range(len(self.list_inputs)):
            lista_data.append(float(self.list_inputs[i].entrie_din.get()))

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
                                            value="Opcion1",
                                            command=lambda: self.render_form(self.introduccion_dato.get()))
        
        self.input_1.grid( row=0, column=0, padx=10, pady=10  )

        self.input_2 = customtkinter.CTkRadioButton(self.navigation_frame, text='Area Activa', 
                                            variable=self.introduccion_dato, 
                                            value="Opcion2", 
                                            command= lambda: self.render_form(self.introduccion_dato.get()))
        
        self.input_2.grid( row=0, column=1, padx=10, pady=10  )


    def render_form(self, into: dict):

        if self.formulario_actual is not None:
            self.formulario_actual.frame.grid_forget()

        if(into == 'Opcion1'):
            self.formulario_actual = ModeloUnoFormulario(self.master,1, self.dict_modelo_masa_activa )
        else:         
            self.formulario_actual = ModeloUnoFormulario(self.master,2, self.dict_modelo_area_activa )
        
        self.formulario_actual.frame.grid(row=2, column=0)        
         
    def get_data_from_form(self):
        print(self.formulario_actual.return_data_inputs())

class Aside:
    def __init__(self, root) -> None:
        self.root = root

        self.aside = customtkinter.CTkFrame(self.root, width=100, fg_color='#CFCFCF', border_color='#1D3F60', border_width=3)
        self.aside.grid_columnconfigure((0,1,2), weight=1)
        self.aside.grid_rowconfigure(0, weight=0)
        self.aside.grid( row=1, column=1, rowspan=10, sticky= 'nswe' )

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
        self.TabTree.add('Muestras 1')
        self.TabTree.add('Muestras 2')
        self.TabTree.add('Muestras 3')
        self.TabTree.add('Muestras 4')
        self.TabTree.add('Muestras 5')
        self.TabTree.add('Muestras 6')
        self.TabTree.add('Muestras 7')        

class SelectableFilesSection:
    def __init__(self, master) -> None:
        self.master = master
        self.list_of_velocities: list[InputSpeed] = list()
        self.data_files = list()
        self.selectable_files = customtkinter.CTkFrame( self.master , fg_color='#CFCFCF' , bg_color='#CFCFCF')
        self.selectable_files.grid_columnconfigure((1,2,3), weight=1)
        self.selectable_files.grid_rowconfigure(0, weight=0)
        self.selectable_files.grid(row=0, column=0, columnspan=3, sticky= 'we', padx=5 )

        self.see = tk.Listbox(self.selectable_files)
        self.see.configure(background="#CFCFCF", font=('Aerial 13'))
        self.see.grid(row=0, column=0, columnspan=4, sticky= 'nswe')    
            
        self.btn_select = customtkinter.CTkButton(self.selectable_files, text='Select your files', fg_color='#2ECC71', command=self.select_files)
        self.btn_select.grid(row=1, column=1, columnspan=1,pady=10, padx=10)
            
        self.btn_deselect = customtkinter.CTkButton(self.selectable_files, text='Clear files', fg_color='#2ECC71')
        self.btn_deselect.grid(row=1, column=2, columnspan=1,pady=10, padx=10)

    def select_files(self) -> None:
            
            """
            Funcion que abre una ventana emergente para poder seleccionar los archivos. 
            """
            files = []
            filez = fd.askopenfilenames(parent=self.selectable_files, title='Choose a file', filetypes=(('text files', 'txt'),))
            files.append(filez) 
            files = split_str(files, -1)
            self.data_files = files

            self.see.clipboard_clear()
            for i in range(len(files)):
                self.see.insert(0, (files[i]))
            vel_var = VelocitiesList(self.master, files, filez, 10)  
            vel_var.render_list()
            self.list_of_velocities = vel_var.get_list()

         #  pyinstaller -F main.py  --collect-all customtkinter -w

class MainScreeen:
    def __init__(self) -> None:
        self.root = customtkinter.CTk()
        self.inizialize_window()      

        self.nav = Navbar(self.root)
        self.aside = Aside(self.root)
        self.tabview = TabView(self.root)
        self.selectable_files = SelectableFilesSection(self.aside.aside)

        self.tipo_de_modelo = None

    #TREE PARA CAMBIAR DE PESTANA

        self.main_container = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 1'))
        self.main_container.pack(fill=BOTH, expand=True)


        self.conntent2 = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 2'))
        self.conntent2.pack(fill=BOTH, expand=True)

        self.content3 = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 3'))
        self.content3.pack(fill=BOTH, expand=True)


        self.content4 = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 4'))
        self.content4.pack(fill=BOTH, expand=True)


        self.content5 = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 5'))
        self.content5.pack(fill=BOTH, expand=True)    


        self.content6 = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 6'))
        self.content6.pack(fill=BOTH, expand=True)        

        self.content7 = VerticalScrolledFrame( self.tabview.TabTree.tab('Muestras 7'))
        self.content7.pack(fill=BOTH, expand=True)            

        btn_next = customtkinter.CTkButton(self.aside.aside ,text='Continue', 
                                            fg_color='#2ECC71',
                                            command=lambda: self.get_data_from_form())
        btn_next.grid(row=10, column=0)        


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
        for i in range(len(self.selectable_files.list_of_velocities)):
            paths.append(self.selectable_files.list_of_velocities[i].get_path())

        #Recibe los datos del entrie del formulario de velocidades.
        for i in range(len(self.selectable_files.list_of_velocities)):
            values.append(float(self.selectable_files.list_of_velocities[i].return_info()))            

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

if __name__ == '__main__':
    M = MainScreeen()


