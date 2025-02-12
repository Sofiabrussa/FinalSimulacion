import pandas as pd
from backend.simulacion import Simulacion

#Ejecucion
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)
sim = simular()  # Crear una instancia de Simulacion
df_resultados, prob_ventas, punto_c = sim.simular(horas=10, gasto=5)  # Ejecutar la simulación
print(df_resultados)  # Mostrar todas las iteraciones en formato de tabla