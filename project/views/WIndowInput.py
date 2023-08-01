import customtkinter
import tkinter as tk
from project.views.Aside import ModeloUnoFormulario 
import project.utils.contstans as CONST

class WindowInput(tk.Toplevel):
    """
    Clase que se encarga de abrir el formulario en una ventana emergente.
    :param: ventana_inicial: es la ventana de la que emerge.
    """
    def __init__(self, ventana_inicial: any, formulario: str, parent: customtkinter.CTk):
        super().__init__(ventana_inicial)
        self.parent = parent
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
        """
        Es el manejo de los datos, pasa los valores del formulario mediante un array a la instancia data de el padre. 
        """
        array = self.formulario_actual.return_data_inputs()
        # Que todos los valores de la lista sean float excepto el ultimo, que sea un string
    
        if all(isinstance(valor, float) for valor in array[:-1]) and isinstance(array[-1], str):
            self.parent.data = array
            self.destroy()

        # if all(isinstance(valor, float) for valor in array):
        #     self.parent.data = array
        #     self.destroy()

        else: 
            if self.message_frame.winfo_ismapped():
                self.message_frame.grid_forget()
                self.label.grid_forget()
                print(array)
            else:    
                self.message_frame.grid( sticky= 'nswe' )
                self.label = customtkinter.CTkLabel(self.message_frame, text='Introduce correctamente los datos: Algun dato no es numerico', text_color='#B71C1C')
                self.label.grid()
                print(array)
     