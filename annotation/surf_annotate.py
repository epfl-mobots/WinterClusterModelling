import numpy as np
import cv2 as cv
import pickle

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

    x = abs(x1-center[0])
    y = abs(y1-center[1])

    print(x1, " ",y1, " ",x2, " ",y2)

    if x>y:
      a = 0.5*(y + np.sqrt(y**2 + 4*x**2))
      b = np.sqrt(a**2 - x**2)
    else:
      b = 0.5*(y + np.sqrt(y**2 + 4*x**2))
      a = np.sqrt(b**2 - y**2)

    axes = (int(a),int(b))
    print(axes)

    # Draw the ellipse
    if action == cv.EVENT_LBUTTONUP:
      cv.ellipse(frame, center, axes, 0, 0, 360, (255,0,0),thickness=-1)
    else :
      cv.ellipse(frame, center, axes, 0, 0, 360, (0,0,255),thickness=-1)

# Create a black image, a window and bind the function to window
cv.namedWindow('image',cv.WINDOW_KEEPRATIO)
cv.setMouseCallback('image',draw_ellipse)

video = cv.VideoCapture("C:/Users/Louise/Desktop/0512(1)-0736_0801.mp4")
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
        cv.imwrite("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/surf/frame_{}.png".format(i),frame)
        #get next frame
        status, frame = video.read()
        blank_frame = frame.copy()
        i=i+1
    if k == ord('q'):
        print(positions)
        f = open("C:/Users/Louise/Documents/EPFL/MA4/Project/data/annotations/surf/tracking.obj", "wb")
        pickle.dump(positions,f)
        f.close()
        break
cv.destroyAllWindows()