import os
from gradio_client import Client, handle_file

with open("../../data/script.txt") as script_file:
    script_data = script_file.read()

client = Client("walidadebayo/text-to-speech-clone")
result = client.predict(
		text=script_data,
		voice="en-US-JennyNeural - en-US (Female)",
		rate=0,
		pitch=0,
		generate_subtitles=True,
		uploaded_file=None,
		api_name="/predict"
)

print(result)

audio_file = result[0]
subtitle_file = result[1]

# Move And Rename The Relevent Files To Current Lcoation
os.rename(audio_file, "../../data/audio.mp3")
os.rename(subtitle_file, "../../data/subtitles.srt")
