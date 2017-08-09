import copy as cp
import numpy as np
import helpers
import argparsers


def load_light_grids(coordinates,
                     dataset='nightlight_grids',
                     dates='all',
                     size='250px_250px',
                     frequency='year',
                     fill_empty=False,
                     verbose=False):
    source_path = argparsers.expand_dataset_source_path(dataset)
    dates = argparsers.expand_dates_string(dates)
    sources = []
    for date in dates:
        sources.append(source_path.format(frequency, date))

    coordinates = [argparsers.expand_coordinates(c) for c in coordinates]
    size = argparsers.expand_size(size)
    # TODO: specify necessity of decimal coordinates
    locs = [helpers.as_pixels(c, coordtype='decimals') for c in coordinates]
    light_grids = np.empty((len(coordinates),
                           len(sources),
                           size[0],
                           size[1]))
    for f_i, f in enumerate(sources):
        if verbose is True:
            print('Loading file {}'.format(f))
        mapped_raster = np.load(f, mmap_mode='r')['arr_0']
        for l_i, loc in enumerate(locs):
            try:
                light_grids[l_i, f_i, :, :] = cp.deepcopy(mapped_raster[
                    loc[0]-int(size[0]/2):loc[0]+int(size[0]/2),
                    loc[1]-int(size[1]/2):loc[1]+int(size[1]/2)
                ])
            except ValueError as e:
                print(coordinates[l_i])
                if fill_empty is False:
                    raise e
                else:
                    light_grids[l_i, f_i, :, :] = np.zeros(size)

        del mapped_raster

    return light_grids
