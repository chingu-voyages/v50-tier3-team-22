from os import getenv, urandom
import cloudinary
import cloudinary.uploader
import cloudinary.api
#for image handling
from fastapi import UploadFile, HTTPException, status
from datetime import datetime, UTC, timedelta

import requests 

CLOUDINARY_URL = getenv("CLOUDINARY_URL")

IMAGE_EXPIRATION_IN_MIN = 15
#Constants for image handling

def image_upload(image : UploadFile, image_name : str | None = None):
    image_url = None
    
    content_type = image.content_type.split("/")[0]
    if content_type != "image":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The file uploaded is not an image type"
        ) 
    if image_name == None:
        image.filename = datetime.now(UTC).isoformat() + urandom(15).hex()
        image_name = image.filename
    else:
        image.filename = image_name
    try:
        cloudinary.config(secure=True)
        cloudinary.uploader.upload(
            image.file, 
            public_id=image.filename, 
            unique_filename = True, 
            use_filename=True, 
            overwrite=True,
            invalidate=True,
            type = "private",
            transformation=[
                {'width': 1920, 'height': 1080, 'crop': 'fill'}
            ]
        )
        expiration_time = datetime.now(UTC) + timedelta(minutes=IMAGE_EXPIRATION_IN_MIN)
        image_url = cloudinary.utils.cloudinary_url(
        image.filename,
        type='private',
        sign_url=True,
        expires_at=int(expiration_time.timestamp())
        )[0]
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Image saving failed") 
    return image_name, image_url
    
def get_image_url(image_name : str) -> str:
    try:
        expiration_time = datetime.now(UTC) + timedelta(minutes=IMAGE_EXPIRATION_IN_MIN)
        image_url = cloudinary.utils.cloudinary_url(
            image_name,
            type='private',
            sign_url=True,
            expires_at=int(expiration_time.timestamp())
            )[0]
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Getting image failed") 
    
    return image_url

def get_image(image_name : str):
    try:
        expiration_time = datetime.now(UTC) + timedelta(minutes=IMAGE_EXPIRATION_IN_MIN)
        image_url = cloudinary.utils.cloudinary_url(
            image_name,
            type='private',
            sign_url=True,
            expires_at=int(expiration_time.timestamp())
            )[0]
        
        response = requests.get(url=image_url)

        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Getting image failed with error {response.status_code}") 
        return response.content
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Getting image failed") 
    
    

def delete_image(image_name : str):
    try:
        response = cloudinary.uploader.destroy(image_name, type="private")
        if response["result"] != "ok":
            print(response)
            raise "error"
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Image deletion failed")
    