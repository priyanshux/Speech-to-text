import speech_recognition as sr
from os import path
import os
from videocaption import convertmp4towav

def getTranscript(path):
    text=[]
    filename=convertmp4towav(path)
    # obtain path to audio file in the same folder as this script
    #AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)

    # use the audio file as the audio source
    r = sr.Recognizer()
    #os.system("substream -v -i video.wav -o video.srt")
    audio_file = sr.AudioFile(filename)
    with audio_file as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition Library
    try:
        text= r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        #return "Could not request results from Speech Recognition service; {0}".format(e)
        return "Could not understand audio"    
        
    return text
