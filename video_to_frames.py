import cv2
import os
 
 # Create frames folder if it dont't exist
if not os.path.exists("frames"):
    os.makedirs("frames")

def FrameCapture(video_path): 
    vidObj = cv2.VideoCapture(video_path) 
    count = 0
    success = 1
  
    while success:

        success, image = vidObj.read() 
        
        if success:
            cv2.imwrite("frames/frame%d.jpg" %count, image)
            count += 1