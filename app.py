from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np
import io
import json
from typing import Optional
import uvicorn
import os
 
app = FastAPI()
 
# Configura CORS para permitir tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia a tu URL de GitHub Pages
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
 
# Endpoint de prueba
@app.get("/")
async def health_check():
    return {"status": "API funcionando", "endpoint": "/afinar"}
 
# Endpoint principal
@app.post("/afinar")
async def afinar_voz(
    audio: UploadFile = File(...),
    note: str = Form("C"),
    octave: str = Form("4"),
    scale: str = Form("major"),
    sensitivity: str = Form("5")
):
    try:
        # 1. Validar archivo de audio
        if not audio.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Formato de audio no soportado")
 
        # 2. Leer y procesar audio
        audio_bytes = await audio.read()
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=44100)
        # 3. Simular afinación (aquí integrarías tu IA real)
        pitch_shift = 2 if note == "C" else -2  # Ejemplo básico
        y_tuned = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_shift)
        # 4. Convertir a bytes para respuesta
        audio_buffer = io.BytesIO()
        librosa.output.write_wav(audio_buffer, y_tuned, sr)
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
        return {
            "status": "success",
            "original_samples": len(y),
            "tuned_samples": len(y_tuned),
            "sample_rate": sr,
            "voz_afinada": audio_base64,
            "detected_pitch": "C4",  # Simulación
            "target_pitch": f"{note}{octave}"
        }
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar audio: {str(e)}")
 
def base64_to_blob(base64_str: str) -> bytes:
    return base64.b64decode(base64_str)
 
# Configuración para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)