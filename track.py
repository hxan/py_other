import cv2
import sys
import time
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
is_track=0
tracker=None
def draw_rectangle(event,x,y,flags,param):
    global frame
    global ix, iy
    global bbox
    global is_track
    global tracker
    if event==cv2.EVENT_LBUTTONDOWN:
        print("cv2.EVENT_LBUTTONDOWN")
        ix, iy = x, y
    elif event==cv2.EVENT_LBUTTONUP:
        print("cv2.EVENT_LBUTTONUP")
        bbox=(ix,iy,x-ix,y-iy)
        if int(minor_ver) < 3:
            #tracker = cv2.Tracker_create(tracker_type)
            tracker = cv2.TrackerMOSSE_create()
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            elif tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            elif tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            elif tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            elif tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            elif tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            elif tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            elif tracker_type =='CSRT':
                tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, bbox)
        print(bbox)
        is_track=1
    elif event==cv2.EVENT_MBUTTONDOWN:
        print("cv2.EVENT_bBUTTONUP")
        is_track=0
    
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE','CSRT']
tracker_type = tracker_types[7]
 
if int(minor_ver) < 3:
    tracker = cv2.TrackerMOSSE_create()
    #tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    elif tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type =='CSRT':
        tracker = cv2.TrackerCSRT_create()
print("type is ",tracker_type) 
video = cv2.VideoCapture(1)
cv2.namedWindow('result')
cv2.setMouseCallback('result',draw_rectangle)  
if not video.isOpened():
    print("Could not open video")
    sys.exit() 
timer = time.time()*1000
while True:
    ok, frame = video.read()
    frame=cv2.resize(frame, (1000,700), interpolation = cv2.INTER_AREA)
    if not ok:
        break
    if is_track==1 :
        
        ok, bbox = tracker.update(frame)
        p1 = (int(bbox[0]), int(bbox[1]) )
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    else :
        cv2.putText(frame, "No Detect", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        
    cv2.waitKey(10)
    fps = int( 1000/(time.time()*1000-timer) )
    timer = time.time()*1000
    cv2.putText(frame,str(fps), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)
    
    cv2.imshow("result", frame)
    
    
        
