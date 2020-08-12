# imports
import os                                                                       
from multiprocessing import Pool                                                
import datetime                                                                             
import time
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                     
                      
if __name__ == '__main__':
	    
	  # if playing back wav file
	  duration = '10'  # number of seconds per recording epoch (i.e. chunk of data)
      
      # number of epochs of recording:
	  n_hours = 500
	  n_epochs = int((n_hours*3600)/int(duration))
	  n_epochs = 1 # set it manually

      # miclocations, save file names
	  pos = 'ralph_test'
	  temp = '6'
	  
	  
	  #enter root directory to save data
	  root_dir = os.path.join(r'C:\data\ralph_dan_calibration', pos+temp)
	  #root_dirs = [r'D:\Cohorts\july_19_audio'+pos+temp, r'E:\july_19_video'+pos+temp]
	  print ("ROOT DIRS: ", root_dir)

    		  	  
	  #  ***************** (optional) CALIBRATION AUDIO TEST *************************
	  
	  #move to False if you are not doing audio calibration tes
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

	  # ***************** RECORD ANIMALS*******************
	
	  # make default directories
	  # Make audio directories on Drive D
	  try: 
		  os.mkdir(root_dir)
	  except:
		  print('Warning, directory already exists. Exiting')
		  quit()
	  try:
		  os.mkdir(os.path.join(root_dir,'audio'))
	  except:
		  pass

	  # Make video/timestamp directories on Drive E
	 # try: 
	#	  os.mkdir(root_dirs[1])
	#  except:
	#	  pass
		  
	  try:
		  os.mkdir(os.path.join(root_dir,'video'))
	  except:
		  pass

	  try:
		  os.mkdir(os.path.join(root_dir,'times'))
	  except:
		  pass			
	  
	  # ******************************** EPOCH LOOPS ****************
	  # loop over all epochs requested
	  for epoch in range(n_epochs):
		  	      	  
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
