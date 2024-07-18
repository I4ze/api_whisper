from fastapi import FastAPI, File, UploadFile
import whisper
import os
import asyncio
from fastapi.responses import JSONResponse

app = FastAPI()

model = whisper.load_model("tiny")

@app.post("/transcrever/")
async def transcrever(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(await file.read())
    loop = asyncio.get_event_loop()
    result = model.transcribe(audio_path, language="pt", fp16=False, verbose=True)
    os.remove(audio_path)

    transcricao = result["text"]
    
    return JSONResponse(content={"transcricao": transcricao}, media_type="application/json; charset=utf-8")