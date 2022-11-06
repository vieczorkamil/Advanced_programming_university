from fastapi import UploadFile, File
from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
from PIL import Image
import PIL.ImageOps
import numpy as np
import shutil

router = APIRouter(
    prefix="/picture",
    tags=["Zadanie 2"]
)


@router.post("/invert")
async def picture_invert(image: UploadFile = File(...)):
    with open("Photos/temp.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    base_image = Image.open("photos/temp.jpg")
    inverted_image = PIL.ImageOps.invert(base_image)
    inverted_image.save("photos/return.jpg")
    return FileResponse("photos/return.jpg")


# FIXME: why that not working????
@router.post("/upload", responses={200: {"content": {"image/jpeg": {}}}}, response_class=Response)
async def picture_update(image: UploadFile = File(...)):
    content = image.file.read()
    temp = bytearray(content)
    for i in range(0, len(content)):
        temp[i] = np.abs(255 - content[i])
    out = bytes(temp)
    return Response(content=out, media_type="image/jpeg")
