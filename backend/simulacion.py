import pandas as pd
import numpy as np
from casa import Casa

class Simulacion:
    
    #Constructor Simulacion
    def __init__(self):
        self.reloj = 0
        self.gasto = 0
        self.casa = None
        self.acu_ganancias = 0
        self.acu_costo = 0
        self.cont_ventas = 0
        self.cont_suscripciones = 0
        self.resultados = []
        self.total_filas = 0

    #Funcion "Simular" simula el proceso de atencion y venta de las casas en un determinado tiempo 
    def simular(self, horas, gasto, prob_atencion, prob_genero, prob_venta_mujer, prob_venta_hombre, utilidad, tiempo_no_atencion, tiempo_no_venta_min, tiempo_no_venta_max, tiempo_venta_min, tiempo_venta_max, tiempo_extra):
        self.gasto = gasto
        self.reloj = 0
        fila = 1
        fin_sim = horas * 60  
        #Proceso la primer casa
        self.casa = Casa() 
        self.reloj = self.__procesar_casa(fila)

        while self.reloj < fin_sim:
            fila += 1
            # Nueva casa en cada iteración
            self.casa = Casa()
            self.reloj = self.__procesar_casa(fila)

        self.total_filas = fila
        
    
    #Funcion "procesar_casa"  procesa una casa en la simulación utilizando las funciones de Casa
    def __procesar_casa(self, fila):
        atencion, fin_atencion, rnd_atencion, tiempo_no_atencion  = self.casa.atencion(self.reloj)
        genero, rnd_genero = self.casa.genero(atencion)
    
        if atencion:
            rnd_venta, venta, rnd_suscripciones, cantidad_suscripciones, rndTiempoAtencion, tiempo_atencion, fin_venta = self.casa.venta(fin_atencion)
            fin_atencion = fin_venta 
            atencion = "SI"
            if venta:
                venta = "SI"
            else:
                venta = "NO"
        else:
            rnd_venta, venta, rnd_suscripciones, cantidad_suscripciones, rndTiempoAtencion, tiempo_atencion, fin_venta = "NO", 0, 0 , 0, 0, 0, 0
            atencion = "NO"
            tiempo_atencion = tiempo_no_atencion
    
        #Acumuladores
        self.acu_ganancias += self.casa.utilidad * cantidad_suscripciones
        self.acu_costo += self.gasto

        #Contadores
        if venta == "SI":
            self.cont_ventas += 1
            self.cont_suscripciones += cantidad_suscripciones  

        self.resultados.append([
            fila, self.reloj, rnd_atencion, atencion, rnd_genero, genero, 
            rndTiempoAtencion, tiempo_atencion, fin_atencion, rnd_venta, venta, 
            rnd_suscripciones, cantidad_suscripciones, self.casa.utilidad * cantidad_suscripciones, self.gasto, 
            self.acu_ganancias, self.acu_costo, fila, self.cont_ventas, self.cont_suscripciones
        ])
        
        return fin_atencion
    
    def obtener_resultados(self):
        prob_ventas = round(self.cont_ventas / self.total_filas , 2) if self.total_filas > 0 else 0 #Calcula la proporción de ventas sobre el total de casas procesadas.
        punto_c = round((self.cont_suscripciones / self.total_filas) * 10000, 0) if self.total_filas > 0 else 0 #Calcula un índice de suscripciones, multiplicándolo por 10,000.

        df = pd.DataFrame(self.resultados, columns=[
            "Nro Fila", "Reloj", "RND Atencion", "Atencion", "RND Genero", "Genero", 
            "RND Tiempo Atencion", "Tiempo Atención", "Fin Atención", "RND Venta", "Venta", 
            "RND Cantidad", "Cantidad", "Ganancia", "Costo", "Ganancia Acumulada", 
            "Costo Acumulado", "Contador Visitas", "Contador Ventas", "Contador Suscripciones"
        ])
        
        # Reemplazar valores fuera de rango o NaN
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)
        df["Genero"] = df["Genero"].fillna("-")

        return df, prob_ventas, punto_c




