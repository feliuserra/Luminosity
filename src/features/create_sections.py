import numpy as np
import pandas as pd


src_img_path = 'data/raw/' +\
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/' +\
    'F182013.v4c_web.stable_lights.avg_vis.tif.npz'

src_img = np.load(src_img_path)['arr_0']


def convolve_coordinates(image,
                         step_size=(150, 150),
                         sub_image_shape=(300, 300)):
    passes = [
        int(image.shape[i]/step_size[i]-sub_image_shape[i]/step_size[i]+1)
        for i in range(2)
    ]
    sub_image_coordinates = np.zeros((passes[0], passes[1], 2, 2))
    for i in range(passes[0]):
        step_i = i*step_size[0]
        for j in range(passes[1]):
            step_j = j*step_size[1]
            sub_image_coordinates[i, j] = [
                [step_i, step_i+sub_image_shape[0]],
                [step_j, step_j+sub_image_shape[1]]
            ]
    return sub_image_coordinates.reshape(passes[0]*passes[1], 2, 2)


def retrieve_sub_img(image, img_pxl):
    return image[img_pxl[0][0]:img_pxl[0][1],
                 img_pxl[1][0]:img_pxl[1][1]]


sub_img_pxl = convolve_coordinates(src_img)
sections = pd.DataFrame(columns=['f',
                                 'mean_luminosity',
                                 'y_off',
                                 'x_off'])
for i, img_pxl in enumerate(sub_img_pxl):
    sections = sections.append(pd.DataFrame([[
        str(i),
        np.mean(retrieve_sub_img(src_img, img_pxl.astype(int))),
        img_pxl[0, 0],
        img_pxl[1, 1],
    ]],
        columns=['f', 'mean_luminosity', 'y_off', 'x_off']
    ))

sections['size'] = 300
sections[sections['mean_luminosity'] > 0].to_csv(
    'data/interim/' +
    'Version_4_DMSP-OLS_Nighttime_Lights_Time_Series/sections.csv',
    index=False)
