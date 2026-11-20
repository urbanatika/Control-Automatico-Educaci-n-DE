"""Servir /media/ en desarrollo con soporte de rangos HTTP (Range), para poder adelantar los videos.

django.views.static.serve no admite Range y el navegador no puede saltar dentro de un MP4.
Solo se usa con DEBUG=True; en producción los archivos los sirve Azure Blob Storage.
"""
import mimetypes
import os
import re

from django.http import FileResponse, Http404, HttpResponse
from django.utils._os import safe_join


def serve_media(request, path, document_root=None):
    try:
        full = safe_join(document_root, path)
    except Exception:
        raise Http404
    if not os.path.isfile(full):
        raise Http404
    size = os.path.getsize(full)
    ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
    if full.endswith(".vtt"):
        ctype = "text/vtt; charset=utf-8"
    m = re.match(r"bytes=(\d*)-(\d*)$", request.headers.get("Range", ""))
    if not m or (not m.group(1) and not m.group(2)):
        resp = FileResponse(open(full, "rb"), content_type=ctype)
        resp["Accept-Ranges"] = "bytes"
        return resp
    if m.group(1):
        start = int(m.group(1))
        end = min(int(m.group(2)) if m.group(2) else size - 1, size - 1)
    else:
        start, end = max(0, size - int(m.group(2))), size - 1
    if start >= size or start > end:
        resp = HttpResponse(status=416)
        resp["Content-Range"] = f"bytes */{size}"
        return resp
    with open(full, "rb") as f:
        f.seek(start)
        data = f.read(end - start + 1)
    resp = HttpResponse(data, status=206, content_type=ctype)
    resp["Content-Range"] = f"bytes {start}-{end}/{size}"
    resp["Accept-Ranges"] = "bytes"
    resp["Content-Length"] = str(len(data))
    return resp
