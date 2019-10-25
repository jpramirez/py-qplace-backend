import speech_recognition as sr

class Recognizer():
    
    def __init__(self,filename):
        self.recognizer = sr.Recognizer()
        print (filename)
        self.FileName = filename

    def Recognize(self):
        print (self.FileName)
        with sr.AudioFile(self.FileName) as source:
			# remove this if it is not working 
			# correctly. 
	        #r.adjust_for_ambient_noise(source) 
            audio_listened = self.recognizer.listen(source) 
        try: 
             # try converting it to text 

                rec = self.recognizer.recognize_google(audio_listened)
                return (rec)
            # write the output to the file. 
                return rec
            # catch any errors. 
        except sr.UnknownValueError: 
                print("Could not understand audio") 
