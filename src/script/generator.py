import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Load Reddit JSON
with open("../../data/subbreddit.json") as raw_file:
    raw_data = json.load(raw_file)

post_title = raw_data[0]["title"]
post_comments = raw_data[0]["comments"][:1]  # Take Only Top Comment

# Flatten Comments For The Context
flattened_comments = []


def extract_comments(comments, level=0):
    for comment in comments:
        prefix = ">" * level
        flattened_comments.append(f"{prefix} {comment['author']}: {comment['body']}")
        if "replies" in comment:
            extract_comments(comment["replies"], level + 1)


extract_comments(post_comments)
comment_context = "\n".join(flattened_comments)

# Gemini API To Generate Content
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=(
            "JUST RETURN THE VOICE OVER NO EXTRA STUFF NO DIRECTIONS ANYTHING SIMPLE STORY TELLING"
            "You are a creative YouTube Shorts scriptwriter. "
            "Based on the given Reddit post and its funniest or most absurd top comments, "
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

with open("../../data/script.txt", "w+") as script_file:
    script_file.write(response.text)
