#!/usr/bin/python

# http://www.chromium.org/developers/how-tos/api-keys
# https://pypi.python.org/pypi/speech/0.5.2  speech
# http://stackoverflow.com/questions/19828332/how-to-embed-google-speech-to-text-api-in-python-program
# https://people.csail.mit.edu/hubert/pyaudio/
# https://pypi.python.org/pypi/SpeechRecognition/
# https://github.com/trakons/py_juno/blob/master/audio.py

#########  IMPORTS

import sys
import os
import urllib2
import json

## record
import pyaudio
import wave

## speech
import pyttsx

#########

##########  CONFIG

LANG = 'en-US' #it-IT en-US
ENCODING = 'l16' # x-flac l16
RATE = '16000' #16000
APIKEY = 'AIzaSyBHvqYmj-7GZFF-9r-8jZMDxdvyVhh7khg'

APILINK = 'https://www.google.com/speech-api/v2/recognize'
OUTPUT = 'json'

#########

#########  FUNCTIONS

def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = ".testoutput.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def result(datav):
    req = urllib2.Request(''+APILINK+'?output='+OUTPUT+'&lang='+LANG+'&key='+APIKEY+'', data=datav, headers={'Content-type': 'audio/'+ENCODING+'; rate='+RATE+''})
    try:
        ret = urllib2.urlopen(req)
    except urllib2.URLError:
        print "Error Transcribing Voicemail"
        sys.exit(1)
        
    try:
        #print ret.read()
        #exit(1)
        return json.loads(ret.read().split(chr(10))[1])['result'][0]['alternative'][0]['transcript']
    except ValueError:
        print 'Decoding JSON has failed'
        sys.exit(1)

def logo():
    print """
                    <-. (`-')_            
              .->      \( OO) )     .->   
   <-.--.,--.(,--.  ,--./ ,--/ (`-')----. 
 (`-'| ,||  | |(`-')|   \ |  | ( OO).-.  '
 (OO |(_||  | |(OO )|  . '|  |)( _) | |  |
,--. |  ||  | | |  \|  |\    |  \|  |)|  |
|  '-'  /\  '-'(_ .'|  | \   |   '  '-'  '
 `-----'  `-----'   `--'  `--'    `-----' 
        ~ By Trakons
    """

def speech(txt):
    engine = pyttsx.init()
    engine.say(txt)
    engine.runAndWait()

#########


#try:
#    filename = sys.argv[1]
#except IndexError:
#    print 'Usage: transcribe.py <file>'
#    sys.exit(1)

#f = open(filename)


logo()
record()

f = open('.testoutput.wav')
#f = open ('hello16bit.wav')
audio = f.read()
f.close()

#print result(audio)
data = result(audio)
print '\nYou say: ',
print data
print '\nNow i try to repeat...'
speech(data)
os.remove(".testoutput.wav")
