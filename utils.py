import open3d as o3d
import numpy as np
from pathlib import Path
from copy import deepcopy


def print_mesh_info(info):
    """Print the mesh information dictionary."""
    print("Mesh Information:")
    print('number of vertices: ',
          info["vertices"].shape[0], 'number of faces: ', info["faces"].shape[0])
    print("AABB Min Bound:", info["aabb"].get_min_bound())
    print("AABB Max Bound:", info["aabb"].get_max_bound())
    print("AABB Extents:", info["aabb"].get_extent())
    print("AABB Volume:", info["aabb"].volume())
    print("OBB Min Bound:", info["obb"].get_min_bound())
    print("OBB Max Bound:", info["obb"].get_max_bound())
    print("OBB Volume:", info["obb"].volume())
    print("OBB Rotation:\n", info["obb"].R)
    print("OBB Extents:", info["obb_extents"])


def load_mesh(file_path:Path,  vis=False):
    """Load a mesh file using Open3D and calculate  bounding boxes.

    Args:
        file_path (Path): Path to mesh file
        vis (bool, optional): visualization option. Defaults to False.

    Returns:
        mesh in open3d, info (dict): Dictionary containing information about object.
    """
    info = {}
    mesh_o3d = o3d.io.read_triangle_mesh(file_path)

    # get vertices and faces and covert then to numpy arrays
    vertices = np.asarray(mesh_o3d.vertices)
    faces = np.asarray(mesh_o3d.triangles)
    info["vertices"] = vertices
    info["faces"] = faces

    # create a new mesh from the vertices and faces to remove all additional information like color or normals
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)

    # Calculate the axis-aligned bounding box
    aabb = mesh_o3d.get_axis_aligned_bounding_box()
    info["aabb"] = aabb

    # Compute the Oriented Bounding Box (OBB)
    obb = mesh_o3d.get_oriented_bounding_box()
    info["obb"] = obb

    # simple way to get the size of the obb is to rotate them to the axis-aligned bounding box and then get the extents
    obb_rotated = deepcopy(obb)
    obb_rotated.rotate(obb_rotated.R.T)
    # print("OBB Extents:", obb_rotated.get_max_bound()-obb_rotated.get_min_bound())
    info["obb_extents"] = obb_rotated.get_max_bound() - \
        obb_rotated.get_min_bound()
    # simple visualization of the bounding boxes and the mesh
    if vis:
        aabb.color = (1, 0, 0)  # RGB values in the range [0, 1]
        obb.color = (0, 0, 1)
        mesh_o3d.compute_vertex_normals()
        mesh_o3d.paint_uniform_color([0.5, 0.5, 0.5])
        o3d.visualization.draw_geometries(
            [mesh_o3d, aabb, obb], mesh_show_wireframe=True)

    return mesh, info


def scale_mesh(mesh, scale_factor):
    # Create a scaling transformation matrix
    scale_matrix = np.eye(4)  # 4x4 identity matrix
    scale_matrix[:3, :3] *= scale_factor  # Apply scaling to the diagonal

    # Apply the scaling transformation to the mesh
    mesh.transform(scale_matrix)
