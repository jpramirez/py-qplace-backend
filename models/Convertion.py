from os import path
from pydub import AudioSegment
import models.Utils


class Convertion():
    def __init__(self,filename,format):
        self.FileName = filename
        self.Format = format



    def Convert(self,toDST):
        sound = AudioSegment.from_mp3(self.FileName)
        sound.export(dst, format="wav")
        Hash256File(dst)
