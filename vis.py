# %%
from pathlib import Path
import open3d as o3d
import numpy as np
from utils import load_mesh, print_mesh_info

# %%
# visualize the mesh with axis-aligned bounding box (red) and oriented bounding box (blue)

# set the model directory
model_dir = Path('./dataset/hammers/model_1/')
initial_mesh_path = model_dir/"object_convex_decomposition.obj"
mesh, info = load_mesh(initial_mesh_path, vis=True)
print_mesh_info(info)


# %%
# visualize the parts of the decomposition in random colors

parts_file = list(model_dir.glob("object_part_*"))
parts = []
for part_file in parts_file:
    parts.append(o3d.io.read_triangle_mesh(part_file))
new_mesh_vis = o3d.geometry.TriangleMesh()

for part in parts:
    vs = np.asarray(part.vertices)
    fs = np.asarray(part.triangles)
    # Create a TriangleMesh object
    current_mesh_vis = o3d.geometry.TriangleMesh()
    current_mesh_vis.vertices = o3d.utility.Vector3dVector(vs)
    current_mesh_vis.triangles = o3d.utility.Vector3iVector(fs)
    current_mesh_vis.paint_uniform_color(np.random.rand(3))
    new_mesh_vis += current_mesh_vis

o3d.visualization.draw_geometries([new_mesh_vis])

# %%
# visualize the labeled point cloud

pcd_labled_file = model_dir/"point_cloud_labeled.ply"
pcd_labeld = o3d.io.read_point_cloud(pcd_labled_file)

o3d.visualization.draw_geometries([pcd_labeld]) # for point cloud visualization
# o3d.visualization.draw_geometries([pcd_labeld, mesh]) # for point cloud visualization with mesh
