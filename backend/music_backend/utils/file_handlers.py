# utils/file_handlers.py
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def save_uploaded_file(file, path):
    """Dosyayı Django'nun dosya sistemine kaydeder."""
    return default_storage.save(path, ContentFile(file.read()))