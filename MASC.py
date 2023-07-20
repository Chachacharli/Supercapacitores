#Librerias
import tkinter as tk
import customtkinter
import tkinter as tk

#constantes
import project.utils.contstans as CONST
from tkinter.constants import *

#Classes
## DATACLASSES
from project.models.DataClasses import EntradaModelo1

## VIEWS
from project.views.VerticalScrolledFrame import VerticalScrolledFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from project.views.Aside import Aside
from project.views.WIndowInput import WindowInput
from project.views.Navbar import Navbar

#Controllers
from project.controllers.ControllerModelo1 import ControllerModelo1



class TabView:
    def __init__(self, root) -> None:
        self.root = root
        self.TabTree = customtkinter.CTkTabview(root, state=DISABLED, fg_color='#1D3F60')
        self.TabTree.grid( row=2, column=3, rowspan=8, columnspan=7, sticky= 'nswe')
        self.TabTree.add('Interpolation')  ## EJES J/cm-2 or J/g^-1 Normalizated vortagram
        self.TabTree.add('Obtaining of K')  ## Y m*V^1/2 miliamper mA*Vs-1/2 X   ##OBTENCION DE K
        self.TabTree.add('VOLTAMPEROGRAM')  ## VOLTAMPEROGRAMAS ESTIMADA VOLTAPEROGRAM
        self.TabTree.add('Total Q')  ##  TOTAL 
        self.TabTree.add('Q%')  ## Q%   
        self.TabTree.add('MASOGRAMA')  ## MASOGRAM 
        self.TabTree.add('ACTIVE THICKNESS')  ## ACTIVE THICKNESS
        

class MainScreeen:
    def __init__(self) -> None:
        self.root = customtkinter.CTk()
        self.inizialize_window()      

        self.nav = Navbar(self.root)
        self.aside = Aside(self.root)
        self.tabview = TabView(self.root)

        self.tipo_de_modelo = None
        self.fomrulario: WindowInput = None
        self.data: list = list()

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
        self.btn_next.grid(row=5, column=0)        


       
        self.open_form = customtkinter.CTkButton(self.aside.aside ,text='Open form', 
                                            fg_color='#2ECC71',
                                            command=lambda: self.abrir_formulario())
        # self.open_form.configure(state='Disable')
        self.open_form.grid(row=5, column=1)  

        self.root.mainloop()

    def get_data_from_form(self) -> None:
        """
        Toma el tipo de modelo en base a la ventana emergente del formulario.
        """
        self.tipo_de_modelo = self.fomrulario.formulario_actual.id              
        self.generate_response(self.data, self.tipo_de_modelo)

    def generate_response(self,data, id) -> None:
        """
        Genera una respuesta para pasarla al Controller para este modelo.
        """
        print(id)
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
        Llama al controlador para manejar todos los datos. Posteriormente renderiza las graficas.
        """
        if(self.tipo_de_modelo == 1 or 2):
            controller = ControllerModelo1(response, self.tipo_de_modelo)
            interpolacion, oxidacion, corriente_total, bars, porcentaje, masograma, insertograma, outputs = controller.manage_data()

        
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
            self.root.title( 'MASC' )
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
        if opcion == "Masa Activa":
            self.fomrulario = WindowInput(self.root, opcion, self)
        elif opcion == "Area Activa":
            self.fomrulario = WindowInput(self.root, opcion, self)

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
