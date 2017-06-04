import os
import numpy as np
import pandas as pd

T = 3

rawpath = 'data/raw/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/'
interimpath = 'data/interim/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/'
processedpath = 'data/processed/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/'
src_names = [f for f in os.listdir(rawpath) if 'npz' in f]
sections = pd.read_csv(interimpath + 'sections.csv',
                       index_col='f')

for i, src_name in enumerate(src_names):
    src = np.load(rawpath + src_name)['arr_0']
    for j, sec in sections.iterrows():
        sec = sec.astype(int)
        section = (
            src[sec['y_off']:sec['y_off']+sec['size'],
                sec['x_off']:sec['x_off']+sec['size']]
        )
        np.savez_compressed(
            interimpath + src_name[3:7] + '-' + str(j) + '.npz',
            section,
            delimiter=',')
