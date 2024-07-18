from fastapi import FastAPI, File, UploadFile
import whisper
import os
import asyncio

app = FastAPI()

model = whisper.load_model("tiny")

@app.post("/transcrever/")
async def transcrever(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(await file.read())
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, model.transcribe, audio_path)
    os.remove(audio_path)
    
    return {"transcricao": result["text"]}
