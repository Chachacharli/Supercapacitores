
import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import math
from scipy.optimize import curve_fit, least_squares

def plot_initial_data(df):
    plt.plot( df['X'], df['Y'], color='red', label='Datos originales filtrados por tiempo')
    plt.show()


def model_f(t, E, Rs, CDL, B):
    return ( (((E/Rs) * np.exp(-(t/(Rs*CDL)) ))) + (B/np.sqrt(t)) + E )
    
def diffusive(t: np.ndarray, t0: float, E: float, Rs: float, Cdl: float, B: float) -> np.ndarray:
    return B/np.sqrt(t - t0)  # + E


def capacitive(t: np.ndarray, t0: float, E: float, Rs: float, Cdl: float, B: float) -> np.ndarray:
    return E*(1 + np.exp(-(t - t0)/Rs/Cdl)/Rs)


def decay_model(t: np.ndarray, t0: float, E: float, Rs: float, Cdl: float, B: float) -> np.ndarray:
    i = (capacitive(t, t0, E, Rs, Cdl, B)
        + diffusive(t, t0, E, Rs, Cdl, B)
        + E )
    return i


model_f = np.vectorize(model_f)


timepo_actual = 2.47E+02 + (5*60)
rango = 5*60



if __name__ == '__main__':



    df = pd.read_csv(r'C:\Users\TCCA_\OneDrive\Escritorio\GUI_SUPERCAPACITORES\raw_data.csv', names=['time', 'current'], skiprows=1)
    #print(df)
    

    

    df.time -= df.time.min()
    df = df[
        (df.time > 25) |
        (df.current > 2.5e-3)
    ].loc[1:, :]
    popt, *_ = curve_fit(
        f=decay_model, xdata=df.time, ydata=df.current,
        p0=(0.1,  0.1, 1e-2, 1e2, 0),
        bounds=(
            ( 0, 1e-6, 1e-3,   1,   0),
            (10,    1,    1, 1e3,   1),
        ),
    )
    #print(popt)
    
    fig, ax = plt.subplots()
    # plt.plot(df.time, df.current, label='Original data')
    # ax.semilogx(df.time, diffusive(df.time, *popt), label='Diffusive fit')
    # ax.semilogx(df.time, capacitive(df.time, *popt), label='Capacitive fit')
    # ax.semilogx(df.time, decay_model(df.time, *popt), label='Total fit')

    # plt.legend()
    #plt.show()