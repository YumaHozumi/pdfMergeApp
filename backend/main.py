from fastapi import FastAPI, File, UploadFile
from typing import List
from PIL import Image
import base64
from io import BytesIO
import PyPDF2

app = FastAPI()

@app.post("/merge")
def test(files: List[str]):
    img_raw = base64.b64decode(files[0])
    img = Image.open(BytesIO(img_raw))
    img.convert("RGB").save("test.jpeg", quality=100)
    return "hello"
