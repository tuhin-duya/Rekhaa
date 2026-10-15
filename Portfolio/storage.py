"""Django storage backed by the project's public Vercel Blob store."""

import json
import os
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class VercelBlobStorage(Storage):
    """Store user-uploaded media in Vercel Blob, not the function filesystem."""

    api_url = "https://vercel.com/api/blob"

    def _token(self):
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not token:
            raise RuntimeError("BLOB_READ_WRITE_TOKEN is not configured")
        return token

    def _open(self, name, mode="rb"):
        if "r" not in mode:
            raise ValueError("Vercel Blob storage only supports reading existing files")
        with urlopen(name, timeout=30) as response:
            return ContentFile(response.read(), name=name)

    def _save(self, name, content):
        query = urlencode({"pathname": name})
        headers = {
            "Authorization": f"Bearer {self._token()}",
            "x-api-version": "11",
            "x-add-random-suffix": "1",
            "x-vercel-blob-access": "public",
        }
        if getattr(content, "content_type", None):
            headers["x-content-type"] = content.content_type
        request = Request(
            f"{self.api_url}?{query}",
            data=content.read(),
            headers=headers,
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
        body = json.dumps({"urls": [name]}).encode()
        request = Request(
            f"{self.api_url}/delete",
            data=body,
            headers={
                "Authorization": f"Bearer {self._token()}",
                "Content-Type": "application/json",
                "x-api-version": "11",
            },
            method="POST",
        )
        with urlopen(request, timeout=30):
            pass

    def exists(self, name):
        return False

    def url(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        return name
