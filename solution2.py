from math import sqrt, pi, exp

import matplotlib.pyplot as plt
import numpy as np


def filter(img, std_deviation, kernel_size=5, meanx=0, meany=0):
    img2 = np.zeros_like(img)
    padding = kernel_size // 2
    kernel = np.zeros((kernel_size, kernel_size))

    for k in range(-padding, padding + 1):
        for l in range(-padding, padding + 1):
            d = sqrt((k - meanx) ** 2 + (l - meany) ** 2)
            kernel[k + padding][l + padding] = exp(-(d ** 2) / (2 * std_deviation ** 2)) / (
                    sqrt(2 * pi) * std_deviation)
    kernel /= kernel.sum()

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            sum = 0
            for k in range(-padding, padding + 1):
                for l in range(-padding, padding + 1):
                    x = i + k
                    y = j + l
                    if x < 0:
                        x = -x
                    elif x >= img.shape[0]:
                        x = 2 * img.shape[0] - 2 - x
                    if y < 0:
                        y = -y
                    elif y >= img.shape[1]:
                        y = 2 * img.shape[1] - 2 - y
                    sum += img[x][y] * kernel[k + padding][l + padding]
            img2[i][j] = sum
    return img2


read_path = "" #your path
save_path = "" #your path too
img = plt.imread(read_path)[:, :]
# img[::5, ::5] = 1
img2 = filter(img, std_deviation=5, kernel_size=11, meanx=0, meany=0)  # kernel size should be odd number!!!!
plt.imsave(save_path, img2)
