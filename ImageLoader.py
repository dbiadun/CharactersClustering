from skimage import io
from Image import Image


class ImageLoader:
    """
    Class used to load images from disk
    """

    @staticmethod
    def load_image(path):
        image_array = io.imread(path)
        return Image(image_array, path)
