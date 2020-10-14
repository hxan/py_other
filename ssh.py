# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import time

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE']
tracker_type = tracker_types[6]
if int(minor_ver) < 3:
    print("asas")
    tracker = cv2.TrackerMOSSE_create()
    #tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
            
            
pathIn=''
label_path='/coco.names'
config_path='/yolov3.cfg'
weights_path='/yolov3.weights'
confidence_thre=0.8
nms_thre=0.3

LABELS = open(label_path).read().strip().split("\n")
nclass = len(LABELS)

net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

boxes=None
idxs=None
x_=None
y_=None
bbox=None
img=None
is_track=0
def mouse(event, x, y, flags, param):
    global boxes
    global idxs
    global is_track
    if event==cv2.EVENT_LBUTTONDOWN:
        if len(idxs) > 0:
                for i in idxs.flatten():
                    (w, h) = (boxes[i][2], boxes[i][3])
                    if(x<x_+w and y<y_+h and x>x_ and y>y_):
                        success, img = capture.read()
                        bbox=(x_,y_,x_+w,y_+h)
                        tracker.init(img, bbox)
                        is_track=1
    elif event==cv2.EVENT_RBUTTONDOWN:
        is_track=0
        
        
        
   #print("object is ",x_,y_,x_+w,y_+h)
   #print("mouse is ",x,y)

def yolo_detect():
    global boxes
    global idxs
    global x_
    global y_
    global img
    #tracker.init(img, bbox)
    while(True):
        start = time.time()
        success, img = capture.read()
            
        (H, W) = img.shape[:2]
        

        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        
        
        net.setInput(blob)
        
        layerOutputs = net.forward(ln)
        
        boxes = []
        confidences = []
        classIDs = []
        
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
        
                if confidence > confidence_thre:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
        
                    
                    x_ = int(centerX - (width / 2))
                    y_ = int(centerY - (height / 2))
        
                    boxes.append([x_, y_, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_thre, nms_thre)
        
        if len(idxs) > 0:
            for i in idxs.flatten():
                (w, h) = (boxes[i][2], boxes[i][3])
                    
                cv2.rectangle(img, (x_, y_), (x_ + w, y_ + h), (100,100,100), 2)
                text = '{}: {:.3f}'.format(LABELS[classIDs[i]], confidences[i])
                
                cv2.putText(img, text, (x_, y_-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
        if is_track==1:
            ok, bbox = tracker.update(img)
            p1 = (int(bbox[0]), int(bbox[1]) )
            p2 = ( int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]) )
            cv2.rectangle(img, p1, p2, (255,0,0), 2, 1)
            
        cv2.imshow("result",img)
        end = time.time()
        cv2.waitKey(10)
        
capture = cv2.VideoCapture(0)
cv2.namedWindow('result')
cv2.setMouseCallback('result',mouse)        
yolo_detect()
cv2.waitKey(0);

