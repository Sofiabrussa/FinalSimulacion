import random 

class Casa:
    #Constructor
    def __init__(self, prob_atencion=0.7, prob_genero=0.8, prob_venta_mujer=0.15, prob_venta_hombre=0.3,
                 utilidad=5, gasto=0.5, tiempo_no_atencion=2, tiempo_no_venta_min=15, tiempo_no_venta_max=25,
                 tiempo_venta_min=15,tiempo_venta_max=15, tiempo_extra=4, cantidad_horas_simular=8):
        self.prob_atencion = prob_atencion
        self.prob_genero = prob_genero
        self.prob_venta_mujer = prob_venta_mujer
        self.prob_venta_hombre = prob_venta_hombre
        self.utilidad = utilidad
        self.gasto = gasto
        self.tiempo_no_atencion = tiempo_no_atencion
        self.tiempo_no_venta_min = tiempo_no_venta_min
        self.tiempo_no_venta_max = tiempo_no_venta_max
        self.tiempo_venta_min = tiempo_venta_min
        self.tiempo_venta_max = tiempo_venta_max
        self.tiempo_extra = tiempo_extra
        self.cantidad_horas_simular = cantidad_horas_simular
        
    def atencion (self, reloj: int):  #atencion recibe el reloj, si no lo atienden, se suma el tiempo de no atencion. Si lo atienden, se retorna valor del reloj normal 
        rnd_atencion = round(random.uniform(0, 0.99), 2)
       
        if rnd_atencion <= self.prob_atencion:
            return True, reloj, rnd_atencion  
        else:
            return False, reloj + self.tiempo_no_atencion, rnd_atencion  

        
    def genero (self, atencion: bool ):
        if atencion:
            rnd_genero = round(random.uniform(0, 0.99), 2) #Genero rnd genero
            
            if rnd_genero <= self.prob_genero:
                return "MUJER", rnd_genero
            else:
                return "HOMBRE", rnd_genero
        else:
            return None, 0  # Usar None para indicar que no se generó un género
    
    def tiempoAtencion(self, venta: bool, cantidad_suscripciones: int):
        if not venta :
            random_entre_min_max = random.randint(self.tiempo_no_venta_min , self.tiempo_no_venta_max)
            tiempo_atencion = random_entre_min_max 
            return random_entre_min_max, tiempo_atencion 
        else:
            random_entre_min_max = random.randint(self.tiempo_venta_min, self.tiempo_venta_max)
            tiempo_atencion = random_entre_min_max + self.tiempo_extra * cantidad_suscripciones
            return random_entre_min_max, tiempo_atencion 
    
    def venta (self, reloj: int):
        
        genero, rnd_genero = self.genero(True)   
        rnd_venta = round(random.uniform(0, 0.99), 2) #Genero rnd de venta
        venta = False
        cantidad_suscripciones = 0
        rnd_suscripciones = 0 
            
        # Determinar si la venta es exitosa según el género
        if (genero == "MUJER" and rnd_venta <= self.prob_venta_mujer) or (genero == "HOMBRE" and rnd_venta <= self.prob_venta_hombre):
            venta = True
            cantidad_suscripciones, rnd_suscripciones = self.calcular_suscripciones(genero)
    
        # Calculo el tiempo de atención 
        rndTiempoAtencion, tiempo_atencion = self.tiempoAtencion(venta, cantidad_suscripciones)
        fin_venta = reloj + tiempo_atencion
        
        return rnd_venta, venta, rnd_suscripciones, cantidad_suscripciones, rndTiempoAtencion, tiempo_atencion, fin_venta
        
    
    def calcular_suscripciones(self, genero: str):
        if genero == "MUJER":
            frecuencias = [0.60, 0.25, 0.10, 0.05]
        elif genero == "HOMBRE":
            frecuencias = [0.20, 0.30, 0.35, 0.15]
        else:
            raise ValueError("El género debe ser 'MUJER' o 'HOMBRE'. Valor recibido: {}".format(genero))
        
        rnd_suscripciones = round(random.uniform(0, 0.99), 2)
        
        if rnd_suscripciones <= frecuencias[0]: 
            return 1, rnd_suscripciones
        elif rnd_suscripciones <= sum(frecuencias[:2]): #sumo las dos prob para obetner el rango 0.60 a 0.85 (para mujer)
            return 2, rnd_suscripciones
        elif rnd_suscripciones <= sum(frecuencias[:3]): #sumo las tres prob para obetner el rango 0.85 a 0.95 (para mujer)
            return 3, rnd_suscripciones
        else:
            return 4, rnd_suscripciones
        


        
        
    