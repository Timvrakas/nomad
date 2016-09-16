import alsaaudio as alsa
import time
import audioop
import math
import RPi.GPIO as GPIO
import time
import wave
import sys
import getopt
#from __future__ import print_function

status = 1

lo = 10000
hi = 32000

log_lo = math.log(lo)
log_hi = math.log(hi)

def play(device, f):    

    print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                               f.getframerate()))
    # Set attributes
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())

    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        device.setformat(alsa.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsa.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsa.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsa.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')
		
    status = 1
		
    device.setperiodsize(320)
    data = f.readframes(320)
    while data:
        d = audioop.max(data, 2)
        vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
        teste = chr(ord('a')+min(max(int(vu*20),0),19))
        if teste != 'a':
            print teste
        if d>0:
            #SETGPIO(teste)
            if status:
                status = 0
                print "Song found now playing!"		
        device.write(data)
        data = f.readframes(320)
		
	
print "##############################"
print "# Waiting for a song to play #"
print "##############################"




card = 'default:CARD=Set'
f = wave.open("test.wav", 'rb')
device = alsa.PCM(card=card)
play(device, f)
f.close()



