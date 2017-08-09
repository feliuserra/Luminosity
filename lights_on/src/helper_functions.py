import numpy as np


def get_plots_per_row(num_plots):
    if num_plots < 6:
        return num_plots
    elif num_plots < 12:
        return 3
    elif num_plots < 20:
        return 4
    else:
        return int(np.sqrt(num_plots))
