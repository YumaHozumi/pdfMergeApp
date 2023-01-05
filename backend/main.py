from fastapi import FastAPI
from typing import List
from PIL import Image
import base64
from io import BytesIO
import PyPDF2
import random, string
import re, os
from pdf2image import convert_from_bytes

app = FastAPI()

@app.post("/merge")
async def start(files: List[str]):
    images = []
    for file in files:
        # 画像じゃないやつは弾く
        if not (is_image_base64(file) or is_pdf(file)): return None
        if is_pdf(file): # 画像がpdfの場合
            file = re.sub('data:.*\/.*;base64,', "", file)
            img_raw = base64.b64decode(file)
            # PILだとpdf形式のやつ読めないので、pdf2imageを使う
            changeimages = convert_from_bytes(img_raw, paths_only=True)
            for img in changeimages:
                images.append(img)
        else: # 画像がpdf以外のやつの場合
            file = re.sub('data:.*\/.*;base64,', "", file)
            img_raw = base64.b64decode(file)
            img_to_rgb = await base64_to_img(img_raw)
            images.append(img_to_rgb)
    output_path = await merge(images)
    output_img = await img_to_base64(output_path)
    await removeFile(output_path)
    return output_img

async def merge(images):
    merger = PyPDF2.PdfFileMerger()
    output_file = "complete_" + randomname(15) + ".pdf"
    paths = []
    for image in images:
        filename = randomname(20) + ".pdf"
        path = os.path.join(".", "temp", filename)
        paths.append(path)
        image.save(path, quality=100)
        merger.append(path)
    merger.write(output_file)
    merger.close()
    await remove(paths)
    return output_file


async def base64_to_img(img):
    new_img = Image.open(BytesIO(img))
    img_to_rgb = new_img.convert("RGB")
    return img_to_rgb

async def img_to_base64(img_path):
    data = None
    with open(img_path, 'rb') as f:
        data = f.read()
    output_base64 = base64.b64encode(data)
    return output_base64

def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def remove(paths: List[str]):
    for path in paths:
        os.remove(path)

async def removeFile(path: str):
    os.remove(path)

# base64がjpeg,png,jpgかどうかを判定する
def is_image_base64(base64_str):
    image_pattern = re.compile(r'^(data:image/(png|jpeg|jpg);base64,)')
    return image_pattern.search(base64_str) is not None

def is_pdf(base64_str):
    image_pattern = re.compile(r'^(data:application/pdf;base64,)')
    return image_pattern.search(base64_str) is not None