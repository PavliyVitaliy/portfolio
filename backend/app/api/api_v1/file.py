from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from api.api_v1.fastapi_users import current_active_superuser
from core.models import User
from services.profile import ProfileService


router = APIRouter(prefix="/file", tags=["File"])

FILES_DIRECTORY = Path(__file__).resolve().parents[2] / "files"
MAX_PROFILE_IMAGE_SIZE = 5 * 1024 * 1024
IMAGE_TYPES = {
    "image/jpeg": (".jpg", b"\xff\xd8\xff"),
    "image/png": (".png", b"\x89PNG\r\n\x1a\n"),
    "image/webp": (".webp", b"RIFF"),
}


def _validate_image(content: bytes, content_type: str | None) -> str:
    if not content or len(content) > MAX_PROFILE_IMAGE_SIZE:
        raise HTTPException(400, "Image must be between 1 byte and 5 MB")
    if content_type not in IMAGE_TYPES:
        raise HTTPException(415, "Only JPEG, PNG, and WebP images are supported")
    extension, signature = IMAGE_TYPES[content_type]
    if not content.startswith(signature):
        raise HTTPException(400, "Image content does not match its content type")
    if content_type == "image/webp" and content[8:12] != b"WEBP":
        raise HTTPException(400, "Image content does not match its content type")
    return extension


@router.get("/profile/{filename}")
async def get_profile_image(filename: str):
    if Path(filename).name != filename:
        raise HTTPException(404, "Image not found")
    path = FILES_DIRECTORY / filename
    if not path.is_file():
        raise HTTPException(404, "Image not found")
    media_type = next(
        (content_type for content_type, (extension, _) in IMAGE_TYPES.items() if filename.endswith(extension)),
        "application/octet-stream",
    )
    return FileResponse(path, media_type=media_type, headers={"X-Content-Type-Options": "nosniff"})


@router.post("/profile", response_model=str)
async def upload_profile_image(
    image: UploadFile = File(...),
    user: User = Depends(current_active_superuser),
):
    content = await image.read(MAX_PROFILE_IMAGE_SIZE + 1)
    extension = _validate_image(content, image.content_type)
    filename = f"{uuid4().hex}{extension}"
    FILES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    (FILES_DIRECTORY / filename).write_bytes(content)

    previous_filename = None
    try:
        previous_filename = (await ProfileService().get_profile(str(user.id))).photo_filename
    except HTTPException as error:
        if error.status_code != 404:
            raise
    await ProfileService().upsert_photo(str(user.id), filename)

    if previous_filename and previous_filename != filename:
        (FILES_DIRECTORY / previous_filename).unlink(missing_ok=True)
    return filename
