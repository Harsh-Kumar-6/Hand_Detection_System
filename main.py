import cv2
import numpy as np
import math
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cam", type=int, default=0, help="camera index")
args = parser.parse_args()

# open the camera
cap = cv2.VideoCapture(args.cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

box = [220, 140, 420, 340]  # virtual box (x1, y1, x2, y2)

# distance thresholds (pixels)
SAFE_DIST = 140
WARN_DIST = 60

# for FPS calculation
prev_time = time.time()
fps = 0

def point_to_box_distance(px, py, box):
    x1, y1, x2, y2 = box
    dx = max(x1 - px, 0, px - x2)
    dy = max(y1 - py, 0, py - y2)
    return math.sqrt(dx*dx + dy*dy)


def nothing(x): pass
cv2.namedWindow("Controls", cv2.WINDOW_NORMAL)
cv2.createTrackbar("SAFE", "Controls", SAFE_DIST, 300, nothing)
cv2.createTrackbar("WARN", "Controls", WARN_DIST, 200, nothing)

cv2.namedWindow("Hand Distance Monitor", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Hand Distance Monitor", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)  # mirror
    h, w = frame.shape[:2]

    # Read trackbars
    SAFE_DIST = cv2.getTrackbarPos("SAFE", "Controls")
    WARN_DIST = cv2.getTrackbarPos("WARN", "Controls")
    if WARN_DIST > SAFE_DIST - 5:
        WARN_DIST = max(5, SAFE_DIST // 3)

    # Convert to HSV & skin color mask
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 30, 60])
    upper = np.array([25, 200, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Mask cleaning
    mask = cv2.GaussianBlur(mask, (7,7), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cx, cy = -1, -1
    state = "No Hand"
    color = (200, 200, 200)

    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        if area > 2000:
            M = cv2.moments(c)
            if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)
                # draw approx contour
                hull = cv2.convexHull(c)
                cv2.drawContours(frame, [hull], -1, (0, 255, 255), 2)

    # Draw virtual box
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    if cx != -1 and cy != -1:
        dist = point_to_box_distance(cx, cy, box)
        if dist > SAFE_DIST:
            state = "SAFE"
            color = (0, 255, 0)
        elif dist > WARN_DIST:
            state = "WARNING"
            color = (0, 255, 255)
        else:
            state = "DANGER"
            color = (0, 0, 255)
            cv2.putText(frame, "DANGER DANGER", (int(w*0.2), 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1.4, (0,0,255), 4, cv2.LINE_AA)
        
        cv2.putText(frame, f"{state}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
        cv2.putText(frame, f"dist:{int(dist)}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # Fps
    cur_time = time.time()
    fps = 0.9*fps + 0.1*(1.0/(cur_time - prev_time)) if (cur_time - prev_time)>0 else fps
    prev_time = cur_time
    cv2.putText(frame, f"FPS: {int(fps)}", (w-140, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    #show the mask for debugging
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    frame_resized = cv2.resize(frame, (640, 480))
    mask_resized  = cv2.resize(mask_bgr, (320, 480)) 

    combined = np.hstack((frame, mask_bgr))

    cv2.imshow("Hand Distance Monitor", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to quit
        break
    if key == ord('s'):
        cv2.imwrite("demo_screenshot.png", frame)
        print("Saved demo_screenshot.png")

cap.release()
cv2.destroyAllWindows()    
