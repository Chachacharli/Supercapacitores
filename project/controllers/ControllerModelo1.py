
from project.models.DataFile import SimpleCSV, SimpleCSV2
from project.models.DataClasses import EntradaModelo1
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
import numpy as np


@dataclass
class MeanBars:
    """
    Guarda en arrays las medias de cada una de las velocidades de barrido del material, para luego usarse para graficar Porcentaje2.
    """
    velocidad: list[float]
    capacitiva: list[float]
    difusiva: list[float]
    dlc: list[float]

class GraphBars:

    """
    Se encarga de graficar la cantidad de carga capacitiva, pseudocapacitiva y DLC de los datos.
    Devuelve un Figure.
    """
    def __init__(self, array_barras: list[pd.DataFrame], velocidades: list[float]) -> plt.figure:
        self.headers = [ 'Capacitiva','Difusiva','Doble layer' ]
        self.lista_velocidades: list[float] = []    
        self.lista_medias_capacitiva: list[float] = []
        self.lista_medias_difusiva: list[float] = []
        self.lista_medias_dlc: list[float] = []
        
        self.lista_vel = [str(vel) for vel in velocidades]

        for i in range(len(array_barras)):      
            self.lista_medias_capacitiva.append(array_barras[i].iloc[:,0].mean())
            self.lista_medias_difusiva.append(array_barras[i].iloc[:,1].mean())
            self.lista_medias_dlc.append( array_barras[i].iloc[:,2].mean())
         
        data = MeanBars(velocidad=self.lista_vel,
                            capacitiva=self.lista_medias_capacitiva, 
                            difusiva=self.lista_medias_difusiva, 
                            dlc=self.lista_medias_dlc)
        
        plt.cla()
        self.fig, self.ax = plt.subplots(1,1)
        self.ax.bar(data.velocidad, data.capacitiva, label='Capacitive')
        self.ax.bar(data.velocidad, data.difusiva, bottom=data.capacitiva, label='Pseudocapacitive')
        self.ax.bar(data.velocidad, data.dlc, bottom=np.add(data.capacitiva,data.difusiva), label='DLC')
        self.ax.legend()
        
    def get_canvas(self):
        return self.fig

class GOxidacion:
    """
    Se encarga de graficar la oxidacion del material.
    """
    def __init__(self, Ukpos, IKpos) -> None:
        fig = plt.figure('OXIDACION')
        ax = fig.add_subplot()   
        ax.set_title('OXIDACION')
        ax.plot(Ukpos,IKpos)
        ax.set_ylabel('m(V^1/2)')
        ax.set_xlabel('mA(Vs-1/2)')  

        self.canvas = fig

    def get_canvas(self) -> plt.figure:
        return self.canvas       
 

class ControllerModelo1:
    def __init__(self, endpoint: EntradaModelo1, id: int) -> None:
        
        self.id = id
        self.endpoint: EntradaModelo1 = endpoint
        self.velocities: list[float] = endpoint.velocidades
        self.data_dict: dict = endpoint.diccionario
        self.paths: list[str] = endpoint.paths
        self.data: list[SimpleCSV] = list()

        if (self.id == 1): 
            for i in range(len(self.velocities)):
                self.data.append( SimpleCSV2(self.paths[i], self.data_dict, self.velocities[i]) )

        else: 
            for i in range(len(self.velocities)):
                self.data.append( SimpleCSV(self.paths[i], self.data_dict, self.velocities[i]) )


    def manage_data(self):

        list_of_plots: list = []
        list_of_corriente_total: list = []
        list_Oxi_Redu: list[SimpleCSV] = []
        list_Ukpos: list[float] = []
        list_bars: list = []
        list_of_porcentaje: list = []
        list_masograma: list = []
        list_insertograma: list = []
        list_output_data: list[dict] = []
        list_porcentaje: list = []
        list_velocidades: list = []

        for i in range(len(self.data)):
            self.data[i].separate_currents()
            self.data[i].interpolar()
            self.data[i].IKDefine()
            self.data[i].polpos_define()
            self.data[i].logpos_logneg_define()
            self.data[i].BposDefinition()
            self.data[i].frac_capaci()
            self.data[i].KI_dentif()
            self.data[i].cargas_promedio()
            list_of_plots.append(self.data[i].generate_plots())
            list_of_corriente_total.append(self.data[i].generate_corriente_total())            


        for i in range(len(self.data)):
            list_bars.append(self.data[i].bars())
            list_Oxi_Redu.append( self.data[i].IKpos )
            list_Ukpos.append( self.data[i].UKpos )
            list_of_porcentaje.append(self.data[i].porcentaje())

            list_porcentaje.append(self.data[i].pandasdt)
            list_velocidades.append(self.data[i].velocidad)
            list_masograma.append(self.data[i].masograma())
            list_insertograma.append(self.data[i].insertograma())
            list_output_data.append(self.data[i].list_data())

        Oxidacion = GOxidacion(list_Ukpos, list_Oxi_Redu).get_canvas()
        graph_bars = GraphBars(list_porcentaje, list_velocidades).get_canvas()

        return list_of_plots, Oxidacion, list_of_corriente_total, graph_bars, list_of_porcentaje, list_masograma, list_insertograma,list_output_data