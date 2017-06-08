import numpy as np
from glob import glob
from geo_helpers import as_pixels

DEF_SRC_PATH = 'data/interim/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Returns/*.npz'


class SectionIntegrityException(Exception):
    """Raise when files aren't available"""


class SectionSeriesLoader(object):

    def __init__(self, start_year=1993, end_year=2013,
                 img_shape=(300, 300), check_integrity=True,
                 SRC_PATH=DEF_SRC_PATH):
        self.available_files = glob(SRC_PATH)
        self.img_extent = np.round((img_shape[0]/2, img_shape[1]/2))\
            .astype(int)
        if check_integrity is True:
            if not len(self.available_files) == end_year - start_year:
                SectionIntegrityException(
                    'The length of available files is not as expected' +
                    'for range {} to {} ({}). There were {} files found.'
                    .format(start_year, end_year, end_year - start_year,
                            len(self.available_files)))

            if str(start_year) not in self.available_files[0]:
                SectionIntegrityException(
                    "First available file doesn't coincide with start year {}"
                    .format(start_year))

            if str(end_year) not in self.available_files[-1]:
                SectionIntegrityException(
                    "First available file doesn't coincide with end year {}"
                    .format(end_year))

    def load(self, target_coords):
        loc = as_pixels(target_coords=target_coords)
        stack = []
        for f in self.available_files:
            print('Loading file {}'.format(f))
            mapped_raster = np.load(f, mmap_mode='r')['arr_0']
            stack.append(mapped_raster[
                loc[0]-self.img_extent[0]:loc[0]+self.img_extent[0],
                loc[1]-self.img_extent[1]:loc[1]+self.img_extent[1]
            ])
            del mapped_raster

        series = np.stack(stack)
        return(series)
