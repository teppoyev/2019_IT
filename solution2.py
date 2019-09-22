from math import sqrt, pi, exp

import matplotlib.pyplot as plt
import numpy as np


def filter(img, std_deviation, kernel_size = 5, meanx = 0, meany = 0):
    img2 = np.zeros_like(img)
    padding = kernel_size // 2
    kernel = np.zeros((kernel_size, kernel_size))

    for l in range (-padding, padding + 1):
        for k in range (-padding, padding + 1):
            d = sqrt((l - meanx) ** 2 + (k - meany) ** 2)
            kernel[l + padding][k + padding] = exp(-(d ** 2) / (2 * std_deviation ** 2)) / (
                    sqrt(2 * pi) * std_deviation)
    kernel /= kernel.sum()

    for i in range(img.shape[0]):
        if i < padding or i >= img.shape[0] - padding:
            for j in range(img.shape[1]):
                img2[i][j] = img[i][j]
        else:
            for j in range(img.shape[1]):
                if j < padding or j >= img.shape[1] - padding:
                    img2[i][j] = img[i][j]
                else:
                    sum = 0
                    for l in range(-padding, padding + 1):
                        for k in range(-padding, padding + 1):
                            sum += img[i + l][j + k] * kernel[l + padding][k + padding]
                    img2[i][j] = sum
    return img2


img = plt.imread("D:\\Users\\Darth_60cx3gr\\Pictures\\Lenna.png")[:, :]
#img[::5, ::5] = 1
img2 = filter(img, std_deviation = 5, kernel_size = 11, meanx = 3, meany = 0) #kernel size should be odd number!!!!
plt.imsave("D:\\Users\\Darth_60cx3gr\\Pictures\\Lenna2.png", img2)
