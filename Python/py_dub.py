from pydub import AudioSegment
from pydub.playback import play
import pathlib

print(pathlib.Path(pathlib.Path.cwd() / 'furret walk around the world.mp3').is_file())

song = AudioSegment.from_file('furret walk around the world.mp3')
#sound1 = sound2 = song
minutes = 1
seconds = 8.58
time = (minutes*60*1000)+(seconds*1000)
#duration = song[34300:time]

sound1 = song[100:34200]

#overlay = sound1.overlay(sound2, position=34300)
#play(sound1)

sound1.export(pathlib.Path.cwd() / 'furret walk cut.mp3', format="mp3")
