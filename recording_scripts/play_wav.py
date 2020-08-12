import matplotlib
#%matplotlib tk

import numpy as np
import datetime 
import cv2
import time

import nidaqmx
import nidaqmx
from nidaqmx.constants import AcquisitionType
import sys

import matplotlib.pyplot as plt
import PySpin
import os

#import simpleaudio as sa
import playsound

def play_beeps(duration, root_dir, wav_fname, start_time):
    #wav_fname = r"C:\Users\cm5635\Downloads\audiocheck.net_sin_7000Hz_0dBFS_.1s.wav"
    #wave_obj = sa.WaveObject.from_wave_read(fname)#from_wave_file("/home/cat/audio.wav")
    #wav_fname = os.path.join('E:/audiocheck.net_sin_7000Hz_0dBFS_.1s.wav')
    
    #wave_obj = sa.WaveObject.from_wave_file(wav_fname)
    #play_obj = wave_obj.play()
    playsound.playsound(wav_fname)
    ctr=1

    pc_time_utc_sec = datetime.datetime.utcnow().timestamp()

    times_click = np.arange(duration)
    print ("TIMES CLICKK", times_click)
    times_idx = 0
    times = []
    while True:
        now = datetime.datetime.utcnow().timestamp()

        #if (now -pc_time_utc_sec)> ctr:
        if (now -pc_time_utc_sec)> times_click[times_idx]:
            #ser_led.write(b'0x00')     # trigger camera
            #ser_speaker.write(b'0x00')     # trigger camera
            #play_obj = wave_obj.play()
            playsound.playsound(wav_fname)

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
    np.savetxt(os.path.join(root_dir, 'times',start_time+'_wav_times.txt'),times)
    return times

if __name__ == '__main__':
		
	root_dir = sys.argv[1]
	duration = int(sys.argv[2])
	wav_fname = str(sys.argv[3])
	start_time = str(sys.argv[4])

	# play speaker sounds
	times = play_beeps(duration, root_dir, wav_fname, start_time)
