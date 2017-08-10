import general_functions as g


def load_light_grid(coordinates,
                    date,
                    **kw_args):
    light_grids, d, n = g.load_light_grids([coordinates],
                                           date,
                                           **kw_args)
    return light_grids[0, 0]


def plot_light_grid(coordinates,
                    date,
                    dataset='nightlight_grids',
                    size='year',
                    frequency='year',
                    style='bone',
                    fill_empty=False,
                    verbose=False,
                    show_marker=False):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=date,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    g.plot_light_grids(lights, dates, names,
                       style=style, show_marker=show_marker)


def animate_light_series(coordinates,
                         date,
                         dataset='nightlight_grids',
                         size='year',
                         frequency='year',
                         style='bone',
                         fill_empty=False,
                         verbose=False,
                         show_marker=False):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=date,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    g.animate_light_grids(lights, dates, names,
                          style=style, show_marker=show_marker)


def plot_light_series(coordinates,
                      dates,
                      dataset='nightlight_grids',
                      size='year',
                      frequency='year',
                      style='bone',
                      fill_empty=False,
                      verbose=False,
                      show_marker=False,
                      method='absolute'):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=dates,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    g.plot_light_grids(lights, dates, names,
                       style=style, show_marker=show_marker)


def plot_light_diff(coordinates,
                    dates,
                    dataset='nightlight_grids',
                    size='year',
                    frequency='year',
                    style='RdBu',
                    fill_empty=False,
                    verbose=False,
                    show_marker=False,
                    method='absolute'):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=dates,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    lights = g.diff_light_grids(lights,
                                method=method)
    # TODO: correct name and date index
    g.plot_light_grids(lights,
                       [
                           '{}-{}'.format(dates[i], d)
                           for i, d in
                           enumerate(dates[1:])
                       ],
                       names,
                       style=style, show_marker=show_marker)


def plot_light_change(coordinates, dates, **kw_args):
    kw_args['method'] = 'absolute'
    plot_light_diff(coordinates, dates, **kw_args)


def plot_light_growth(coordinates, dates, **kw_args):
    kw_args['method'] = 'growth'
    plot_light_diff(coordinates, dates, **kw_args)


def animate_light_diff(coordinates,
                       date,
                       dataset='nightlight_grids',
                       size='year',
                       frequency='year',
                       style='nipy_spectral',
                       fill_empty=False,
                       verbose=False,
                       show_marker=False,
                       method='absolute'):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=date,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    lights = g.diff_light_grids(lights,
                                method=method)
    g.animate_light_grids(lights, dates, names,
                          style=style, show_marker=show_marker)


def animate_light_change(coordinates, dates, **kw_args):
    kw_args['method'] = 'absolute'
    animate_light_diff(coordinates, dates, **kw_args)


def animate_light_growth(coordinates, dates, **kw_args):
    kw_args['method'] = 'growth'
    animate_light_diff(coordinates, dates, **kw_args)


def plot_aggregated_light_series(coordinates,
                                 date,
                                 dataset='nightlight_grids',
                                 size='year',
                                 frequency='year',
                                 style='bone',
                                 fill_empty=False,
                                 verbose=False,
                                 show_marker=False,
                                 method='sum'):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=date,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    agg_df = g.aggregate_light_grids(lights, dates, names, method=method)
    g.plot_aggregated_light_grids(agg_df)


def plot_aggregated_light_sum(coordinates, date, **kw_args):
    kw_args['method'] = 'sum'
    plot_aggregated_light_series(coordinates, date, **kw_args)


def plot_aggregated_light_mean(coordinates, date, **kw_args):
    kw_args['method'] = 'mean'
    plot_aggregated_light_series(coordinates, date, **kw_args)


def plot_aggregated_light_series_diff(coordinates,
                                      dates,
                                      dataset='nightlight_grids',
                                      size='year',
                                      frequency='year',
                                      style='bone',
                                      fill_empty=False,
                                      verbose=False,
                                      show_marker=False,
                                      agg_method='sum',
                                      diff_method='absolute'):
    lights, dates, names = g.load_light_grids([coordinates],
                                              dataset=dataset,
                                              dates=dates,
                                              frequency=frequency,
                                              fill_empty=fill_empty,
                                              verbose=verbose)
    lights = g.diff_light_grids(lights,
                                method=diff_method)
    agg_df = g.aggregate_light_grids(lights,
                                     [
                                         '{}-{}'.format(dates[i], d)
                                         for i, d in
                                         enumerate(dates[1:])
                                      ],
                                     names)
    g.plot_aggregated_light_grids(agg_df)


def plot_light_series_mean_change(coordinates, dates, **kw_args):
    kw_args['diff_method'] = 'absolute'
    kw_args['agg_method'] = 'mean'
    plot_aggregated_light_series_diff(coordinates, dates, **kw_args)


def plot_light_series_sum_change(coordinates, dates, **kw_args):
    kw_args['diff_method'] = 'absolute'
    kw_args['agg_method'] = 'sum'
    plot_aggregated_light_series_diff(coordinates, dates, **kw_args)


def plot_light_series_sum_growth(coordinates, dates, **kw_args):
    kw_args['diff_method'] = 'absolute'
    kw_args['agg_method'] = 'sum'
    plot_aggregated_light_series_diff(coordinates, dates, **kw_args)
