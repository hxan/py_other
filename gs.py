import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3, origin=[0, 0, 0])

pcd = o3d.io.read_point_cloud("E://10_.ply")

print((pcd.colors) )

plane_model, inliers = pcd.segment_plane(distance_threshold=0.003	,
                                         ransac_n=4000,
                                         num_iterations=10000)

[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([255, 0, 0])


hull, _ = inlier_cloud.compute_convex_hull()
hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
hull_ls.paint_uniform_color((1, 0, 0))





#print(np.asarray(hull_ls.points) )




#print( len ( np.asarray(hull_ls.points) ) )
np_point=np.asarray(hull_ls.points)
print(np_point[1]-np_point[0])
len_np_point=len(np_point)-1

for i in range(0,len_np_point ):
	unit=np_point[i+1]-np_point[i]
	j=0
	while j<1:
		t=np_point[i]+j*unit
		#print(t)
		np_point=np.append(np_point,[t],axis=0)
		#print(len(np_point))
		j+=0.01


test_pcd = o3d.geometry.PointCloud()  # 定义点云
 
test_pcd.points = o3d.utility.Vector3dVector(np_point)  # 定义点云坐标位置



aabb_hull=test_pcd.get_oriented_bounding_box()
aabb_hull.color=(0,0,255)



	#rint(i+1)
#test_pcd.color=(1,0,0)

aabb = inlier_cloud.get_oriented_bounding_box()
print("get_box_points")
print( np.asarray( aabb.get_box_points()) )
aabb.color=(255,0,0)
#print(np.asarray( aabb.get_box_points() ) )

outlier_cloud = pcd.select_by_index(inliers, invert=True)
outlier_cloud.paint_uniform_color([0, 255, 0])

plane_model, inliers_out = outlier_cloud.segment_plane(distance_threshold=0.015,
                                         ransac_n=30,
                                         num_iterations=400)



fuck_cloud = outlier_cloud.select_by_index(inliers_out)
fuck_cloud.paint_uniform_color([0,0,0])


o3d.visualization.draw_geometries([inlier_cloud,outlier_cloud,aabb])
