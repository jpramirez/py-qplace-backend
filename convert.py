from os import path
from pydub import AudioSegment

# files                                                                         
src = "transcript.mp3"
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound
sound.export(dst, format="wav")