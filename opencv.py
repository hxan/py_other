  
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
import o3d_inter
x_=5
y_=5
aligned_depth_frame=None
aligned_depth_frame=None
aligned_frames=None
frames=None
str_res_xyz="asas"

def draw(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global x_
        global y_
        global str_res_xyz
        x_=x
        y_=y
        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        distance = aligned_depth_frame.get_distance(x_,y_)
        str_res_xyz = str( rs.rs2_deproject_pixel_to_point(depth_intrin,[x_,y_],distance) )

# Create a pipeline
pipeline = rs.pipeline()


config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

fo = open("temp", "w")

align_to = rs.stream.color
align = rs.align(align_to)
cv2.namedWindow('Example')
cv2.setMouseCallback('Example',draw)

try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Remove background - Set pixels further than clipping_distance to grey
        
	
        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
       # images = np.hstack((bg_removed, depth_colormap))
        
        str_res_xy='('+str(x_)+','+str(y_)+')'

        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        np_point=[[0,0,0]]
        for i in range(0,640):
            for j in range(0,480):
                distance = aligned_depth_frame.get_distance(i,j)
                t = rs.rs2_deproject_pixel_to_point(depth_intrin,[i,j],distance)
                #np_point=np.append(np_point,[t],axis=0)
                fo.write( str(t).strip('[').strip(']')+'\n' )








        

        color_image_ = cv2.putText(color_image, str_res_xy+str_res_xyz, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 25, 255), 2)
        depth_colormap_=cv2.putText(depth_colormap, str_res_xy+str_res_xyz, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 25, 255), 2)

        cv2.imshow('Example', color_image_)
        cv2.imshow('Example__',depth_colormap_)
        cv2.waitKey(1)

finally:
    pipeline.stop()