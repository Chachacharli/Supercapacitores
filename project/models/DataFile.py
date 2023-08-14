
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
from project.interfaces._ISetStatus import _ISetState
from scipy.interpolate import interp1d 
import pandas as pd
from dataclasses import dataclass
from project.utils.contstans import FONT_SIZES_PLOTS as FONT

import warnings
warnings.simplefilter('ignore', np.RankWarning)

""" 
Considere esta clase como una unidad para el manejo de un solo dataset/archivo csv.

Esta clase se encarga de administrar localmente un archivo csv para su posterior lectura y sobrescritura.

Hay que tomar en cuenta que esta diseñado para que se le proporcione un path desde el tkFileDialog.askopenfilename de Tkinter. 
"""

@dataclass
class OutputData:
    UExppos: list
    IExpoos: list




class Muestra1:
    def __init__(self, UExp , IExp, UExppos, IExppos, velocidad, reference) -> None:
        fig, ax = plt.subplots(1,1, dpi = 80, figsize= (10,10))
        fig.suptitle(f'velocidad: {velocidad}') 
        ax.plot( UExp,IExp , label='Experimental data')
        ax.scatter(UExppos, IExppos, c='red', label='Interpolate data')
        ax.legend()        
        # SET FOTN LABELS AND TICKS
        ax.set_ylabel('I/cm-2', fontsize=FONT['title'])
        ax.set_xlabel(f'E(V vs {reference})', fontsize=FONT['title'])  
        # ax.tick_params(axis='x', labelsize=FONT['ticks'] )
        # ax.tick_params(axis='y', labelsize=FONT['ticks'] )
        self.canvas = fig
    
class CorrienteTotal:
    def __init__(self, linspace_varr, UExp , IExp, Imodelpos, Imodelneg, velocidad) -> None:
        fig, ax = plt.subplots(1,1, dpi = 80, figsize= (10,10))
        fig.suptitle(f'Velocidad C&D: {velocidad} mV/s')
        ax.plot( UExp, IExp, label='Experimental data')
        ax.plot(linspace_varr[0: len(linspace_varr)-1 ],Imodelpos, 'o b', label='ImodelPos' )   
        ax.plot(linspace_varr[0: len(linspace_varr)-1 ], Imodelneg, 'o r', label='ImodelNeg')        
        # ax.set_ylabel('I (A/g)', labelsize=FONT['ticks'])
        # ax.set_xlabel('U (V)',   labelsize=FONT['ticks'])
        # ax.tick_params(axis='x', labelsize=FONT['ticks'] )
        # ax.tick_params(axis='y', labelsize=FONT['ticks'] )        
        ax.legend()
        
        self.canvas = fig


class Barras: 
    def __init__(self, pandasdt: pd.DataFrame, barras ) -> None:
        self.barras = barras
        fig, axs = plt.subplots(3,1, sharex=True, sharey=True)
        axs[0].bar(range(len(self.barras)),pandasdt['Capacitiva'], color='red')
        axs[0].set_title('Capacitiva')
        axs[1].bar(range(len(self.barras)),pandasdt['Difusiva'], color='blue')
        axs[1].set_title('Difusiva')
        axs[2].bar(range(len(self.barras)),pandasdt['Doble layer'], color='orange')
        axs[2].set_title('Doble layer')
        self.canvas = fig

    

class Porcentaje: 
    def __init__(self, data: pd.DataFrame) -> None:
        self.pandasdt = data
        capacitiva = self.pandasdt['Capacitiva']
        difusiva = self.pandasdt['Difusiva']
        dlc = self.pandasdt['Doble layer']

        fig, axs = plt.subplots(1,1, dpi = 80, figsize= (10,10))
        axs.bar(['Ejemplo'], difusiva)  
        axs.bar(['Ejemplo'], capacitiva, bottom=difusiva)
        self.canvas = fig
            
class Masograma:
    def __init__(self, linspace_varr, masapos, masaneg) -> None:
        fig, axs = plt.subplots(1,1, dpi = 80)
        axs.plot( linspace_varr[0][0:len(linspace_varr[0])-1], ( masapos * 1e6 ), 'r')
        axs.plot( linspace_varr[0][0:len(linspace_varr[0])-1], ( masaneg * 1e6 ))
        self.canvas = fig        
        
    
class IDataFile(ABC): 
    #En el inicializador solo se le proporciona su path para posteriormente manejar este atributo
    #El estado de la clase inicial es true, este estado cambiara en base a si se cumplen todos los parametros para que continue la cadena de codidgo,
    #si esta cadena se rompe, el estado cambiara a False y retornaremos un fallo para la GUI
    def __init__(self, path: str) -> None:
        self.path = path
        self.state = True 

class StepBars:
    def __init__(self, barras) -> plt.figure:
        
        self.barrasdf = pd.DataFrame(barras, columns=['Capacitiva', 'Difusiva', 'DLC'])
        fig, axs = plt.subplots(3,1, sharex=True, sharey=True)
        axs[0].bar(range(len(barras)),self.barrasdf['Capacitiva'], color='red')
        axs[0].set_title('Capacitiva')
        axs[1].bar(range(len(barras)),self.barrasdf['Difusiva'], color='blue')
        axs[1].set_title('Difusiva')
        axs[2].bar(range(len(barras)),self.barrasdf['DLC'], color='orange')
        axs[2].set_title('Doble layer')
        print('barras')
        print(self.barrasdf)
        self.canvas = fig

class SimpleCSV(IDataFile):
    """
    Modelo 1 AREA ACTIVA
    AT = QD/cm2 * MM/Fq
    """
    def __init__(self, path: str, data: dict, velocidad: float) -> None:
        super().__init__(path)
        #Datos iniciales y principales
        self.path = path
        self.data = data
        self.csv = np.loadtxt( self.path )
        self.DivWin = int(data['ventana'])
        self.electron_refernce = data['referencia']
        self.areasup = int(data['areasup']) 
        self.velocidad = velocidad
        self.velocidadE = velocidad/10000
        self.UKpos = self.velocidadE **0.5 
        self.UKneg = self.velocidadE **0.5 
        self.DLC = data['DLC']
        self.cteact = (data['pesomol']/(data['electrones']*96500*data['densidad']))
        print(f'Datos: {data}')        
        #StepOne data
        self.UExp = self.csv[:,0]
        self.IExp = self.csv[:,1] * 2
        self.win = max(self.UExp) - min(self.UExp)
        self.linspace_varr = ( (np.linspace(min(self.UExp), max(self.UExp), self.DivWin)), self.win )
        self.UExppos: list[float] = []
        self.IExppos: list[float] = []
        self.UExpneg: list[float] = []
        self.IExpneg: list[float] = []
        self.Ineg: list[float] = []
        self.Ipos: list[float] = []

        #StepTwo
        self.IKpos: list[float] = []
        self.IKneg: list[float] = []

        #StepThree
        self.p: list[float] = []
        self.q: list[float] = []
        self.Imodelpos: list[float] = []
        self.Imodelneg: list[float] = []
        self.Imodelpos_1: list[float] = []
        self.Imodelpos_2: list[float] = []
        self.Imodelneg_1: list[float] = []
        self.Imodelneg_2: list[float] = []

        #StepFour
        self.Vlog: float = np.log10(self.velocidadE)
        self.logpos:list[float] = []
        self.logneg:list[float] = []
        self.bpos: list[float] = []   
        self.rbpos: list[float] = []
        self.bneg: list[float] = []
        self.rbneg: list[float] = []

        #Step Five
        self.difV: float = (self.win/self.DivWin)
        self.Qc: list[float] = []
        self.Qd: list[float] = []
        self.FracCapacipos: list[float] = []
        self.FracCapacineg: list[float] = []
        self.FracDiffuspos: list[float] = []
        self.FracDiffusneg: list[float] = []
        self.KIdentifpos: list[float] = []
        self.KIdentifneg: list[float] = []

        #Step Six
        self.barras: list[float] = []
        self.Qct: list[float] = []
        self.Qdt: list[float] = []
        self.Qt: list[float] = []

        #Step Seven
        self.Qdpos: list[float] = 0
        self.Qdneg: list[float] = 0
        self.insert: list[float] = []
        self.inserneg: list[float] = []
        self.masaneg: list[float] = []
        self.masapos: list[float] = []
        self.pandasdt: pd.DataFrame = None

    def get_csv(self) -> np.ndarray:
        """
        Devuelve el csv, un objeto de np.readtxt()
        """
        return self.csv
        
    def separate_currents(self):
        """
        Sobreescribe las corrientes separandolas en catodicas y anodicas
        """
        #Corrientes catodicas 
        Diff = np.diff(self.UExp)
        for idx, d in enumerate(Diff):
            if(d>0):
                self.UExppos.append(self.UExp[idx])
                self.IExppos.append(self.IExp[idx])
        #Corrientes anodicas
        for idx, d in enumerate(Diff):
            if(d<0):
                self.UExpneg.append(self.UExp[idx])
                self.IExpneg.append(self.IExp[idx])
        
    def interpolar(self):
        """
        Interpola las correintes catodicas y anodicas mediante 'interp1d'
        """
        Ipos_f = interp1d(self.UExppos,self.IExppos, kind='linear') 
        Ineg_f = interp1d(self.UExpneg,self.IExpneg, kind='linear') 

        for ipo in range(len((self.linspace_varr[0]))):
            try:
                self.Ipos.append(Ipos_f(self.linspace_varr[0][ipo]))
            except Exception as e:
                print('Se excluyo por: {}'.format(e))
                

        for ipo in range(len((self.linspace_varr[0]))):
            try:
                self.Ineg.append(Ineg_f(self.linspace_varr[0][ipo]))
            except Exception as e:
                print('Se excluyo por: {}'.format(e))
                


    def IKDefine(self):
        """
        Determina la IK positivo y negativo
        """
        for i in range(len(self.Ipos)):
            self.IKpos.append( (self.Ipos[i] / self.UKpos) )
            self.IKneg.append( self.Ineg[i] / self.UKpos)

    def polpos_define(self):
        
        for iter in range(len(self.IKpos)):
            #[self.UKpos], self.IKpos[iter],1
            # self.p.append( np.polyfit( [self.UKpos], self.IKpos[iter],1 ) )
            self.p.append( np.polyfit( [self.UKpos], [self.IKpos[iter]] ,1 ) )
            self.q.append( np.polyfit( [self.UKneg], [self.IKneg[iter]],1) )

        for pep in range(len(self.p)): 
                self.Imodelpos.append(((self.p[pep][0]) * self.velocidadE) + (self.p[pep][1] * (self.velocidadE**0.5))) 
                self.Imodelneg.append(((self.q[pep][0]) * self.velocidadE) + (self.q[pep][1] * (self.velocidadE**0.5))) 
                self.Imodelpos_1.append( self.p[pep][0] * self.velocidadE )
                self.Imodelneg_1.append( self.q[pep][0] * self.velocidadE)
                self.Imodelpos_2.append( self.p[pep][1] * self.UKpos)
                self.Imodelneg_2.append( self.q[pep][1] * self.UKneg)

    def logpos_logneg_define(self):
        for i in range(len(self.Ipos)):
            self.logpos.append(np.emath.log10(self.Ipos[i]))
            self.logneg.append(np.emath.log10(self.Ineg[i]))

    def BposDefinition(self):
        for i in range(len(self.logpos)):
            self.bpos.append(np.polyfit( [self.Vlog], [self.logpos[i]],1))
            self.bneg.append(np.polyfit([self.Vlog], [self.logneg[i]] ,1))

        for rb in range(len(self.bpos)):
            self.rbpos.append( self.bpos[rb][0].real )
            self.rbneg.append( self.bneg[rb][0].real )

    def cargas_promedio(self):
        for i in range(len(self.Imodelneg)):    

            media_positiva = ((( np.abs(self.Imodelpos_1[i] ) )*self.difV) /self.velocidadE)
            media_negativa = ((( np.abs(self.Imodelneg_1[i] ) )*self.difV) /self.velocidadE)
            self.Qc.append( ((media_positiva + media_negativa)/2))
            
            media_positiva = ( ( ( np.abs(self.Imodelpos_2[i] ) )*self.difV) /self.velocidadE)
            media_negativa = ( ( ( np.abs(self.Imodelneg_2[i] ) )*self.difV) /self.velocidadE)
            self.Qd.append( ((media_positiva + media_negativa)/2))
  
    def frac_capaci(self):
        for i in range( len(self.Imodelpos_1)):
            self.FracCapacipos.append( self.Imodelpos_1[i] / self.Imodelpos[i])
            self.FracCapacineg.append( self.Imodelneg_1[i] / self.Imodelneg[i])
            self.FracDiffuspos.append( self.Imodelpos_2[i] / self.Imodelpos[i])
            self.FracDiffusneg.append( self.Imodelneg_2[i] / self.Imodelneg[i])

    def KI_dentif(self):
        for i in range(len(self.p)):
            self.KIdentifpos.append( self.p[i][0] )
            self.KIdentifneg.append( self.q[i][0] )
    
    def insertograma(self):
        self.Qdpos = 0
        self.Qdneg = 0

        """
        ESPESOR ACTIVO EN CM
        
        AT = QD/cm^2 * MM/Fq
        donde 
        AT: Active thickness
        QD: Diffusion charge
        MM: Molecular mass
        Fq: Faraday 
        """
        Fq = 96485.3329
        
        # for i in range(len(self.Imodelpos_1)):
        #     self.insert.append( self.cteact * ((self.Qd[i]/self.areasup)/Fq))
        #     self.inserneg.append( self.cteact * (self.Qdneg/self.areasup) )

        for i in range(len(self.Imodelpos_1)):
            self.Qdpos = (self.Qdpos + ((self.Imodelpos_2[i]* self.difV)/self.velocidadE))
            self.Qdneg = (self.Qdneg + ((self.Imodelneg_2[i]* self.difV)/self.velocidadE))
            self.insert.append( self.cteact * ((self.Qd[i]/self.areasup)/10000) *1E+7 )
            # self.inserneg.append( self.cteact * (self.Qdneg/self.areasup) )  <-- Este valor representa los valores negativos dle insertogrtama, omitelo

        fig, ax = plt.subplots(1,1)
        ax.plot(self.linspace_varr[0][0:len(self.linspace_varr[0])-1], self.insert, 'b')
        return fig

    def bars(self) -> Barras:
        """
        Graficas de barrras
        """
        for i in range(len(self.Imodelneg)):
            self.barras.append( [ ((self.Qc[i])-(self.DLC/self.DivWin)), (self.Qd[i]), (self.DLC/self.DivWin) ] )
        self.pandasdt = pd.DataFrame(self.barras,  columns = [ 'Capacitiva','Difusiva','Doble layer' ])
        print('BARRAS')
        print(self.pandasdt)
        b = Barras(pandasdt=self.pandasdt, barras = self.barras)
        return b.canvas
    
    def porcentaje(self):
        """
        Genera las graficas de porcentaje de las corrientes.
        """

        p = Porcentaje(pd.DataFrame(self.barras,  columns = [ 'Capacitiva','Difusiva','Doble layer' ]) )
        return p.canvas
    
    def masograma(self):

        """
        Genera el masograma calculando masapos y masaneg.
        """
        

        Qdpos=0
        Qdneg=0
        Mmol = 7 #g/mol
        elec = 1
        masaelec= 0.0033*0.7;
        
        for i in range(len(self.Imodelneg_2)):
            Qdpos = Qdpos+ (self.Imodelpos_2[i]*self.difV)/self.velocidadE
            Qdneg = Qdneg- (self.Imodelneg_2[i]*self.difV)/self.velocidadE
            self.masapos.append( Mmol * Qdpos * masaelec / (elec * 96500))
            self.masaneg.append( Mmol * Qdneg * masaelec / (elec * 96500))


        self.masapos = np.array(self.masapos)
        self.masaneg = np.array(self.masaneg)


        m = Masograma(self.linspace_varr, self.masapos, self.masaneg)
        return m.canvas
    
    #Empezamos con devolver las graficas con los datos
    def generate_plots(self) -> Muestra1:
        """
        Genera los plots para devolver todos los canvas de la interpolacion 
        """
        v = Muestra1(self.UExp, self.IExp, self.UExppos, self.IExppos, self.velocidad, self.electron_refernce)
        return v.canvas
    
    def generate_corriente_total(self) -> CorrienteTotal:
        """
        Genera los plots para devolver todos los canvas de corrientes totales
        """        
        c = CorrienteTotal(self.linspace_varr[0], self.UExp, self.IExp, self.Imodelpos, self.Imodelneg, self.velocidad)
        return c.canvas

    def generate_StepBars(self) -> StepBars:
        """
        Genera los plots para devolver todos los canvas de corrientes totales en steps
        """        
        c = StepBars(self.barras)
        return c.canvas


    def list_data(self) -> OutputData:
        """
        Devuelve un objeto con todos los datos internos para imprimirse
        """
        return OutputData(
            self.UExppos,
            self.IExppos
        )
    




class SimpleCSV2(IDataFile):
    """
    Modelo 1 MASA ACTIVA 
    """
    def __init__(self, path: str, data: dict, velocidad: float) -> None:
        super().__init__(path)
        #Datos iniciales y principales
        self.path = path
        self.data = data
        self.csv = np.loadtxt( self.path )
        self.DivWin = int(data['ventana'])
        
        self.masalec = float(data['masalec']) * 0.7
        print(data)
        self.electron_refernce = data['referencia']
        print(f'ELECTRON DE REFERNCIA MODELO 2: {self.electron_refernce}')
        self.velocidad = velocidad
        self.velocidadE = velocidad/10000
        self.UKpos = self.velocidadE **0.5 
        self.UKneg = self.velocidadE **0.5 
        self.DLC = data['DLC']
        self.cteact = (data['pesomol']/(data['electrones']*96500*data['densidad']))
        print(f'Datos: {data}')

        #StepOne data
        self.UExp = self.csv[:,0]
        self.IExp = self.csv[:,1]
        self.win = max(self.UExp) - min(self.UExp)
        self.linspace_varr = ( (np.linspace(min(self.UExp), max(self.UExp), self.DivWin)), self.win )
        self.UExppos: list[float] = []
        self.IExppos: list[float] = []
        self.UExpneg: list[float] = []
        self.IExpneg: list[float] = []
        self.Ineg: list[float] = []
        self.Ipos: list[float] = []

        #StepTwo
        self.IKpos: list[float] = []
        self.IKneg: list[float] = []

        #StepThree
        self.p: list[float] = []
        self.q: list[float] = []
        self.Imodelpos: list[float] = []
        self.Imodelneg: list[float] = []
        self.Imodelpos_1: list[float] = []
        self.Imodelpos_2: list[float] = []
        self.Imodelneg_1: list[float] = []
        self.Imodelneg_2: list[float] = []

        #StepFour
        self.Vlog: float = np.log10(self.velocidadE)
        self.logpos:list[float] = []
        self.logneg:list[float] = []
        self.bpos: list[float] = []   
        self.rbpos: list[float] = []
        self.bneg: list[float] = []
        self.rbneg: list[float] = []

        #Step Five
        self.difV: float = (self.win/self.DivWin)
        self.Qc: list[float] = []
        self.Qd: list[float] = []
        self.FracCapacipos: list[float] = []
        self.FracCapacineg: list[float] = []
        self.FracDiffuspos: list[float] = []
        self.FracDiffusneg: list[float] = []
        self.KIdentifpos: list[float] = []
        self.KIdentifneg: list[float] = []

        #Step Six
        self.barras: list[float] = []
        self.Qct: list[float] = []
        self.Qdt: list[float] = []
        self.Qt: list[float] = []

        #Step Seven
        self.Qdpos: list[float] = 0
        self.Qdneg: list[float] = 0
        self.insert: list[float] = []
        self.inserneg: list[float] = []
        self.masaneg: list[float] = []
        self.masapos: list[float] = []
        self.pandasdt: pd.DataFrame = None

    def get_csv(self) -> np.ndarray:
        """
        Devuelve el csv, un objeto de np.readtxt()
        """
        return self.csv
        
    def separate_currents(self):
        """
        Sobreescribe las corrientes separandolas en catodicas y anodicas
        """
        #Corrientes catodicas 
        Diff = np.diff(self.UExp)
        for idx, d in enumerate(Diff):
            if(d>0):
                self.UExppos.append(self.UExp[idx])
                self.IExppos.append(self.IExp[idx])  
        #Corrientes anodicas
        for idx, d in enumerate(Diff):
            if(d<0):
                self.UExpneg.append(self.UExp[idx])
                self.IExpneg.append(self.IExp[idx])
        
    def interpolar(self):
        """
        Interpola las correintes catodicas y anodicas mediante 'interp1d'
        """
        Ipos_f = interp1d(self.UExppos,self.IExppos, kind='linear') 
        Ineg_f = interp1d(self.UExpneg,self.IExpneg, kind='linear') 

        for ipo in range(len((self.linspace_varr[0]))):
            try:
                self.Ipos.append(Ipos_f(self.linspace_varr[0][ipo]))
            except Exception as e:
                print('Se excluyo por: {}'.format(e))
                

        for ipo in range(len((self.linspace_varr[0]))):
            try:
                self.Ineg.append(Ineg_f(self.linspace_varr[0][ipo]))
            except Exception as e:
                print('Se excluyo por: {}'.format(e))
                


    def IKDefine(self):
        """
        Determina la IK positivo y negativo
        """
        for i in range(len(self.Ipos)):
            self.IKpos.append( (self.Ipos[i] / self.UKpos) )
            self.IKneg.append( self.Ineg[i] / self.UKpos)

    def polpos_define(self):
        
        for iter in range(len(self.IKpos)):
            #[self.UKpos], self.IKpos[iter],1
            # self.p.append( np.polyfit( [self.UKpos], self.IKpos[iter],1 ) )
            self.p.append( np.polyfit( [self.UKpos], [self.IKpos[iter]] ,1 ) )
            self.q.append( np.polyfit( [self.UKneg], [self.IKneg[iter]],1) )

        for pep in range(len(self.p)): 
                self.Imodelpos.append(((self.p[pep][0]) * self.velocidadE) + (self.p[pep][1] * (self.velocidadE**0.5))) 
                self.Imodelneg.append(((self.q[pep][0]) * self.velocidadE) + (self.q[pep][1] * (self.velocidadE**0.5))) 
                self.Imodelpos_1.append( self.p[pep][0] * self.velocidadE )
                self.Imodelneg_1.append( self.q[pep][0] * self.velocidadE)
                self.Imodelpos_2.append( self.p[pep][1] * self.UKpos)
                self.Imodelneg_2.append( self.q[pep][1] * self.UKneg)

    def logpos_logneg_define(self):
        for i in range(len(self.Ipos)):
            self.logpos.append(np.emath.log10(self.Ipos[i]))
            self.logneg.append(np.emath.log10(self.Ineg[i]))

    def BposDefinition(self):
        for i in range(len(self.logpos)):
            self.bpos.append(np.polyfit( [self.Vlog], [self.logpos[i]],1))
            self.bneg.append(np.polyfit([self.Vlog], [self.logneg[i]] ,1))

        for rb in range(len(self.bpos)):
            self.rbpos.append( self.bpos[rb][0].real )
            self.rbneg.append( self.bneg[rb][0].real )

    def cargas_promedio(self):
        for i in range(len(self.Imodelneg)):    

            media_positiva = ((( np.abs(self.Imodelpos_1[i] ) )*self.difV) /self.velocidadE)
            media_negativa = ((( np.abs(self.Imodelneg_1[i] ) )*self.difV) /self.velocidadE)
            self.Qc.append( ((media_positiva + media_negativa)/2))
            
            media_positiva = ( ( ( np.abs(self.Imodelpos_2[i] ) )*self.difV) /self.velocidadE)
            media_negativa = ( ( ( np.abs(self.Imodelneg_2[i] ) )*self.difV) /self.velocidadE)
            self.Qd.append( ((media_positiva + media_negativa)/2))
  
    def frac_capaci(self):
        for i in range( len(self.Imodelpos_1)):
            self.FracCapacipos.append( self.Imodelpos_1[i] / self.Imodelpos[i])
            self.FracCapacineg.append( self.Imodelneg_1[i] / self.Imodelneg[i])
            self.FracDiffuspos.append( self.Imodelpos_2[i] / self.Imodelpos[i])
            self.FracDiffusneg.append( self.Imodelneg_2[i] / self.Imodelneg[i])

    def KI_dentif(self):
        for i in range(len(self.p)):
            self.KIdentifpos.append( self.p[i][0] )
            self.KIdentifneg.append( self.q[i][0] )
    
    def insertograma(self):
        self.Qdpos = 0
        self.Qdneg = 0

        for i in range(len(self.Imodelpos_1)):
            self.Qdpos = (self.Qdpos + ((self.Imodelpos_2[i]* self.difV)/self.velocidadE)) # A/g*s
            self.Qdneg = (self.Qdneg + ((self.Imodelneg_2[i]* self.difV)/self.velocidadE))# A/g*s
            self.insert.append( self.cteact * ((self.Qd[i]/self.masalec)/10000) *1E+7 )
            # self.inserneg.append( self.cteact * (self.Qdneg/self.masalec) )
        fig, ax = plt.subplots(1,1)
        ax.plot(self.linspace_varr[0][0:len(self.linspace_varr[0])-1], self.insert, 'b')
        ax.set_xlabel('E(V vs Electrodo')
        ax.set_ylabel('Active Thickness nm')
        return fig

        #Muestra 6 Active Thickness
        ## X E(V vs Electrodo "Electrodo es input de usuario") 
        ## Y ACtive Thickness nm


        ## M ng
        ## V
        

    def bars(self) -> Barras:
        """
        Graficas de barrras
        """
        for i in range(len(self.Imodelneg)):
            self.barras.append( [ ((self.Qc[i])-(self.DLC/self.DivWin)), (self.Qd[i]), (self.DLC/self.DivWin) ] )
        self.pandasdt = pd.DataFrame(self.barras,  columns = [ 'Capacitiva','Difusiva','Doble layer' ])
        
        b = Barras(pandasdt=self.pandasdt, barras = self.barras)
        return b.canvas
    
    def porcentaje(self):
        """
        Genera las graficas de porcentaje de las corrientes.
        """

        p = Porcentaje(pd.DataFrame(self.barras,  columns = [ 'Capacitiva','Difusiva','Doble layer' ]) )
        return p.canvas
    
    def masograma(self):

        """
        Genera el masograma calculando masapos y masaneg.
        """
        

        Qdpos=0
        Qdneg=0
        Mmol = 7 #g/mol
        elec = 1
        masaelec= 0.0033*0.7;
        
        for i in range(len(self.Imodelneg_2)):
            Qdpos = Qdpos+ (self.Imodelpos_2[i]*self.difV)/self.velocidadE
            Qdneg = Qdneg- (self.Imodelneg_2[i]*self.difV)/self.velocidadE
            self.masapos.append( Mmol * Qdpos * masaelec / (elec * 96500))
            self.masaneg.append( Mmol * Qdneg * masaelec / (elec * 96500))


        self.masapos = np.array(self.masapos)
        self.masaneg = np.array(self.masaneg)


        m = Masograma(self.linspace_varr, self.masapos, self.masaneg)
        return m.canvas
    
    #Empezamos con devolver las graficas con los datos
    def generate_plots(self) -> Muestra1:
        """
        Genera los plots para devolver todos los canvas de la interpolacion 
        """
        v = Muestra1(self.UExp, self.IExp, self.UExppos, self.IExppos, self.velocidad, self.electron_refernce)
        return v.canvas
    
    def generate_corriente_total(self) -> CorrienteTotal:
        """
        Genera los plots para devolver todos los canvas de corrientes totales
        """        
        c = CorrienteTotal(self.linspace_varr[0], self.UExp, self.IExp, self.Imodelpos, self.Imodelneg, self.velocidad)
        return c.canvas
    
    def generate_StepBars(self) -> StepBars:
        """
        Genera los plots para devolver todos los canvas de corrientes totales en steps
        """        
        c = StepBars(self.barras)
        return c.canvas

    def list_data(self) -> OutputData:
        """
        Devuelve un objeto con todos los datos internos para imprimirse
        """
        return OutputData(
            self.UExppos,
            self.IExppos
        )
    