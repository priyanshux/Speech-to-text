import pysrt, os
import speech_recognition as sr
import srt
import libass
import ffmpeg
import time 
import soundfile as sf
import pysubs2
def makesrt():
    filename="video.wav"
    subs=[]
    text=""#\"\"\\"
    t1=[]
    #f = open("video.srt","a")
    audio_file = sr.AudioFile(filename)
    i=1
    f = sf.SoundFile(filename)
    total_time=float(format(len(f) / f.samplerate))
    r = sr.Recognizer()
    start_time=0
    end_time=0
    while((i-1)*5<total_time) : 
        start_time=end_time
        end_time=end_time+5
        with audio_file as source:
            audio = r.record(source,offset=(i-1)*5,duration=5)  # read the 5sec audio file
        # recognize speech using Google Speech Recognition Library
        try:
            t1= r.recognize_google(audio)
            text+=str(i)+"\n"+time.strftime('%H:%M:%S', time.gmtime(start_time))+",0 --> "+time.strftime('%H:%M:%S', time.gmtime(end_time))+",0\n"+t1+"\n\n"
            print(t1)
            #text=to_srt(text)
            k=srt.parse(text,ignore_errors=True) 
            subs.append(k)
            #print(k)
        except sr.UnknownValueError:
            print()
        except sr.RequestError as e:
            #return "Could not request results from Speech Recognition service; {0}".format(e)
            print("Could not understand audio : "+e)   
            break
        i=i+1
    #text+="\n\"\"\""
    print(text)
    with open("colorsvideo.srt", "w") as fp:
        fp.write(text)
        fp.close()
    os.system("ffmpeg -i colorsvideo.srt colorsvideo.ass")#ffmpeg -i colorsvideo.srt colorsvideo.ass
    os.system("ffmpeg -i colorsvideo.m4v -vf ass=colorsvideo.ass mysubtitledmovie.m4v")
    #ffmpeg -i colorsvideo.m4v -i colorsvideo.srt -c copy -c:s mov_text subtitledcolorsvideo.m4v
    #f.save('video.srt', encoding='utf-8')
    print(subs)
    return text
print(makesrt())