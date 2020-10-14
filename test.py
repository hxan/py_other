import open3d
import numpy as np
import cv2
import time
# 绘制open3d坐标系
axis_pcd = open3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])


# 在3D坐标上绘制点：坐标点[x,y,z]对应R，G，B颜色
points = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])

colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]#红色x轴，绿色y轴，红色z轴
 
test_pcd = open3d.geometry.PointCloud()  # 定义点云
 
test_pcd.points = open3d.utility.Vector3dVector(np.random.rand(100,3))  # 定义点云坐标位置
#test_pcd.colors = open3d.utility.Vector3dVector(colors)  # 定义点云的颜色

vis = open3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(test_pcd)
vis.add_geometry(axis_pcd)

while True:
	test_pcd.points = open3d.utility.Vector3dVector(np.random.rand(100,3))  # 定义点云坐标位置
	vis.update_geometry(test_pcd)
	vis.poll_events()
	vis.update_renderer()
	time.sleep(0.1)

#print(np.asarray(test_pcd.points))
#open3d.visualization.draw_geometries([test_pcd] + [axis_pcd], window_name="Open3D2"	)
#open3d.visualization.draw_geometries([axis_pcd], window_name="Open3D"	)