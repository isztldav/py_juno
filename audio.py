#!/usr/bin/python

#########  IMPORTS

import sys
import os
import urllib2
import json
import pyaudio
import wave

#########

##########  CONFIG

LANG = 'en-us' #it-it en-us
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

#########


#try:
#    filename = sys.argv[1]
#except IndexError:
#    print 'Usage: transcribe.py <file>'
#    sys.exit(1)

#f = open(filename)

record()

f = open('.testoutput.wav')
audio = f.read()
f.close()

print result(audio)
os.remove(".testoutput.wav")
