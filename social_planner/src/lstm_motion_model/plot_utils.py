from visdom import Visdom
import json
import numpy as np

def rescale_plot(vis, env, win):
    window_data = json.loads(vis.get_window_data(env=env, win=win))
    y_data = window_data['content']['data'][0]['y']
    middle_percent = 80 
    end_percent = (100 - middle_percent) / 2
    percentiles = [end_percent, 100 - end_percent]
    lower, upper = np.percentile(y_data, percentiles)
    diff = upper - lower
    padding = diff * (25 + end_percent) / middle_percent
    ylims = [lower - padding, upper + padding]
    opts = {'layoutopts': {'plotly': {'yaxis': {'range': ylims}}}}
    vis.update_window_opts(env=env, win=win, opts=opts)
