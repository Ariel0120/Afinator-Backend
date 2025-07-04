from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
import base64
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
)
@app.post("/afinar")
async def afinar_voz(audio: UploadFile = File(...)):
    try:
        # 1. Validar el archivo
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Formato de audio no soportado")
 
        # 2. Leer el audio (sin procesar aún)
        contents = await audio.read()
        # 3. Simular respuesta exitosa (para pruebas)
        return {
            "status": "success",
            "message": "Audio recibido (modo prueba)",
            "bytes_recibidos": len(contents),
            "formato": audio.content_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")