from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile
from PIL import Image
import PIL.ImageOps
import shutil
import sympy


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/prime/{number}")
async def check_number(number: int):
    return {"Is number prime": sympy.isprime(number)}


@app.post("/picture/invert")
async def picture_invert(image: UploadFile):
    with open("Photos/destination.png", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    base_image = Image.open("Photos/destination.png")
    inverted_image = PIL.ImageOps.invert(base_image)
    inverted_image.save("Photos/return.png")
    # return Response(content=inverted_image.tobytes(), media_type="image/png")
    return FileResponse("Photos/return.png")
