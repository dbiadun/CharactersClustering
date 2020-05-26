from ImageLoader import ImageLoader
from ClusteringHandler import ClusteringHandler
from HTMLCreator import HTMLCreator


class Runner:
    """
    Class used to run the whole clustering.
    """

    @staticmethod
    def run(paths_file):
        images = Runner._load_images(paths_file)
        clustered_images = ClusteringHandler.cluster(images)
        HTMLCreator.create_html('template.html', 'index.html', clustered_images=clustered_images, clusters_count=len(clustered_images))

    @staticmethod
    def _load_images(paths_file):
        paths = []
        with open(paths_file, 'r') as fh:
            for line in fh:
                paths.append(line[:-1])

        paths_list = [ImageLoader.load_image(path) for path in paths[:1000]]
        return paths_list
