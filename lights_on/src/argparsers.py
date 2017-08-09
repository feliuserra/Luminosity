import re
import numpy as np


def expand_coordinates(coord_str):
    coordinates = {}
    matches = re.findall(r'((?:n|s)[0-9.]{0,9}|(?:e|w)[0-9.]{0,9})',
                         coord_str,
                         re.IGNORECASE)
    if not len(matches) == 2:
        raise Exception('Invalid coordinates given')

    for m in matches:
        if re.match(r'(n|s)', m[0], re.IGNORECASE):
            coordinates['lat'] = float(m[1:])
            if re.match(r's', m[0], re.IGNORECASE):
                coordinates['lat'] = - coordinates['lat']
        elif re.match(r'(e|w)', m[0], re.IGNORECASE):
            coordinates['lng'] = float(m[1:])
            if re.match(r'w', m[0], re.IGNORECASE):
                coordinates['lng'] = - coordinates['lng']
        else:
            raise Exception('Coordinate "{}" not understood'
                            .format(m))
    return coordinates


def expand_source(src_str):
    root = '../data'
    if not re.match(r'[a-z]_[0-9_]*', src_str):
        Exception('Invalid source given')

    freq = re.search(r'^[a-z]{4,5}', src_str).group(0)
    date_parts = [n.lstrip('0') for n in re.findall(r'[0-9]{1,4}', src_str)]
    name = '-'.join(date_parts)
    return '{}/{}/{}/{}.npz'.format(root, 'nightlights', freq, name)


def expand_dataset_source_path(dtst_str, root_path='../data'):
    return '{}/{}/'\
           .format(root_path, 'nightlights') + '{}/{}.npz'


def expand_dates_string(dt_str):
    if dt_str == 'all':
        return ['1993', '2013']
    else:
        raise Exception('Invalid dates')


def expand_size(size_str):
    pixel_size = (np.nan, np.nan)
    if not re.match(r'[0-9.]{1,11}px_[0-9.]{1,11}px', size_str):
        Exception('Invalid size given')

    if re.match(r'[0-9.]{0,9}px_[0-9.]{0,9}px', size_str):
        values = [int(v) for v in re.findall(r'[0-9.]{1,9}', size_str)]
        pixel_size = values

    return tuple(pixel_size)
