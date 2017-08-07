import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import helpers
import argparsers
import seaborn


def load_lights(coordinates,
               source,
               size):
    source = argparsers.expand_source(source)
    coordinates = argparsers.expand_coordinates(coordinates)
    pixel_size = argparsers.expand_size(size)
    pixels = helpers.as_pixels(coordinates, coordtype='decimals') # TODO: specify necessity of decimal coordinates
    mapped_raster = np.load(source, mmap_mode='r')['arr_0']
    img = cp.deepcopy(mapped_raster[
        pixels[0]-int(pixel_size[0]/2):pixels[0]+int(pixel_size[0]/2),
        pixels[1]-int(pixel_size[1]/2):pixels[1]+int(pixel_size[1]/2)
    ])
    del mapped_raster
    return img


def plot_lights(coordinates,
               source,
               size,
               style='bone',
               show_marker=False):
    img = load_lights(coordinates, source, size)
    plt.figure(figsize=(20, 20))
    plt.imshow(img, cmap=style)
    plt.xticks([])
    plt.yticks([])
    if show_marker is True:
        pixel_size = argparsers.expand_size(size)
        plt.plot(pixel_size[0] / 2,
                 pixel_size[1] / 2,
                 'co',
                 mew=8,
                 ms=14)
    plt.show()
