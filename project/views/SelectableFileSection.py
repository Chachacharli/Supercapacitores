import customtkinter
import tkinter as tk
from project.views.VelocitiesList import VelocitiesList, InputSpeed
from project.utils.split_str import split_str
import tkinter.filedialog as fd



class SelectableFilesSection:
    def __init__(self, master) -> None:
        self.master = master
        self.list_of_velocities: list[InputSpeed] = list()
        self.data_files = list()
        self.selectable_files = customtkinter.CTkFrame( self.master , fg_color='#CFCFCF' , bg_color='#CFCFCF')
        self.selectable_files.grid_columnconfigure((1,2,3), weight=1)
        self.selectable_files.grid_rowconfigure(0, weight=0)
        self.selectable_files.grid(row=0, column=0, columnspan=10, sticky= 'we', padx=5 )

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