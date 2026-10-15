"""Django storage backed by the project's public Vercel Blob store."""

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from vercel.blob import BlobClient


@deconstructible
class VercelBlobStorage(Storage):
    """Store user-uploaded media in Vercel Blob, not the function filesystem."""

    def _open(self, name, mode="rb"):
        if "r" not in mode:
            raise ValueError("Vercel Blob storage only supports reading existing files")
        with BlobClient() as client:
            result = client.get(name, access="public")
        return ContentFile(bytes(result), name=name)

    def _save(self, name, content):
        with BlobClient() as client:
            blob = client.put(
                name,
                content.read(),
                access="public",
                content_type=getattr(content, "content_type", None),
                add_random_suffix=True,
            )
        return blob.url

    def delete(self, name):
        if name.startswith(("http://", "https://")):
            with BlobClient() as client:
                client.delete(name)

    def exists(self, name):
        return False

    def url(self, name):
        if name.startswith(("http://", "https://")):
            return name
        return f"{settings.MEDIA_URL}{name.lstrip('/')}"

    def get_available_name(self, name, max_length=None):
        return name
