# threads-api-python

Unofficial Python Automation Toolkit for Meta Threads (Web API & Instagram Barcelona Stack).

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, reliable reverse-engineered client for Meta Threads that mimics web browser requests using TLS fingerprinting (`curl_cffi`) and direct GraphQL/REST endpoints.

---

## Features

- **Authentication Flexibility:**
  - Import directly from Chrome extension [Session Switcher](https://chromewebstore.google.com/) exported `.json` file.
  - Import from Python dictionary or raw HTTP `Cookie` header string.
  - Environment variables support (`THREADS_SESSIONID`, `THREADS_CSRFTOKEN`).
- **Full Publishing Capabilities:**
  - 📝 **Text Posts & Replies:** Publish new posts or reply to threads.
  - 💬 **Quote Posts:** Quote other posts with your thoughts.
  - 🔗 **Link Previews:** Attach URL previews.
  - 🖼️ **Single Photo Post:** Automatic JPEG upload & dimension detection.
  - 📸 **Carousel Posts:** Multi-slide posts supporting 2 to 20 images.
  - 🎥 **Video Posts:** Upload `.mp4` videos with metadata.
- **Social Interactions:**
  - ❤️ **Like & Unlike:** Fast GraphQL mutations.
  - 🔁 **Repost & Delete Repost:** Share posts to your profile or undo reshares.
  - 📁 **Archive Posts:** Archive posts from your profile timeline.
- **Data Querying & Scraping:**
  - 📰 **Timeline Feeds:** Fetch *For You* or *Following* feeds.
  - 🔍 **Thread & Reply Retrieval:** Read replies and comments from any post.
  - 👤 **User Profiles:** Retrieve profile data (follower count, bio, verified badge).
- **Anti-Bot & Stealth:**
  - Native Chrome TLS fingerprint impersonation (bypasses bot detection).
  - Built-in randomized jitter helper (`sleep_random`).
  - Full HTTP / HTTPS proxy support.

---

## Installation

```bash
pip install curl_cffi Pillow
```

Or install in development mode:

```bash
git clone https://github.com/agusibrahim/threads-api-python.git
cd threads-api-python
pip install -e .
```

---

## Quickstart

### 1. Authentication

Export your active Threads web session using **Session Switcher** extension or copy your cookies from Chrome DevTools:

```python
from threads_api import ThreadsClient, SessionAuth

# Option A: From Session Switcher JSON
bot = ThreadsClient("session.json")

# Option B: From dictionary
auth = SessionAuth.from_dict({
    "sessionid": "YOUR_SESSION_ID",
    "csrftoken": "YOUR_CSRF_TOKEN",
    "ds_user_id": "YOUR_USER_ID"
})
bot = ThreadsClient(auth)

# Option C: With HTTP Proxy
bot = ThreadsClient(auth, proxy="http://user:pass@host:port")
```

### 2. Publishing Posts

```python
# Text Post
res = bot.create_post("Hello from Python automation! 🚀")
print("Post Link:", res["media"]["permalink"])

# Reply to a thread
bot.create_post("Awesome insight!", reply_to_post_id="4006113249393395447")

# Single Photo Post
bot.create_photo_post(
    text="Check out today's view 🌅",
    image="photo.jpg"
)

# Carousel Post (2 - 20 photos)
bot.create_carousel_post(
    text="5 Tips for Python Developers 📚",
    images=["slide_1.jpg", "slide_2.jpg", "slide_3.jpg"]
)
```

### 3. Interactions & Feed

```python
# Like & Unlike
bot.like_post("4006113249393395447")
bot.unlike_post("4006113249393395447")

# Repost
bot.repost("4006113249393395447")
bot.delete_repost("4006113249393395447")

# Get Feed
feed = bot.get_feed(variant="for_you")
for edge in feed["data"]["feedData"]["edges"]:
    post = edge["node"]["text_post_app_thread"]["thread_items"][0]["post"]
    print(f"@{post['user']['username']}: {post.get('caption', {}).get('text')}")
```

---

## Command Line Interface (CLI)

You can run automated actions directly from terminal:

```bash
# Post text
python3 cli.py "Hello world from CLI"

# Post photo
python3 cli.py photo banner.jpg "My new photo"

# Post carousel
python3 cli.py carousel "Carousel title" slide1.jpg slide2.jpg slide3.jpg

# Fetch latest feed
python3 cli.py feed

# Like post
python3 cli.py like 4006113249393395447
```

---

## Disclaimer

This project is for educational and research purposes only. It is not affiliated with, authorized, maintained, or endorsed by Meta, Instagram, or Threads. Use responsibly and respect rate limits.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
