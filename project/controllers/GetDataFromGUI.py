from project.models.DataFile import SimpleCSV
import matplotlib.pyplot as plt

class GOxidacion:
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
    list_output_data: list[dict] = []

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
        list_masograma.append(list_data[i].masograma())

        list_output_data.append(list_data[i].list_data())

    
    Oxidacion = GOxidacion(list_Ukpos, list_Oxi_Redu).get_canvas()
    

    return list_of_plots, Oxidacion, list_of_corriente_total, list_bars, list_of_porcentaje, list_masograma,list_output_data





