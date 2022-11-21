from fastapi import File
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from PIL import Image
import PIL.ImageOps
import io

router = APIRouter(
    prefix="/picture",
    tags=["Zadanie 2"]
)


@router.post("/invert")
async def picture_invert(image: bytes = File(...)):
    return StreamingResponse(invert_colors(image), media_type="image/jpeg")


def invert_colors(input_image: bytes) -> bytes:
    inverted_image = PIL.ImageOps.invert(Image.open(io.BytesIO(input_image)))
    output_image = io.BytesIO()
    inverted_image.save(output_image, format='jpeg')
    output_image.seek(0)
    return output_image
