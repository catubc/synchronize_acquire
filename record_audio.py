import matplotlib

import numpy as np
import datetime 
import cv2
import time

import nidaqmx
from nidaqmx.constants import AcquisitionType
import sys

import matplotlib.pyplot as plt
import PySpin
import simpleaudio as sa
import os

def record_audio(root_dir, duration, start_time):

	# make additional directory for particular epoch:
    try:
        os.mkdir(os.path.join(root_dir,'audio',start_time))
    except: 
        print ("COULDN'T MAKE DIRECTORY")
        
    fname_out = os.path.join(root_dir,'audio',start_time, start_time+'_audio')
    print ("Saving to: ",fname_out)
    #location = 'animals'
    #sample_time = 60*10  # units = seconds
    #s_freq = 250000
    s_freq = 125000
    print (s_freq)
    print ("Location: ", root_dir)
    num_samples = duration*s_freq
    dt = 1/s_freq

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
        task.ai_channels.add_ai_voltage_chan("Dev1/ai4")

        task.timing.cfg_samp_clk_timing(s_freq,
                                       sample_mode = AcquisitionType.CONTINUOUS)
        #nidaqmx._task_modules.channels.ai_channel.AIChannel.ai_max = 3.3
        #nidaqmx._task_modules.channels.ai_channel.AIChannel.ai_min = -3.3
        #print ("Voltages: ", task.ai_channels.all.ai_max, task.ai_channels.all.ai_min)
        
        # MEMORY LEAK BUG ISSUE; Cat discussing with NI
        data1 = task.read(number_of_samples_per_channel=num_samples, timeout = nidaqmx.constants.WAIT_INFINITELY)
        print ("Finished audio acquisition")

    #data1=np.array(data1)
    #print (data1.shape)
    for k in range(len(data1)):
       np.save(fname_out+"_mic_"+str(k), data1[k])

if __name__ == '__main__':
	
	root_dir = sys.argv[1]
	duration = int(sys.argv[2])
	start_time = str(sys.argv[3])
	print('Record audio root directory name: '+ root_dir)
	
	record_audio(root_dir, duration, start_time)

