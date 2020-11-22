#--------------------------------------------------------------------------------------------------------------------- 
# Importing Dependecies 
#---------------------------------------------------------------------------------------------------------------------

import time
import string
import pyaudio
import speech_recognition as sr
from plyer import notification 
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from nltk.tokenize import sent_tokenize, word_tokenize 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#--------------------------------------------------------------------------------------------------------------------- 
# Utility Function to convert speech to text
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
# Function  -> perform_this_task(latency, wait_parameter, start_time, array_RoS)
# Arguments -> latency : specifies amount of time to be reduced to compensate start & end time delay during recording
#              wait_parameter : specifies number of consecutives iterations to wait before stopping recording
#              start_time     : specifies time when function is called
#              array_RoS      : Array to store the rate of speech of each iteration
# Returns   -> Array with rate of speech of each iteration
#------------------------------------------------------------------------------------------------------------------- 
def perform_this_task(latency,wait_parameter, start_time,array_RoS):
    wait_count=0
    while 1:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        guess = recognize_speech_from_mic(recognizer, microphone)
        print(guess["transcription"])
        if guess["transcription"] == None:
            print("\n\nYou are not speaking...okay then bye")
            if wait_count < wait_parameter:
                wait_count = wait_count + 1   
                continue
            else:
                return

        wait_count = 0
        time_of_speech = time.time() - start_time - latency   #Subtracting latency
        words_in_speech = sum([i.strip(string.punctuation).isalpha() for i in guess["transcription"].split()])
        rate_of_speech = (words_in_speech*60)/ time_of_speech

        # Printing messages to test results. Comment the lines after final testing.
        print("\nYou said      : ",guess["transcription"])
        print("Words in speech : ", words_in_speech) 
        print("Time Taken      : ", str(round(time_of_speech,2))+" seconds.")      
        print("Rate of Speech  : " + str(round(rate_of_speech,2)) +" WPM.\n") # Rate of speech in Words per minute

        array_RoS.append(round(rate_of_speech,2))
        return array_RoS        

#--------------------------------------------------------------------------------------------------------------------- 
# Main Function -> Will be called when user hits the start button in RoS Feature
# Returns       -> Average rate of speech & Array with rate of speech of each iteration
#---------------------------------------------------------------------------------------------------------------------
def getRoS():
    array_RoS = list()
    average_RoS = 0
    array_RoS = perform_this_task(3,2,time.time(),array_RoS)
    
    if array_RoS != None:
        for ros in array_RoS:
            average_RoS = average_RoS + ros
        average_RoS = average_RoS / len(array_RoS)
        
    return average_RoS, array_RoS  

#---------------------------------------------------------------------------------------------------------------------
getRoS()
