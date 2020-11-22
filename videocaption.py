import moviepy.editor as mp
import speech_recognition as sr
#from speech2text import getTranscript
# Insert Local Video File Path
def convertmp4towav(path) :
    clip = mp.VideoFileClip(path)

    # Insert Local Audio File Path
    clip.audio.write_audiofile("video.wav",codec='pcm_s16le')

    # initialize the recognizer
    return "video.wav"