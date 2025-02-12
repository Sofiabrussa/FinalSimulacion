import pandas as pd
from simulacion import Simulacion

#Ejecucion
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)

sim = Simulacion()  # Crear una instancia de Simulacion
sim.simular(horas=10, gasto=5)  # Ejecutar la simulación

df, prob_ventas, punto_c = sim.obtener_resultados()

print(df) 