from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
import requests
import io
import base64
from fastapi.responses import HTMLResponse
from PIL import Image
from io import BytesIO
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
        # Open the image with Pillow
        image = Image.open(io.BytesIO(response.content))

        # Resize the image to 400x400
        image = image.resize((400, 400), Image.LANCZOS)

        # Save resized image to a BytesIO object
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_byte_array = buffered.getvalue()

        # Encode the resized image as base64
        image_url = "data:image/jpeg;base64," + base64.b64encode(img_byte_array).decode('utf-8')

        return HTMLResponse(f'<div id="result-image-box"><img src="{image_url}" alt="Generated Image"/></div>')
    else:
        return HTMLResponse('<p>Error generating image</p>')
