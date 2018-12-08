from PIL import Image
import numpy as np
from math import ceil


def read_image(file_name):
    im = Image.open(file_name)
    matrix = np.array(im)
    mm = np.int_(matrix)
    print(im.format, im.size, im.mode)
    return mm


def shift_image(mm):
    for i in range(len(mm)):
        for j in range(len(mm[0])):
            mm[i][j] = mm[i][j] - 128
    print(mm)
    return mm


def square_matrix(m_matrix, mode):
    row = len(m_matrix)
    col = len(m_matrix[0])
    new_row = ceil(row / mode) * mode
    new_col = ceil(col / mode) * mode
    if new_row > new_col:
        n_matrix = np.zeros((new_row, new_row), dtype=int)
        for i in range(len(m_matrix)):
            for j in range(len(m_matrix[0])):
                n_matrix[i][j] = m_matrix[i][j]
        print(n_matrix)
        return n_matrix
    else:
        n_matrix = np.zeros((new_col, new_col), dtype=int)
        for i in range(len(m_matrix)):
            for j in range(len(m_matrix[0])):
                n_matrix[i][j] = m_matrix[i][j]
        print(n_matrix)
        return n_matrix


def sub_images(new_mm, mode):
    sliced_images = []
    for i in range(0, len(new_mm), mode):
        for j in range(0, len(new_mm[0]), mode):
            sliced_images.append(new_mm[i:i + mode, j:j + mode])
    print(sliced_images[101])
    print(len(sliced_images))

def dct_construct(mode):




def 2dct(sub_images):
    res = []
    for sub_image in sub_images:
        transport = np.transpose(sub_image)
        d = dct_compute(sub_image)
        td = dct_compute(transport)
        res[].append(d * sub_image * td)
    return res



if __name__ == '__main__':
    mm = read_image("Kodak08gray.bmp")
    mm = shift_image(mm)
    n_mm = square_matrix(mm, 8)
    sub_images(n_mm, 8)
    print("Welcome to my image compressor!")
