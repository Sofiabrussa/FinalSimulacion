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
        
    def atencion (self, reloj: float):
        rnd_atencion = round(random.random(), 2) #Genero random para la atencion 
        atencion = False
        fin_atencion = 0
        
        if rnd_atencion <= self.prob_atencion: 
            atencion = "SI"
        else:
            atencion = "NO"
            fin_atencion = reloj + self.tiempo_no_atencion
        
        return atencion, fin_atencion, rnd_atencion
    
    def genero (self, atencion: str ):
        if atencion == "SI":
            rnd_genero = round(random.random(), 2) #Genero rnd de genero
            genero = ""
            
            if rnd_genero <= self.prob_genero:
                genero = "MUJER"
            else:
                genero = "HOMBRE"
            
            return genero, rnd_genero
        return None, None  #Aseguraro de devolver algo
    
    def tiempoAtencion(self, venta: str, cantidad_suscripciones: int):
        if venta == "NO":
            random_entre_min_max = random.randint(self.tiempo_no_venta_min , self.tiempo_no_venta_max)
            tiempo_atencion = random_entre_min_max 
            return random_entre_min_max, tiempo_atencion 
        else:
            random_entre_min_max = random.randint(self.tiempo_venta_min, self.tiempo_venta_max)
            tiempo_atencion = random_entre_min_max + self.tiempo_extra * cantidad_suscripciones
            return random_entre_min_max, tiempo_atencion 
    
    def Venta (self, genero: str, reloj: float):
        if genero:
            rnd_venta = round(random.random(), 2) #Genero rnd de venta
            venta = False
            fin_venta = 0
            rnd_suscripciones = 0
            
            #Verifico si la venta es exitosa y calculo cantidad de suscripciones
            if genero == "MUJER" and rnd_venta <= self.prob_venta_mujer:
                venta = "SI"
                cantidad_suscripciones, rnd_suscripciones = self.calcular_suscripciones(genero)
            elif genero == "HOMBRE" and rnd_venta <= self.prob_venta_hombre:
                venta = "SI"
                cantidad_suscripciones, rnd_suscripciones = self.calcular_suscripciones(genero)
            else:
                venta = "NO"
                cantidad_suscripciones = 0
            
            # Calculo el tiempo de atención 
            rndTiempoAtencion, tiempo_atencion = self.tiempoAtencion(venta, cantidad_suscripciones)
            fin_venta = reloj + tiempo_atencion
            return venta, fin_venta, rnd_venta, cantidad_suscripciones, rnd_suscripciones, rndTiempoAtencion, tiempo_atencion
        return "NO", 0, 0 , 0 , 0, 0, 0  
    
    def calcular_suscripciones(self, genero: str):
        if genero == "MUJER":
            frecuencias = [0.60, 0.25, 0.10, 0.05]
        elif genero == "HOMBRE":
            frecuencias = [0.20, 0.30, 0.35, 0.15]
        else:
            return 0
        
        rnd_suscripciones = round(random.random(), 2)
        
        if rnd_suscripciones <= frecuencias[0]: 
            return 1, rnd_suscripciones
        elif rnd_suscripciones <= sum(frecuencias[:2]): #sumo las dos prob para obetner el rango 0.60 a 0.85 (para mujer)
            return 2, rnd_suscripciones
        elif rnd_suscripciones <= sum(frecuencias[:3]): #sumo las tres prob para obetner el rango 0.85 a 0.95 (para mujer)
            return 3, rnd_suscripciones
        else:
            return 4, rnd_suscripciones
        


        
        
    
    
# Pruebas
casa = Casa()
atencion, fin_atencion, rnd_atencion = casa.atencion(reloj=10)  
genero, rnd_genero = casa.genero(atencion) 

# Si la atención es NO, el fin_atencion ya está definido. Si es SI, se usa Venta.
if atencion == "SI":
    venta, fin_venta, rnd_venta, cant_suscripciones, rnd_suscripciones, rndTiempoAtencion, tiempo_atencion = casa.Venta(genero, reloj=10)
    fin_atencion = fin_venta 
else:
    venta, rnd_venta, cant_suscripciones, rnd_suscripciones, rndTiempoAtencion, tiempo_atencion = "NO", 0, 0, 0, 0, 0

print(f"RNDAtencion: {rnd_atencion}, Atención: {atencion}, RNDGenero: {rnd_genero}, Género: {genero}, RNDVenta: {rnd_venta}, Venta: {venta}, RNDSuscripcion: {rnd_suscripciones}, cant_suscripciones: {cant_suscripciones}, RND Atencion: {rndTiempoAtencion}, Tiempo Atencion: {tiempo_atencion}, Fin atencion:  {fin_atencion}")
