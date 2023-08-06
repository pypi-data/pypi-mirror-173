from __future__ import annotations

import logging
import re
from io import BytesIO

log = logging.getLogger(__name__)


class Image(BytesIO):
    def __init__(self, content=None, filename=None):
        self.filename = filename
        self.format = filename.split(".")[-1].lower()
        super().__init__(content)

    def save(self, filename=None, mode="wb"):
        filename = filename or self.filename
        nbytes = len(self.getvalue())
        with open(filename, mode) as f:
            f.write(self.read())
        log.info(f"Written {len(self.getvalue()):d} bytes to {filename:s}")
        return nbytes

    def _repr_png_(self):
        if self.format == "png":
            return self.getvalue()

    def _repr_jpeg_(self):
        if self.format in ["jpeg", "jpg"]:
            return self.getvalue()

    def _repr_svg_(self):
        if self.format == "svg":
            return self.getvalue()

    @classmethod
    def from_response(cls, response):
        filename = re.findall(
            "filename=(.+)", response.headers.get("content-disposition")
        )[0]
        return cls(content=response.content, filename=filename)
