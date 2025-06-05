from src.script.generator import generate_script
from src.editor.video import generate_final_video
from src.voice.generator import generate_voiceover
from src.reddit.scrapper import scrape_subreddit_data
from src.background.processor import process_background
from src.background.downloader import generate_background

from src.logger import get_logger

logger = get_logger("VidBot")

logger.header("Welcome To Vid Bot")
logger.separator()

logger.info("Scrapping Off Subreddit To Get Data")

try:
    scrape_subreddit_data(subreddit_name="askreddit", limit=1)
    logger.success("Done! Moving To Next Setp")

except Exception as e:
    logger.error(f"Error Occured While Scrapping The Subreddit : {e}")

logger.info("Using Gemini To Generate Script")

try:
    generate_script()
    logger.success("Done! Moving To Next Step")
except Exception as e:
    logger.error(f"Error Occured While Generating Script With Gemini : {e}")

logger.info("Using TTS Service To Generate VoiceOver")

try:
    generate_voiceover()
    logger.success("Done! Moving To Next Step")
except Exception as e:
    logger.error(f"Error Occured While Generating Voice Over : {e}")

logger.info("Getting Background Video")

try:
    generate_background()
    logger.info("Done! Moving To Next Step")
except Exception as e:
    logger.error(f"Error Occured While Downloading Background Video : {e}")

logger.info("Processing Background Video")

try:
    process_background()
    logger.success("Done! Moving To Next Step")
except Exception as e:
    logger.error(f"Error Occured While Processing Background Video : {e}")

logger.info("Generating Final Video")

try:
    generate_final_video()
    logger.success("Done! Process Completed")
except Exception as e:
    logger.error(f"Error Generating Final Video : {e}")
