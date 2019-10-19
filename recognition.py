import speech_recognition as sr


parser = argparse.ArgumentParser(description='Split a WAV file at silence.')
parser.add_argument('input_file', type=str, help='The WAV file to split.')
#

args = parser.parse_args()

input_filename = args.input_file
r = sr.Recognizer()
fh = open("recognized.txt", "w+")
with sr.AudioFile(input_filename) as source: 
			# remove this if it is not working 
			# correctly. 
	#r.adjust_for_ambient_noise(source) 
	audio_listened = r.listen(source) 
try: 
    # try converting it to text 
    rec = r.recognize_google(audio_listened) 
    # write the output to the file. 
    print (rec)
    fh.write(rec+". ") 
    fh.close()

# catch any errors. 
except sr.UnknownValueError: 
    print("Could not understand audio") 
