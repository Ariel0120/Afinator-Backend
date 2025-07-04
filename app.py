from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np
import io
 
app = FastAPI()
 
# Configura CORS (permite conexiones desde tu frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs (cambia luego a tu GitHub Pages)
    allow_methods=["POST"],  # Solo acepta peticiones POST
)
 
@app.post("/afinar")
async def afinar_voz(audio: UploadFile = File(...)):
    # 1. Leer el audio del usuario
    audio_bytes = await audio.read()
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=44100)
    # 2. Simular afinación (aquí iría tu IA real)
    voz_afinada = y * 1.2  # Ejemplo: sube el pitch un 20%
    return {
        "voz_afinada": voz_afinada.tolist(),  # Convierte a lista para JSON
        "sample_rate": sr
    }