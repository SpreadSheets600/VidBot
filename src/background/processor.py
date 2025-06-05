import os
import random
from pathlib import Path
from moviepy import VideoFileClip

from ..logger import get_logger

logger = get_logger("VidBot")


def get_data_file_path(filename):
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    return project_root / "data" / filename


def get_video_duration(video_path):
    try:
        with VideoFileClip(str(video_path)) as clip:
            return clip.duration
    except Exception as e:
        logger.error(f"Error Getting Video Duration : {e}")
        return None


def crop_ratio(clip):
    width, height = clip.size

    # Calculate Target Dimentions
    target_ratio = 9 / 16
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        new_height = height

        x_center = width // 2
        x1 = x_center - new_width // 2
        x2 = x1 + new_width

        cropped_clip = clip.cropped(x1=x1, y1=0, x2=x2, y2=new_height)

    else:
        new_width = width
        new_height = int(width / target_ratio)

        y_center = height // 2
        y1 = y_center - new_height // 2
        y2 = y1 + new_height

        cropped_clip = clip.cropped(x1=0, y1=y1, x2=new_width, y2=y2)

    logger.info(
        f"Cropped From {width}x{height} - {cropped_clip.size[0]}x{cropped_clip.size[1]}"
    )
    return cropped_clip


def trim_random_minute(input_video_path, output_video_path, trim_duration=60):
    try:
        if not input_video_path.exists():
            logger.error(f"Input Video File {input_video_path} Does Not Exsist.")
            return False

        total_duration = get_video_duration(input_video_path)
        if total_duration is None:
            return False

        logger.info(
            f"Total Video Duration : {total_duration:.2f} Seconds ({total_duration/60:.2f} Minutes)"
        )

        if total_duration < trim_duration:
            logger.warning(f"Video Is Only {total_duration:.2f} Seconds Long")
            logger.info("Using Entire Video Duration")

            start_time = 0
            end_time = total_duration

        else:
            max_start_time = total_duration - trim_duration
            start_time = random.uniform(0, max_start_time)
            end_time = start_time + trim_duration

        logger.info(f"Selected Time Range : {start_time:.2f}s - {end_time:.2f}s")
        logger.info(f"Trimming {end_time - start_time:.2f} Seconds Of Video")

        with VideoFileClip(str(input_video_path)) as video:
            trimmed_clip = video.subclipped(start_time, end_time)
            cropped_clip = crop_ratio(trimmed_clip)

            output_video_path.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Saving Trimed And Cropped Video To : {output_video_path}")

            cropped_clip.write_videofile(
                str(output_video_path),
                codec="libx264",
                audio_codec="aac",
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                logger=None,
            )

            logger.info("Video Processing Done!")
            return True

    except Exception as e:
        logger.error(f"Error Processing Video : {e}")
        return False


def process_background():
    input_video = get_data_file_path("background.mp4")  # Input Video
    output_video = get_data_file_path("processed.mp4")  # Output Video

    success = trim_random_minute(input_video, output_video, trim_duration=60)
    return success
