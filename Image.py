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
        self.top_border = 0
        self.right_border = 0
        self.bottom_border = 0
        self.left_border = 0

        self._simplify_colors()
        self._reduce_dimension()
        self._cut_borders_off(0)
        self._cut_borders_off(c.DENSITY_THRESHOLD)

    def get_scaled_image(self, x, y):
        new_img = np.zeros((x, y), int)
        cur_x, cur_y = self.img.shape

        for i in range(x):
            for j in range(y):
                new_img[i, j] = self.img[i * cur_x // x, j * cur_y // y]

        return new_img

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
