import cloudinary.uploader
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '../.env'
load_dotenv(dotenv_path=env_path)

cloudinary.config(cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key=os.getenv('CLOUDINARY_API_KEY'), 
    api_secret=os.getenv('CLOUDINARY_API_SECRET'))

def upload(file):
    try:
        response = cloudinary.uploader.upload(file)
        return response
    except Exception as e:
        pass

