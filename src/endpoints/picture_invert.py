from fastapi import UploadFile, File
from fastapi import APIRouter
from fastapi.responses import FileResponse
from PIL import Image
import PIL.ImageOps
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
