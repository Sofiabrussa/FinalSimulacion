import pandas as pd
from simulacion import Simulacion
from fastapi import FastAPI

""" #Ejecucion
pd.set_option('display.max_rows', None)  # Muestra todas las filas
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)
 """
app = FastAPI()

@app.post("/simulacion")
async def simulate(horas: int, gasto: float):
    sim = Simulacion()
    sim.simular(horas=240, gasto=5)
    df, prob_ventas, punto_c = sim.obtener_resultados()

    return {
        "results": df.to_dict(orient="records"),
        "prob_ventas": prob_ventas,
        "punto_c": punto_c
    }