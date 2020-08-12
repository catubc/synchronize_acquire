# imports
import os                                                                       
from multiprocessing import Pool                                                
import datetime                                                                             
import time
                               

# call this function with each individual core of multiprocessing pool
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                     
# main code to run                 
if __name__ == '__main__':
	    
	  ''' Setup recording of video  + audio for a set # of epochs.
	      Each epoch is specified in seconds (Note: do not record longer than 3600 seconds due to memory issues
	  '''  
	    
	  # duration of a single epoch of recording
	  duration = '10'  # number of seconds per recording epoch (i.e. chunk of data)
      
      # number hours of recording requested; e.g. 3 weeks continous ~- 500 hours;
      # the scripts can always be stopped by force (ctrl-C)
	  n_hours = 500
	  
	  # compute the number of epochs required given each epoch duration and the total # of hours needed
	  n_epochs = int((n_hours*3600)/int(duration))
	  
	  # overwrite n_epochs for testing purposes and calibration testing
	  n_epochs = 1 # set it manually

      # use these as subdirectories when running many tests in a row
	  pos = 'ralph_test'
	  temp = '6'
	  
	  
	  # enter root directory to save data
	  # PLEASE NOTE: This main part of the root directory must be created manually
	  # 	         the pos+temp parts will be added automatically in each run
	  root_dir = os.path.join(r'C:\data\ralph_dan_calibration', pos+temp)
	  print ("ROOT DIRS: ", root_dir)

    		  	  
	  #  ***************** (optional) CALIBRATION AUDIO TEST *************************
	  #  This code is used to run calbiration tests of audio
	  # set flag to False if not doing audio calibration tests
	  if True:
	      n_epochs = 1
	      
		  #temp = '20000Hz'
		  #temp = 'USV_6'
		  #temp = 'USV_9'
		  #temp = 'USV_10'
		  #temp = 'USV_17'

		  # TONES
	      wav_fname = os.path.join(r"C:\data\data\waves\audiocheck.net_sin_7000Hz_0dBFS_.1s.wav")
		  #wav_fname = os.path.join(r"C:\data\data\waves\audiocheck.net_sin_20000Hz_0dBFS_.1s.wav")

		  # USVs
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-4_11_49_32_007766_snippet_6.wav"
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-4_11_49_32_007766_snippet_9_7Khz_clean.wav"
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-4_11_49_32_007766_snippet_10_harmonics.wav"
		  #wav_fname = r"C:\data\data\waves\USVs\tests\2020-3-15_03_51_56_415333_snippet_17.wav"

	  # ***************** MAKE ALL REQUIRED DIRECOTIRES ******************
	
	  # make default directories
	  # Make audio directories on Drive D
	  try: 
		  os.mkdir(root_dir)
	  except:
		  print('Warning, directory already exists. Exiting')
		  quit()
		  
	  # make audio directory	  
	  try:
		  os.mkdir(os.path.join(root_dir,'audio'))
	  except:
		  pass

	  # make video directory
	  try:
		  os.mkdir(os.path.join(root_dir,'video'))
	  except:
		  pass

      # make time stamp directory
	  try:
		  os.mkdir(os.path.join(root_dir,'times'))
	  except:
		  pass			
	  
	  # ******************************** EPOCH LOOPS ****************
	  # loop over all epochs requested
	  for epoch in range(n_epochs):

		  # grab real time of start of each epoch and convert to human readable directory
		  start_time = datetime.datetime.utcnow()
		  start_time = start_time - datetime.timedelta(hours=4)
		  start_time = start_time.strftime('%Y-%m-%d %H:%M:%S.%f').replace(" ", "_").replace(":","_").replace("-","_").replace(".","_")

		  print ("")
		  print ("")
		  print ("")
		  	  
		  print ("RECORDING EPOCH # :", epoch, " / ", n_epochs, "START TIME: ", start_time, "  duration: ", duration,  " sec")
		  processes = (
			### #r'c:\data\record_multiple_streams\play_beeps2.py'+" "+root_dir+ " " + duration,
			#r'c:\data\record_multiple_streams\ttl_pulse.py'+" "+root_dir+ " " + duration+" "+wav_fname+" "+start_time,
			#r'c:\data\record_multiple_streams\play_wav.py'+" "+root_dir+ " " + duration+" "+wav_fname+" "+start_time,
			r'c:\data\record_multiple_streams\record_audio.py'+" "+root_dir+ " " + duration+" "+start_time,
			r'c:\data\record_multiple_streams\record_video.py'+" "+root_dir+ " " + duration+" "+start_time)
			
		  with Pool(3) as pool:
			  res = pool.map(run_process, processes)
		
		  pool.close
		  
		  time.sleep(1)
		  
		  print ("")
		  print ("")
		  print ("")
