import cv2
 
def FrameCapture(): 
    
    vidObj = cv2.VideoCapture() 
    
    count = 0
    
    success = 1
  
    while success: 

        success, image = vidObj.read() 
  
        cv2.imwrite("frames%d.jpg" % count, image)
  
        count += 1
            
# if __name__ == '__main__': 

#     FrameCapture("bad_apple.mp4")