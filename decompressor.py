import numpy as np
import sys
from math import sqrt
from math import cos
from math import pi
from PIL import Image

"""
this compressor support three quality level:  low (PSNR = 30), medium (PSNR = 40), and high (PSNR = 50)
I use three corresponding luminance quantization matrix to support this three quality levels
by default, the compressor uses medium quality
"""
# the luminance quantization matrix with low-quality: PSNR = 30
low_jpeg_lq_matrix = [[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
                      [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                      [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
                      [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]]
# the luminance quantization matrix with medium-quality: PSNR = 40
medium_jpeg_lq_matrix = [[4, 3, 4, 7, 9, 11, 14, 17], [3, 3, 4, 7, 9, 12, 12, 12],
                         [4, 4, 5, 9, 12, 12, 12, 12], [7, 7, 9, 12, 12, 12, 12, 12],
                         [9, 9, 12, 12, 12, 12, 12, 12], [11, 12, 12, 12, 12, 12, 12, 12],
                         [14, 12, 12, 12, 12, 12, 12, 12], [17, 12, 12, 12, 12, 12, 12, 12]]
# the luminance quantization matrix with high-quality: PSNR = 50
high_jpeg_lq_matrix = [[1, 1, 1, 1, 1, 1, 1, 2], [1, 1, 1, 1, 1, 1, 1, 2],
                       [1, 1, 1, 1, 1, 1, 2, 2], [1, 1, 1, 1, 1, 2, 2, 3],
                       [1, 1, 1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 3, 3, 3],
                       [1, 1, 2, 2, 3, 3, 3, 3], [2, 2, 2, 3, 3, 3, 3, 3]]


class DeCompressor:
    def __init__(self, fname, mode, quality):
        # self.fname = fname.split('.')[0]
        self.fname = fname.split('/')[-1].split('.')[0]
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        self.num_rows = int(content[0].split()[0])
        self.num_cols = int(content[0].split()[1])
        content = content[1:]
        self.zig_zag_list = [lst.split() for lst in content]
        if quality == 0:
            self.jpeg_lq_matrix = low_jpeg_lq_matrix
        elif quality == 2:
            self.jpeg_lq_matrix = high_jpeg_lq_matrix
        else:
            self.jpeg_lq_matrix = medium_jpeg_lq_matrix
        self.mode = mode
        self.dct_matrix = np.empty((mode, mode), dtype=float)
        self.i_dct_matrix = np.empty((mode, mode), dtype=float)
        # test
        # print(self.zig_zag_list[0])

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
        # test
        # print(model_m)
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
        # test
        # print(sub_images)
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
            # test
            # print(quantization_matrix)
        else:
            quantization_matrix = self.jpeg_lq_matrix

        dct_images = []
        for image in sub_images:
            dct_image = np.empty((n, n), dtype=int)
            for i in range(n):
                for j in range(n):
                    dct_image[i][j] = image[i][j] * quantization_matrix[i][j]
            dct_images.append(dct_image)
        # test
        # print(dct_images)
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
        # test
        # print("dct_matrix")
        # print(self.dct_matrix)
        # print("i_dct_matrix")
        # print(self.i_dct_matrix)

    def restore_from_dct(self):
        dct_images = self.restore_from_q()
        sub_images = []
        for image in dct_images:
            restored_image = np.matmul(np.matmul(self.i_dct_matrix, image), self.dct_matrix)
            sub_images.append(restored_image.astype(int))
        # test
        # print(sub_images)
        return sub_images

    def stack_matrix(self):
        rows = self.num_rows
        cols = self.num_cols
        mode = self.mode
        whole_matrix = np.zeros((rows, cols), dtype=int)
        sub_images = self.restore_from_dct()
        for i in range(int(rows / mode)):
            for j in range(int(cols / mode)):
                whole_matrix[i * mode:(i + 1) * mode, j * mode:(j + 1) * mode] = sub_images[i * int(cols / mode) + j]
        # test
        # print(whole_matrix)
        return whole_matrix

    def level_shift(self):
        matrix = self.stack_matrix()
        matrix = matrix + 128
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] < 0:
                    matrix[i][j] = 0
                elif matrix[i][j] > 255:
                    matrix[i][j] = 255
        # test
        # print(matrix)
        return matrix

    def write_to_pic(self):
        matrix = self.level_shift()
        img = Image.fromarray(np.uint8(matrix), 'L')
        img.save(self.fname + '.bmp')

    def scale_lq_mtx(self):
        matrix = self.jpeg_lq_matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = matrix[i][j] * 5
        self.jpeg_lq_matrix = matrix


if __name__ == '__main__':
    print("Welcome to my image decompressor!")
    decompressor = DeCompressor(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    # decompressor.scale_lq_mtx()
    decompressor.construct_dct()
    decompressor.write_to_pic()
