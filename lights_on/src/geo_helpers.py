import numpy as np


def translate_degrees(coord):
    a, b = str(coord).split(".")
    b = float(b) * (10 ** (2 - len(b)))
    b = b / 60
    return float(a) + b


def as_pixels(target_coords,
              imgtype="Version 4 DMSP-OLS Nighttime Lights Time Series",
              offset=None,
              coordtype='degrees'):
    """
    Takes a dictionary of target coordinates and calculates
    the pixel location of those coordinates in the reference system
    of the selected image collection.
    """
    if coordtype == 'degrees':
        print({k: translate_degrees(v) for k, v in target_coords.items()})
    elif coordtype == 'decimals':
        pass
    else:
        raise Exception(
                "Please specify valid coordinate type" +
                "(coordtype=('decimals', 'degrees')")

    img_coord = {
        'Version 4 DMSP-OLS Nighttime Lights Time Series': {
            'lft': 180,
            'rgt': 180,
            'top': 75,
            'bot': 65
        }
    }.get(imgtype)
    img_size = {
        'Version 4 DMSP-OLS Nighttime Lights Time Series': {
            'x': 16801,
            'y': 43201
        }
    }.get(imgtype)
    # if offset is None:
    #     offset = {'x': 0, 'y': 0}

    rates = {
        'x': img_size['x'] / (img_coord['top'] + img_coord['bot']),
        'y': img_size['y'] / (img_coord['lft'] + img_coord['rgt'])
    }
    pixels = (
        (img_coord['top'] - target_coords['lat']) * rates['x'],
        (img_coord['lft'] + target_coords['lng']) * rates['y']
    )
    return np.round(pixels).astype(int)
