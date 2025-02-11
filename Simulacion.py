import pandas as pd
import numpy as np
from Casa import Casa

class Simulacion:
    
    #Constructor Simulacion
    def __init__(self):
        self.reloj = 0
        self.casa = None
        self.acu_ganancias = 0
        self.acu_costo = 0
        self.cont_ventas = 0
        self.cont_suscripciones = 0
        self.resultados = []

    #Funcion "Simular" simula el proceso de atencion y venta de las casas en un determinado tiempo 
    def simular(self, horas, gasto):
        fin_sim = horas * 60  
        self.reloj = 0
        fila = 0
        #Proceso la primer casa
        self.casa = Casa() 
        nuevo_reloj = self.procesar_casa(fila, gasto, self.reloj)  
        self.reloj = nuevo_reloj

        while self.reloj < fin_sim:
            fila += 1
            # Nueva casa en cada iteración
            self.casa = Casa()
            nuevo_reloj = self.procesar_casa(fila, gasto, self.reloj)
            self.reloj = nuevo_reloj 

        prob_ventas = round(self.cont_ventas / fila, 2) if fila > 0 else 0 #Calcula la proporción de ventas sobre el total de casas procesadas.
        punto_c = round((self.cont_suscripciones / fila) * 10000, 0) if fila > 0 else 0 #Calcula un índice de suscripciones, multiplicándolo por 10,000.
    
        return pd.DataFrame(self.resultados, columns=[
            "Nro Fila", "Reloj", "RND Atencion", "Atencion", "RND Genero", "Genero", 
            "RND Tiempo Atencion", "Tiempo Atención", "Fin Atención", "RND Venta", "Venta", 
            "RND Cantidad", "Cantidad", "Ganancia", "Costo", "Ganancia Acumulada", 
            "Costo Acumulado", "Contador Visitas", "Contador Ventas", "Contador Suscripciones"
        ]), prob_ventas, punto_c
    
    #Funcion "procesar_casa"  procesa una casa en la simulación utilizando las funciones de Casa
    def procesar_casa(self, fila, gasto, reloj: int):
        atencion, fin_atencion, rnd_atencion = self.casa.atencion(reloj)
        genero, rnd_genero = self.casa.genero(atencion)
    
        if atencion:
            rnd_venta, venta, rnd_suscripciones, cantidad_suscripciones, rndTiempoAtencion, tiempo_atencion, fin_venta = self.casa.venta(fin_atencion)
            fin_atencion = fin_venta 
        else:
            rnd_venta, venta, rnd_suscripciones, cantidad_suscripciones, rndTiempoAtencion, tiempo_atencion, fin_venta = "NO", 0, 0 , 0, 0, 0, 0
    
        #Acumuladores
        self.acu_ganancias += self.casa.utilidad * cantidad_suscripciones
        self.acu_costo += gasto

        #Contadores
        if venta:
            self.cont_ventas += 1
            self.cont_suscripciones += cantidad_suscripciones  

        self.resultados.append([
            fila, self.reloj, rnd_atencion, atencion, rnd_genero, genero, 
            rndTiempoAtencion, tiempo_atencion, fin_atencion, rnd_venta, venta, 
            rnd_suscripciones, cantidad_suscripciones, self.casa.utilidad * cantidad_suscripciones, gasto, 
            self.acu_ganancias, self.acu_costo, fila, self.cont_ventas, self.cont_suscripciones
        ])
        
        return fin_atencion


#Ejecucion
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)
sim = Simulacion()  # Crear una instancia de Simulacion
df_resultados, prob_ventas, punto_c = sim.simular(horas=10, gasto=5)  # Ejecutar la simulación
print(df_resultados)  # Mostrar todas las iteraciones en formato de tabla
