
import numpy as np
import os
from scipy.spatial.distance import cosine
from plyfile import PlyData

def extract_ply(ply_path):
    # Load PLY data
    ply_data = PlyData.read(ply_path)
    
    # Assuming you have a way to extract relevant features from PLY data
    feature = extract_features_from_ply(ply_data)
    
    return feature / np.linalg.norm(feature)

def extract_features_from_ply(ply_data):
    # Get vertex coordinates as float arrays
    x = ply_data['vertex']['x']
    y = ply_data['vertex']['y']
    z = ply_data['vertex']['z']
    verts = np.stack([x, y, z], axis=-1)

    # Flatten coordinate arrays
    verts = verts.reshape(-1)

    return verts

# Define the directory containing PLY files
ply_directory = "./Ply_files/"

# Create a list of PLY file paths in the directory
ply_files = [os.path.join(ply_directory, ply) for ply in os.listdir(ply_directory) if ply.endswith(".ply")]

# Determine the maximum feature dimensionality
max_feature_dimension = 0
for ply_file in ply_files:
    sample_feature = extract_ply(ply_path=ply_file)
    max_feature_dimension = max(max_feature_dimension, len(sample_feature))

# Initialize an array to store features
all_features = np.zeros(shape=(len(ply_files), max_feature_dimension))

# Extract features from each PLY file and pad them to have the same dimension
for i in range(len(ply_files)):
    feature = extract_ply(ply_path=ply_files[i])
    all_features[i, :len(feature)] = np.array(feature)

# Pad features with zeros to have the same shape
for i in range(len(all_features)):
    all_features[i] = np.pad(all_features[i], (0, max_feature_dimension - len(all_features[i])))

# Extract features from the query PLY file
query_ply_path = "./ply/Roomba drive wheel gear 34-12 tooth.ply"
query = extract_ply(ply_path=query_ply_path)

# Pad query features with zeros to have the same shape as other features
query = np.pad(query, (0, max_feature_dimension - len(query)))

# Calculate cosine similarities between the query and all features
similarities = [1 - cosine(query, feature) for feature in all_features]


# Find the indices of the top 5 most similar PLY files
ids = np.argsort(similarities)[::-1][:3]
alpha = similarities


def closest_to_one(numbers):
    closest = None
    min_difference = float('inf')
    
    for number in numbers:
        difference = abs(1 - number)
        if difference < min_difference:
            min_difference = difference
            closest = number*100
            
    return closest


result = closest_to_one(alpha)

print(result)
print("Similarities: ", similarities )
print("Index Number", ids)
