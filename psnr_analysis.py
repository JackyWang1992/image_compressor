import numpy as np
import sys
from PIL import Image


def compare_mse(true_mm, test_mm):
    true_mtrx = true_mm
    res_mtrx = test_mm
    true_mtrx.astype(float)
    res_mtrx.astype(float)
    return np.mean(np.square(true_mtrx - res_mtrx), dtype=float)


def compare_psnr(true_mm, test_mm):
    dmin = np.iinfo(np.uint8).min
    dmax = np.iinfo(np.uint8).max
    true_min = np.min(true_mm)
    if true_min > 0:
        data_range = dmax
    else:
        data_range = dmax - dmin

    err = compare_mse(true_mm, test_mm)
    return 10 * np.log10((data_range ** 2) / err)


if __name__ == '__main__':
    img1 = Image.open(sys.argv[1])
    tm = np.int_(np.array(img1))
    img2 = Image.open(sys.argv[2])
    rm = np.int_(np.array(img2))
    print(compare_psnr(tm, rm))
