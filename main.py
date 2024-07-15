import sys
import os

from fastapi import FastAPI, File, UploadFile
sys.path.append(os.path.join(os.path.dirname(__file__), 'whisper'))
import whisper
import os

app = FastAPI()

model = whisper.load_model("base")

@app.post("/transcrever/")
async def transcrever(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(file.file.read())
    result = model.transcribe(audio_path)
    os.remove(audio_path)

    return {"transcricao": result["text"]}
