import matplotlib

import numpy as np
import datetime
import time
import datetime
import serial
import os

import sounddevice as sd
import sys

import serial
ser_speaker = serial.Serial(
    port='COM3',
    baudrate = 24000,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

# launch 

def send_ttl_pulse(duration, isi, root_dir, epoch):
    ctr=1
    pc_time_utc_sec = datetime.datetime.utcnow().timestamp()

    times_click = np.arange(0,duration,isi)
    times_idx = 0
    times = []
    while True:
        now = datetime.datetime.utcnow().timestamp()

        #if (now -pc_time_utc_sec)> ctr:
        if (now -pc_time_utc_sec)> times_click[times_idx]:
            #ser_led.write(b'0x00')     # trigger camera
            ser_speaker.write(b'0x00')     # trigger camera
            times.append(now-pc_time_utc_sec)
            #print ("  Done waiting ")
            print ("click time ", times_click[times_idx], " sec")
            #beep(1)
            times_idx+=1            

        if times_idx>=len(times_click):
            break
        if (now -pc_time_utc_sec)> duration:
            break

    print ("Times clicked: ", times)

    np.savetxt(os.path.join(root_dir,'times',"ttl_times_"+str(epoch).zfill(5)+".txt"),times, fmt="%s")
   
root_dir = sys.argv[1]
print ("root_dir :" , root_dir)
duration = int(sys.argv[2])
print ("duration :" , duration)

isi = 1  # inter beep interval

epoch=0

send_ttl_pulse(duration, isi, root_dir, epoch)
