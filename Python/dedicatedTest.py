from pytube import YouTube
from moviepy.editor import *
import os

# specify the YouTube video URL
url = "https://www.youtube.com/watch?v=Bd1Bxxqb-bM"

# create a YouTube object
yt = YouTube(url)

# get the highest-quality audio stream
audio_stream = yt.streams.filter(only_audio=True)

# download the audio stream to a file
audio_file = audio_stream.download()

# convert the audio file to an MP3 file
audio_clip = AudioFileClip(audio_file)
mp3_file = os.path.splitext(audio_file)[0] + '.mp3'
audio_clip.write_audiofile(mp3_file)

# delete the original audio file
audio_clip.close()
os.remove(audio_file)

print(f"Downloaded {yt.title} as an MP3 file: {mp3_file}")
