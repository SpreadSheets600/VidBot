import os
import sys
import json
from pathlib import Path
from .yars.yars import YARS
from .yars.utils import display_results, download_image

from ..logger import get_logger
logger = get_logger("VidBot")

miner = YARS()

def get_data_file_path():
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent

    return project_root / "data" / "subreddit.json"

filename = get_data_file_path()

def scrape_subreddit_data(subreddit_name, limit=5, filename=filename):
    try:
        subreddit_posts = miner.fetch_subreddit_posts(
            subreddit_name, limit=limit, category="hot", time_filter="all"
        )

        try:
            with open(filename, "r") as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        for i, post in enumerate(subreddit_posts, 1):
            permalink = post["permalink"]
            post_details = miner.scrape_post_details(permalink)

            logger.info(f"Processing Post {i}")

            if post_details:
                post_data = {
                    "title": post.get("title", ""),
                    "author": post.get("author", ""),
                    "created_utc": post.get("created_utc", ""),
                    "num_comments": post.get("num_comments", 0),
                    "score": post.get("score", 0),
                    "permalink": post.get("permalink", ""),
                    "image_url": post.get("image_url", ""),
                    "thumbnail_url": post.get("thumbnail_url", ""),
                    "body": post_details.get("body", ""),
                    "comments": post_details.get("comments", []),
                }

                existing_data.append(post_data)
                save_to_json(existing_data, filename)
            else:
                logger.error(f"Failed To Scrape Details For : {post['title']}")

    except Exception as e:
        logger.error(f"Error Occured While Scrapping The Subreddit : {e}")

def save_to_json(data, filename=filename):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        logger.success(f"Saved Subreddit Data As {filename}")
    except Exception as e:
        logger.error(f"Error Saving Subreddit Data As {filename} : {e}")
