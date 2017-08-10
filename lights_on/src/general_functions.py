import copy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import helpers
import helper_functions as h
import argparsers
from matplotlib.axes import Axes
from matplotlib.animation import FuncAnimation


def load_light_grids(coordinates,
                     dates,
                     dataset='nightlight_grids',
                     size='250px_250px',
                     frequency='year',
                     fill_empty=False,
                     verbose=False):
    source_path = argparsers.expand_dataset_source_path(dataset)
    dates = argparsers.expand_dates_string(dates)
    sources = []
    for date in dates:
        sources.append(source_path.format(frequency, date))

    names = [argparsers.expand_names(c) for c in coordinates]
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

    return (light_grids, dates, names)


def diff_light_grids(grids, method='absolute'):
    if method == 'absolute':
        return np.diff(grids, axis=1)

    if method == 'growth':
        grids = grids + 1  # Avoid 0's
        change = np.diff(grids, axis=1)
        growth = np.ndarray(change.shape)
        for i in range(change.shape[1]):
            growth[:, i] = change[:, i] / grids[:, i]

        return growth

    raise Exception('Invalid method')


def plot_light_grids(grids,
                     dates,
                     names,
                     style='bone',
                     show_marker=False,
                     l=0):
    figsize = (15, 20)
    per_row = h.get_plots_per_row(grids.shape[1])
    fig, ax = plt.subplots(int(np.ceil(grids.shape[1] / per_row)),
                           per_row,
                           figsize=figsize)
    if isinstance(ax, Axes):
        ax = np.array([ax])

    for i, axi in enumerate(ax.flat):
        if i < grids.shape[1]:
            axi.imshow(grids[l, i], cmap=style)
            axi.set_xticks([])
            axi.set_yticks([])
            axi.set_title('{} in {}'.format(names[i], dates[i]))

        else:
            fig.delaxes(axi)

    plt.tight_layout()
    return plt.show()


def animate_light_grids(grids,
                        dates,
                        names,
                        style='bone',
                        show_marker=False,
                        l=0):
    i = 0
    fig, ax = plt.subplots(figsize=(15, 20))
    img = ax.imshow(grids[l, i], cmap=style)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(dates[i])

    def update(i):
        img.set_array(grids[l, i])
        if names is not None:
            ax.set_title(dates[i])

    anim = FuncAnimation(fig, update, frames=np.arange(0, grids.shape[1]),
                         interval=500)
    anim.save('../figures/animation.gif', dpi=80, writer='imagemagick')
    print('View and download the animation at `../figures/animation.gif`')


def aggregate_light_grids(grids,
                          dates,
                          names,
                          method='sum'):
    if method == 'sum':
        df = pd.DataFrame(grids.sum(axis=(2, 3)))

    if method in ['mean', 'average', 'avg']:
        df = pd.DataFrame(grids.mean(axis=(2, 3)))

    if method in ['standard_deviation', 'std', 'std_dev']:
        df = pd.DataFrame(grids.std(axis=(2, 3)))

    if method in ['variance', 'var']:
        df = pd.DataFrame(grids.var(axis=(2, 3)))

    if df is None:
        raise Exception('Invalid method')

    df = df.rename(columns={i: t for i, t in enumerate(dates)})
    df = df.transpose()
    df = df.rename(columns={i: str(c) for i, c in enumerate(names)})
    df.to_csv('../data/aggregate.csv')
    print('View and download the aggregate at `../data/aggregate.csv`')
    return df


def plot_aggregated_light_grids(df):
    plt.plot(df.values)
    try:
        plt.xticks(df.index)
    except TypeError:
        plt.xticks([i for i in range(df.shape[0])])

    plt.show()
