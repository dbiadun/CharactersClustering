import os


class ClustersPrinter:
    """
    Class used to print clusters in proper format
    """

    @staticmethod
    def print_clusters_to_file(clustered_images, file_path):
        with open(file_path, 'w') as fh:
            for cluster in clustered_images:
                image_names = [os.path.basename(image.path) for image in cluster]
                fh.write(' '.join(image_names) + '\n')
