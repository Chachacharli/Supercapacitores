from abc import ABC
import numpy as np  

from DataFile import SimpleCSV

""""
Esta clase se encarga de verificar si los csv suministrados cumplen con el formato adecuado 
"""

class Verifier(ABC):

    def __init__(self, data_matrix: any) -> None:
        self.data = data_matrix


class IVerifierSimpleCSV(Verifier):

    """
    Formato necesario para ser verficado: [[list],[list]] -> Un dataset con dos columnas 
    """

    def __init__(self, data_matrix: SimpleCSV) -> None:
        super().__init__(data_matrix)
        self.data = data_matrix

    def verify(self) -> bool:
        response = True
        
        return response
        

