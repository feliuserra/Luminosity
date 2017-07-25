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
    root = '../data'
    if not re.match(r'[a-z]_[0-9_]*', src_str):
        Exception('Invalid source given')

    freq = re.search(r'^[a-z]{4,5}', src_str).group(0)
    date_parts = [n.lstrip('0') for n in re.findall(r'[0-9]{1,4}', src_str)]
    name = '-'.join(date_parts)
    return '{}/{}/{}/{}.npz'.format(root, 'nightlights', freq, name)


def expand_size(size_str):
    pixel_size = (np.nan, np.nan)
    if not re.match(r'[0-9.]{1,11}px_[0-9.]{1,11}px', size_str):
        Exception('Invalid size given')

    if re.match(r'[0-9.]{0,9}px_[0-9.]{0,9}px', size_str):
        values = [int(v) for v in re.findall(r'[0-9.]{1,9}', size_str)]
        pixel_size = values

    return tuple(pixel_size)
