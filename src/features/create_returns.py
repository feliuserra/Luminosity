import glob
import numpy as np
from scipy import sparse as ss


files = glob.glob(
    'data/raw/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/*')
for i in range(1, len(files)):
    print(files[i])
    A = ss.csr_matrix(np.load(files[i-1])['arr_0'])
    B = ss.csr_matrix(np.load(files[i])['arr_0'])
    C = B - A
    np.savez_compressed(files[i]
                        .replace('raw', 'interim')
                        .replace('Series', 'Returns'),
                        C.todense())
