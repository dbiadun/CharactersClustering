from skimage import io
from Image import Image


class ImageLoader:
    """
    Class used to load images from disk
    """

    @staticmethod
    def load_images(paths_file):
        paths = []
        with open(paths_file, 'r') as fh:
            for line in fh:
                paths.append(line[:-1])

        paths_list = [ImageLoader._load_single_image(path) for path in paths]
        return paths_list

    @staticmethod
    def _load_single_image(path):
        image_array = io.imread(path)
        return Image(image_array, path)
