import os
from typing import Any, Annotated
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import func, select

from backend.api.deps import CurrentUser, get_current_user
from backend.api.schemas import Message


router = APIRouter(prefix="/uploads", tags=["uploads"])

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(CURRENT_DIR, '..', '..', 'data', 'uploads')
DIR_DATA = os.path.abspath(DIR_DATA)

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # bytes


@router.post(
    "/article",
    dependencies=[Depends(get_current_user)]
)
async def upload_article_image(
    file: UploadFile = File(...)
):
    DIR_FILE = os.path.join(DIR_DATA, 'articles')
    file_ext = file.filename.split(".")[-1]

    file.filename = f"{uuid.uuid4()}.{file_ext}"
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size is {MAX_FILE_SIZE_MB}MB."
        )

    try:
        with open(f"{DIR_FILE}/{file.filename}", "wb") as f:
            f.write(contents)
    except:
        raise HTTPException(
            status_code=500,
            detail='File not uploaded.'
        )

    return {"filename": file.filename}


@router.get(
    "/article/{filename}",
)
async def get_article_image(filename: str) -> FileResponse:
    DIR_FILE = os.path.join(DIR_DATA, 'articles', filename)

    if not os.path.exists(DIR_FILE):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(DIR_FILE)


@router.patch(
    "/article/{filename}",
    dependencies=[Depends(get_current_user)]
)
async def update_article_image(
    filename: str, file: UploadFile = File(...)
) -> Message:
    DIR_FILE = os.path.join(DIR_DATA, 'articles', filename)
    contents = await file.read()

    if not os.path.exists(DIR_FILE):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    try:
        with open(DIR_FILE, "wb") as f:
            f.write(contents)
    except:
        raise HTTPException(
            status_code=500,
            detail='File not uploaded.'
        )
    
    return Message(message="File updated.")


@router.delete(
    "/article/{filename}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
async def delete_article_image(filename: str) -> Message:
    DIR_FILE = os.path.join(DIR_DATA, 'articles', filename)

    if not os.path.exists(DIR_FILE):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )
    try:
        os.remove(DIR_FILE)
    except Exception:
        raise HTTPException(status_code=500, detail="Error deleting file.")
    
    return Message(message="File deleted successfully.")


@router.post(
    "/profiles",
    dependencies=[Depends(get_current_user)]
)
async def upload_profiles_image(
    file: UploadFile = File(...)
):
    DIR_FILE = os.path.join(DIR_DATA, 'profiles')
    file_ext = file.filename.split(".")[-1]

    file.filename = f"{uuid.uuid4()}.{file_ext}"
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size is {MAX_FILE_SIZE_MB}MB."
        )

    try:
        with open(f"{DIR_FILE}/{file.filename}", "wb") as f:
            f.write(contents)
    except:
        raise HTTPException(
            status_code=500,
            detail='File not uploaded.'
        )

    return {"filename": file.filename}


@router.get(
    "/profiles/{filename}",
)
async def get_profiles_image(filename: str) -> FileResponse:
    DIR_FILE = os.path.join(DIR_DATA, 'profiles', filename)

    if not os.path.exists(DIR_FILE):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(DIR_FILE)


@router.patch(
    "/profiles/{filename}",
    dependencies=[Depends(get_current_user)]
)
async def update_profiles_image(
    filename: str, file: UploadFile = File(...)
) -> Message:
    DIR_FILE = os.path.join(DIR_DATA, 'profiles', filename)
    contents = await file.read()

    if not os.path.exists(DIR_FILE):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    try:
        with open(DIR_FILE, "wb") as f:
            f.write(contents)
    except:
        raise HTTPException(
            status_code=500,
            detail='File not uploaded.'
        )
    
    return Message(message="File updated.")


@router.delete(
    "/profiles/{filename}",
    dependencies=[Depends(get_current_user)],
    response_model=Message
)
async def delete_profiles_image(filename: str) -> Message:
    DIR_FILE = os.path.join(DIR_DATA, 'profiles', filename)

    if not os.path.exists(DIR_FILE):
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )
    try:
        os.remove(DIR_FILE)
    except Exception:
        raise HTTPException(status_code=500, detail="Error deleting file.")
    
    return Message(message="File deleted successfully.")