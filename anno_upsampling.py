#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:40:24 2022

@author: tgottsch
"""
# import contextlib
# @contextlib.contextmanager
# def tqdm_joblib(tqdm_object):
#     """Context manager to patch joblib to report into tqdm progress bar given as argument"""
#     class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)

#         def __call__(self, *args, **kwargs):
#             tqdm_object.update(n=self.batch_size)
#             return super().__call__(*args, **kwargs)

#     old_batch_callback = joblib.parallel.BatchCompletionCallBack
#     joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
#     try:
#         yield tqdm_object
#     finally:
#         joblib.parallel.BatchCompletionCallBack = old_batch_callback
#         tqdm_object.close()  


if __name__ == "__main__":  
   
  #%%############################################################################
  ### Initialization 
  ###############################################################################
  import datetime
  import numpy as np
  # import gc
  import os  
  import tifffile
  from PIL import Image
  # from joblib import Parallel, delayed
  # import joblib
  # from tqdm import tqdm  
  # #ClearMap path
  # import sys
  # sys.path.append('/home/user/anaconda3/clearmap/ClearMap2')
  # #%% Initialize workspace
  
  # import pyqtgraph as pg
  # print(pg.QtCore.PYQT_VERSION_STR)
  
  # from ClearMap.Environment import *  #analysis:ignore
  
  # #directories and files
  # directory = '/scratch/201205_LSstandardMouse/'
  
  # expression_raw      = 'anno_upscaled_to_rot-stitched.npy'   
  # expression_auto     = '5657_C1-stitched_AF_lv4.npy'  
  
  # ws = wsp.Workspace('CellMap', directory=directory);
  # ws.update(raw=expression_raw, autofluorescence=expression_auto)  
  # ws.info()
  
  # ws.debug = False
  
  # resources_directory = settings.resources_path
  
  # #%%Convert tif files to npy files NECCESSARY!
  # io.convert_files(ws.filename('raw', extension='tif'), extension='npy',
  #                 processes=40, verbose=True);
  
  # #%% Convert npy to tif to load in ImageJ
  # io.convert_files(ws.filename('raw', extension='npy'), extension='tif',
  #                 processes=40, verbose=True);
  
  #%%############################################################################
  ### upscale atlas for full-resolution registration 
  ###############################################################################
  ### check image
  # import cv2
  # imS = cv2.resize(source_mm[0], (800, 600))                # Resize image
  # cv2.imshow("output", imS) 
  directory = '/scratch/201205_LSstandardMouse/'
  slice_tmp_folder    = "/scratch/201205_LSstandardMouse/slice_tmp_folder/"
  resample_tmp_folder = "/scratch/201205_LSstandardMouse/resample_tmp_folder/"
  x, y, z = 5735, 7578, 2581 #matching resolution
  #x, y, z = 466*2, 616*2, 259*2 #double the resolution
  
  # load the source registration file as mm (write protected) [z,y,x]
  source_file = os.path.join(directory, "bspline_annotation_result.1.tif")
  source_mm = tifffile.imread(source_file)
  
  ### 1. STEP: upscale x,y direction and hold z stable
  starttime = datetime.datetime.now()
  # create the final upscale file (just reserves the space on HDD)
  target_file = os.path.join(directory, "anno_upscaled_to_stitched.npy")
  target_mm = np.memmap(target_file, dtype="float32", mode="w+", shape=(259,y,x))
  
  # loop over all slices:
  for i in range(source_mm.shape[0]):
    looptime = datetime.datetime.now()
  
    slice = np.array(Image.fromarray(source_mm[i]).resize((x, y), Image.NEAREST))
    target_mm[i] = slice
    target_mm.flush()
    
    print(f"slice {i} of {len(source_mm[:,:,0])} in {datetime.datetime.now()-looptime}")
  
  # final print  
  print(f"{len(source_mm[:,:,0])} slices upscaled in {datetime.datetime.now()-starttime}")
  # test time = 0:05:18
  
  # import pytiff
  # with pytiff.Tiff(directory + "anno_upscaled_to_stitched.tif", "w", bigtiff=True) as handle:
  #   handle.write(target_mm)
  
  ###############################################################################
  # ##  ### 2. STEP: upscale z direction and hold xy stable
  ###############################################################################
  # # load the source registration file as mm (write protected) [z,y,x]
  source_file = os.path.join(directory, "anno_upscaled_to_stitched.npy")
  source_mm = np.memmap(source_file, dtype="float32", mode="r", shape=(259,y,x))
  
  # create the final upscale file (just reserves the space on HDD)
  # target_file = os.path.join(directory, "anno_upscaled_to_xyz-stitched.npy")
  # target_3d = np.memmap(target_file, dtype="float32", mode="w+", shape=(z,y,x))
  
  target_file = os.path.join(directory, "anno_upscaled_to_rot-stitched.npy")
  target_rot = np.memmap(target_file, dtype="float32", mode="w+", shape=(y,z,x))
  
  source_mm = np.rot90(source_mm, 1, axes=(0,1))
  # target_mm = np.rot90(target_mm, 1, axes=(1,2))
  
  starttime = datetime.datetime.now()
 
  # loop over all slices:
  for i in range(source_mm.shape[0]):
    looptime = datetime.datetime.now()
    
    slice = np.array(Image.fromarray(source_mm[i]).resize((x,z), Image.NEAREST))
    #slice = np.array(Image.fromarray(source_mm[i]).resize((z, x), Image.NEAREST))
    #slice = tifffile.imread(f"{resample_tmp_folder}slice_xy-upscaled_{i}.tif")
    target_rot[i] = slice
    target_rot.flush()
    
    print(f"slice {i} of {len(source_mm[:,:,0])} in {datetime.datetime.now()-looptime}")
  
  target_rot = np.rot90(target_rot, -1, axes=(0,1))
  target_rot.flush()
  
  # final print  
  print(f"{len(source_mm[:,:,0])} slices upscaled in {datetime.datetime.now()-starttime}")
  
  ###############################################################################
  # ##  ### 3. STEP: convert to tif
  ###############################################################################
  tifffile.imsave(directory + 'my_image.tif', target_rot)
  ###############################################################################
  # ## sanity check!
  ###############################################################################
  
  # for i in range(target_rot.shape[0]):
  #   looptime = datetime.datetime.now()
  #   slice_save(i)
  #   print(f"slice {i} of {target_rot.shape[0]} in {datetime.datetime.now()-looptime}")
 
  # def slice_save(i):
  #  #looptime = datetime.datetime.now()
  #  tifffile.imwrite(f"{slice_tmp_folder}slice_{i}.tif", target_rot[i])
  #  #print(f"slice {i} of {target_mm.shape[0]} in {datetime.datetime.now()-looptime}")
 
 # # convert 3d smoothing parallel processing  
  # with tqdm_joblib(tqdm(desc="My calculation", total=target_rot.shape[0])) as progress_bar:
  #  results = Parallel(n_jobs=72)(delayed(slice_save)(i) for i in range(target_rot.shape[0])) 
 
  # ### check image
  # import cv2
  # imS = cv2.resize(target_rot[200], (800, 600))                # Resize image
  # cv2.imshow("output", imS) 
 