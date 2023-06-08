from abc import ABC
from dataclasses import dataclass
from DataFile import IDataFile
import math as mt
import numpy as np

@dataclass
class DataCurrentC:
    """
    Celula minima para la corriente capacitiva, contiene dentro todos los datos necesarios para calcularla.
    
    E/Rs^-t/Rs*Cdl
    """    
    E: float #Voltaje 
    Rs: float #Series Resitance - La resistencia en serie es la resistencia que se encuentra dentro de la célula entre los electrodos y el colector de corriente. 
    Cdl: float # Double Layer Capacitance 
    time: float #Tiempo 

    def capacity_current(self):
        """
        Devuelve la corriente capacitiva de ese momento
        """        
        try: 
            capacity = mt.pow((self.E/self.Rs), -(self.time/(self.Rs*self.Cdl)))
        except Exception as e : 
            raise e 

        return capacity


@dataclass
class DataCurrentD: 
    """
    Celula minima para la corriente difusiva, contiene dentro todos los datos necesarios para calcularla.
    
    B/t^-1/2
    """
    B: float
    time: float


@dataclass
class StepData:
    """
    El step en el que se encuentra el proceso.
    """
    step: int
    step_length: float
    time: float
    voltage: float

@dataclass
class ExperimentalData:
    """
    'x' y 'y' de los datos experimentales. 
    """
    time: float
    current: float

@dataclass
class DataCurrentT:
    """
    La respuesta de la corriente para cada paso potencial, es la suma de todos estos datos.

    """
    IC: DataCurrentC
    ID: DataCurrentD    
    IR: float

    def sum(self):
        return self.IC + self.ID + self.IR
    

class GDataCurrent:
    def __init__(self,experimental, current, time) -> None:        
        
        self.experimental = experimental
        self.DataCurrentList: list[DataCurrentT] = current
        self.StepPotencialList: list[StepData] = time
        
        #plotear grafica



class AbSPECS(ABC):
    """
    Clase padre de SPECS, se basa en la validacion de su propia instancia para continuar o autocancelarse
    """
    def __init__(self) -> None:
        self._valid = True
        

    @property
    def validate(self):
        return self._valid
    
    @validate.setter
    def validate(self, v):
        self._valid = v

class SPECS(IDataFile):
    """
    Modelo 2 del programa.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        
        self.data = np.loadtxt(path)
        self.time = self.data[:,0]
        self.voltage = self.data[:,1]        



if __name__ == '__main__':
    pass