from fastapi import (
    APIRouter,
    File,
    HTTPException,
)
from fastapi.responses import FileResponse
from core.config import settings
import os


router = APIRouter(
    prefix=settings.api.v1.file,
    tags=["File"],
)

path_to_files = "files"


@router.post("/download/image")
def download_file(file_name: str = File(...)):
    file_path = os.path.join(os.getcwd(), path_to_files, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(404)
    return FileResponse(path=file_path, media_type="image/png")
