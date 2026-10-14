from pathlib import Path
import pandas as pd

#estas tres primeras libres sirben para que el py corra da igual donde sea ejcutado

CARPETA_SCRIPT = Path(__file__).parent
RUTA_CSV = CARPETA_SCRIPT / "raw" / "vehicles.csv"
RUTA_JSON = CARPETA_SCRIPT.parent / "datos" / "coches.json"



NOMBRES = {
    "id": "id",
    "make": "marca",
    "model": "modelo",
    "year": "anio",
    "VClass": "carroceria",
    "consumo_l100km": "consumo_l100km",
    "consumo_kwh100km": "consumo_kwh100km",
    "autonomia_km": "autonomia_km",
    "charge240": "carga_horas",
    "co2_gkm": "co2_gkm",
    "displ": "cilindrada_l",
    "cylinders": "cilindros",
    "drive": "traccion",
    "trany": "transmision",
}

#EXTRACT

def extract():
    df = pd.read_csv(RUTA_CSV, low_memory=False)
    return df

def transform(df):
    # Filtrar solo los híbridos enchufables
    phev = df[df["atvType"] == "Plug-in Hybrid"].copy()

    # Corregir tipos
    phev["rangeA"] = pd.to_numeric(phev["rangeA"])
    phev["cylinders"] = phev["cylinders"].astype(int)

    # Convertir a unidades europeas
    phev["consumo_l100km"] = (235.215 / phev["comb08"]).round(1)
    phev["consumo_kwh100km"] = (phev["combE"] / 1.609344).round(1)
    phev["co2_gkm"] = (phev["co2TailpipeGpm"] / 1.609344).round(0).astype(int)
    phev["autonomia_km"] = (phev["rangeA"] * 1.609344).round(0).astype(int)

    # Seleccionar y renombrar columnas
    coches = phev[list(NOMBRES.keys())].rename(columns=NOMBRES)
    return coches

def load(coches):
    RUTA_JSON.parent.mkdir(exist_ok=True)
    coches.to_json(RUTA_JSON, orient="records", force_ascii=False, indent=2)

if __name__ == "__main__":
    coches = transform(extract())
    load(coches)
    print(f"Guardados {len(coches)} coches en {RUTA_JSON}")




