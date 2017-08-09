import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import helpers
import argparsers


def load_lights(coordinates,
                source,
                size):
    source = argparsers.expand_source(source)
    coordinates = argparsers.expand_coordinates(coordinates)
    pixel_size = argparsers.expand_size(size)
    # TODO: specify necessity of decimal coordinates
    loc = helpers.as_pixels(coordinates, coordtype='decimals')
    mapped_raster = np.load(source, mmap_mode='r')['arr_0']
    img = cp.deepcopy(mapped_raster[
        loc[0]-int(pixel_size[0]/2):loc[0]+int(pixel_size[0]/2),
        loc[1]-int(pixel_size[1]/2):loc[1]+int(pixel_size[1]/2)
    ])
    del mapped_raster
    return img


def load_lights_multiple(coordinates,
                         sources,
                         size,
                         fill_empty=False,
                         verbose=False):
    sources = [argparsers.expand_source(s) for s in sources]
    coordinates = [argparsers.expand_coordinates(c) for c in coordinates]
    size = argparsers.expand_size(size)
    # TODO: specify necessity of decimal coordinates
    locs = [helpers.as_pixels(c, coordtype='decimals') for c in coordinates]
    lights = np.empty((len(coordinates),
                       len(sources),
                       size[0],
                       size[1]))
    for f_i, f in enumerate(sources):
        if verbose is True:
            print('Loading file {}'.format(f))
        mapped_raster = np.load(f, mmap_mode='r')['arr_0']
        for l_i, loc in enumerate(locs):
            try:
                lights[l_i, f_i, :, :] = cp.deepcopy(mapped_raster[
                    loc[0]-int(size[0]/2):loc[0]+int(size[0]/2),
                    loc[1]-int(size[1]/2):loc[1]+int(size[1]/2)
                ])
            except ValueError as e:
                print(coordinates[l_i])
                if fill_empty is False:
                    raise e
                else:
                    lights[l_i, f_i, :, :] = np.zeros(size)

        del mapped_raster

    return lights


def aggregate_lights(coordinates,
                     sources,
                     size,
                     agg='sum'):
    pass


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


def plot_lights_difference(coordinates,
                           sources,
                           size,
                           style='bone'):
    imgs = []
    for i in range(len(sources) - 1):
        imgs.append(
            load_lights(coordinates, sources[i+1], size) -
            load_lights(coordinates, sources[i], size))

    fig, ax = plt.subplots(int(np.ceil(len(imgs) / 4)),
                           4,
                           figsize=(15, 10))
    for i, axi in enumerate(ax.flat):
        if i < len(imgs):
            axi.imshow(imgs[i], cmap=style)
            axi.set_xticks([])
            axi.set_yticks([])
        else:
            fig.delaxes(axi)

    plt.draw()
