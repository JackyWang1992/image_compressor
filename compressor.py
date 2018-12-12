from PIL import Image
import numpy as np
from math import sqrt
from math import ceil
from math import cos
from math import pi
import csv
import sys

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
medium_jpeg_lq_matrix = [[2, 2, 3, 4, 5, 6, 8, 11], [2, 2, 2, 4, 5, 7, 9, 11],
                         [3, 2, 3, 5, 7, 9, 11, 12], [4, 4, 5, 7, 9, 11, 12, 12],
                         [5, 5, 7, 9, 11, 12, 12, 12], [6, 7, 9, 11, 12, 12, 12, 12],
                         [8, 9, 11, 12, 12, 12, 12, 12], [11, 12, 12, 12, 12, 12, 12, 12]]
# the luminance quantization matrix with high-quality: PSNR = 50
high_jpeg_lq_matrix = [[1, 1, 1, 1, 1, 1, 1, 2], [1, 1, 1, 1, 1, 1, 1, 2],
                       [1, 1, 1, 1, 1, 1, 2, 2], [1, 1, 1, 1, 1, 2, 2, 3],
                       [1, 1, 1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 3, 3, 3],
                       [1, 1, 2, 2, 3, 3, 3, 3], [2, 2, 2, 3, 3, 3, 3, 3]]

"""
the matrix for test purpose
"""
test_matrix = np.array([[50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                        [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50]])


class Compressor:
    def __init__(self, file_name, mode, quality):
        self.im = Image.open(file_name)
        self.mm = np.int_(np.array(self.im))
        # choose the quality of compressed pictures
        if quality == 0:
            self.jpeg_lq_matrix = low_jpeg_lq_matrix
        elif quality == 2:
            self.jpeg_lq_matrix = high_jpeg_lq_matrix
        else:
            self.jpeg_lq_matrix = medium_jpeg_lq_matrix

        self.mode = mode
        self.num_rows = 0
        self.num_cols = 0
        self.dct_matrix = np.empty((mode, mode), dtype=float)
        self.i_dct_matrix = np.empty((mode, mode), dtype=float)
        # test
        # print(self.im.format, self.im.size, self.im.mode)

    def shift_image(self):
        matrix = self.mm
        print(matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = matrix[i][j] - 128
        # test
        # print(matrix)
        return matrix

    def square_matrix(self):
        mode = self.mode
        m_matrix = self.shift_image()
        row = len(m_matrix)
        col = len(m_matrix[0])
        new_row = ceil(row / mode) * mode
        new_col = ceil(col / mode) * mode
        n_matrix = np.zeros((new_row, new_col), dtype=int)
        for i in range(len(m_matrix)):
            for j in range(len(m_matrix[0])):
                n_matrix[i][j] = m_matrix[i][j]
        # test
        # print(n_matrix)
        self.num_rows = len(n_matrix)
        self.num_cols = len(n_matrix[0])
        return n_matrix

    def sub_images(self):
        mode = self.mode
        new_mm = self.square_matrix()
        sliced_images = []
        for i in range(0, len(new_mm), mode):
            for j in range(0, len(new_mm[0]), mode):
                sliced_images.append(new_mm[i:i + mode, j:j + mode])
        # test
        # print(sliced_images[0])
        print(len(sliced_images))
        return sliced_images

    def construct_dct(self):
        mode = self.mode
        for i in range(mode):
            for j in range(mode):
                if i == 0:
                    self.dct_matrix[i][j] = sqrt(1.0 / mode) * cos(((2 * j + 1) * i) / (2 * mode) * pi)
                else:
                    self.dct_matrix[i][j] = sqrt(2.0 / mode) * cos(((2 * j + 1) * i) / (2 * mode) * pi)
        self.i_dct_matrix = self.dct_matrix.transpose()
        # print("dct_matrix")
        # print(self.dct_matrix)
        # print("i_dct_matrix")
        print(self.i_dct_matrix)

    def compute_dct(self):
        sliced_images = self.sub_images()
        dct_images = []
        for image in sliced_images:
            dct_images.append(np.matmul(np.matmul(self.dct_matrix, image), self.i_dct_matrix))
        # test
        # print(dct_images)
        return dct_images

    def quantize(self):
        dct_images = self.compute_dct()
        if self.mode == 16:
            quantization_matrix = np.empty((self.mode, self.mode), dtype=int)
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

        quantized_images = []
        for image in dct_images:
            quantized_image = np.empty((self.mode, self.mode), dtype=int)
            for i in range(self.mode):
                for j in range(self.mode):
                    quantized_image[i][j] = round(image[i][j] / quantization_matrix[i][j])
            quantized_images.append(quantized_image)
        # test
        # print(quantized_images)
        return quantized_images

    def zig_zag_matrix(self):
        quantized_images = self.quantize()
        lst = []
        for q_m in quantized_images:
            z = []
            n = self.mode
            for i in range(2 * (n - 1) + 1):
                bound = 0 if i < n else i - n + 1
                for j in range(bound, i - bound + 1):
                    z.append(q_m[j][i - j] if i % 2 != 0 else q_m[i - j][j])
            lst.append(z)
        # test
        # print(lst)
        return lst

    def write_file(self):
        lst = self.zig_zag_matrix()

        with open('out.csv', 'w') as f:
            wr = csv.writer(f, delimiter=' ')
            wr.writerow([self.num_rows, self.num_cols])
            wr.writerows(lst)


if __name__ == '__main__':
    print("Welcome to my image compressor!")
    compressor = Compressor(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    compressor.construct_dct()
    compressor.write_file()
