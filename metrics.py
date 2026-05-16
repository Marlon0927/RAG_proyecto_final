import pandas as pd
import os

CSV_PATH = "metricas.csv"

# ========================================
# FIDELIDAD
# ========================================

def evaluar_fidelidad(respuesta, contexto):

    respuesta = respuesta.lower()
    contexto = contexto.lower()

    palabras = [

        palabra

        for palabra in respuesta.split()

        if len(palabra) > 5
    ]

    if len(palabras) == 0:

        return 0

    coincidencias = sum(

        1

        for palabra in palabras

        if palabra in contexto
    )

    score = coincidencias / len(palabras)

    return round(score, 2)

# ========================================
# RELEVANCIA
# ========================================

def evaluar_relevancia(distancias):

    if not distancias:

        return 0

    promedio = sum(distancias) / len(distancias)

    score = 1 - promedio

    return round(max(score, 0), 2)

# ========================================
# GUARDAR MÉTRICAS
# ========================================

def guardar_metricas(data):

    df = pd.DataFrame([data])

    existe = os.path.exists(CSV_PATH)

    df.to_csv(

        CSV_PATH,

        mode="a",

        header=not existe,

        index=False
    )