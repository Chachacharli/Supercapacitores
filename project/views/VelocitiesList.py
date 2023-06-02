import customtkinter
import tkinter as tk
from abc import ABC

class ListOfSomething(ABC):
     def __init__(self, some_list: list[any]) -> None:
          pass

class InputSpeed:
    """
    Componente que renderiza y devuelve los inputs de las velocidades de los archivos seleccionados.
    """
    def __init__(self,master: any, name: str, path: str) -> None:
            self.variable = tk.StringVar()
            self.variable.set(None) 
            self.path = path
            self.input = customtkinter.CTkEntry(
                master, 
                placeholder_text= name,
                 border_color='#2CC985' )     
               
    def render_input(self,column: int, row: int) -> None:
        self.input.grid( column=column,row=row,rowspan=2,padx=10, pady= 10)    
    
    def return_info(self) -> float:
        return self.input.get()
    
    def get_path(self) -> str:
        return self.path

class VelocitiesList:

        """
        Almacena y renderiza la lista de Objetos de los inputs de entrada.
        """

        def __init__(self, parent: object, list_data: list[str] ,list_paths: tuple[str] ,item_height: int) -> list[InputSpeed]:
            
            self.bubble: list[InputSpeed] = []
            self.list_data: list[str] = list_data
            self.list_paths: tuple[str] = list_paths
            self.number_of_data: int = len(list_data)
            self.item_height: int = item_height

            self.frame = tk.Canvas(parent, background='#CFCFCF')
            self.frame.columnconfigure(4, weight=0)
            self.frame.grid(row=1, column=0, columnspan=4, sticky= 'nswe' )

            customtkinter.CTkLabel(self.frame, text='Velocidades').grid(row=0, column=0, columnspan=4, sticky= 'nswe' ,pady=5)

            for i in range(len(list_data)):
                if (i%2 ==0):         
                    self.bubble.append( InputSpeed( self.frame, list_data[i], list_paths[i]))
                else:
                     self.bubble.append(InputSpeed( self.frame, list_data[i], list_paths[i] ))
            
        def render_list(self):
            for i in range(len(self.bubble)): 
                if (i%2 ==0):     
                    self.bubble[i].render_input(1, i+1)
                else:
                    self.bubble[i].render_input(2, i)                    
            
        def get_list(self) -> list[InputSpeed]:
            return self.bubble
        
        def get_data_each(self) -> list[int]:
            list_of_data = [] 
            for i in range(len(self.bubble)):
               list_of_data.append(self.bubble[i].return_info())
            return(list_of_data)