import numpy as np
import cv2 as cv
import pickle

def terminate():
  print(positions)
  f = open("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/surf_blank/tracking.obj", "wb")
  pickle.dump(positions,f)
  f.close()

positions = []

def draw_ellipse(action, x, y, flags, *userdata):
  # Referencing global variables 
  global p1, p2
  # Mark the top left corner, when left mouse button is pressed
  if action == cv.EVENT_LBUTTONDOWN or action == cv.EVENT_RBUTTONDOWN:
    p1 = [(x,y)]
    # When left mouse button is released, mark bottom right corner
  elif action == cv.EVENT_LBUTTONUP or action == cv.EVENT_RBUTTONUP:
    p2 = [(x,y)]

    x1 = p1[0][0]
    x2 = p2[0][0]
    y1 = p1[0][1]
    y2 = p2[0][1]

    center = ((x1+x2)//2,(y1+y2)//2)
    a = abs(x1-x2)//2
    b = abs(y1-y2)//2
    axes = (a,b)

    # Draw the ellipse
    if action == cv.EVENT_LBUTTONUP:
      cv.ellipse(frame, center, axes, 0, 0, 360, (255,0,0),thickness=-1)
    else :
      cv.ellipse(frame, center, axes, 0, 0, 360, (0,0,255),thickness=-1)

# Create a black image, a window and bind the function to window
cv.namedWindow('image',cv.WINDOW_KEEPRATIO)
cv.setMouseCallback('image',draw_ellipse)

path = "C:/Users/Louise/Documents/EPFL/MA4/Project/video_data/"
vid_files = [path+"hive5_rpi1_day-2201{}.mp4".format(i) for i in range(11,21)]
vid_files = ["C:/Users/Louise/Documents/EPFL/MA4/Project/experimental data/video_data/hive5_rpi1_day-220116.mp4"]

for vf in vid_files:
  print(vf)
  video = cv.VideoCapture(vf)
  amount_of_frames = video.get(cv.CAP_PROP_FRAME_COUNT)
  print(amount_of_frames)
  video.set(cv.CAP_PROP_POS_FRAMES, 0)
  status, frame = video.read()
  blank_frame = frame.copy()

  i = 0
  while(1):
      cv.imshow('image',frame)
      cv.resizeWindow('image', 960, 720)
      k = cv.waitKey(1) & 0xFF
      if k == ord('z'):
          #restore blank version of frame
          frame = blank_frame.copy()
      if k == ord('n'):
          #save annotated image
          #print("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/surf_blank/{}_frame_{}.png".format(vf[87:-4],900*i))
          cv.imwrite("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/surf_blank/{}_frame_{}.png".format(vf[87:-4],900*i),frame)
          i=i+1
          
          #get next frame
          if 900*i < amount_of_frames:
            video.set(cv.CAP_PROP_POS_FRAMES, 900*i)
            status, frame = video.read()
            blank_frame = frame.copy()
          else:
            terminate()
            break
          
      if k == ord('q'):
          terminate()
          break
  cv.destroyAllWindows()