import numpy as np
import cv2 as cv
import pickle

positions = []

# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(frame,(x,y),5,(255,0,0),-1)
        positions.append([x,y,i])
# Create a black image, a window and bind the function to window
cv.namedWindow('image',cv.WINDOW_KEEPRATIO)
cv.setMouseCallback('image',draw_circle)

video = cv.VideoCapture("C:/Users/Louise/Desktop/0512(1)-0736_0801.mp4")
status, frame = video.read()
i = 0
while(1):
    cv.imshow('image',frame)
    cv.resizeWindow('image', 960, 720)
    k = cv.waitKey(1) & 0xFF
    if k == ord('n'):
        #save annotated image
        cv.imwrite("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/frame_{}.png".format(i),frame)
        #get next frame
        status, frame = video.read()
        i=i+1
    if k == ord('q'):
        print(positions)
        f = open("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/tracking.obj", "wb")
        pickle.dump(positions,f)
        f.close()
        break
cv.destroyAllWindows()