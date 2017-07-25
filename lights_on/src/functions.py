import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import helpers
import argparsers


def load_image(coordinates,
               source,
               size):
    source = argparsers.expand_source(source)
    coordinates = argparsers.expand_coordinates(coordinates)
    pixel_size = argparsers.expand_size(size)
    pixels = helpers.as_pixels(coordinates)
    mapped_raster = np.load(source, mmap_mode='r')['arr_0']
    img = cp.deepcopy(mapped_raster[
        pixels[0]-pixel_size[0]:pixels[0]+pixel_size[0],
        pixels[1]-pixel_size[1]:pixels[1]+pixel_size[1]
    ])
    del mapped_raster
    return img


def plot_image(coordinates,
               source,
               size):
    img = load_image(coordinates, source, size)
    plt.imshow(img)
    plt.show()
