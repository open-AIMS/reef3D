#Processing LTMP videos for Structural Complexity

<b>Data</b>: MP4 videos recorded in stereo using GoPro Hero 6 in 4K format. 

<b>Steps:</b>

1.	Split videos into 6 frames per second: For each video run the following code from terminal to extract the frames. `vname` = File name of video, `stime`= time from which to start extracting frames (follow the hh:mm:ss format, e.g., 00:00:05). The final name of frames will be named by `v#`, refering to the number of the video 1 or 2 and `CH`, refering to the Left (LC) or Right (RC) camera. `PATH` is the directory where the videos are contained. 

		  cd PATH
		  ffmpeg -i vname -ss stime -vf fps=6 -q:v 1 v#_%4d_CH.jpg

2.	Open a new Metashape document and save using the reef name, site and transect. 

	> For example:
	> CARTERREEF_Site1Tran1
		  
3.	Import frames into 400 images per chunk into Metashape. The first video would contain slightly more than 400 images from left and right cameras, for most of the cases. If that is the case, upload all images from the first video into a single chunk, even if there are more than 400 images in that one. The same will happen for the last chunk. 
4. Rename every chunk with the exact name of the reef, site #, transect # and section (A, B, C...) 
	> For example: CARTER REEF_Site1Tran1_A
 
4. Estimate image quality for all images in each chunk and disbale images which quality index is less than 0.5. To do this:

	*	Double-clik on each chunk to select it (name highlights in bold).
	*	From the `Photos` pannel list the image details
	* 	Order images by quality and select the ones that are less than 0.5
	*  Click on disable image icon at the top of the pannel.

5.	Add Camera calibration for each chunk:
	*	Double-clik on each chunk to select it (name highlights in bold).
	*	Open camera calibration dialog from Tools/Camera Calibration...
	* 	Import the following calibration file: `GoPro4K_OR.xml`
	*  Enter 3 in Focal lenght field
	*  Hit OK.
	*  Repeat for every chunk.

5.	Run the following batch processing script to process the data:`batch_process_LTMPgopro.xml`. To do this:

	*	Save project
	*	Run batch process from workflow menu
	* 	Open batch process script from `3d_ltmp/scripts/batch_jobs`
	*  Ensure that all chunks are selected for each batch step
	*  Ensure that the checkbox "save after each step" is ticked
	*  Run
	*  A pop-up window should appear asking if processing this task over the network. Click Yes and disconnect once option appear in the next pop-up window
		
7. Once processed (Note:it takes a few hours), for eahc chunk, check the following and fill the Excel spreadsheet accordingly:

	* Model rotation. Rotate if necesary
	* Number of images analigned
	* Quality of Dense reconstruction. Clean up model if necesary.
	* All markers are included. Add markers if necesary
	* Add scale bars. Reference distance = 0.4
	* Estiamtion error
8. Save project
9. Export using the batch script `MS_export_batch.xml`


