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
#              wait_parameter : specifies number of iterations to wait before stopping recording
#              start_time     : specifies time when function is called
#              array_RoS      : Array to store the rate of speech of each iteration
# Returns   -> Array with rate of speech of each iteration
#------------------------------------------------------------------------------------------------------------------- 
def perform_this_task(latency, wait_parameter, start_time,array_RoS):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    guess = recognize_speech_from_mic(recognizer, microphone)
    
    if guess["transcription"] == None:
        print("\n\nYou are not speaking...okay then bye")
        if wait_parameter <= 0:
            return
        else:
            wait_parameter = wait_parameter -1
            perform_this_task(latency, wait_parameter,time.time(),array_RoS)
    
    
    time_of_speech = time.time() - start_time - latency   #Subtracting latency
    words_in_speech = sum([i.strip(string.punctuation).isalpha() for i in guess["transcription"].split()])
    rate_of_speech = (words_in_speech*60)/ time_of_speech
    
    #-------------------------------------------------------------------------------------------------------------- 
    # Printing messages to test results. Uncomment the lines below for testing purposes 
    #--------------------------------------------------------------------------------------------------------------
    '''
    print("You said : ",guess["transcription"])
    print("Words in speech : ", words_in_speech) 
    print("Time Taken : ", time_of_speech)      
    print("Rate of Speech: " + str(rate_of_speech) +" WPM.") # Rate of speech in Words per minute
    '''
    array_RoS.append(rate_of_speech)
    perform_this_task(latency, wait_parameter,time.time(),array_RoS) #Recursive call with current time
    
#--------------------------------------------------------------------------------------------------------------------- 
# Main Function -> Will be called when user hits the start button in RoS Feature
# Returns       -> Average rate of speech & Array with rate of speech of each iteration
#---------------------------------------------------------------------------------------------------------------------
def getRoS():
    array_RoS = list()
    average_RoS = 0
    array_RoS = perform_this_task(time.time())
    for ros in array_RoS:
        average_RoS = average_RoS + ros
        
    average_RoS = average_RoS / len(average_RoS)
    return average_RoS, array_RoS   
    
