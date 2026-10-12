"""
Example usage of threads_api
"""

from threads_api import ThreadsClient, SessionAuth

def main():
    # 1. Initialize from Session Switcher JSON or dictionary
    # bot = ThreadsClient("session.json")
    
    auth = SessionAuth.from_dict({
        "sessionid": "YOUR_SESSION_ID",
        "csrftoken": "YOUR_CSRF_TOKEN",
        "ds_user_id": "YOUR_NUMERIC_USER_ID"
    })
    bot = ThreadsClient(auth)

    # 2. Text Post
    # res = bot.create_post("Hello world from Threads API!")
    # print("Post URL:", res.get("media", {}).get("permalink"))

    # 3. Single Photo Post
    # bot.create_photo_post("Beautiful sunset", image="sunset.jpg")

    # 4. Carousel Post (2 - 20 photos)
    # bot.create_carousel_post("Multi slide tips", images=["slide1.jpg", "slide2.jpg"])

    # 5. Interaction
    # bot.like_post("MEDIA_ID")
    # bot.repost("MEDIA_ID")

    # 6. Read Feed
    # feed = bot.get_feed(variant="for_you")
    # print("Feed:", feed)

if __name__ == "__main__":
    main()
