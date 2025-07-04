from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np
import io
import base64
import uvicorn
 
app = FastAPI()
 
# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)
 
@app.post("/afinar")
async def afinar_voz(audio: UploadFile = File(...)):
    try:
        # 1. Validar audio
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Formato no soportado")
        # 2. Leer y procesar audio (ejemplo: subir pitch)
        audio_bytes = await audio.read()
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=44100)
        y_tuned = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)
        # 3. Convertir a WAV y enviar
        with io.BytesIO() as buffer:
            librosa.output.write_wav(buffer, y_tuned, sr)
            audio_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return {
            "status": "success",
            "voz_afinada": audio_base64,
            "formato": "audio/wav",
            "sample_rate": sr
        }
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)