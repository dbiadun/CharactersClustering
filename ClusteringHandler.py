import numpy as np
import json
from sklearn.cluster import AgglomerativeClustering

from ImagesDistanceCalculator import ImagesDistanceCalculator
import constants as c


class ClusteringHandler:
    """
    Class used to divide images into clusters
    """

    @staticmethod
    def cluster(images):
        if c.DISTANCES_COMPUTED_YET:
            with open('distances.json', 'r') as fh:
                distances = json.load(fh)
        else:
            distances = ClusteringHandler._compute_distances_matrix(images)
            if c.SAVE_DISTANCES:
                with open('distances.json', 'w') as fh:
                    json.dump(distances.tolist(), fh)

        clustering = AgglomerativeClustering(n_clusters=None, affinity='precomputed', linkage='average',
                                             distance_threshold=c.DISTANCE_THRESHOLD)
        clustering.fit(distances)
        clusters = ClusteringHandler._get_clusters(clustering, images)
        return clusters

    @staticmethod
    def _compute_distances_matrix(images):
        distances = np.zeros((len(images), len(images)), float)
        for i in range(len(images)):
            print(f"Computing distances for {i} image.")
            for j in range(len(images)):
                if i <= j:
                    dist = ImagesDistanceCalculator.calculate_distance(images[i], images[j])
                    distances[i, j] = dist
                    distances[j, i] = dist

        return distances

    @staticmethod
    def _get_clusters(clustering, images):
        clusters = [[] for _ in range(clustering.n_clusters_)]
        for i in range(len(clustering.labels_)):
            cluster_number = clustering.labels_[i]
            clusters[cluster_number].append(images[i])

        return clusters
