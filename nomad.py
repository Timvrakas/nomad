import alsaaudio as alsa
import time
import audioop
import math
import RPi.GPIO as GPIO
import wave
import sys
import getopt
import threading


from neopixel import *

lo = 10000
hi = 32000



log_lo = math.log(lo)
log_hi = math.log(hi)

class LEDState(object):
    def __init__(self, value):
        self.value = value
        
    def set(self, value):
        self.value = value
        
    def get(self):
        return self.value

class Lights ( threading.Thread ):
    def __init__ ( self, ledState ):
        self.ledState = ledState
        threading.Thread.__init__ ( self )
        time.sleep(0.001)

    def run ( self ):
        print "Making Lights Blink!"
        strip = Adafruit_NeoPixel(17, 18, 800000, 5, False, 255)
        strip.begin()
        #Main ligtng loop
        while(True):
        
            led = ledState.get()
            print(led)
            
            for i in range(1,11):
                strip.setPixelColor(i, Color(int(led*12.5), 0, 0))
            
            for i in range(11,14):
                strip.setPixelColor(i, Color(int(led*12.5*0.6), int(led*12.5), 0))
                
            for i in range(14,17):
                strip.setPixelColor(i, Color(0, int(led*12.5), 0))
                
            strip.show()
            time.sleep(0.01)


class Play ( threading.Thread ):
    def __init__ ( self, path, ledState ):
        self.path = path
        self.ledState = ledState
        threading.Thread.__init__ ( self )
        time.sleep(0.001)

    def run( self ):
        file = wave.open(path, 'rb')
        card = 'default:CARD=Set'
        device = alsa.PCM(card=card)
        print('%d channels, %d sampling rate\n' % (file.getnchannels(),
                                                   file.getframerate()))
        # Set attributes
        device.setchannels(file.getnchannels())
        device.setrate(file.getframerate())

        # 8bit is unsigned in wav files
        if file.getsampwidth() == 1:
            device.setformat(alsa.PCM_FORMAT_U8)
        # Otherwise we assume signed data, little endian
        elif file.getsampwidth() == 2:
            device.setformat(alsa.PCM_FORMAT_S16_LE)
        elif file.getsampwidth() == 3:
            device.setformat(alsa.PCM_FORMAT_S24_LE)
        elif file.getsampwidth() == 4:
            device.setformat(alsa.PCM_FORMAT_S32_LE)
        else:
            raise ValueError('Unsupported format')
                
        device.setperiodsize(320)
        data = file.readframes(320)
        while data:
            d = audioop.max(data, 2)
            vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
            ledState.set(min(max(int(vu*20),0),20))
            device.write(data)
            data = file.readframes(320)
        led = 0;
        file.close()
        
        
#Main Codez:

ledState = LEDState(0)
Lights(ledState).start()

while(True):
    path = "audio/1.wav"
    Play(path, ledState).start()
    time.sleep(6)

