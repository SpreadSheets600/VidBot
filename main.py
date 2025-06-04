from src.logger import get_logger
from src.script.generator import generate_script
from src.reddit.scrapper import scrape_subreddit_data

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
