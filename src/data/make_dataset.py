import os
import numpy as np
from tifffile import TiffFile


def create_compressed_numpy_arrays(filelist):
    for fn in filelist:
        with TiffFile(str(wd) + '/data/external/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/' + fn) as tif:
            arr = tif.asarray()
            print(arr.shape)
            np.savez_compressed(str(wd) + '/data/raw/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/' + str(fn), arr)


if __name__ == "__main__":
    wd = os.getcwd()
    print(wd)
    filelist = os.listdir(str(wd) + '/data/external/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series')
    create_compressed_numpy_arrays(filelist)
