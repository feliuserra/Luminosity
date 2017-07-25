import copy as cp
import numpy as np
from argparsers import expand_coordinates
from argparsers import expand_source
from argparsers import expand_size


def translate_degrees(coord):
    a, b = str(coord).split(".")
    b = float(b) * (10 ** (2 - len(b)))
    b = b / 60
    return float(a) + b


def as_pixels(coordinates,
              dataset="annual_nl",
              offset=None,
              coordtype='degrees'):
    """
    Takes a dictionary of target coordinates and calculates
    the pixel pixelsation of those coordinates in the reference system
    of the selected image collection.
    """
    img_coord = {
        'annual_nl': {
            'lft': 180,
            'rgt': 180,
            'top': 75,
            'bot': 65
        }
    }.get(dataset)
    img_size = {
        'annual_nl': {
            'x': 16801,
            'y': 43201
        }
    }.get(dataset)
    # if offset is None:
    #     offset = {'x': 0, 'y': 0}

    rates = {
        'x': img_size['x'] / (img_coord['top'] + img_coord['bot']),
        'y': img_size['y'] / (img_coord['lft'] + img_coord['rgt'])
    }
    pixels = (
        (img_coord['top'] - coordinates['lat']) * rates['x'],
        (img_coord['lft'] + coordinates['lng']) * rates['y']
    )
    return np.round(pixels).astype(int)


def load_image(coordinates,
               source,
               size):
    source = expand_source(source)
    print(source)
    coordinates = expand_coordinates(coordinates)
    pixel_size = expand_size(size)
    pixels = as_pixels(coordinates)
    mapped_raster = np.load(source, mmap_mode='r')['arr_0']
    img = cp.deepcopy(mapped_raster[
        pixels[0]-pixel_size[0]:pixels[0]+pixel_size[0],
        pixels[1]-pixel_size[1]:pixels[1]+pixel_size[1]
    ])
    del mapped_raster
    return img


print(load_image('lat1.35_lng103.8', 'year_2000', '200px_200px'))
