from simulacion import Simulacion
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Defino el formato esperado de los datos en la solicitud
class SimulacionRequest(BaseModel):
    prob_atencion: float
    prob_genero: float
    prob_venta_mujer: float
    prob_venta_hombre: float
    utilidad: float
    gasto: float
    tiempo_no_atencion: float
    tiempo_no_venta_min: float
    tiempo_no_venta_max: float
    tiempo_venta_min: float
    tiempo_venta_max: float
    tiempo_extra: float
    cantidad_horas_simular: int

@app.post("/simulacion")
async def simulate(request: SimulacionRequest):
    try:
        sim = Simulacion()
        
        sim.simular(
            prob_atencion=request.prob_atencion,
            prob_genero=request.prob_genero,
            prob_venta_mujer=request.prob_venta_mujer,
            prob_venta_hombre=request.prob_venta_hombre,
            utilidad=request.utilidad,
            gasto=request.gasto,
            tiempo_no_atencion=request.tiempo_no_atencion,
            tiempo_no_venta_min=request.tiempo_no_venta_min,
            tiempo_no_venta_max=request.tiempo_no_venta_max,
            tiempo_venta_min=request.tiempo_venta_min,
            tiempo_venta_max=request.tiempo_venta_max,
            tiempo_extra=request.tiempo_extra,
            cantidad_horas_simular=request.cantidad_horas_simular,
        )

        df, prob_ventas, punto_c = sim.obtener_resultados()
        return {
            "results": df.to_dict(orient="records"),
            "prob_ventas": prob_ventas,
            "punto_c": punto_c
        }

    except Exception as e:
        return {"error": str(e)}    
