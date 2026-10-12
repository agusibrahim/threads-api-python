#!/usr/bin/env python3
"""
Unit and Integration Tests for Threads API Toolkit
"""

import io
import os
import unittest
from PIL import Image

from threads_api import ThreadsClient, SessionAuth, MediaUploader
from threads_api.constants import BARCELONA_APP_ID, DEFAULT_LSD
import json

class TestSessionAuth(unittest.TestCase):
    def test_from_dict(self):
        auth = SessionAuth.from_dict({
            "sessionid": "dummy_session",
            "csrftoken": "dummy_csrf",
            "ds_user_id": "12345"
        })
        self.assertEqual(auth.sessionid, "dummy_session")
        self.assertEqual(auth.csrftoken, "dummy_csrf")
        self.assertEqual(auth.ds_user_id, "12345")
        self.assertEqual(auth.cookies["sessionid"], "dummy_session")

    def test_from_cookie_string(self):
        raw = "sessionid=test_sess; csrftoken=test_csrf; ds_user_id=999"
        auth = SessionAuth.from_cookie_string(raw)
        self.assertEqual(auth.sessionid, "test_sess")
        self.assertEqual(auth.csrftoken, "test_csrf")
        self.assertEqual(auth.ds_user_id, "999")

    def test_from_session_switcher_mock(self):
        import tempfile
        sample_json = {
            "sessions": [
                {
                    "name": "test_profile",
                    "domain": "threads.com",
                    "cookies": [
                        {"name": "sessionid", "value": "test_session_id"},
                        {"name": "csrftoken", "value": "test_csrf_token"},
                        {"name": "ds_user_id", "value": "999888777"}
                    ]
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as tf:
            json.dump(sample_json, tf)
            tf.flush()
            tmp_path = tf.name

        try:
            auth = SessionAuth.from_session_switcher(tmp_path)
            self.assertEqual(auth.sessionid, "test_session_id")
            self.assertEqual(auth.csrftoken, "test_csrf_token")
            self.assertEqual(auth.ds_user_id, "999888777")
        finally:
            os.remove(tmp_path)

    def test_missing_required_cookies(self):
        with self.assertRaises(ValueError):
            SessionAuth.from_dict({"sessionid": "only_sess"})


class TestMediaUploader(unittest.TestCase):
    def test_image_dimensions(self):
        buf = io.BytesIO()
        img = Image.new("RGB", (640, 480), color="blue")
        img.save(buf, format="JPEG")
        raw_bytes = buf.getvalue()

        w, h = MediaUploader.get_image_dimensions(raw_bytes)
        self.assertEqual(w, 640)
        self.assertEqual(h, 480)

    def test_read_bytes_from_bytesio(self):
        buf = io.BytesIO(b"sample_data")
        res = MediaUploader._read_bytes(buf)
        self.assertEqual(res, b"sample_data")


class TestThreadsClient(unittest.TestCase):
    def setUp(self):
        self.auth = SessionAuth(sessionid="fake_session", csrftoken="fake_csrf", ds_user_id="123")
        self.client = ThreadsClient(self.auth)

    def test_headers_initialized(self):
        self.assertEqual(self.client.base_headers["x-ig-app-id"], BARCELONA_APP_ID)
        self.assertEqual(self.client.base_headers["x-csrftoken"], "fake_csrf")
        self.assertEqual(self.client.base_headers["x-fb-lsd"], DEFAULT_LSD)

    def test_carousel_validation(self):
        with self.assertRaises(ValueError):
            # Carousel requires at least 2 images
            self.client.create_carousel_post("caption", ["only_one.jpg"])

        with self.assertRaises(ValueError):
            # Carousel maximum 20 images
            self.client.create_carousel_post("caption", [f"img_{i}.jpg" for i in range(25)])


if __name__ == "__main__":
    unittest.main()
