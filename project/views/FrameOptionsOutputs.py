import customtkinter
from dataclasses import dataclass

@dataclass
class FormDataRequest:
    """
    Formato para acceder a que datos de salida se desea tener.
    """
    Muestra1: bool
    Muestra2: bool
    Muestra3: bool
    Muestra4: bool
    Muestra5: bool


class FrameOptionsOutputs:
    def __init__(self, master) -> None:
        """
        Setea todas las opciones de outputs para generar los reportes finales.
        """

        self.format = FormDataRequest(False,False,False,False,False)

        self.report_true = False
        
        self.navigation_frame2 = customtkinter.CTkFrame(master, corner_radius=0,fg_color='#CFCFCF')
        self.navigation_frame2.grid(row=4, column=0, sticky="nsew",  columnspan=4, padx=5)
        self.navigation_frame2.grid_rowconfigure(10, weight=1)        

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.navigation_frame2,text='Generate report', command=self.is_checked)
        self.checkbox_1.grid(row=0, column=0, pady=(20, 0), padx=20, sticky="n")


        self.label = customtkinter.CTkFrame(self.navigation_frame2, fg_color='#CFCFCF')
        self.header = customtkinter.CTkLabel(self.label, text='Selecciona tus datos', bg_color='#CFCFCF',fg_color='#CFCFCF')

        self.check_interpolacion = customtkinter.CTkCheckBox(self.label, text='Muestra1',bg_color='#CFCFCF',fg_color='#CFCFCF',  command=self.get_data)
        self.check_masograma = customtkinter.CTkCheckBox(self.label, text='Muestra2',bg_color='#CFCFCF',fg_color='#CFCFCF', command=self.get_data)
        self.check_oxidacion = customtkinter.CTkCheckBox(self.label, text='Muestra3',bg_color='#CFCFCF',fg_color='#CFCFCF',  command=self.get_data)
        self.check_polyfit = customtkinter.CTkCheckBox(self.label, text='Muestra4',bg_color='#CFCFCF',fg_color='#CFCFCF',  command=self.get_data)
        self.check_cargatotal = customtkinter.CTkCheckBox(self.label, text='Muestra5',bg_color='#CFCFCF',fg_color='#CFCFCF',  command=self.get_data)
        


    def is_checked(self):
        if(bool(self.checkbox_1.get())):
            self.label.grid(row=2, column=0, columnspan=3)
            self.header.grid(row=0, column=0, padx=5,pady=5)
            self.check_interpolacion.grid(row=1, column=0,padx=5, pady=5)
            self.check_masograma.grid(row=1, column=1,padx=5, pady=5)
            self.check_oxidacion.grid(row=2,column=0,padx=5, pady=5)
            self.check_polyfit.grid(row=2,column=1,padx=5, pady=5)
            self.check_cargatotal.grid(row=3,column=0,padx=5, pady=5)      
        else:
            self.label.grid_forget()
            self.format = FormDataRequest(False,False,False,False,False)


    def get_data(self):
        self.format = FormDataRequest(
            bool(self.check_interpolacion.get()),
            bool(self.check_masograma.get()),
            bool(self.check_oxidacion.get()),
            bool(self.check_polyfit.get()),
            bool(self.check_cargatotal.get()),
        )
        