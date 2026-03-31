import tweepy
import json
import os
import random
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )

def get_posts_to_publish():
    with open("posts.json", "r") as f:
        posts = json.load(f)
    return [p for p in posts if not p.get("published", False)]

def publish_post(client, post):
    response = client.create_tweet(text=post["content"])
    return response

def mark_as_published(post_id):
    with open("posts.json", "r") as f:
        posts = json.load(f)
    
    for post in posts:
        if post["id"] == post_id:
            post["published"] = True
            break
    
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=2)

def should_post_now():
    return True

def main():
    if not should_post_now():
        print("Not a posting time, skipping.")
        return
    
    client = get_client()
    pending = get_posts_to_publish()
    
    if not pending:
        print("No pending posts.")
        return
    
    post = pending[0]
    
    try:
        publish_post(client, post)
        mark_as_published(post["id"])
        print(f"Published post {post['id']}: {post['content'][:50]}...")
    except Exception as e:
        print(f"Error publishing: {e}")

if __name__ == "__main__":
    main()