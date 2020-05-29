import sys

from ImageLoader import ImageLoader
from ClusteringHandler import ClusteringHandler
from HTMLCreator import HTMLCreator
import constants as c

if len(sys.argv) < 2:
    print("Please pass a path to a file containing image paths list")
else:
    paths_file = sys.argv[1]
    images = ImageLoader.load_images(paths_file)
    clustered_images = ClusteringHandler.cluster(images)
    HTMLCreator.create_html(c.HTML_TEMPLATE, c.HTML_OUTPUT, clustered_images=clustered_images,
                            clusters_count=len(clustered_images))

