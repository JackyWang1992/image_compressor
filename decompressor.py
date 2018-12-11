import numpy as np
import sys


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


if __name__ == '__main__':
    print("Welcome to my image decompressor!")
    decompressor = DeCompressor(sys.argv[1], int(sys.argv[2]))
    decompressor.de_zig_zag()
