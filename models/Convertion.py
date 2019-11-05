from os import path
from pydub import AudioSegment
import models.Utils


class Convertion():
    formats_to_convert = ['.m4a']
    
    def __init__(self,filename,format):
        self.FileName = filename
        self.Format = format




    def Convert(self,toDST):
       if self.FileName.endswith(tuple(formats_to_convert)):
            (path, file_extension) = os.path.splitext(self.FileName)
            file_extension_final = file_extension.replace('.', '')
            try:
                track = AudioSegment.from_file(filepath,
                        file_extension_final)
                wav_filename = filename.replace(file_extension_final, 'wav')
                wav_path = dirpath + '/' + wav_filename
                print('CONVERTING: ' + str(filepath))
                file_handle = track.export(wav_path, format='wav')
                os.remove(filepath)
            except:
                print("ERROR CONVERTING " + str(filepath))
