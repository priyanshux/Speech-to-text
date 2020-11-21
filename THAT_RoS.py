#--------------------------------------------------------------------------------------------------------------------- 
# Importing Dependecies 
#---------------------------------------------------------------------------------------------------------------------

import speech_recognition as sr
import pyaudio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from nltk.tokenize import sent_tokenize, word_tokenize 
from plyer import notification 
import string
import time

#--------------------------------------------------------------------------------------------------------------------- 
# Utility Functions 
#---------------------------------------------------------------------------------------------------------------------
def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
      
    response = {"success": True,"error": None,"transcription": None}

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response
#------------------------------------------------------------------------------------------------------------------- 
def perform_this_task(start_time):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    guess = recognize_speech_from_mic(recognizer, microphone)
    if guess["transcription"] == None:
        print("\n\nYou are not speaking...okay then bye")
        perform_this_task(time.time())
    
    time_of_speech = time.time() - start_time - 3   #Subtracting latency
    words_in_speech = sum([i.strip(string.punctuation).isalpha() for i in guess["transcription"].split()])
    rate_of_speech = (words_in_speech*60)/ time_of_speech
    
    #-------------------------------------------------------------------------------------------------------------- 
    # Printing messages to test results. Uncomment the lines below for testing purposes 
    #--------------------------------------------------------------------------------------------------------------
    '''
    print("You said : ",guess["transcription"])
    print("Words in speech : ",words_in_speech) 
    print("Time Taken : ",time_of_speech)      
    print("Rate of Speech: " + str(rate_of_speech) +" WPM.") 
    '''
    perform_this_task(time.time()) #Recursive call with current time
#------------------------------------------------------------------------------------------------------------------- 


perform_this_task(time.time())
