from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="API de Predicción de Precios de Casas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que cualquier frontend se conecte para desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, etc.
    allow_headers=["*"],
)

modelo = joblib.load('models/modelo_casas.pkl')
columnas_entrenamiento = joblib.load('models/columnas_modelo.pkl')

# 2. Mensaje de bienvenida en la ruta principal
@app.get("/")
def ruta_principal():
    return FileResponse("index.html")

# 3. Estructura de validación de datos (El guardia de seguridad)
class CasaInput(BaseModel):
    Area_SqFt: float
    Rooms: float
    Build_Year: int
    Location: str
    Street_Type: str
    Furnishing: str
    Property_Type: str
    Has_Pool: str

# 4. El motor de predicción
@app.post("/predecir")
def predecir_precio(casa: CasaInput):
    # Convertimos a DataFrame
    df_input = pd.DataFrame([casa.model_dump()])
    # Pasamos el texto a binario
    df_dummies = pd.get_dummies(df_input)
    # Moldeamos las columnas para que coincidan con las del entrenamiento
    df_final = df_dummies.reindex(columns=columnas_entrenamiento, fill_value=0)
    # Hacemos la predicción
    prediccion = modelo.predict(df_final)
    return {
        "mensaje": "Predicción exitosa",
        "precio_estimado": round(prediccion[0], 2)
    }