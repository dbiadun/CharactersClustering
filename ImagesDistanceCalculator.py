import constants as c


# TODO: punishment for different proportions and percentage of blacks,
#  punishment for different distances to black from edges (t/r, b/h, c/e, n/u) or completely different metric
#  based on distances from black in each direction for every point
class ImagesDistanceCalculator:
    """
    Class used to calculate distance between two images.
    """

    @staticmethod
    def calculate_distance(image1, image2):
        img1, img2 = ImagesDistanceCalculator._get_scaled_image_arrays(image1, image2)

        main_distance = ImagesDistanceCalculator._get_main_distance(img1, img2)
        size_distance = ImagesDistanceCalculator._get_size_distance(image1, image2)
        borders_distance = ImagesDistanceCalculator._get_borders_distance(image1, image2)

        return main_distance + 0.001 * (size_distance + borders_distance)

    @staticmethod
    def _get_scaled_image_arrays(image1, image2):
        x1, y1 = image1.img.shape
        x2, y2 = image2.img.shape

        x = max(x1, x2)
        y = max(y1, y2)

        img1 = image1.get_scaled_image(x, y)
        img2 = image2.get_scaled_image(x, y)

        return img1, img2

    @staticmethod
    def _get_main_distance(img1, img2):
        dist1 = img1[(img1 == c.BLACK) & (img2 != c.BLACK)].size / img1[img1 == c.BLACK].size
        dist2 = img2[(img2 == c.BLACK) & (img1 != c.BLACK)].size / img2[img2 == c.BLACK].size
        return dist1 + dist2

    @staticmethod
    def _get_size_distance(image1, image2):
        x1, y1 = image1.img.shape
        x2, y2 = image2.img.shape

        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def _get_borders_distance(image1, image2):
        top = abs(image1.top_border - image2.top_border)
        right = abs(image1.right_border - image2.right_border)
        bottom = abs(image1.bottom_border - image2.bottom_border)
        left = abs(image1.left_border - image2.left_border)

        return top + right + bottom + left
