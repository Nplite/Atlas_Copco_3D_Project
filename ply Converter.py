import os
import numpy as np
from stl import mesh
from plyfile import PlyData, PlyElement

# Input and output folders 
stl_folder = './match_stl/'
ply_folder = './ply/'

# Loop through STL files
for stl_file in os.listdir(stl_folder):
  if stl_file.lower().endswith('.stl'):
    
    # Full path to files
    stl_path = os.path.join(stl_folder, stl_file)
    ply_path = os.path.join(ply_folder, os.path.splitext(stl_file)[0] + '.ply')
    
    # Load STL file
    print(f'Converting {stl_path}')
    stl_mesh = mesh.Mesh.from_file(stl_path)
    
    # Extract vertices and faces
    stl_verts = stl_mesh.points[:, :3]
    stl_faces = np.reshape(stl_mesh.vectors, (-1, 3))
    
    # Flatten faces to 1D array
    stl_faces = stl_faces.flatten()
    
    # Create PlyElements
    vertex = np.array([tuple(vert) for vert in stl_verts],  
                      dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
                      
    face = np.array(stl_faces,
                  dtype=[('vertex_indices', 'i4', (3,))])
    
    # Create PlyData and write
    ply = PlyData([PlyElement.describe(vertex, 'vertex'),
                   PlyElement.describe(face, 'face')])
                   
    with open(ply_path, 'wb') as ply_file:
      ply.write(ply_file)
      
print('Conversion complete')