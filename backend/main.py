from fastapi import FastAPI
from typing import List
from PIL import Image
import base64
from io import BytesIO
import PyPDF2
import random, string
import re, os

app = FastAPI()

@app.post("/merge")
async def test(files: List[str]):
    images = []
    for file in files:
        img_raw = base64.b64decode(file)
        img_to_rgb = await base64_to_img(img_raw)
        images.append(img_to_rgb)
    await merge(images)
    return "hello"

async def merge(images):
    merger = PyPDF2.PdfFileMerger()
    output_file = "complete_" + randomname(15) + ".pdf"
    paths = []
    for image in images:
        filename = randomname(20) + ".pdf"
        path = os.path.join(".", "temp", filename)
        paths.append(path)
        image.save(path)
        merger.append(path)
    merger.write(output_file)
    merger.close()
    await remove(paths)


async def base64_to_img(img):
    new_img = Image.open(BytesIO(img))
    img_to_rgb = new_img.convert("RGB")
    return img_to_rgb

def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def remove(paths: List[str]):
    for path in paths:
        os.remove(path)

async def removeFile(path: str):
    os.remove(path)

"""
def merge(files):
    merger = PyPDF2.PdfFileMerger()
    filename = randomname(20) + ".pdf"
    base = os.path.join(settings.MEDIA_ROOT, "documents")
    path = os.path.join(str(base), filename)
    match = re.compile(r'(png|jpg|jpeg)')
    for file in files:
        if not re.search(r'\.(pdf|jpg|png|jpeg)$', str(file)):
            return None, None
        p = Document(document=file)
        p.save()
        # postされたデータを一旦保存
        temp_path = os.path.join(base, str(file))
        if re.search(r'\.(jpg|png|jpeg)$', str(file)):
            im = Image.open(temp_path)
            new_file_name = match.sub("pdf", str(file))
            pdf_path = os.path.join(str(base), new_file_name)
            im.convert("RGB").save(pdf_path, quality=100)
            os.remove(temp_path)
            merger.append(pdf_path)
            del im

        else:
            merger.append(file)

    merger.write(path)
    merger.close()
    return path, filename
"""