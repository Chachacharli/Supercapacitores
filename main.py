import tkinter as tk
from tkinter import StringVar
import customtkinter
import tkinter.filedialog as fd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from project.models.DataFile import SimpleCSV
from project.views.MainInput import MainInput
from project.views.VelocitiesList import VelocitiesList
from project.views.FrameOptionsOutputs import FrameOptionsOutputs
from project.views.VerticalScrolledFrame import VerticalScrolledFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image
import os
import sys
#CONTROLLERS
from project.controllers.GetDataFromGUI import get_data_from_GUI, StepOne
import numpy as np
list_of_velocities: list = []

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")


def save_data(name: str, obj: SimpleCSV,number: int):
    """
    Guarda los datos que se procesaron dependiendo de los parametros recibidos.
    :param name: Nombre de salida del archivo
    :param obj: Clase del que se sacaran los datos
    """

    data = {
        "Muestra1": [obj.UExppos, obj.IExppos],
        "Muestra2": [obj.IKpos, obj.IKneg],
        "Muestra3": [obj.p[0], obj.q[0]],
        "Muestra4": [obj.barras[0], obj.barras[1], obj.barras[2]],
        "Muestra5": [obj.masapos, obj.masaneg],
        "Modelos": [obj.Imodelpos, obj.Imodelpos_1, obj.Imodelpos_2, obj.Imodelneg, obj.Imodelneg_1, obj.Imodelneg_2]

    }

    np.savetxt(f'{name}_{obj.velocidad}.txt', np.transpose(data[name]))
    

def split_str(files: list, position: int) -> list:
        """
        Toma la dirección de proporcionada y devuelve solo el nombre y la extención del archivo

        :param files: lista de direcciones de los archivos.
        :param position: Numero de posicion del input asociado.

        """
        bubble = []
        for i in range(len(files[0])):
            x = files[0][i].split('/')
            bubble.append(x[position]) 
        return bubble
        
def set_variables_modelo1(diccionary_of_variables: dict) -> list:
        """ 
        Esta funcion genera la cantidad de variables de punto flotante respecto a la 
        cantidad de keys de un diccionario dado.

        diccionary_of_variables: Diccionario con todos los datos introducidos.
        """

        bubble = []
        for i,( k, v) in enumerate(diccionary_of_variables.items()):
            bubble.append(StringVar(name=k))

        return bubble
 
def set_velocities(velocities: list) -> None:
        """
        Renderiza las entries para introdicir las velocidades.
        """
        label_vels = customtkinter.CTkScrollbar(aside, corner_radius=0, height=200)
        label_vels.grid( row=1, column=0, columnspan=4, sticky= 'nswe', pady=10 )
        label = customtkinter.CTkButton(label_vels,text='llal')
        label.pack()
        text = customtkinter.CTkTextbox(label_vels,height=500)
        text.pack()

def select_files() -> None:
        
        """
        Funcion que abre una ventana emergente para poder seleccionar los archivos. 
        """

        global list_of_velocities

        files = []
        filez = fd.askopenfilenames(parent=root, title='Choose a file', filetypes=(('text files', 'txt'),))
        files.append(filez) 
        files = split_str(files, -1)
        see.clipboard_clear()
        for i in range(len(files)):
            see.insert(0, (files[i]))
        vel_var = VelocitiesList(aside, files, filez, 10)  
        vel_var.render_list()
        list_of_velocities = vel_var.get_list()
        
def clear_files() -> None:
        """
        Elimina las entries del Frame.
        """
        files = []
        see.clipboard_clear()
        VelocitiesList(aside, files,[], 10)

def full_screen() -> None:
        root.attributes('-fullscreen',False)

def inizialize_window(root: customtkinter.CTk) -> None:
        root.title( 'SuperCapacitoresSoftware' )
        width= root.winfo_screenwidth()
        height= root.winfo_screenheight()    
        root.minsize( width= width, height= height)
        root.state('zoomed')


#TOMAR LAS VARIABLES DEPENDIENDO DEL MODELO
def get_variables_modelo1()->list:
    global list_of_velocities
    

    lista_de_velocidades: list[int] = []
    
    for i, (k,v) in enumerate(modelo1_variables.items()):
       try: 
            modelo1_respuestas[k] = (float(lista_variables_asig[i].get()))    

       except Exception as e:
            print('Algo malolo sucedio')
            print(f'Error: {e}')

    for i in range(len(list_of_velocities)):
        try:
            lista_de_velocidades.append(float(list_of_velocities[i].return_info()))
        except Exception as e:
            print(e)

    modelo1_respuestas["velocidades"] = lista_de_velocidades

    data_objects = get_data_from_GUI(entries= len(list_of_velocities), paths= list_of_velocities, data= modelo1_respuestas)

    
    #Start controller Step One
    interpolacion, oxidacion, corriente_total, bars, porcentaje, masograma, outputs = StepOne(data_objects)   
    
    
    #Quitar imagen
    TabTree.configure(state='Activate')

    print('FORMAT')

    if(frame_option.format.Muestra1 or frame_option.format.Muestra2 
       or frame_option.format.Muestra3 or frame_option.format.Muestra4 
       or frame_option.format.Muestra5):
        
        for i in range(len(data_objects)):
            if(frame_option.format.Muestra1):
                save_data('Muestra1', data_objects[i], i)
            if(frame_option.format.Muestra2):
                save_data('Muestra2', data_objects[i], i)
            if(frame_option.format.Muestra3):
                save_data('Muestra3', data_objects[i], i)
            if(frame_option.format.Muestra4):
                save_data('Muestra4', data_objects[i], i)   
            if(frame_option.format.Muestra5):
                save_data('Muestra5', data_objects[i], i)


    #Renderizar grafica de oxidacion
    canvasOxidacion = FigureCanvasTkAgg(oxidacion, conntent2.interior)
    canvasOxidacion.draw()
    canvasOxidacion.get_tk_widget().pack(fill='both', pady=20, padx=20)

    navbar_tool_bar2 = NavigationToolbar2Tk(canvasOxidacion, conntent2.interior, pack_toolbar=False)
    navbar_tool_bar2.update()
    navbar_tool_bar2.pack(fill='both' )  

    #Este for se encarga de plotear y renderizar las graficas en las diferentes ramas del arbol 
    for i in range(len(interpolacion)):
        canvas = FigureCanvasTkAgg(interpolacion[i], main_container.interior)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
        navbar_tool_bar = NavigationToolbar2Tk(canvas, main_container.interior, pack_toolbar=False)
        navbar_tool_bar.update()
        navbar_tool_bar.pack(fill='both' )

        corriente_canvas = FigureCanvasTkAgg(corriente_total[i], content3.interior)
        corriente_canvas.draw()
        corriente_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
        navbar_tool_bar = NavigationToolbar2Tk(corriente_canvas, content3.interior, pack_toolbar=False)
        navbar_tool_bar.update()
        navbar_tool_bar.pack(fill='both' )

        bars_canvas = FigureCanvasTkAgg(bars[i], content4.interior)
        bars_canvas.draw()
        bars_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
        navbar_tool_bar = NavigationToolbar2Tk(bars_canvas, content4.interior, pack_toolbar=False)
        navbar_tool_bar.update()
        navbar_tool_bar.pack(fill='both' )        

        porcentaje_canvas = FigureCanvasTkAgg(porcentaje[i], content5.interior)
        porcentaje_canvas.draw()
        porcentaje_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
        porcentaje_canvas = NavigationToolbar2Tk(porcentaje_canvas, content5.interior, pack_toolbar=False)
        porcentaje_canvas.update()
        porcentaje_canvas.pack(fill='both' )              

        masograna_canvas = FigureCanvasTkAgg(masograma[i], content6.interior)
        masograna_canvas.draw()
        masograna_canvas.get_tk_widget().pack(fill='both', pady=20, padx=20)
        masograna_canvas = NavigationToolbar2Tk(masograna_canvas, content6.interior, pack_toolbar=False)
        masograna_canvas.update()
        masograna_canvas.pack(fill='both' )          


modelo1_variables = {
    "pesomol": "g/mol",
    "densidad": "g/m3",
    "areasup": "m^2/g",
    "ventana": "int",
    "DLC": "int"
}

modelo1_respuestas = {
    "pesomol": " ",
    "densidad": " ",
    "areasup": " ",
    "ventana": " ",
    "DLC": " ",
    "velocidades": []
}



if __name__ == '__main__':


    customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

    files = []


    root = customtkinter.CTk()
    inizialize_window(root)

    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_columnconfigure(4, weight=1)
    root.grid_columnconfigure(5, weight=1)
    root.grid_columnconfigure(6, weight=1)
    root.grid_columnconfigure(7, weight=1)
    root.grid_columnconfigure(8, weight=1)
    root.grid_columnconfigure(9, weight=1)
    root.grid_columnconfigure(10, weight=1)
        
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_rowconfigure(7, weight=1)
    root.grid_rowconfigure(8, weight=1)
    root.grid_rowconfigure(9, weight=1)
    root.grid_rowconfigure(10, weight=1)
    
    nav = customtkinter.CTkFrame(root, height=100, fg_color='#1d3f60')
    nav.grid(row=0, column=1, columnspan=10, sticky= 'we')

    #LIST OF RADIO BUTTONS 
    radio_value = StringVar(value="") 
    radio_buton_modelo1 = customtkinter.CTkRadioButton(nav, text='Modelo 1', variable=radio_value, value="B", text_color='white', command= lambda: print('activar modelo 1'))
    radio_buton_modelo1.grid(row=0,column=1, padx=10, pady=10)
    radio_buton_modelo2 = customtkinter.CTkRadioButton(nav, text='Modelo 2', variable=radio_value, value="A",text_color='white',command= lambda: print('activar modelo 2'))
    radio_buton_modelo2.grid(row=0,column=2, padx=10, pady=10)    

    aside = customtkinter.CTkFrame(root, width=100, fg_color='#CFCFCF', border_color='#1D3F60', border_width=3)
    aside.grid_columnconfigure((0,1,2), weight=1)
    aside.grid_rowconfigure(0, weight=0)
    aside.grid( row=1, column=1, rowspan=10, sticky= 'nswe' )

    # footer = customtkinter.CTkFrame( root, width=200, height=80)
    # footer.grid(row=10, column=3, columnspan=7, sticky= 'nswe')

    TabTree = customtkinter.CTkTabview(root, state=DISABLED, fg_color='#1D3F60')
    TabTree.grid( row=2, column=3, rowspan=8, columnspan=7, sticky= 'nswe')
    TabTree.add('Muestras 1')
    TabTree.add('Muestras 2')
    TabTree.add('Muestras 3')
    TabTree.add('Muestras 4')
    TabTree.add('Muestras 5')
    TabTree.add('Muestras 6')

    #TREE PARA CAMBIAR DE PESTANA

    main_container = VerticalScrolledFrame( TabTree.tab('Muestras 1'))
    main_container.pack(fill=BOTH, expand=True)



    conntent2 = VerticalScrolledFrame( TabTree.tab('Muestras 2'))
    conntent2.pack(fill=BOTH, expand=True)

    content3 = VerticalScrolledFrame( TabTree.tab('Muestras 3'))
    content3.pack(fill=BOTH, expand=True)


    content4 = VerticalScrolledFrame( TabTree.tab('Muestras 4'))
    content4.pack(fill=BOTH, expand=True)


    content5 = VerticalScrolledFrame( TabTree.tab('Muestras 5'))
    content5.pack(fill=BOTH, expand=True)    


    content6 = VerticalScrolledFrame( TabTree.tab('Muestras 6'))
    content6.pack(fill=BOTH, expand=True)        

    #Inputs
    selectable_files = customtkinter.CTkFrame( aside , fg_color='#CFCFCF' , bg_color='#CFCFCF')
    selectable_files.grid_columnconfigure((1,2,3), weight=1)
    selectable_files.grid_rowconfigure(0, weight=0)
    selectable_files.grid(row=0, column=0, columnspan=3, sticky= 'we', padx=5 )

    see = tk.Listbox(selectable_files)
    see.configure(background="#CFCFCF", font=('Aerial 13'))
    see.grid(row=0, column=0, columnspan=4, sticky= 'nswe')

    #Boton para seleccionar archivos
    btn_select = customtkinter.CTkButton(selectable_files, text='Select your files', command=select_files, fg_color='#2ECC71')
    btn_select.grid(row=1, column=1, columnspan=1,pady=10, padx=10)
        
    btn_deselect = customtkinter.CTkButton(selectable_files, text='Clear files', command=clear_files, fg_color='#2ECC71')
    btn_deselect.grid(row=1, column=2, columnspan=1,pady=10, padx=10)

    navigation_frame = customtkinter.CTkFrame(aside, corner_radius=0,  fg_color='#CFCFCF')
    navigation_frame.grid(row=3, column=0, sticky="nsew",  columnspan=4, padx=5)
    navigation_frame.grid_rowconfigure(10, weight=1)
        
    #Inputs 
    lista_variables_asig = set_variables_modelo1(modelo1_variables)
    for i,( c, v) in enumerate(modelo1_variables.items()):
        MainInput(navigation_frame,i, c, v, lista_variables_asig[i])
            
    btn_next = customtkinter.CTkButton(navigation_frame,text='Continue', 
                                           command=(get_variables_modelo1), fg_color='#2ECC71')
    btn_next.grid()
            
    frame_option = FrameOptionsOutputs(aside)  
    
    root.mainloop()

