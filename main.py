from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
import requests, io, base64
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

load_dotenv()  

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read())
    
# Hugging Face API URL
API_URL = os.getenv("API_URL")

# POST endpoint to generate image from text
@app.post("/textToImage")
async def text_to_image(text: str = Form(...)):
    payload = {
        "inputs": text
    }

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("API_KEY")}'
}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.headers.get('Content-Type') == 'image/jpeg':
        image_stream = io.BytesIO(response.content)
        image_url = "data:image/jpeg;base64," + base64.b64encode(image_stream.getvalue()).decode('utf-8')
        return HTMLResponse(f'<img src="{image_url}" alt="Generated Image"/>')
    else:
        return HTMLResponse('<p>Error generating image</p>')
