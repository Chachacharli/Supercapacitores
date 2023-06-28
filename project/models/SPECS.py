from abc import ABC
from dataclasses import dataclass
from DataFile import IDataFile
import math 
import numpy as np
import pandas as pd
from enum import Enum
import matplotlib.pyplot as plt
import scipy as sc
from scipy.optimize import curve_fit
from scipy.stats import linregress


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
            capacity = math.pow((self.E/self.Rs), -(self.time/(self.Rs*self.Cdl)))
        except Exception as e : 
            raise e 

        return capacity


@dataclass
class DataCurrentD: 
    """
    Celula minima para la corriente difusiva, contiene dentro todos los datos necesarios para calcularla.
    
    B/t^-(1/2)
    """
    B: float
    time: float


@dataclass
class StepData: #TRATAR DE HACER INA FUNCION PARA AGREGAR EN UNA LISTA LOS DATOS DE LAC CORRIENTES
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



class AbcSPECS(ABC):
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

    SPECS_DF = pd.read_excel(r'C:\Users\TCCA_\OneDrive\Escritorio\GUI_SUPERCAPACITORES\PCGA-SDR1-3-30-3M-CaNO3.xlsx', header=None)
    numpy_matrix = np.array(SPECS_DF.iloc[2:])

    
    minutes = 20
    minutes_from = 15
    length_step = 247.40 + minutes * 60 
    length_step_start = 247.40 + minutes_from * 60 

    df = SPECS_DF.iloc[2:]
    headers = ['X', 'Y']
    df = pd.DataFrame(numpy_matrix, columns=headers)
    print()
    print(df.head())
    print()

    df['X'] = df['X'].astype(float)
    df['Y'] = df['Y'].astype(float)

    # Obtener los valores de X e Y del DataFrame


    datos_filtrados = df.loc[(df['X'] >= length_step_start) & (df['X'] <= length_step)]
    print(datos_filtrados.head())

    x_data = datos_filtrados['X'].values
    y_data = datos_filtrados['Y'].values

    plt.plot( df['X'], df['Y'], color='red', label='Datos originales filtrados por tiempo')
    plt.show()

    # Calcular los coeficientes de la regresión lineal
    A = np.vstack([x_data, np.ones(len(x_data))]).T
    m, c = np.linalg.lstsq(A, y_data, rcond=None)[0]

    # Generar los valores predichos de Y
    y_pred = m * x_data + c

    print(m, c)
    # Graficar los datos originales y la regresión lineal
    plt.plot(x_data, y_data, color='red', label='Datos originales filtrados por tiempo')
    plt.plot(x_data, y_pred, color='blue', label='Regresión lineal')
    plt.xlabel('t')
    plt.ylabel('<I>/mA')
    plt.title('Regresión lineal de mínimos cuadrados')
    plt.legend()
    plt.show()


    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    popt, pcov = curve_fit(func, x_data, y_data)
    
    a, b, c = popt 


    # Graficar los datos y la curva ajustada
    plt.plot(x_data, y_data, label='Datos')
    plt.plot(x_data, func(x_data, a, b, c), 'r-', label='Ajuste')
    plt.legend()
    plt.show()


    # Datos de ejemplo
    t = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([5, 7, 9, 10, 12, 14, 16, 17, 19, 21])

    # Definir la función no lineal
    def func(t, B):
        return 0.5 / np.sqrt(t)

    # Realizar la regresión no lineal
    params, _ = curve_fit(func, x_data, y_data)

    # Obtener los parámetros ajustados
    B_fit = params[0]

    # Generar puntos para graficar la curva ajustada
    t_fit = np.linspace(min(t), max(t), 100)
    y_fit = func(t_fit, B_fit)


    # Graficar los datos originales y la curva ajustada
    plt.plot(x_data, y_data, label='Datos originales')
    plt.plot(t_fit, y_fit, 'r-', label='Curva ajustada')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.legend()
    plt.show()



    M = np.vstack([x_data, np.ones(len(x_data))]).T

    alpha = np.linalg.lstsq(A, y_data, rcond=None)[0]
    b = np.exp(alpha[1])

    plt.plot(x_data, y_data, label='Datos originales')
    plt.plot(x_data, b*np.exp(alpha[0] * x_data), 'r-', label='Curva ajustada')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.legend()
    plt.show()    

    #  E(Y) = log(C) + Z log(X)
