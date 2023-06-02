from project.models.DataFile import SimpleCSV
import matplotlib.pyplot as plt
import pandas as pd
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
        ax.set_ylabel('Intensity')
        ax.set_xlabel('Scan rate')  

        self.canvas = fig

    def get_canvas(self) -> plt.figure:
        return self.canvas       
        


def get_data_from_GUI(entries: int, paths: list, data: dict) -> list[SimpleCSV]:
    bubble: list[SimpleCSV] = []
    for i in range(entries):
        bubble.append(SimpleCSV(paths[i].get_path(), data, data['velocidades'][i]))

    for i in range(len(bubble)):
        print(bubble[i].path)
    
    print(data)
    return(bubble)

def StepOne(list_data: list[SimpleCSV]):
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

    for i in range(len(list_data)):
        list_data[i].separate_currents()
        list_data[i].interpolar()
        list_data[i].IKDefine()
        list_data[i].polpos_define()
        list_data[i].logpos_logneg_define()
        list_data[i].BposDefinition()
        list_data[i].frac_capaci()
        list_data[i].KI_dentif()
        list_data[i].cargas_promedio()
        list_of_plots.append(list_data[i].generate_plots())
        list_of_corriente_total.append(list_data[i].generate_corriente_total())

    for i in range(len(list_data)):
        list_bars.append(list_data[i].bars())
        list_Oxi_Redu.append( list_data[i].IKpos )
        list_Ukpos.append( list_data[i].UKpos )
        list_of_porcentaje.append(list_data[i].porcentaje())

        list_porcentaje.append(list_data[i].pandasdt)
        list_velocidades.append(list_data[i].velocidad)
        list_masograma.append(list_data[i].masograma())
        list_insertograma.append(list_data[i].insertograma())
        list_output_data.append(list_data[i].list_data())

    
    Oxidacion = GOxidacion(list_Ukpos, list_Oxi_Redu).get_canvas()
    graph_bars = GraphBars(list_porcentaje, list_velocidades).get_canvas()

    return list_of_plots, Oxidacion, list_of_corriente_total, graph_bars, list_of_porcentaje, list_masograma, list_insertograma,list_output_data
    




