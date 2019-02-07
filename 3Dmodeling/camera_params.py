import pickle
    
##TODO complete these parameters and link to scripts.
camdict={
    ## GoPro Hero5/6 stereo bar filming in 4k video
    'gopro4k':{
        'dateformat': '%Y:%m:%d %H:%M:%S',
        'cam_dist': 0.4,
        'stereo':True,
        'calfile': '',
        'chunk_size': 200,
        'overlap': 20,
        'lstring': '_LC',
        'overlap_threshold':[0.5,0.7],
        'tol_threshold':80,
        'qual_threshold':0.7},
    ## GoPro Hero5/6 stereo bar filming in 2.7k video, linear FOV
    'gopro2.7k':{
        'dateformat': '%Y:%m:%d %H:%M:%S',
        'cam_dist': 0.4,
        'stereo':True,
        'calfile': 'gopro27k_vid_calibration',
        'chunk_size': 200,
        'overlap': 20,
        'lstring': '_LC',
        'overlap_threshold':[0.5,0.7],
        'tol_threshold':80,
        'qual_threshold':0.7},
    ## GoPro Hero 5/6 stereo bar time-lapse (2Hz) linear FOV 
    'gopro_stills':{
        'dateformat': '%Y:%m:%d %H:%M:%S',
        'cam_dist': 0.4,
        'stereo':True,
        'calfile': "callibration_fisheye.xml",
        'chunk_size': 200,
        'overlap': 20,
        'lstring': '_LC',
        'overlap_threshold':[0.5,0.7],
        'tol_threshold':80,
        'qual_threshold':0.5},
    ## Canon G7x shooting burst mode (4fps) for short transects (5m)
    'G7burst':{
        'dateformat': '%Y:%m:%d %H:%M:%S',
        'cam_dist': '',
        'stereo':False,
        'calfile': 'g7x8photos.xml',
        'chunk_size': 1000,
        'overlap': 0,
        'lstring': '',
        'overlap_threshold':[],
        'tol_threshold':80,
        'qual_threshold':0.5},
    ## Sony RX100 V ing stereo bar, filming in 4k with wide-angle lens
    'RX1004k':{
        'dateformat': '%Y:%m:%d %H:%M:%S',
        'cam_dist': 0.4,
        'stereo':True,
        'calfile': "sony rx100 V.xml",
        'chunk_size': 200,
        'overlap': 20,
        'lstring': '_LC',
        'overlap_threshold':[0.5,0.7],
        'tol_threshold':80,
        'qual_threshold':0.7},
    }

    

with open('/Users/uqmgonz1/Desktop/'+ 'test' + '.pkl', 'wb') as f:
    pickle.dump(camdict, f, pickle.HIGHEST_PROTOCOL)