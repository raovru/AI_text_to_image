from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import io
import base64
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],  # Adjust this with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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
        image = Image.open(io.BytesIO(response.content))

        image = image.resize((400, 400), Image.LANCZOS)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_byte_array = buffered.getvalue()

        image_base64 = base64.b64encode(img_byte_array).decode('utf-8')

        return JSONResponse(content={"image": image_base64})
    else:
        return JSONResponse(content={"Error": "Unable to generate image"})
