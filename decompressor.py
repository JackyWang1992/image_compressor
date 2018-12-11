import numpy as np
import sys
from math import sqrt
from math import ceil
from math import cos
from math import pi


class DeCompressor:
    def __init__(self, fname, mode):
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        self.zig_zag_list = [lst.split() for lst in content]
        # self.mm = np.array([[50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
        #                     [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
        #                     [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
        #                     [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50]])
        self.jpeg_lq_matrix = [[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
                               [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                               [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
                               [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]]
        self.mode = mode
        self.dct_matrix = np.empty((mode, mode), dtype=float)
        self.i_dct_matrix = np.empty((mode, mode), dtype=float)
        # test
        print(self.zig_zag_list[0])

    def zig_zag_model(self):
        model_m = np.empty((self.mode, self.mode), dtype=int)
        index = -1
        n = self.mode
        for i in range(2 * (n - 1) + 1):
            bound = 0 if i < n else i - n + 1
            for j in range(bound, i - bound + 1):
                index = index + 1
                if i % 2 != 0:
                    model_m[j, i - j] = index
                else:
                    model_m[i - j, j] = index
        print(model_m)
        return model_m

    def de_zig_zag(self):
        zz_list = self.zig_zag_list
        model_lst = self.zig_zag_model()
        sub_images = []
        n = self.mode
        for lst in zz_list:
            mtrx = np.empty((n, n), dtype=int)
            for i in range(n):
                for j in range(n):
                    mtrx[i][j] = lst[model_lst[i][j]]
            sub_images.append(mtrx)
        print(sub_images)
        return sub_images

    def restore_from_q(self):
        sub_images = self.de_zig_zag()
        n = self.mode
        if n == 16:
            quantization_matrix = np.empty((n, n), dtype=int)
            for i in range(8):
                for j in range(8):
                    quantization_matrix[2 * i][2 * j] = self.jpeg_lq_matrix[i][j]
                    quantization_matrix[2 * i + 1][2 * j] = self.jpeg_lq_matrix[i][j]
                    quantization_matrix[2 * i][2 * j + 1] = self.jpeg_lq_matrix[i][j]
                    quantization_matrix[2 * i + 1][2 * j + 1] = self.jpeg_lq_matrix[i][j]
            print(quantization_matrix)
        else:
            quantization_matrix = self.jpeg_lq_matrix

        dct_images = []
        for image in sub_images:
            dct_image = np.empty((n, n), dtype=int)
            for i in range(n):
                for j in range(n):
                    dct_image[i][j] = image[i][j] * quantization_matrix[i][j]
            dct_images.append(dct_image)
        print(dct_images)
        return dct_images

    def construct_dct(self):
        mode = self.mode
        for i in range(mode):
            for j in range(mode):
                if i == 0:
                    self.dct_matrix[i][j] = sqrt(1.0 / mode) * cos(((2 * j + 1) * i) / (2 * mode) * pi)
                else:
                    self.dct_matrix[i][j] = sqrt(2.0 / mode) * cos(((2 * j + 1) * i) / (2 * mode) * pi)
        self.i_dct_matrix = self.dct_matrix.transpose()
        print("dct_matrix")
        print(self.dct_matrix)
        print("i_dct_matrix")
        print(self.i_dct_matrix)


if __name__ == '__main__':
    print("Welcome to my image decompressor!")
    decompressor = DeCompressor(sys.argv[1], int(sys.argv[2]))
    decompressor.restore_from_q()
    decompressor.construct_dct()
