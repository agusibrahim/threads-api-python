"""
Main Threads API Automation Client
"""

import json
import random
import time
import uuid
from typing import Dict, List, Optional, Union

from curl_cffi import requests

from .auth import SessionAuth
from .constants import (
    BASE_URL,
    GRAPHQL_URL,
    GRAPHQL_QUERY_URL,
    BARCELONA_APP_ID,
    ASBD_ID,
    BLOKS_VERSION_ID,
    DEFAULT_LSD,
    DEFAULT_JAZOEST,
    DEFAULT_USER_AGENT,
    DEFAULT_RELAY_FLAGS,
    DOC_ID_LIKE,
    DOC_ID_UNLIKE,
    DOC_ID_CREATE_REPOST,
    DOC_ID_DELETE_REPOST,
    DOC_ID_FEED_DIRECT,
    DOC_ID_FEED_PAGINATION,
    DOC_ID_POST_DETAIL,
    DOC_ID_POST_REPLIES,
    DOC_ID_USER_PROFILE,
    DOC_ID_ARCHIVE_POST,
    DOC_ID_DELETE_ARCHIVED_POST,
    ENDPOINT_CONFIGURE_TEXT,
    ENDPOINT_CONFIGURE_FEED_IMAGE,
    ENDPOINT_CONFIGURE_SIDECAR,
)
from .media import MediaUploader


class ThreadsClient:
    """
    Client automasi Threads berbasis Web API (Instagram Barcelona stack).
    """

    def __init__(
        self,
        auth: Union[SessionAuth, str, Dict[str, str]],
        proxy: Optional[str] = None,
        impersonate: str = "chrome124",
        fb_dtsg: Optional[str] = None,
    ):
        if isinstance(auth, SessionAuth):
            self.auth = auth
        elif isinstance(auth, str):
            if auth.endswith(".json"):
                self.auth = SessionAuth.from_session_switcher(auth)
            else:
                self.auth = SessionAuth.from_cookie_string(auth)
        elif isinstance(auth, dict):
            self.auth = SessionAuth.from_dict(auth)
        else:
            raise TypeError("Auth harus berupa instance SessionAuth, path file JSON, string cookie, atau dict.")

        self.user_id = self.auth.ds_user_id
        self.csrftoken = self.auth.csrftoken
        self.lsd = DEFAULT_LSD
        self.fb_dtsg = fb_dtsg or self.auth.extra_cookies.get("fb_dtsg", "")
        self.web_session_id = f"{uuid.uuid4().hex[:6]}:{uuid.uuid4().hex[:6]}:{uuid.uuid4().hex[:6]}"

        # Setup browser impersonation & session
        self.session = requests.Session(impersonate=impersonate)
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

        self.session.cookies.update(self.auth.cookies)

        self.base_headers = {
            "authority": "www.threads.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "origin": "https://www.threads.com",
            "referer": "https://www.threads.com/",
            "user-agent": DEFAULT_USER_AGENT,
            "x-asbd-id": ASBD_ID,
            "x-bloks-version-id": BLOKS_VERSION_ID,
            "x-csrftoken": self.csrftoken,
            "x-ig-app-id": BARCELONA_APP_ID,
            "x-instagram-ajax": "0",
            "x-fb-lsd": self.lsd,
            "x-web-session-id": self.web_session_id,
        }

    # --------------------------------------------------------------------------
    # Utility & Anti-Detection
    # --------------------------------------------------------------------------
    @staticmethod
    def sleep_random(min_seconds: float = 3.0, max_seconds: float = 8.0):
        """Menambahkan jeda acak untuk mensimulasikan perilaku pengguna nyata."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay

    def check_login(self) -> bool:
        """
        Memeriksa apakah sesi saat ini masih aktif dan terautentikasi.
        """
        try:
            profile = self.get_user_profile(self.user_id) if self.user_id else None
            return bool(profile)
        except Exception:
            return False

    # --------------------------------------------------------------------------
    # Posting Features (Text, Photo, Carousel, Video, Quote, Link)
    # --------------------------------------------------------------------------
    def create_post(
        self,
        text: str,
        reply_to_post_id: Optional[str] = None,
        quote_post_id: Optional[str] = None,
        link_attachment_url: Optional[str] = None,
    ) -> dict:
        """
        Membuat postingan teks baru, balasan (reply), atau quote post.
        """
        url = f"{BASE_URL}{ENDPOINT_CONFIGURE_TEXT}"
        is_reply = bool(reply_to_post_id)
        composer_session_id = str(uuid.uuid4())
        upload_id = str(int(time.time() * 1000))

        app_info = {
            "community_flair_id": None,
            "composer_session_id": composer_session_id,
            "entry_point": "create_reply" if is_reply else "create_post",
            "excluded_inline_media_ids": "[]",
            "fediverse_composer_enabled": True,
            "is_genai_invocation_post": False,
            "is_reply_approval_enabled": False,
            "is_spoiler_media": False,
            "link_attachment_url": link_attachment_url,
            "link_preview_default_render_style": None,
            "quoted_post_id": quote_post_id,
            "reply_control": 0,
            "reply_id": reply_to_post_id if is_reply else None,
            "text_with_entities": {"entities": [], "text": text},
        }

        payload = {
            "audience": "default",
            "caption": text,
            "creator_geo_gating_info": json.dumps({"whitelist_country_codes": []}),
            "is_upload_type_override_allowed": "1",
            "publish_mode": "text_post",
            "should_include_permalink": "true",
            "text_post_app_info": json.dumps(app_info),
            "upload_id": upload_id,
            "jazoest": DEFAULT_JAZOEST,
        }

        if is_reply:
            payload["barcelona_source_reply_id"] = reply_to_post_id

        res = self.session.post(url, headers=self.base_headers, data=payload)
        return res.json()

    def create_photo_post(
        self,
        text: str,
        image: Union[str, bytes],
        reply_to_post_id: Optional[str] = None,
    ) -> dict:
        """
        Membuat postingan 1 foto (single photo) dengan caption.
        """
        upload_id = MediaUploader.upload_photo(
            self.session, self.base_headers, image, is_sidecar=False
        )
        is_reply = bool(reply_to_post_id)
        composer_session_id = str(uuid.uuid4())

        app_info = {
            "composer_session_id": composer_session_id,
            "entry_point": "create_reply" if is_reply else "create_post",
            "excluded_inline_media_ids": "[]",
            "fediverse_composer_enabled": True,
            "is_genai_invocation_post": False,
            "is_reply_approval_enabled": False,
            "is_spoiler_media": False,
            "reply_control": 0,
            "reply_id": reply_to_post_id if is_reply else None,
            "text_with_entities": {"entities": [], "text": text},
        }

        payload = {
            "audience": "default",
            "caption": text,
            "creator_geo_gating_info": json.dumps({"whitelist_country_codes": []}),
            "is_threads": "1",
            "should_include_permalink": "true",
            "text_post_app_info": json.dumps(app_info),
            "upload_id": upload_id,
            "jazoest": DEFAULT_JAZOEST,
        }

        if is_reply:
            payload["barcelona_source_reply_id"] = reply_to_post_id

        url = f"{BASE_URL}{ENDPOINT_CONFIGURE_FEED_IMAGE}"
        res = self.session.post(url, headers=self.base_headers, data=payload)
        return res.json()

    def create_carousel_post(
        self,
        text: str,
        images: List[Union[str, bytes]],
        reply_to_post_id: Optional[str] = None,
    ) -> dict:
        """
        Membuat postingan carousel (multi-slide foto) dengan caption.
        """
        if not (2 <= len(images) <= 20):
            raise ValueError("Carousel membutuhkan 2 hingga 20 gambar.")

        uploaded_ids = []
        for img in images:
            up_id = MediaUploader.upload_photo(
                self.session, self.base_headers, img, is_sidecar=True
            )
            uploaded_ids.append(up_id)
            time.sleep(1)

        is_reply = bool(reply_to_post_id)
        composer_session_id = str(uuid.uuid4())
        client_sidecar_id = str(int(time.time() * 1000))

        text_post_app_info = {
            "composer_session_id": composer_session_id,
            "entry_point": "create_reply" if is_reply else "create_post",
            "excluded_inline_media_ids": "[]",
            "fediverse_composer_enabled": True,
            "is_genai_invocation_post": False,
            "is_reply_approval_enabled": False,
            "is_spoiler_media": False,
            "reply_control": 0,
            "reply_id": reply_to_post_id if is_reply else None,
            "text_with_entities": {"entities": [], "text": text},
        }

        payload = {
            "audience": "default",
            "caption": text,
            "children_metadata": [{"upload_id": uid} for uid in uploaded_ids],
            "client_sidecar_id": client_sidecar_id,
            "creator_geo_gating_info": json.dumps({"whitelist_country_codes": []}),
            "is_threads": True,
            "should_include_permalink": True,
            "text_post_app_info": json.dumps(text_post_app_info),
            "web_session_id": self.web_session_id,
            "jazoest": DEFAULT_JAZOEST,
        }

        if is_reply:
            payload["barcelona_source_reply_id"] = reply_to_post_id

        conf_headers = self.base_headers.copy()
        conf_headers["content-type"] = "text/plain;charset=UTF-8"

        url = f"{BASE_URL}{ENDPOINT_CONFIGURE_SIDECAR}"
        res = self.session.post(url, headers=conf_headers, data=json.dumps(payload))
        return res.json()

    def create_video_post(
        self,
        text: str,
        video: Union[str, bytes],
        width: int = 1080,
        height: int = 1920,
        reply_to_post_id: Optional[str] = None,
    ) -> dict:
        """
        Membuat postingan video (.mp4) dengan caption.
        """
        upload_id = MediaUploader.upload_video(
            self.session, self.base_headers, video, width=width, height=height, is_sidecar=False
        )
        is_reply = bool(reply_to_post_id)
        composer_session_id = str(uuid.uuid4())

        app_info = {
            "composer_session_id": composer_session_id,
            "entry_point": "create_reply" if is_reply else "create_post",
            "excluded_inline_media_ids": "[]",
            "fediverse_composer_enabled": True,
            "is_genai_invocation_post": False,
            "is_reply_approval_enabled": False,
            "is_spoiler_media": False,
            "reply_control": 0,
            "reply_id": reply_to_post_id if is_reply else None,
            "text_with_entities": {"entities": [], "text": text},
        }

        payload = {
            "audience": "default",
            "caption": text,
            "creator_geo_gating_info": json.dumps({"whitelist_country_codes": []}),
            "is_threads": "1",
            "should_include_permalink": "true",
            "text_post_app_info": json.dumps(app_info),
            "upload_id": upload_id,
            "video_subtitles_enabled": "0",
            "jazoest": DEFAULT_JAZOEST,
        }

        if is_reply:
            payload["barcelona_source_reply_id"] = reply_to_post_id

        url = f"{BASE_URL}{ENDPOINT_CONFIGURE_FEED_IMAGE}"
        res = self.session.post(url, headers=self.base_headers, data=payload)
        return res.json()

    # --------------------------------------------------------------------------
    # Interactivity Features (Like, Unlike, Repost, Delete Repost)
    # --------------------------------------------------------------------------
    def _call_graphql_mutation(self, friendly_name: str, doc_id: str, variables: dict) -> dict:
        headers = self.base_headers.copy()
        headers["x-fb-friendly-name"] = friendly_name

        payload = {
            "lsd": self.lsd,
            "fb_api_req_friendly_name": friendly_name,
            "variables": json.dumps(variables),
            "doc_id": doc_id,
        }

        res = self.session.post(GRAPHQL_URL, headers=headers, data=payload)
        return res.json()

    def like_post(self, media_id: str) -> dict:
        """Menyukai (Like) postingan berdasarkan media ID."""
        return self._call_graphql_mutation(
            friendly_name="useTHLikeMutationLikeMutation",
            doc_id=DOC_ID_LIKE,
            variables={
                "mediaID": str(media_id),
                "requestData": {
                    "barcelona_source_reply_id_str": None,
                    "container_module": "ig_text_post_permalink",
                    "inventory_source": None,
                },
            },
        )

    def unlike_post(self, media_id: str) -> dict:
        """Membatalkan suka (Unlike) postingan berdasarkan media ID."""
        return self._call_graphql_mutation(
            friendly_name="useTHLikeMutationUnlikeMutation",
            doc_id=DOC_ID_UNLIKE,
            variables={
                "mediaID": str(media_id),
                "requestData": {
                    "barcelona_source_reply_id_str": None,
                    "container_module": "ig_text_post_permalink",
                    "inventory_source": None,
                },
            },
        )

    def repost(self, media_id: str) -> dict:
        """Membagikan ulang (Repost) postingan ke profil Anda."""
        return self._call_graphql_mutation(
            friendly_name="useTHCreateRepostMutation",
            doc_id=DOC_ID_CREATE_REPOST,
            variables={"mediaID": str(media_id)},
        )

    def delete_repost(self, media_id: str) -> dict:
        """Membatalkan repost (Hapus Repost) postingan."""
        return self._call_graphql_mutation(
            friendly_name="useTHDeleteRepostMutation",
            doc_id=DOC_ID_DELETE_REPOST,
            variables={"mediaID": str(media_id)},
        )

    def archive_post(self, media_id: str) -> dict:
        """Mengarsipkan postingan (menyembunyikan dari profil)."""
        return self._call_graphql_mutation(
            friendly_name="useBarcelonaArchivePostMutation",
            doc_id=DOC_ID_ARCHIVE_POST,
            variables={"mediaID": str(media_id)},
        )

    # --------------------------------------------------------------------------
    # Feed & Query Features (Get Post, Feed, Replies, Profile)
    # --------------------------------------------------------------------------
    def _call_graphql_query(self, friendly_name: str, doc_id: str, variables: dict) -> dict:
        headers = self.base_headers.copy()
        headers["x-fb-friendly-name"] = friendly_name

        payload = {
            "av": self.user_id or "0",
            "__user": "0",
            "__a": "1",
            "__comet_req": "29",
            "fb_dtsg": self.fb_dtsg,
            "jazoest": "26104",
            "lsd": self.lsd,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": friendly_name,
            "server_timestamps": "true",
            "variables": json.dumps(variables),
            "doc_id": doc_id,
        }

        res = self.session.post(GRAPHQL_QUERY_URL, headers=headers, data=payload)
        return res.json()

    def get_feed(self, variant: str = "for_you") -> dict:
        """
        Mengambil feed timeline ('for_you' atau 'following').
        """
        vars_dict = {
            "data": {
                "pagination_source": "text_post_feed_threads",
                "reason": "cold_start_fetch",
            },
            "variant": variant,
            **DEFAULT_RELAY_FLAGS,
        }
        return self._call_graphql_query(
            friendly_name="BarcelonaFeedDirectQuery",
            doc_id=DOC_ID_FEED_DIRECT,
            variables=vars_dict,
        )

    def get_post(self, post_id: str) -> dict:
        """
        Mengambil data detail sebuah postingan (media, user, like_count, gambar, dll).
        """
        vars_dict = {"postID": str(post_id), **DEFAULT_RELAY_FLAGS}
        return self._call_graphql_query(
            friendly_name="BarcelonaPostPageTargetQuery",
            doc_id=DOC_ID_POST_DETAIL,
            variables=vars_dict,
        )

    def get_replies(self, post_id: str, first: int = 10, after: Optional[str] = None) -> dict:
        """
        Mengambil komentar/balasan dari postingan tertentu.
        """
        vars_dict = {
            "after": after,
            "filterType": None,
            "first": first,
            "postID": str(post_id),
            "sortOrder": "TOP",
            **DEFAULT_RELAY_FLAGS,
            "__relay_internal__pv__BarcelonaHasPermalinkIndentationrelayprovider": False,
        }
        return self._call_graphql_query(
            friendly_name="BarcelonaPostPageDirectRepliesRefetchQuery",
            doc_id=DOC_ID_POST_REPLIES,
            variables=vars_dict,
        )

    def get_user_profile(self, username: str) -> dict:
        """
        Mengambil data profil pengguna (ID, follower count, verified status, dll).
        """
        vars_dict = {"username": username, **DEFAULT_RELAY_FLAGS}
        return self._call_graphql_query(
            friendly_name="BarcelonaUsernameHovercardImplDirectQuery",
            doc_id=DOC_ID_USER_PROFILE,
            variables=vars_dict,
        )
