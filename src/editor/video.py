import os
from pathlib import Path
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    CompositeAudioClip,
    TextClip,
)

from ..logger import get_logger

logger = get_logger("VidBot")


def get_data_file_path(filename):
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    return project_root / "data" / filename

def get_font_file_path():
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    return project_root / "src" / "editor" / "font.ttf"

def create_subtitle_generator(video_size):
    video_width, video_height = video_size
    subtitle_box_width = int(video_width * 0.9)
    subtitle_box_height = int(video_height * 0.5)

    def generator(text):
        return TextClip(
            text=text,
            font_size=16,
            color="yellow",
            stroke_width=2,
            font=get_font_file_path(),
            method="caption",
            text_align="center",
            stroke_color="black",
            size=(subtitle_box_width, subtitle_box_height),
        )

    return generator


def merge_video_audio_subtitles(video_path, audio_path, srt_path, output_path):
    try:
        for file_path, file_type in [
            (video_path, "Video"),
            (audio_path, "Audio"),
            (srt_path, "SRT"),
        ]:
            if not file_path.exists():
                logger.error(f"{file_type} File {file_path} Does Not Exist.")
                return False

        logger.info("Loading Video File ...")
        video_clip = VideoFileClip(str(video_path))
        video_duration = video_clip.duration
        video_size = video_clip.size

        logger.info(
            f"Video Loaded : {video_size[0]}x{video_size[1]} | Duration : {video_duration:.2f}s"
        )

        logger.info("Loading Audio File ...")

        audio_clip = AudioFileClip(str(audio_path))
        audio_duration = audio_clip.duration

        logger.info(f"Audio Loaded : Duration : {audio_duration:.2f}s")

        final_duration = min(video_duration, audio_duration)

        video_clip = video_clip.subclipped(0, final_duration)
        audio_clip = audio_clip.subclipped(0, final_duration)

        logger.info(f"Synced Duration : {final_duration:.2f}s")

        video_clip.audio = CompositeAudioClip([audio_clip])

        logger.info("Loading Subtitles ...")

        try:
            subtitle_generator = create_subtitle_generator(video_size)

            subtitle_clip = SubtitlesClip(
                str(srt_path), make_textclip=subtitle_generator, encoding="utf-8"
            )

            subtitle_clip = subtitle_clip.with_position(("center"))
            subtitle_clip = subtitle_clip.with_duration(final_duration)

            logger.info("Subtitles Loaded Successfully")

            final_video = CompositeVideoClip([video_clip, subtitle_clip])

        except Exception as e:
            logger.warning(f"Error Loading Subtitles: {e}")
            logger.info("Proceeding Without Subtitles")
            final_video = video_clip

        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Rendering Final Video To: {output_path}")
        logger.info(
            "This May Take Some Time Depending On Size And Quality Of The video ....."
        )

        final_video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            logger=None,
            fps=60,
        )

        video_clip.close()
        audio_clip.close()
        final_video.close()

        logger.info("Video Generation Successsful")
        return True

    except Exception as e:
        logger.error(f"Error Generating Video : {e}")
        return False


def generate_final_video():
    audio_file = get_data_file_path("audio.mp3")
    srt_file = get_data_file_path("subtitles.srt")
    output_file = get_data_file_path("final_video.mp4")
    video_file = get_data_file_path("trimmed_video.mp4")

    success = merge_video_audio_subtitles(video_file, audio_file, srt_file, output_file)

    if success:
        logger.info("Video Saved In Directory")
