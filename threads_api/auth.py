"""
Authentication & Session Management for Threads Automation
"""

import json
import os
from typing import Dict, Optional, Union

class SessionAuth:
    """
    Mengelola kredensial sesi Threads (cookies, CSRF token, user ID).
    """

    def __init__(
        self,
        sessionid: str,
        csrftoken: str,
        ds_user_id: Optional[str] = None,
        extra_cookies: Optional[Dict[str, str]] = None
    ):
        if not sessionid:
            raise ValueError("sessionid wajib diisi.")
        if not csrftoken:
            raise ValueError("csrftoken wajib diisi.")

        self.sessionid = sessionid
        self.csrftoken = csrftoken
        self.ds_user_id = ds_user_id or (sessionid.split("%3A")[0] if "%3A" in sessionid else None)
        self.extra_cookies = extra_cookies or {}

    @property
    def cookies(self) -> Dict[str, str]:
        """Mengembalikan dict cookies lengkap untuk HTTP client."""
        base = {
            "sessionid": self.sessionid,
            "csrftoken": self.csrftoken,
        }
        if self.ds_user_id:
            base["ds_user_id"] = str(self.ds_user_id)
        base.update(self.extra_cookies)
        return base

    @classmethod
    def from_session_switcher(cls, file_path: str, session_index: int = 0) -> "SessionAuth":
        """
        Membaca sesi langsung dari file JSON ekspor ekstensi Chrome Session Switcher.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File session switcher tidak ditemukan: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        sessions = data.get("sessions", [])
        if not sessions:
            raise ValueError("Tidak ada session yang ditemukan di dalam file JSON.")

        if session_index >= len(sessions):
            raise IndexError(f"Session index {session_index} di luar jangkauan (total {len(sessions)} session).")

        raw_cookies = sessions[session_index].get("cookies", [])
        cookie_map = {c["name"]: c["value"] for c in raw_cookies if "name" in c and "value" in c}

        sessionid = cookie_map.pop("sessionid", None)
        csrftoken = cookie_map.pop("csrftoken", None)
        ds_user_id = cookie_map.pop("ds_user_id", None)

        if not sessionid or not csrftoken:
            raise ValueError("File session-switcher tidak memuat cookie sessionid atau csrftoken yang valid.")

        return cls(
            sessionid=sessionid,
            csrftoken=csrftoken,
            ds_user_id=ds_user_id,
            extra_cookies=cookie_map
        )

    @classmethod
    def from_dict(cls, cookies: Dict[str, str]) -> "SessionAuth":
        """
        Membaca sesi dari dictionary cookies standar.
        """
        c = dict(cookies)
        sessionid = c.pop("sessionid", None)
        csrftoken = c.pop("csrftoken", None)
        ds_user_id = c.pop("ds_user_id", None)
        return cls(sessionid=sessionid, csrftoken=csrftoken, ds_user_id=ds_user_id, extra_cookies=c)

    @classmethod
    def from_cookie_string(cls, cookie_string: str) -> "SessionAuth":
        """
        Membaca sesi dari string header Cookie ('sessionid=...; csrftoken=...').
        """
        cookie_map = {}
        for item in cookie_string.split(";"):
            item = item.strip()
            if "=" in item:
                k, v = item.split("=", 1)
                cookie_map[k.strip()] = v.strip()
        return cls.from_dict(cookie_map)

    @classmethod
    def from_env(cls, prefix: str = "THREADS_") -> "SessionAuth":
        """
        Membaca sesi dari environment variables (misal: THREADS_SESSIONID, THREADS_CSRFTOKEN).
        """
        sessionid = os.environ.get(f"{prefix}SESSIONID")
        csrftoken = os.environ.get(f"{prefix}CSRFTOKEN")
        ds_user_id = os.environ.get(f"{prefix}USER_ID")
        if not sessionid or not csrftoken:
            raise ValueError(f"Environment variables {prefix}SESSIONID dan {prefix}CSRFTOKEN wajib diisi.")
        return cls(sessionid=sessionid, csrftoken=csrftoken, ds_user_id=ds_user_id)
