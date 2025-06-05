import os
import json
import yt_dlp
from pathlib import Path

from ..logger import get_logger

logger = get_logger("VidBot")


def get_data_file_path(filename):
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    return project_root / "data" / filename


def load_youtube_links():
    try:
        with open("links.json", "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("links", data.get("urls", []))
        else:
            logger.error("Invalid JSON Structure")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Error Parsing JSON File : {e}")
        return []
    except Exception as e:
        logger.error(f"Error Loading YouTube Links : {e}")
        return []


def download_youtube_video(url, output_path):
    try:
        logger.info(f"Starting Download From : {url}")

        ydl_opts = {
            "format": "best[ext=mp4]/best",  # Download Best Quality MP4 | Fallback : Best
            "outtmpl": str(output_path),  # Output Filename
            "noplaylist": True,  # Only Single Video
            "no_warnings": False,  # Show Warnings
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "Unknown")
            duration = info.get("duration", 0)

            logger.info(f"Video : {video_title}")
            logger.info(f"Duration : {duration // 60}:{duration % 60:02d}")

            ydl.download([url])

        if output_path.exists():
            logger.info(f"Successfully Downloaded : {output_path}")
            return True
        else:
            logger.error("Download Failed - Output File Not Found!")
            return False

    except yt_dlp.DownloadError as e:
        logger.error(f"Download Error For {url} : {e}")
        return False
    except Exception as e:
        logger.error(f"Error Downloading From {url} : {e}")
        return False


def generate_background():
    output_file = get_data_file_path("background.mp4")

    if output_file.exists():
        logger.info("File Already Exists! Skipping Download.")
        return

    output_file.parent.mkdir(parents=True, exist_ok=True)

    youtube_links = load_youtube_links()

    if not youtube_links:
        logger.error("No YouTube Links Found In JSON File")
        return

    for i, link in enumerate(youtube_links, 1):
        if isinstance(link, str) and link.strip():
            logger.info(
                f"Attempting To Download From {i}/{len(youtube_links)} : {link}"
            )

            if download_youtube_video(link.strip(), output_file):
                logger.info("Download Completed!")
                break
            else:
                logger.warning(f"Failed To Download From {link}, Trying Next Link ...")
        else:
            logger.warning(f"Invalid link format: {link}")
    else:
        logger.error("Failed To Download From Any Provided Links!")
