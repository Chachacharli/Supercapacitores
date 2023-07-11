import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares
from scipy.stats import linregress

def model_f(t, E, Rs, CDL, B):
    return ( (((E/Rs) * np.exp(-(t/(Rs*CDL)) ))) + (B/np.sqrt(t)) + E )
    
model_f = np.vectorize(model_f)

df = pd.read_excel(r'C:\Users\TCCA_\OneDrive\Escritorio\GUI_SUPERCAPACITORES\PCGA-SDR1-3-30-3M-CaNO3.xlsx', names=['X','Y'], skiprows=2)

initial_time = 2.47E+02 #s
rang = 60*5
initial_step = initial_time + rang
end_step = initial_step + rang

step =  df[(df['X'] >= initial_step) & (df['X'] <= end_step)]
peak = step['Y'].max()
index_peak = step['Y'].idxmax()


step = step.loc[index_peak:]


x_values = step['X'].values
y_values = step['Y'].values
print(len(x_values))
print(len(y_values))

distancias = []
for i in range(len(x_values)):
    distancia = np.sqrt((x_values[i] - x_values[i-1])**2 + (y_values[i] - y_values[i-1])**2)
    distancias.append(distancia)

# Calcula la media de las distancias
media_distancias = np.mean(distancias)
print(media_distancias)
print(step)

df_filtrado = step[distancias <= media_distancias]

# df_filtrado = step[condicion]
#popt, _ = curve_fit(model_f, step['X'], step['Y'])

#print(popt)

filtro = ((df >= -0.000010) & (df <= 0.000010))
df_reemplazado = step.where(~filtro, pd.NA)
df_sin_menores = df_reemplazado.dropna()

print(df_sin_menores)

# Obtener los valores de 'x' y 'y' como arrays numpy
x = df_sin_menores['X'].values
y = df_sin_menores['Y'].values

# Realizar la regresión lineal utilizando linregress de SciPy
slope, intercept, r_value, p_value, std_err = linregress(x, y)
y_pred = slope * x + intercept

# Imprimir los coeficientes y el coeficiente de determinación (r cuadrado)
print('Coeficiente:', slope)
print('Intercepto:', intercept)
print('Coeficiente de determinación (r cuadrado):', r_value ** 2)

plt.plot(df_sin_menores['X'], df_sin_menores['Y'])
plt.scatter(step.loc[index_peak, 'X'],step.loc[index_peak, 'Y'], color='orange')
plt.plot(x, y_pred, color='red', label='Regresión lineal')
plt.show()

