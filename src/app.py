from fastapi import FastAPI
import sympy
from fastapi import UploadFile, File
from fastapi.responses import FileResponse, Response
from PIL import Image
import PIL.ImageOps
import numpy as np
import shutil

app = FastAPI(
    title="Zaawansowane programowanie - FastAPI"
)


@app.get("/", tags=["Default"])
async def read_root():
    return {"Hello": "World"}


@app.get("/prime/{number}", tags=["Zadanie 1"])
async def check_number(number: int):
    if check_correctnes(number):
        response = {"Is number prime": sympy.isprime(number)}
    else:
        response = {"Error handler": "Not valid input number"}
    return response


@app.post("/picture/invert", tags=["Zadanie 2"])
async def picture_invert(image: UploadFile = File(...)):
    with open("Photos/temp.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    base_image = Image.open("photos/temp.jpg")
    inverted_image = PIL.ImageOps.invert(base_image)
    inverted_image.save("photos/return.jpg")
    return FileResponse("photos/return.jpg")


# FIXME: why that not working????
@app.post("/picture/upload", responses={200: {"content": {"image/jpeg": {}}}}, response_class=Response)
async def picture_update(image: UploadFile = File(...)):
    content = image.file.read()
    temp = bytearray(content)
    for i in range(0, len(content)):
        temp[i] = np.abs(255 - content[i])
    out = bytes(temp)
    return Response(content=out, media_type="image/jpeg")

""" Helpers functions """


def check_correctnes(number: int) -> bool:
    if number <= 1:
        return False
    else:
        return True
