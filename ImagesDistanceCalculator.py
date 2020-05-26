import constants as c

import numpy as np


class ImagesDistanceCalculator:
    """
    Class used to calculate distance between two images.
    """

    @staticmethod
    def calculate_distance(image1, image2):
        main_distance = ImagesDistanceCalculator._get_main_distance(image1, image2)
        size_distance = ImagesDistanceCalculator._get_size_distance(image1, image2)
        borders_distance = ImagesDistanceCalculator._get_borders_distance(image1, image2)
        proportions_distance = ImagesDistanceCalculator._get_proportions_distance(image1, image2)
        # black_dists_distance = ImagesDistanceCalculator._get_black_dists_distance(image1, image2)
        max_blac_dists_distance = ImagesDistanceCalculator._get_max_black_dists_distance(image1, image2)

        return main_distance + 0.001 * (size_distance + borders_distance) + 0.5 * (
                    2 ** (2 * proportions_distance) - 1) + 0.2 * (2 ** (2 * max_blac_dists_distance) - 1)

    @staticmethod
    def _get_scaled_image_arrays(image1, image2):
        y, x = ImagesDistanceCalculator._get_scaled_images_shape(image1, image2)
        img1 = image1.get_scaled_image(y, x)
        img2 = image2.get_scaled_image(y, x)

        return img1, img2

    @staticmethod
    def _get_main_distance(image1, image2):
        img1, img2 = ImagesDistanceCalculator._get_scaled_image_arrays(image1, image2)

        black1 = (img1 == c.BLACK)
        black2 = (img2 == c.BLACK)
        dist1 = img1[black1 & np.invert(black2)].size / img1[black1].size
        dist2 = img2[black2 & np.invert(black1)].size / img2[black2].size
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

    @staticmethod
    def _get_proportions_distance(image1, image2):
        proportions1 = image1.proportions
        proportions2 = image2.proportions
        mx = max(proportions1, proportions2)
        mn = min(proportions1, proportions2)

        return (mx / mn) - 1

    @staticmethod
    def _get_black_dists_distance(image1, image2):
        y, x = ImagesDistanceCalculator._get_scaled_images_shape(image1, image2)
        top_d1, right_d1, bottom_d1, left_d1 = image1.get_scaled_black_dists(y, x)
        top_d2, right_d2, bottom_d2, left_d2 = image2.get_scaled_black_dists(y, x)

        top = np.sum(np.absolute(top_d1 - top_d2))
        right = np.sum(np.absolute(right_d1 - right_d2))
        bottom = np.sum(np.absolute(bottom_d1 - bottom_d2))
        left = np.sum(np.absolute(left_d1 - left_d2))

        top_sum = np.sum(top_d1) + np.sum(top_d2)
        right_sum = np.sum(right_d1) + np.sum(right_d2)
        bottom_sum = np.sum(bottom_d1) + np.sum(bottom_d2)
        left_sum = np.sum(left_d1) + np.sum(left_d2)

        top_distance = top / top_sum if top_sum > 0 else 0
        right_distance = right / right_sum if right_sum > 0 else 0
        bottom_distance = bottom / bottom_sum if bottom_sum > 0 else 0
        left_distance = left / left_sum if left_sum > 0 else 0

        overall_distance = top_distance + right_distance + bottom_distance + left_distance
        return overall_distance

    @staticmethod
    def _get_max_black_dists_distance(image1, image2):
        top = abs(image1.max_top_black_dist - image2.max_top_black_dist)
        middle_v = abs(image1.max_middle_v_black_dist - image2.max_middle_v_black_dist)
        bottom = abs(image1.max_bottom_black_dist - image2.max_bottom_black_dist)
        # left = abs(image1.max_left_black_dist - image2.max_left_black_dist)
        # middle_h = abs(image1.max_middle_h_black_dist - image2.max_middle_h_black_dist)
        # right = abs(image1.max_right_black_dist - image2.max_right_black_dist)

        return top + middle_v + bottom

    @staticmethod
    def _get_scaled_images_shape(image1, image2):
        y1, x1 = image1.img.shape
        y2, x2 = image2.img.shape

        y = max(y1, y2)
        x = max(x1, x2)

        return y, x
