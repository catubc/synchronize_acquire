# imports
import numpy as np
import datetime 
import cv2
import time
import os

import PySpin

import sys

def setup_camera():
    print ("SETUP VIDEO RECORDING STAGE #1")

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Get current library version
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, 
                                            version.type, version.build))
    
    return system

def setup2(system, FPS, duration):
    print ("SETUP VIDEO RECORDING STAGE #2")

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()
    cam = cam_list[0]

    # Retrieve TL device nodemap and print device information
    nodemap_tldevice = cam.GetTLDeviceNodeMap()

    # Initialize camera
    cam.Init()

    # Retrieve GenICam nodemap
    nodemap = cam.GetNodeMap()

    # Acquire images
    #acquire_images(cam, nodemap, nodemap_tldevice)

    node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))

    node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')

    acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

    # set the frame rate manually
    cam.AcquisitionFrameRateEnable.SetValue(True)
    cam.AcquisitionFrameRate.SetValue(FPS)

    # check frame rate is correct
    node_acquisition_framerate = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
    framerate_to_set = node_acquisition_framerate.GetValue()
    print ("Frame rate to be set to %dFPS" % framerate_to_set)

    # Set integer value from entry node as new value of enumeration node
    node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

    # set default saving directory

    # set opencv recorder parameters
    height, width, layers = [1280,1024,3]
    size= (height, width)

    # avi compression option
    option = PySpin.H264Option()
    option.frameRate = int(framerate_to_set)
    option.bitrate = 5000000
    option.height = 1024
    option.width = 1280
    
    print ("DONE SETUP CAMERA")
    
    return cam, option, size, framerate_to_set
    
# record video    
def record_video(root_dir, system, FPS, cam, 
				 option, size, start_time,
				 ttl_device):

    print ("STARTING RECORDING")
    try: 
        cam.EndAcquisition()
    except:
        pass

	# make additional directory for particular epoch:
    try:
        os.mkdir(os.path.join(root_dir,'times',start_time))
    except: 
        print ("COULDN'T MAKE DIRECTORY")
		
    try:
        os.mkdir(os.path.join(root_dir,'video',start_time))
    except: 
        print ("COULDN'T MAKE DIRECTORY")
        
	# initialize time stamps for camera internal clock
    times_gpu_clock=[]

	# initialize time stamps for randomized ttl pulse
    ttl_ctr = 0
    ttl_times_requested = np.arange(0,duration, 1)
    #ttl_times_requested = np.float32(np.arange(0,duration, 30))[1:]
   # ttl_times_requested += np.random.rand(ttl_times_requested.shape[0])*30
    
    # save array with actual times based on PC clock
    ttl_times_actual = []
	
	# start a new video file
    cv2_file = os.path.join(root_dir,'video',start_time, start_time+'.avi')
    print ("SAVING VIDEO TO: ", cv2_file)
    out = cv2.VideoWriter(cv2_file,cv2.VideoWriter_fourcc(*'DIVX'), FPS, size)

	# start clock
    start_time_pc = datetime.datetime.utcnow().timestamp()

	# start video acquisition and grab individual video files
    cam.BeginAcquisition()

	# grab individual video frames
    for k in range(int(option.frameRate)*duration):
        image_result = cam.GetNextImage()
		
        time_pc = datetime.datetime.utcnow().timestamp()
		
        time_gpu = image_result.GetTimeStamp()

        times_gpu_clock.append(time_gpu*1E-9)
		
        if k%100==0:
            print("Frame: ", k, "start_time: ", time_gpu)

		# convert image to bgr for saving
        images_avi = image_result.Convert(PySpin.PixelFormat_BGR8)

		# add image to opencv avi file
        out.write(images_avi.GetData().reshape((1024, 1280, 3)))

		# release iamge
        image_result.Release()

        try:
            if (time_pc-start_time_pc)>ttl_times_requested[ttl_ctr]:
                ttl_device.write(b'0x00')     # trigger camera
                print ("Saved TTL time: ", time_pc)
                ttl_times_actual.append(time_pc)
                ttl_ctr+=1            
        except:
            pass    

	# close the video recording
    out.release()

	# close the camera
    cam.EndAcquisition()
    
    # save data

			
	# save GPU frame time stamps
    np.savetxt(os.path.join(root_dir,'times',start_time, start_time+'_frame_times_gpu_clock.txt'),times_gpu_clock, fmt='%f')

    # save ttl pulses on PC clock
    np.savetxt(os.path.join(root_dir,'times',start_time, start_time+'_ttl_times_pc_clock.txt'),ttl_times_actual, fmt='%f')

    # save ttl pulses on PC clock
    np.savetxt(os.path.join(root_dir,'times',start_time, start_time+'_ttl_times_requested.txt'),ttl_times_requested, fmt='%f')
    
    # save starting time of cam acquisition on PC Clock
    np.savetxt(os.path.join(root_dir,'times',start_time, start_time+'_start_time_pc_clock.txt'),[start_time_pc], fmt='%f')
		
		
def setup_serial_port():
	import serial
	ttl_device = serial.Serial(
		port='COM3',
		baudrate = 24000,
		parity='N',
		stopbits=1,
		bytesize=8,
		timeout=1
	)
	
	return ttl_device

# launch 



if __name__ == '__main__':
	# initialize recordings recording
	#root_dir = r"E:\july_8_gerbil2"

	root_dir = sys.argv[1]
	duration = int(sys.argv[2])
	start_time = str(sys.argv[3])
	#n_epochs = int(sys.argv[4])

	FPS = int(25)

	# setup TTL pulse
	ttl_device = setup_serial_port()

	# setup camera stage 1
	system = setup_camera()

	# setup camera stage 2
	cam, option, size, framerate_to_set  = setup2(system, FPS, duration)

	# record video
	record_video(root_dir, system, framerate_to_set, cam, option, size, start_time, ttl_device)
