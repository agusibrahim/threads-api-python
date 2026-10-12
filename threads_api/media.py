"""
Media Upload Utilities for Threads Automation (Photos, Carousels, Videos)
"""

import io
import json
import os
import time
from typing import Tuple, Union
from PIL import Image

from .constants import (
    BARCELONA_APP_ID,
    ASBD_ID,
    RUPLOAD_PHOTO_URL,
    RUPLOAD_VIDEO_URL
)

class MediaUploader:
    """
    Menangani pengunggahan berkas media (foto & video) ke endpoint rupload Meta.
    """

    @staticmethod
    def _read_bytes(source: Union[str, bytes, io.BytesIO]) -> bytes:
        if isinstance(source, bytes):
            return source
        elif isinstance(source, io.BytesIO):
            return source.getvalue()
        elif isinstance(source, str):
            if not os.path.exists(source):
                raise FileNotFoundError(f"File media tidak ditemukan: {source}")
            with open(source, "rb") as f:
                return f.read()
        else:
            raise TypeError("Source media harus berupa filepath (str), bytes, atau BytesIO.")

    @classmethod
    def get_image_dimensions(cls, image_bytes: bytes) -> Tuple[int, int]:
        """Mendapatkan dimensi (width, height) dari bytes gambar menggunakan Pillow."""
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                return img.size  # (width, height)
        except Exception:
            # Fallback resolusi standar persegi
            return (1080, 1080)

    @classmethod
    def upload_photo(
        cls,
        session,
        base_headers: dict,
        image_source: Union[str, bytes, io.BytesIO],
        is_sidecar: bool = False
    ) -> str:
        """
        Mengunggah berkas foto ke Threads.
        Mengembalikan upload_id yang dapat dipakai di endpoint configure.
        """
        data_bytes = cls._read_bytes(image_source)
        width, height = cls.get_image_dimensions(data_bytes)

        upload_id = str(int(time.time() * 1000))
        entity_name = f"fb_uploader_{upload_id}"

        rupload_params = {
            "is_sidecar": "1" if is_sidecar else "0",
            "is_threads": "1",
            "media_type": 1,
            "upload_id": upload_id,
            "upload_media_height": height,
            "upload_media_width": width
        }

        headers = {
            "authority": "www.threads.com",
            "accept": "*/*",
            "offset": "0",
            "x-entity-length": str(len(data_bytes)),
            "x-entity-name": entity_name,
            "x-entity-type": "image/jpeg",
            "x-ig-app-id": BARCELONA_APP_ID,
            "x-asbd-id": ASBD_ID,
            "x-instagram-rupload-params": json.dumps(rupload_params),
            "x-csrftoken": base_headers.get("x-csrftoken", ""),
            "origin": "https://www.threads.com",
            "referer": "https://www.threads.com/",
            "user-agent": base_headers.get("user-agent", ""),
        }

        url = f"{RUPLOAD_PHOTO_URL}/{entity_name}"
        res = session.post(url, headers=headers, data=data_bytes)
        if res.status_code != 200:
            raise RuntimeError(f"Gagal mengunggah foto ke Threads: HTTP {res.status_code} - {res.text}")

        res_json = res.json()
        return str(res_json.get("upload_id", upload_id))

    @classmethod
    def upload_video(
        cls,
        session,
        base_headers: dict,
        video_source: Union[str, bytes, io.BytesIO],
        width: int = 1080,
        height: int = 1920,
        is_sidecar: bool = False
    ) -> str:
        """
        Mengunggah berkas video (.mp4) ke Threads.
        Mengembalikan upload_id yang dapat dipakai di endpoint configure.
        """
        data_bytes = cls._read_bytes(video_source)
        upload_id = str(int(time.time() * 1000))
        entity_name = f"fb_uploader_{upload_id}"

        rupload_params = {
            "extract_cover_frame": "1",
            "is_sidecar": "1" if is_sidecar else "0",
            "is_threads": "1",
            "media_type": 2,
            "upload_id": upload_id,
            "upload_media_height": height,
            "upload_media_width": width
        }

        headers = {
            "authority": "www.threads.com",
            "accept": "*/*",
            "offset": "0",
            "x-entity-length": str(len(data_bytes)),
            "x-entity-name": entity_name,
            "x-entity-type": "video/mp4",
            "x-ig-app-id": BARCELONA_APP_ID,
            "x-asbd-id": ASBD_ID,
            "x-instagram-rupload-params": json.dumps(rupload_params),
            "x-csrftoken": base_headers.get("x-csrftoken", ""),
            "origin": "https://www.threads.com",
            "referer": "https://www.threads.com/",
            "user-agent": base_headers.get("user-agent", ""),
        }

        url = f"{RUPLOAD_VIDEO_URL}/{entity_name}"
        res = session.post(url, headers=headers, data=data_bytes)
        if res.status_code != 200:
            raise RuntimeError(f"Gagal mengunggah video ke Threads: HTTP {res.status_code} - {res.text}")

        res_json = res.json()
        return str(res_json.get("upload_id", upload_id))
