import copy
import numpy as np
from glob import glob
from helpers import as_pixels

DEF_SRC_PATH = 'data/interim/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Returns/*.npz'


class SectionIntegrityException(Exception):
    """Raise when files aren't available"""


class SectionSeriesLoader(object):

    def __init__(self, start_year=1993, end_year=2013,
                 img_shape=(200, 200), check_integrity=True,
                 SRC_PATH=DEF_SRC_PATH):
        self.available_files = sorted(glob(SRC_PATH))
        self.selected_files = self.available_files[start_year
                                                   - 1992:end_year
                                                   - 1992 + 1]
        self.img_shape = img_shape
        self.end_year = end_year
        self.img_extent = np.round((img_shape[0]/2, img_shape[1]/2))\
            .astype(int)
        if check_integrity is True:
            print(self.selected_files)
            if str(start_year) not in self.selected_files[0]:
                raise SectionIntegrityException(
                    "First available file doesn't coincide with start year {}"
                    .format(start_year))

            if str(end_year) not in self.selected_files[-1]:
                raise SectionIntegrityException(
                    "First available file doesn't coincide with end year {}"
                    .format(end_year))

    def load(self, target_coords):
        loc = as_pixels(target_coords=target_coords)
        stack = []
        for f in self.selected_files:
            print('Loading file {}'.format(f))
            mapped_raster = np.load(f, mmap_mode='r')['arr_0']
            stack.append(copy.deepcopy(mapped_raster[
                loc[0]-self.img_extent[0]:loc[0]+self.img_extent[0],
                loc[1]-self.img_extent[1]:loc[1]+self.img_extent[1]
            ]))
            del mapped_raster

        series = np.stack(stack)
        return(series)

    def load_multiple(self, target_coords_list, fill_empty=True):
        locs = [as_pixels(target_coords=tc) for tc in target_coords_list]
        series = np.empty((len(target_coords_list),
                           len(self.selected_files),
                           self.img_shape[0],
                           self.img_shape[1]))
        for f_i, f in enumerate(self.selected_files):
            print('Loading file {}'.format(f))
            mapped_raster = np.load(f, mmap_mode='r')['arr_0']
            for l_i, loc in enumerate(locs):
                try:
                    series[l_i, f_i, :, :] = copy.deepcopy(mapped_raster[
                        loc[0]-self.img_extent[0]:loc[0]+self.img_extent[0],
                        loc[1]-self.img_extent[1]:loc[1]+self.img_extent[1]
                    ])
                except ValueError as e:
                    print(target_coords_list[l_i])
                    if fill_empty is False:
                        raise e
                    else:
                        series[l_i, f_i, :, :] = np.zeros(self.img_shape)

            del mapped_raster

        return(series)

    def load_multiple_means(self, target_coords_list, fill_empty=True):
        locs = [as_pixels(target_coords=tc) for tc in target_coords_list]
        series = np.empty((len(target_coords_list),
                           len(self.selected_files)))
        for f_i, f in enumerate(self.selected_files):
            print('Loading file {}'.format(f))
            mapped_raster = np.load(f, mmap_mode='r')['arr_0']
            for l_i, loc in enumerate(locs):
                try:
                    series[l_i, f_i] = mapped_raster[
                        loc[0]-self.img_extent[0]:loc[0]+self.img_extent[0],
                        loc[1]-self.img_extent[1]:loc[1]+self.img_extent[1]
                    ].mean()
                except ValueError as e:
                    print(target_coords_list[l_i])
                    if fill_empty is False:
                        raise e
                    else:
                        series[l_i, f_i] = 0

            del mapped_raster

    def load_multiple_sums(self, target_coords_list, fill_empty=True):
        locs = [as_pixels(target_coords=tc) for tc in target_coords_list]
        series = np.empty((len(target_coords_list),
                           len(self.selected_files)))
        for f_i, f in enumerate(self.selected_files):
            print('Loading file {}'.format(f))
            mapped_raster = np.load(f, mmap_mode='r')['arr_0']
            for l_i, loc in enumerate(locs):
                try:
                    series[l_i, f_i] = mapped_raster[
                        loc[0]-self.img_extent[0]:loc[0]+self.img_extent[0],
                        loc[1]-self.img_extent[1]:loc[1]+self.img_extent[1]
                    ].sum()
                except ValueError as e:
                    print(target_coords_list[l_i])
                    if fill_empty is False:
                        raise e
                    else:
                        series[l_i, f_i] = 0

            del mapped_raster

        return(series)
