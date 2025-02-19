import random 

class SEXO:
    HOMBRE = "HOMBRE"
    MUJER = "MUJER"

class Casa:
    #Constructor Casa
    def __init__(self, prob_atencion, prob_genero, prob_venta_mujer, prob_venta_hombre,
                 utilidad, gasto, tiempo_no_atencion, tiempo_no_venta_min, tiempo_no_venta_max,
                 tiempo_venta_min,tiempo_venta_max, tiempo_extra, cantidad_horas_simular):
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
        
    #Funcion "atencion" recibe el reloj, si no lo atienden, se suma el tiempo de no atencion. Si lo atienden, se retorna valor del reloj    
    def atencion(self, reloj: int):   
        rnd_atencion = random.uniform(0.01, 0.99)
       
        if rnd_atencion <= self.prob_atencion:
            return True, reloj, rnd_atencion, self.tiempo_no_atencion
        else:
            return False, reloj + self.tiempo_no_atencion, rnd_atencion, self.tiempo_no_atencion  

    #Funcion "genero" recibe si fue atendido o no. Si lo atienden, calcula si es mujer u hombre  
    def genero(self, atencion: bool ):
        if atencion:
            rnd_genero = random.uniform(0.01, 0.99) 
            
            if rnd_genero <= self.prob_genero:
                return SEXO.MUJER, rnd_genero
            else:
                return SEXO.HOMBRE, rnd_genero
        else:
            return "-", 0 
    
    #Funcion "tiempo_atencion" recibe si hubo venta y en base a eso calcula el tiempo de venta o no venta
    # valor=min+(random×(max−min))
    def tiempo_atencion(self, venta: bool, cantidad_suscripciones: int):
        random_para_min_max = random.uniform(0.01, 0.99) 
        
        if venta :
            random_entre_min_max = (random_para_min_max * (self.tiempo_venta_max - self.tiempo_venta_min)) + self.tiempo_venta_min
            tiempo_atencion = random_entre_min_max + self.tiempo_extra * cantidad_suscripciones   
        else:
            random_entre_min_max = self.tiempo_no_venta_min + random_para_min_max * (self.tiempo_no_venta_max - self.tiempo_no_venta_min)
            tiempo_atencion = random_entre_min_max 
        
        return random_para_min_max, tiempo_atencion 
   
   #Funcion "venta" recibe el reloj actual, calcula en base a si es hombre o mujer si se concreta o no la venta 
    def venta(self, reloj: int, genero, rnd_genero):  
        rnd_venta = random.uniform(0.01, 0.99)
        venta = False
        cantidad_suscripciones = 0
        rnd_suscripciones = 0
        
        if genero == SEXO.MUJER:
            if rnd_venta <= self.prob_venta_mujer:
                venta = True
                cantidad_suscripciones, rnd_suscripciones = self.calcular_suscripciones(genero)
        elif genero == SEXO.HOMBRE:
            if rnd_venta <= self.prob_venta_hombre:
                venta = True
                cantidad_suscripciones, rnd_suscripciones = self.calcular_suscripciones(genero)
    
        # Calculo el tiempo de atención 
        rndTiempoAtencion, tiempo_atencion = self.tiempo_atencion(venta, cantidad_suscripciones)
        fin_venta = reloj + tiempo_atencion
        
        return rnd_venta, venta, rnd_suscripciones, cantidad_suscripciones, rndTiempoAtencion, tiempo_atencion, fin_venta
        
    
    #Funcion "calcular_suscripciones" recibe el genero y segun estadisticas calcula la cantidad de suscripciones que vende
    def calcular_suscripciones(self, genero: str):
        if genero == SEXO.MUJER:
            frecuencias = [0.60, 0.25, 0.10, 0.05]
        elif genero == SEXO.HOMBRE:
            frecuencias = [0.20, 0.30, 0.35, 0.15]
        else:
            raise ValueError("El género debe ser 'MUJER' o 'HOMBRE'. Valor recibido: {}".format(genero))
        
        rnd_suscripciones = random.uniform(0.01, 0.99)
        
        if rnd_suscripciones <= frecuencias[0]: 
            return 1, rnd_suscripciones
        elif rnd_suscripciones <= sum(frecuencias[:2]): 
            return 2, rnd_suscripciones
        elif rnd_suscripciones <= sum(frecuencias[:3]): 
            return 3, rnd_suscripciones
        else:
            return 4, rnd_suscripciones
        


        
        
    