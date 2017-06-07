import glob
import numpy as np


files = glob.glob(
    'data/raw/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/*')
for i in range(1, len(files)):
    print(files[i])
    A = np.load(files[i-1])['arr_0']
    B = np.load(files[i])['arr_0']
    C = np.diff(np.stack([B, A]).astype(float), axis=0)  # convert because it's
    np.savez_compressed(files[i]                         # `uint8` type
                        .replace('raw', 'interim')
                        .replace('Series', 'Returns'),
                        C[0])
