import pandas as pd
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

# permite definir el formato esperado de los datos en la solicitud
class SimulacionRequest(BaseModel):
    horas: int
    gasto: float

@app.post("/simulacion")
async def simulate(request: SimulacionRequest):
    try:
        sim = Simulacion()
        sim.simular(horas=request.horas, gasto=request.gasto)
        df, prob_ventas, punto_c = sim.obtener_resultados()
        return {
            "results": df.to_dict(orient="records"),
            "prob_ventas": prob_ventas,
            "punto_c": punto_c
        }
    except Exception as e:
        print(f"Error en la simulación: {e}")  # Log para identificar el error
        raise HTTPException(status_code=500, detail=str(e))
