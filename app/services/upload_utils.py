import os
import bleach
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_media(files, folder):
    """
    Uploads media files to Cloudinary and returns their URLs.
    
    :param files: List of file objects to upload.
    :param folder: Folder in Cloudinary where files will be stored.
    :return: List of URLs of the uploaded files.
    """
    urls = []
    for file in files:
        if file:
            response = cloudinary.uploader.upload(file, folder=folder)
            urls.append(response.get('secure_url'))
    return urls
def sanitize_html(content):
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS + ["p", "br", "h1", "h2", "h3", "strong", "em", "u", "a"]
    return bleach.clean(content, tags=allowed_tags, strip=True)