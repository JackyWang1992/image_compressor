from PIL import Image
import numpy as np
from math import sqrt
from math import ceil
from math import cos
from math import pi


class Compressor:
    def __init__(self, file_name, mode):
        self.im = Image.open(file_name)
        # self.mm = np.int_(np.array(self.im))
        self.mm = np.array([[50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                            [50, 50, 50, 50, 200, 200, 200, 200], [50, 50, 50, 50, 200, 200, 200, 200],
                            [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50],
                            [200, 200, 200, 200, 50, 50, 50, 50], [200, 200, 200, 200, 50, 50, 50, 50]])
        self.jpeg_lq_matrix = [[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
                               [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                               [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
                               [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]]
        self.mode = mode
        self.dct_matrix = np.empty((mode, mode), dtype=float)
        self.i_dct_matrix = np.empty((mode, mode), dtype=float)
        # test
        print(self.im.format, self.im.size, self.im.mode)

    def shift_image(self):
        matrix = self.mm
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = matrix[i][j] - 128
        # test
        print(matrix)
        return matrix

    def square_matrix(self):
        mode = self.mode
        m_matrix = self.shift_image()
        row = len(m_matrix)
        col = len(m_matrix[0])
        new_row = ceil(row / mode) * mode
        new_col = ceil(col / mode) * mode
        if new_row > new_col:
            n_matrix = np.zeros((new_row, new_row), dtype=int)
            for i in range(len(m_matrix)):
                for j in range(len(m_matrix[0])):
                    n_matrix[i][j] = m_matrix[i][j]
            # test
            print(n_matrix)
            return n_matrix
        else:
            n_matrix = np.zeros((new_col, new_col), dtype=int)
            for i in range(len(m_matrix)):
                for j in range(len(m_matrix[0])):
                    n_matrix[i][j] = m_matrix[i][j]
            # test
            print(n_matrix)
            return n_matrix

    def sub_images(self):
        mode = self.mode
        new_mm = self.square_matrix()
        sliced_images = []
        for i in range(0, len(new_mm), mode):
            for j in range(0, len(new_mm[0]), mode):
                sliced_images.append(new_mm[i:i + mode, j:j + mode])
        # test
        print(sliced_images[0])
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
        print("dct_matrix")
        print(self.dct_matrix)
        print("i_dct_matrix")
        print(self.i_dct_matrix)

    def compute_dct(self):
        sliced_images = self.sub_images()
        dct_images = []
        for image in sliced_images:
            dct_images.append(np.matmul(np.matmul(self.dct_matrix, image), self.i_dct_matrix))
        print(dct_images)
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
            print(quantization_matrix)
        else:
            quantization_matrix = self.jpeg_lq_matrix

        quantized_images = []
        for image in dct_images:
            quantized_image = np.empty((self.mode, self.mode), dtype=int)
            for i in range(self.mode):
                for j in range(self.mode):
                    quantized_image[i][j] = round(image[i][j] / quantization_matrix[i][j])
            quantized_images.append(quantized_image)
        print(quantized_images)
        return quantized_images

    def zig_zag_matrix(self):
        quantized_images = self.quantize()
        lst = []
        for q_m in quantized_images:
            z = []
            n = self.mode
            for i in range(2 * (n - 1) + 1):
                bound = 0 if i < n else i - n + 1
                for j in range(bound, i-bound + 1):
                    z.append(q_m[j][i - j] if i % 2 != 0 else q_m[i - j][j])
            lst.append(z)
        print(lst)
        return lst


# def dct_construct(mode):
#
#
#
#
# def 2dct(sub_images):
#     res = []
#     for sub_image in sub_images:
#         transport = np.transpose(sub_image)
#         d = dct_compute(sub_image)
#         td = dct_compute(transport)
#         res[].append(d * sub_image * td)
#     return res

if __name__ == '__main__':
    compressor = Compressor("Kodak08gray.bmp", 8)
    compressor.construct_dct()
    compressor.zig_zag_matrix()
    print("Welcome to my image compressor!")
