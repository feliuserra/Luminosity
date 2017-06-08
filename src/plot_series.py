import matplotlib.pyplot as plt
from models.section_series import SectionSeriesLoader

series_loader = SectionSeriesLoader(
    img_shape=(200, 200))

haiti_series = series_loader.load({
    'lat': 18.53,
    'lng': -72.34
})


def plot_series(series):
    max_abs = max(abs(series.max()), abs(series.min()))
    fig, ax = plt.subplots(5, 4, figsize=(20, 20))
    for i, axi in enumerate(ax.flat):
        axi.imshow(series[i],
                   vmin=-max_abs, vmax=max_abs,
                   cmap='RdYlGn')
        axi.set(xticks=[], yticks=[])

    plt.show()


if __name__ == '__main__':
    plot_series(haiti_series)
