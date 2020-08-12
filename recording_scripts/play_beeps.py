import matplotlib
#%matplotlib tk

import numpy as np
import datetime 
import cv2
import time

import nidaqmx
import nidaqmx
from nidaqmx.constants import AcquisitionType

import matplotlib.pyplot as plt
import PySpin
#from Specgram.Specgram import Specgram
#from playsound import playsound
import simpleaudio as sa

def play_beeps(duration=10):
    fname = r"C:\Users\cm5635\Downloads\audiocheck.net_sin_7000Hz_0dBFS_.1s.wav"
    #wave_obj = sa.WaveObject.from_wave_read(fname)#from_wave_file("/home/cat/audio.wav")
    wave_obj = sa.WaveObject.from_wave_file(fname)
    play_obj = wave_obj.play()
    #play_obj.wait_done()
    
    #duration = 30
    ctr=1
    pc_time_utc_sec = datetime.datetime.utcnow().timestamp()

    times_click = np.arange(duration)
    times_idx = 0
    times = []
    while True:
        now = datetime.datetime.utcnow().timestamp()

        #if (now -pc_time_utc_sec)> ctr:
        if (now -pc_time_utc_sec)> times_click[times_idx]:
            #ser_led.write(b'0x00')     # trigger camera
            #ser_speaker.write(b'0x00')     # trigger camera
            play_obj = wave_obj.play()
            times.append(now-pc_time_utc_sec)
            #print ("  Done waiting ")
            print ("click time ", times_click[times_idx], " sec")
            #beep(1)
            times_idx+=1            

        if times_idx>=len(times_click):
            break
        if (now -pc_time_utc_sec)> duration:
            break

    print ("Times beeped: ", times)
    #np.savetxt('/mnt/53abab64-8e58-435f-ae3f-45613b0ecb71/may_12_60sectests/time_str_'+\
    #            str(round(np.random.rand(),6))+'.txt',times)
    return times

if __name__ == '__main__':
	duration = 10

	# play speaker sounds
	times = play_beeps(duration)
