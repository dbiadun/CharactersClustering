import numpy as np
import constants as c


class Image:
    """
    Class used to store single image.
    """

    def __init__(self, img, path):
        """
        Constructor cuts changes all colors to only black/white, cuts off
        white borders and stores size of those borders.
        """
        self.img = img
        self.path = path
        self.proportions = 1

        self.top_border = 0
        self.right_border = 0
        self.bottom_border = 0
        self.left_border = 0

        self._simplify_colors()
        self._reduce_dimension()
        self._cut_borders_off(0)

        self._set_proportions()

        self._cut_borders_off(c.DENSITY_THRESHOLD)

        self.top_black_dists = np.zeros(self.img.shape, int)
        self.right_black_dists = np.zeros(self.img.shape, int)
        self.bottom_black_dists = np.zeros(self.img.shape, int)
        self.left_black_dists = np.zeros(self.img.shape, int)

        self.max_top_black_dist = 0
        self.max_middle_v_black_dist = 0
        self.max_bottom_black_dist = 0
        self.max_left_black_dist = 0
        self.max_middle_h_black_dist = 0
        self.max_right_black_dist = 0

        self.scaled_image_sizes = [5, 10, 20, 40]
        self.scaled_images = []
        self.scaled_masks = []
        self.mask_sizes = []
        self._set_scaled_images_and_masks()

        self._set_black_dists()
        self._normalize_max_black_dists()

    def get_scaled_image(self, y, x):
        # new_img = np.zeros((y, x), int)
        cur_y, cur_x = self.img.shape
        old_y_indices = np.arange(y) * cur_y // y
        # [i * cur_y // y for i in range(y)]
        old_x_indices = np.arange(x) * cur_x // x
        # [j * cur_x // x for j in range(x)]
        new_img = self.img[np.ix_(old_y_indices, old_x_indices)]
        # for i in range(y):
        #     for j in range(x):
        #         new_img[i, j] = self.img[old_y_indices[i], old_x_indices[j]]
        return new_img

    def get_scaled_black_dists(self, y, x):
        top_d = np.zeros((y, x), int)
        right_d = np.zeros((y, x), int)
        bottom_d = np.zeros((y, x), int)
        left_d = np.zeros((y, x), int)
        cur_y, cur_x = self.img.shape

        for i in range(y):
            for j in range(x):
                top_d[i, j] = self.top_black_dists[i * cur_y // y, j * cur_x // x] * y // cur_y
                right_d[i, j] = self.right_black_dists[i * cur_y // y, j * cur_x // x] * x // cur_x
                bottom_d[i, j] = self.bottom_black_dists[i * cur_y // y, j * cur_x // x] * y // cur_y
                left_d[i, j] = self.left_black_dists[i * cur_y // y, j * cur_x // x] * x // cur_x

        return top_d, right_d, bottom_d, left_d

    def get_printable_image(self):
        """
        Makes image ready to print (replaces integer values in array by rgb arrays).
        """
        x, y = self.img.shape
        return_image = np.zeros((x, y, 3), int)

        for i in range(x):
            for j in range(y):
                color = self.img[i][j]
                return_image[i][j] = [color, color, color]

        return return_image

    def _simplify_colors(self):
        """
        Changes all colors to white or black.
        """
        self.img[self.img > c.COLOR_THRESHOLD] = c.WHITE
        self.img[self.img <= c.COLOR_THRESHOLD] = c.BLACK

    def _reduce_dimension(self):
        """
        Replaces rgb arrays by simple integers.
        """
        x, y, _ = self.img.shape
        new_img = np.zeros((x, y), int)
        for i in range(x):
            for j in range(y):
                if (self.img[i][j] == [c.BLACK, c.BLACK, c.BLACK]).all():
                    new_img[i][j] = c.BLACK
                else:
                    new_img[i][j] = c.WHITE

        self.img = new_img

    def _cut_borders_off(self, min_density):
        """
        Cuts off white borders and stores the size of those borders.
        """
        more_to_cut = True
        top_border = 0
        right_border = 0
        bottom_border = 0
        left_border = 0

        while more_to_cut:
            more_to_cut = False

            cut = True
            x_size = self.img.shape[1] - left_border - right_border
            while cut:
                border = self.img[top_border, left_border:self.img.shape[1] - right_border]
                black_count = border[border == c.BLACK].size
                if black_count / x_size <= min_density:
                    top_border += 1
                    more_to_cut = True
                else:
                    cut = False

            cut = True
            y_size = self.img.shape[0] - top_border - bottom_border
            while cut:
                border = self.img[top_border:self.img.shape[0] - bottom_border, - 1 - right_border]
                black_count = border[border == c.BLACK].size
                if black_count / y_size <= min_density:
                    right_border += 1
                    more_to_cut = True
                else:
                    cut = False

            cut = True
            x_size = self.img.shape[1] - left_border - right_border
            while cut:
                border = self.img[- 1 - bottom_border, left_border:self.img.shape[1] - right_border]
                black_count = border[border == c.BLACK].size
                if black_count / x_size <= min_density:
                    bottom_border += 1
                    more_to_cut = True
                else:
                    cut = False

            cut = True
            y_size = self.img.shape[0] - top_border - bottom_border
            while cut:
                border = self.img[top_border:self.img.shape[0] - bottom_border, left_border]
                black_count = border[border == c.BLACK].size
                if black_count / y_size <= min_density:
                    left_border += 1
                    more_to_cut = True
                else:
                    cut = False

        self.top_border += top_border
        self.right_border += right_border
        self.bottom_border += bottom_border
        self.left_border += left_border

        self.img = self.img[top_border:self.img.shape[0] - bottom_border, left_border:self.img.shape[1] - right_border]

    def _set_proportions(self):
        x, y = self.img.shape
        self.proportions = x / y

    def _set_scaled_images_and_masks(self):
        for size in self.scaled_image_sizes:
            img = self.get_scaled_image(size, size)
            mask = img == c.BLACK
            mask_size = img[mask].size
            self.scaled_images.append(img)
            self.scaled_masks.append(mask)
            self.mask_sizes.append(mask_size)

    def _set_black_dists(self):
        y, x = self.img.shape

        for j in range(x):
            dist = 0
            after_first_black = False
            for i in range(y):
                if self.img[i][j] == c.BLACK:
                    self.top_black_dists[i][j] = 0
                    if after_first_black:
                        if dist > self.max_middle_v_black_dist:
                            self.max_middle_v_black_dist = dist
                    else:
                        if 0 < j < x - 1:
                            # Border white sequence shouldn't be taken into consideration
                            if dist > self.max_top_black_dist:
                                self.max_top_black_dist = dist
                        after_first_black = True
                    dist = 0
                else:
                    dist += 1
                    self.top_black_dists[i][j] = dist
            if 0 < j < x - 1:
                if dist > self.max_bottom_black_dist:
                    self.max_bottom_black_dist = dist

        for i in range(y):
            dist = 0
            for j in range(x - 1, -1, -1):
                if self.img[i][j] == c.BLACK:
                    self.right_black_dists[i][j] = 0
                    dist = 0
                else:
                    dist += 1
                    self.right_black_dists[i][j] = dist

        for j in range(x):
            dist = 0
            for i in range(y - 1, -1, -1):
                if self.img[i][j] == c.BLACK:
                    self.bottom_black_dists[i][j] = 0
                    dist = 0
                else:
                    dist += 1
                    self.bottom_black_dists[i][j] = dist

        for i in range(y):
            dist = 0
            after_first_black = False
            for j in range(x):
                if self.img[i][j] == c.BLACK:
                    self.left_black_dists[i][j] = 0
                    if after_first_black:
                        if dist > self.max_middle_h_black_dist:
                            self.max_middle_h_black_dist = dist
                    else:
                        if 0 < i < y - 1:
                            if dist > self.max_left_black_dist:
                                self.max_left_black_dist = dist
                        after_first_black = True
                    dist = 0
                else:
                    dist += 1
                    self.left_black_dists[i][j] = dist
            if 0 < i < y - 1:
                if dist > self.max_right_black_dist:
                    self.max_right_black_dist = dist

    def _normalize_max_black_dists(self):
        y, x = self.img.shape

        self.max_top_black_dist /= y
        self.max_middle_v_black_dist /= y
        self.max_bottom_black_dist /= y
        self.max_left_black_dist /= x
        self.max_middle_h_black_dist /= x
        self.max_right_black_dist /= x
