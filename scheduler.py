import tweepy
import json
import os
import random
from datetime import datetime, date
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

def load_posts():
    with open("posts.json", "r") as f:
        return json.load(f)

def save_posts(posts):
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=2)

def get_todays_published_count(posts):
    today = date.today().isoformat()
    return sum(1 for p in posts if p.get("published_date") == today)

def should_post_today(posts):
    daily_target = random.randint(3, 7)
    published_today = get_todays_published_count(posts)
    return published_today < daily_target

def roll_post_chance():
    # ~30% chance each time the workflow runs to actually post
    # With 5 runs/day this gives organic randomness
    return random.random() < 0.30

def main():
    client = get_client()
    posts = load_posts()
    pending = [p for p in posts if not p.get("published", False)]

    if not pending:
        print("No pending posts.")
        return

    if not should_post_today(posts):
        print("Daily post limit reached.")
        return

    if not roll_post_chance():
        print("Not posting this run (random skip).")
        return

    post = pending[0]

    try:
        client.create_tweet(text=post["content"])
        post["published"] = True
        post["published_date"] = date.today().isoformat()
        save_posts(posts)
        print(f"Published: {post['content'][:60]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()