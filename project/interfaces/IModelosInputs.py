from abc import ABC
from tkinter import StringVar

class IModelosInputs(ABC):
    def __init__(self, dict_var: dict) -> None:
        self.dict_var = dict_var
        
    def set_variables(self):
        "Devuelve un array con el nombre de cada una de las variables a introducir del diccionario."
        bubble = []
        for i,( k, v) in enumerate(self.dict_var.items()):
            bubble.append(StringVar(name=k))
        return bubble        
    
    @property
    def set_dict(self):
         return self.dict_var
    
    @set_dict.setter
    def set_dict(self, nvalue: dict):
         self.dict_var =  nvalue
