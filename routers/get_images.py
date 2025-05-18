from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os 


router = APIRouter(
    prefix='/getimages',
    tags=['Todos']
)


IMAGE_DIR = os.path.join("utils", "images")


@router.get("/{image_name}")
def get_image(image_name: str):
    safe_name = os.path.basename(image_name) + ".png"
    image_path = os.path.join(IMAGE_DIR, safe_name)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path, media_type="image/png")
