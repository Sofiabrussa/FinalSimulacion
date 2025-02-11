import pandas as pd
import numpy as np
from Casa import Casa

class Simulacion:
    def __init__(self):
        self.reloj = 0
        self.casa = None
        self.acu_ganancias = 0
        self.acu_costo = 0
        self.cont_ventas = 0
        self.cont_suscripciones = 0
        self.resultados = []

    def simular(self, horas, gasto):
        fin_sim = horas * 60 #Se convierte la simulacion en minutos
        fila = 0
        self.casa = Casa() #se instancia la primer casa
        self.procesar_casa(fila, gasto) #Se procesa la primer fila

        while self.reloj < fin_sim:
            fila += 1 # Se incrementa el número de iteraciones.
            atencion, fin_atencion, rnd_atencion = self.casa.atencion(self.reloj)
            if atencion == "SI":
                self.reloj += 1  # Avanzar en caso de atención
            else:
                self.reloj = max(self.reloj + 1, fin_atencion)  # Asegurar avance en caso de "NO"

            self.casa = Casa()
            self.procesar_casa(fila, gasto)

        prob_ventas = round(self.cont_ventas / fila, 2)
        punto_c = round((self.cont_suscripciones / fila) * 10000, 0)
        print(f"[DEBUG] Fila: {fila}, Reloj: {self.reloj}")  #quitar esto 

        
        return pd.DataFrame(self.resultados, columns=[
            "Nro Fila", "Reloj", "RND Atencion", "Atencion", "RND Genero", "Genero", 
            "RND Tiempo Atencion", "Tiempo Atención", "Fin Atención", "RND Venta", "Venta", 
            "RND Cantidad", "Cantidad", "Ganancia", "Costo", "Ganancia Acumulada", 
            "Costo Acumulado", "Contador Visitas", "Contador Ventas", "Contador Suscripciones"
        ]), prob_ventas, punto_c
    
    def procesar_casa(self, fila, gasto):
        atencion, fin_atencion, rnd_atencion = self.casa.atencion(self.reloj)
        genero, rnd_genero = self.casa.genero(atencion)
        venta, fin_venta, rnd_venta, cant_venta, rnd_cant_venta, rnd_tiempo_atencion, tiempo_atencion = self.casa.venta(genero, self.reloj)
        
        self.acu_ganancias += self.casa.utilidad * cant_venta
        self.acu_costo += gasto
        if venta == "SI":
            self.cont_ventas += 1
            self.cont_suscripciones += cant_venta
        
        self.resultados.append([
            fila, self.reloj, rnd_atencion, atencion, rnd_genero, genero, 
            rnd_tiempo_atencion, tiempo_atencion, fin_atencion, rnd_venta, venta, 
            rnd_cant_venta, cant_venta, self.casa.utilidad * cant_venta, gasto, 
            self.acu_ganancias, self.acu_costo, fila, self.cont_ventas, self.cont_suscripciones
        ])


#Ejecucion
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)
sim = Simulacion()  # Crear una instancia de Simulacion
df_resultados, prob_ventas, punto_c = sim.simular(horas=10, gasto=5)  # Ejecutar la simulación
print(df_resultados)  # Mostrar todas las iteraciones en formato de tabla
