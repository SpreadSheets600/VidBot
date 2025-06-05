import os
import json
import random
from google import genai
from pathlib import Path
from google.genai import types
from dotenv import load_dotenv

from ..logger import get_logger

logger = get_logger("VidBot")

load_dotenv()


def get_data_file_path(filename):
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent

    return project_root / "data" / filename


def generate_script():
    # Load Reddit JSON
    with open(get_data_file_path("subreddit.json")) as raw_file:
        raw_data = json.load(raw_file)

    post_title = raw_data[0]["title"]
    post_comments = (
        [random.choice(raw_data[0]["comments"])] if raw_data[0]["comments"] else []
    )  # Take Random Comment

    # Flatten Comments For The Context
    flattened_comments = []

    def extract_comments(comments, level=0):
        for comment in comments:
            prefix = ">" * level
            flattened_comments.append(
                f"{prefix} {comment['author']}: {comment['body']}"
            )
            if "replies" in comment:
                extract_comments(comment["replies"], level + 1)

    extract_comments(post_comments)
    comment_context = "\n".join(flattened_comments)

    # Gemini API To Generate Content
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "JUST RETURN THE VOICE OVER."
                    "You are a creative YouTube Shorts scriptwriter. "
                    "Based on the given Reddit post and its funniest or most absurd top comment."
                    "write a single 30–60 second funny, engaging story based script suitable for a vertical video. "
                    "Only write ONE script, use the comment chain as inspiration, and keep it light and meme-worthy. "
                    "Add in parts of your own imagination if you feel the story is small, make it a big meme. "
                    "Just output the script narration only, no outlines, no visuals, no extra formatting."
                )
            ),
            contents=[
                "role: user",
                f"parts : [Title: {post_title}, Comments: + {comment_context}",
            ],
        )
    except Exception as e:
        logger.error(f"Error Generating Script From Gemini : {e}")

    with open(get_data_file_path("script.txt"), "w+") as script_file:
        script_file.write(response.text.replace("\n", ""))
