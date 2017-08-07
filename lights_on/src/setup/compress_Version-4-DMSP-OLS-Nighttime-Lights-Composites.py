import os
import re
import numpy as np
from tifffile import TiffFile


def create_compressed_numpy_arrays(filelist):
    for fn in filelist:
        year = re.search('(?<=F\d{2})\d{4}', fn).group(0)
        with TiffFile(str(wd) + '/data/downloads/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/' + fn) as tif:
            with tif.asarray() as arr:
                np.savez_compressed(str(wd) + '/data/nightlights/year/' + str(year), arr)
                del arr

if __name__ == "__main__":
    wd = os.getcwd()
    filelist = os.listdir(str(wd) + '/data/downloads/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series')
    create_compressed_numpy_arrays(filelist)
