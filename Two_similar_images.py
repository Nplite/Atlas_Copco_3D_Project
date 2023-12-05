import os
import numpy as np
from plyfile import PlyData, PlyElement
from stl import mesh
from scipy import spatial
from mpl_toolkits.mplot3d import Axes3D

def convert_stl_to_ply(stl_path, output_folder='./Ply_files'):
    """
    Convert an STL file to a PLY file.

    Args:
        stl_path (str): Path to the input STL file.
        output_folder (str): Path to the output folder. Defaults to './Ply_files'.

    Returns:
        str: Path to the generated PLY file.
    """
    # Load STL file
    stl_mesh = mesh.Mesh.from_file(stl_path)

    # Check vertex shape and slice to x,y,z if needed
    if stl_mesh.points.shape[1] > 3:
        vertices = stl_mesh.points[:, :3]
    else:
        vertices = stl_mesh.points

    # Extract and flatten faces
    faces = stl_mesh.vectors.reshape(-1, 3)
    faces = faces.flatten()

    # Nest faces in tuple
    faces = [(face,) for face in faces]

    # Create PlyElements
    vertex = np.array([tuple(vert) for vert in vertices],  
                     dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])

    face = np.array(faces, 
                   dtype=[('vertex_indices', 'i4', (3,))])

    # Create PlyData object
    ply = PlyData([PlyElement.describe(vertex, 'vertex'),
                   PlyElement.describe(face, 'face')])

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Export Ply file
    output_ply_path = os.path.join(output_folder, os.path.splitext(os.path.basename(stl_path))[0] + '.ply')
    ply.write(output_ply_path)
    
    return output_ply_path

# Rest of the code remains the same...


def compare_ply_similarity(ply1_path, ply2_path):
    """
    Compare the similarity between two PLY files.

    Args:
        ply1_path (str): Path to the first PLY file.
        ply2_path (str): Path to the second PLY file.

    Returns:
        float: Cosine similarity as a percentage.
    """
    # Load PLY files
    ply1 = PlyData.read(ply1_path)
    ply2 = PlyData.read(ply2_path)

    # Get vertex coordinates as float arrays
    x1 = ply1['vertex']['x']
    y1 = ply1['vertex']['y']
    z1 = ply1['vertex']['z']
    verts1 = np.stack([x1, y1, z1], axis=-1)

    x2 = ply2['vertex']['x']
    y2 = ply2['vertex']['y']
    z2 = ply2['vertex']['z']
    verts2 = np.stack([x2, y2, z2], axis=-1)

    # Take subset if different sizes
    num_verts = min(len(verts1), len(verts2))
    verts1 = verts1[:num_verts]
    verts2 = verts2[:num_verts]

    # Flatten coordinate arrays
    verts1 = verts1.reshape(-1)
    verts2 = verts2.reshape(-1)

    # Calculate cosine similarity
    cos_sim = 1 - spatial.distance.cosine(verts1, verts2)

    # Convert to percentage
    cosine_similarity = cos_sim * 100

    print("Number of Vertices:", num_verts)
    print("Cosine Similarity:", cos_sim)
    print("Similarity Percentage:", "{:.2f}%".format(cosine_similarity))


if __name__ == "__main__":
    stl_path1 = './match_stl/chair 2209202301.stl'
    stl_path2 = './match_stl/chair2509202303.stl'

    # Validate if input files exist
    if not (os.path.exists(stl_path1) and os.path.exists(stl_path2)):
        print("Error: One or more input files do not exist.")
    else:
        try:
            ply1_path = convert_stl_to_ply(stl_path1)
            ply2_path = convert_stl_to_ply(stl_path2)

            compare_ply_similarity(ply1_path, ply2_path)
        except Exception as e:
            print(f"Error converting STL to PLY: {str(e)}")

