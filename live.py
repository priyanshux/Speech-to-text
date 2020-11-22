import speech_recognition as sr
from os import path
import time

def getLiveCaption():
    text=[]
    r = sr.Recognizer()
    while(1):
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)#set background threshold noise
            audio = r.record(source,2) #to record for 2 secs
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text=r.recognize_google(audio)
            print(text)
        except sr.UnknownValueError:
            print(" ")#Google Speech Recognition could not understand audio
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
       

        
    return text


#filename=  input("Enter file-name: ")
print("Say something!")
text=getLiveCaption()

