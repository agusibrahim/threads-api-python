#!/usr/bin/env python3
"""
Threads Automation Bot CLI & Quick Runner
Wraps the modular threads_api package.
"""

import os
import sys

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threads_api import ThreadsClient, ThreadsBot, SessionAuth

DEFAULT_SESSION_FILE = os.environ.get(
    "THREADS_SESSION_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "session.json")
)

if __name__ == "__main__":
    if not os.path.exists(DEFAULT_SESSION_FILE):
        print(f"[!] Session file tidak ditemukan di {DEFAULT_SESSION_FILE}")
        sys.exit(1)

    bot = ThreadsClient(DEFAULT_SESSION_FILE)
    print(f"[*] Terhubung dengan User ID: {bot.user_id}")

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "post" and len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            print(f"[*] Posting status: '{text}'...")
            res = bot.create_post(text)
            media = res.get("media", {})
            print(f"[✓] Berhasil diposting! Link: {media.get('permalink')}")

        elif cmd == "photo" and len(sys.argv) > 3:
            img_path = sys.argv[2]
            text = " ".join(sys.argv[3:])
            print(f"[*] Posting foto ({img_path}): '{text}'...")
            res = bot.create_photo_post(text, img_path)
            media = res.get("media", {})
            print(f"[✓] Berhasil diposting! Link: {media.get('permalink')}")

        elif cmd == "carousel" and len(sys.argv) > 3:
            # Format: python3 threads_bot.py carousel "caption" img1 img2 ...
            caption = sys.argv[2]
            img_paths = sys.argv[3:]
            print(f"[*] Posting carousel ({len(img_paths)} gambar): '{caption}'...")
            res = bot.create_carousel_post(caption, img_paths)
            media = res.get("media", {})
            print(f"[✓] Berhasil diposting! Link: {media.get('permalink')}")

        elif cmd == "feed":
            print("[*] Mengambil timeline feed terbaru...")
            res = bot.get_feed()
            edges = res.get("data", {}).get("feedData", {}).get("edges", [])
            print(f"[✓] Ditemukan {len(edges)} postingan:")
            for i, edge in enumerate(edges, 1):
                p = edge["node"]["text_post_app_thread"]["thread_items"][0]["post"]
                user = p["user"]["username"]
                cap = p.get("caption", {}).get("text", "")[:60] if p.get("caption") else "(tanpa teks)"
                print(f"  {i}. @{user}: {cap.strip()} [ID: {p['pk']}]")

        elif cmd == "like" and len(sys.argv) > 2:
            post_id = sys.argv[2]
            print(f"[*] Menyukai postingan {post_id}...")
            res = bot.like_post(post_id)
            print(f"[✓] Hasil: {res}")

        else:
            # Fallback direct text post
            text = " ".join(sys.argv[1:])
            print(f"[*] Posting status: '{text}'...")
            res = bot.create_post(text)
            media = res.get("media", {})
            print(f"[✓] Berhasil diposting! Link: {media.get('permalink')}")

    else:
        print("\n[i] Panduan Perintah Threads Bot:")
        print("  python3 threads_bot.py 'Teks postingan langsung'")
        print("  python3 threads_bot.py post 'Teks status baru'")
        print("  python3 threads_bot.py photo <path_foto> 'Caption foto'")
        print("  python3 threads_bot.py carousel 'Caption' <path1> <path2> ...")
        print("  python3 threads_bot.py feed")
        print("  python3 threads_bot.py like <post_id>")
