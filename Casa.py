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
    
