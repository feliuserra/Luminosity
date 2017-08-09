import copy as cp
import numpy as np
import matplotlib.pyplot as plt
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


def diff_light_grids(grids, logic='absolute'):
    if logic == 'absolute':
        return np.diff(grids, axis=1)

    if logic == 'growth':
        grids = grids + 1  # Avoid 0's
        change = np.diff(grids, axis=1)
        growth = np.ndarray(change.shape)
        for i in range(change.shape[1]):
            growth[:, i] = change[:, i] / grids[:, i]

        return growth

    raise Exception('Invalid logic')


def plot_light_grids(grids,
                     titles=None,
                     style='bone',
                     show_marker=False,
                     l=0):
    figsize = (15, 20)
    if grids.shape[1] < 6:
        per_row = grids.shape[1]
    elif grids.shape[1] < 12:
        per_row = 3
    elif grids.shape[1] < 20:
        per_row = 4
    else:
        per_row = int(np.sqrt(grids.shape[1]))

    fig, ax = plt.subplots(int(np.ceil(grids.shape[1] / per_row)),
                           per_row,
                           figsize=figsize)
    for i, axi in enumerate(ax.flat):
        if i < grids.shape[1]:
            axi.imshow(grids[l, i], cmap=style)
            axi.set_xticks([])
            axi.set_yticks([])
            if titles is not None:
                axi.set_title(titles[i])

        else:
            fig.delaxes(axi)

    plt.tight_layout()
    return plt.show()
