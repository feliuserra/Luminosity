import re
import numpy as np


def expand_coordinates(coord_str):
    coordinates = {}
    matches = re.findall(r'(?:lat|lng)[0-9.]{0,9}', coord_str)
    if not len(matches) == 2:
        Exception('Invalid coordinates given')

    for m in matches:
        print(str(m))
        coordinates[m[:3]] = float(m[3:])
    return coordinates


def expand_source(src_str):
    if not re.match(r'[a-z]_[0-9_]', src_str):
        Exception('Invalid source given')

    # frequency = re.search(r'^[a-z]{4,5}', src_str).group(0)
    # return str(source)
    return '../data/Version_4_DMSP-OLS_Nighttime_' +\
           'Lights_Time_Series/F182013.v4c_web.stable_lights.avg_vis.tif.npz'


def expand_size(size_str):
    pixel_size = (np.nan, np.nan)
    if re.split(r'_', size_str) != 2:
        Exception('Invalid size given')

    if re.match(r'[0-9.]{0,9}px_[0-9.]{0,9}px', size_str):
        values = [int(v) for v in re.findall(r'[0-9.]{1,9}', size_str)]
        pixel_size = values

    return tuple(pixel_size)
