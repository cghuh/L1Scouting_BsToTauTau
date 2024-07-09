import numpy as np
from sklearn.cluster import DBSCAN
import math

# Custom spherical distance function for DBSCAN
def spherical_distance(point1, point2):
    delta_eta = point1[0] - point2[0]
    delta_phi = math.fmod(point1[1] - point2[1] + 3*math.pi, 2*math.pi) - math.pi  # Wraparound for phi
    delta_z = point1[2] - point2[2]
    return np.sqrt(delta_eta**2 + delta_phi**2 + delta_z**2)

# Generate random 3D points (eta, phi, z)
points = np.array([
    [10.1, 10.1, 10.1],
    [1.0, 2.0, 3.0],
    [8.0, 8.0, 8.0],
    [10.0, 10.0, 10.0],
    [1.1, 2.1, 3.1],
])

# Define the distance threshold and minimum samples for DBSCAN
eps = 1.0
min_samples = 2

# Perform DBSCAN clustering
dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric=spherical_distance)
dbscan.fit(points)

# Get the labels of clusters
labels = dbscan.labels_
num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
clustered_data = np.hstack((points, labels.reshape(-1, 1)))

print(f"Number of clusters found: {num_clusters}")

# Optionally, print the size of each cluster
for cluster_id in set(labels):
    if cluster_id == -1:
        continue  # Skip noise
    cluster_size = sum(labels == cluster_id)
    print(f"Cluster {cluster_id} size: {cluster_size}")

# Print clustered points
print("Clustered Points with Labels:")
for point in clustered_data:
    if not int(point[3] == -1):
        print(f"Point: {point[:3]}, Cluster: {int(point[3])}")