"""Django storage backed by the project's public Vercel Blob store."""

import json
import os
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class VercelBlobStorage(Storage):
    """Store new uploads in Vercel Blob and keep legacy /media/ files working."""

    api_url = "https://vercel.com/api/blob"

    def _token(self):
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not token:
            raise RuntimeError("BLOB_READ_WRITE_TOKEN is not configured")
        return token

    def _open(self, name, mode="rb"):
        if "r" not in mode:
            raise ValueError("Vercel Blob storage only supports reading existing files")
        with urlopen(self.url(name), timeout=30) as response:
            return ContentFile(response.read(), name=name)

    def _save(self, name, content):
        request = Request(
            f"{self.api_url}?{urlencode({'pathname': name})}",
            data=content.read(),
            headers={
                "Authorization": f"Bearer {self._token()}",
                "x-api-version": "12",
                "x-add-random-suffix": "1",
                "x-vercel-blob-access": "public",
                "x-content-type": getattr(content, "content_type", None) or "application/octet-stream",
            },
            method="PUT",
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)["url"]
        except HTTPError as error:
            raise RuntimeError("Vercel Blob could not save the upload") from error

    def delete(self, name):
        if not name.startswith(("http://", "https://")):
            return
        request = Request(
            f"{self.api_url}/delete",
            data=json.dumps({"urls": [name]}).encode(),
            headers={
                "Authorization": f"Bearer {self._token()}",
                "Content-Type": "application/json",
                "x-api-version": "12",
            },
            method="POST",
        )
        with urlopen(request, timeout=30):
            pass

    def exists(self, name):
        return False

    def url(self, name):
        if name.startswith(("http://", "https://")):
            return name
        return f"{settings.MEDIA_URL.rstrip('/')}/{name.lstrip('/')}"

    def get_available_name(self, name, max_length=None):
        return name
