import os
from pathlib import Path
from gradio_client import Client

from ..logger import get_logger

logger = get_logger("VidBot")


def get_data_file_path(filename):
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent

    return project_root / "data" / filename


def generate_voiceover():
    try:
        # Read The Script From The script.txt File
        script_path = get_data_file_path("script.txt")

        if not script_path.exists():
            logger.error(f"Script File {script_path} Does Not Exist")
            return

        with open(script_path, "r") as script_file:
            script_data = script_file.read()

        # Interact with the Gradio Client API to generate voiceover and subtitles
        try:
            client = Client("walidadebayo/text-to-speech-clone")
            result = client.predict(
                text=script_data,
                voice="en-US-JennyNeural - en-US (Female)",
                rate=0,
                pitch=0,
                generate_subtitles=True,
                uploaded_file=None,
                api_name="/predict",
            )

            # Extract Audio And Subtitles File Data
            audio_file = result[0]
            subtitle_file = result[1]

        except Exception as e:
            logger.error(f"Error Generating Voice Over : {e}")
            return

        # Move And Rename The Files To The Main Directory
        try:
            audio_dest = get_data_file_path("audio.mp3")
            subtitle_dest = get_data_file_path("subtitles.srt")

            if not os.path.exists(audio_file):
                logger.error(f"Audio File {audio_file} Does Not Exist.")
                return

            if not os.path.exists(subtitle_file):
                logger.error(f"Subtitle File {subtitle_file} Does Not Exist.")
                return

            os.rename(audio_file, audio_dest)
            os.rename(subtitle_file, subtitle_dest)

        except Exception as e:
            logger.exception(f"Error Moving Files To The Current Location : {e}")

    except Exception as e:
        logger.exception(f"Unexpected Error In Generating Voiceover : {e}")
