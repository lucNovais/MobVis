import random
from turtle import color
from pandas.core.algorithms import diff
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from mobvis.utils import Converters
from mobvis.utils import Timer

from mobvis.utils.Utils import fix_size_conditions
from mobvis.utils.Utils import freedman_diaconis

def config_histogram_plot(metric_type, differ_nodes):
    if metric_type == 'TRVD':
        x_values = 'travel_distance'
        title_complement = 'Travel Distance'
    elif metric_type == 'RADG':
        x_values = 'radius_of_gyration'
        title_complement = 'Radius of Gyration'
    elif metric_type == 'VIST':
        x_values = 'visit_time'
        title_complement = 'Tempo de Visita'
    elif metric_type == 'TRVT':
        x_values = 'travel_time'
        title_complement = 'Tempo de Viagem'
    elif metric_type == 'INCO':
        x_values = 'intercontact_time'
        title_complement = 'Intercontact Time'

    if differ_nodes:
        cmap = 'id'
    else:
        cmap = None

    return [x_values, cmap, title_complement]

@Timer.timed
def plot_metric_histogram(metric_df, initial_id, metric_type, differ_nodes=False, nodes_list=None, max_users=None, num_bins=None, hnorm=None,
                         show_title=True, show_y_label = True, img_width=600, img_height=560, title='Histogram '):
    print(f'Generating the {metric_type} histogram...')

    [x_values, cmap, title_complement] = config_histogram_plot(metric_type, differ_nodes)

    if 'id' in metric_df.columns:
        original_size = metric_df.id.size
        plt_metric = fix_size_conditions(original_size, initial_id, metric_df, original_size, max_users, nodes_list)
    else:
        original_size = metric_df.id2.size
        plt_metric = metric_df

    x_tick = freedman_diaconis(plt_metric[x_values].values, returnas='width')
    num_bins = freedman_diaconis(plt_metric[x_values].values, returnas='bins')

    print(f'num_bins = {num_bins}')

    if num_bins <= 15:
        pass
    elif 15 < num_bins <= 25:
        x_tick = x_tick * 1.8
        print(f'XTICK {x_tick}')
    elif 25 < num_bins <= 40:
        x_tick = x_tick * 3.2
    elif 40 < num_bins <= 80:
        x_tick = x_tick * 4
        num_bins = int(num_bins / 1.2)
    elif 80 < num_bins <= 120:
        x_tick = x_tick * 5.6
        num_bins = int(num_bins / 2.5)
    elif 120 < num_bins <= 200:
        x_tick = int(x_tick * 10)
        num_bins = int(num_bins / 4.5)
    elif 200 < num_bins <= 260:
        x_tick = int(x_tick * 26)
        num_bins = int(num_bins / 7)
    elif 260 < num_bins <= 460:
        x_tick = int(x_tick * 40)
        num_bins = int(num_bins / 7)
    elif 460 < num_bins <= 900:
        x_tick = int(x_tick * 100)
        num_bins = int(num_bins / 15)
    else:
        x_tick = int(x_tick * 122)
        num_bins = int(num_bins / 30)

    fig = px.histogram(
        plt_metric,
        x=x_values,
        color=cmap,
        color_discrete_sequence=px.colors.qualitative.Dark2,
        nbins=num_bins,
        marginal='rug',
        histnorm=hnorm,
        labels={
            x_values: title_complement
        }
    )
    
    if show_title:
        title_dict = {
            'text': title + title_complement,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        margin_dict['l'] = 10
        margin_dict['r'] = 10
        y_title = None
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10
        y_title = 'Occurrences'

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=18,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        yaxis_title=y_title,
        xaxis_title=title_complement,
        margin=margin_dict,
        xaxis=dict(
            tickmode='linear',
            dtick=x_tick
        )
    )

    fig.update_yaxes(
        tickfont=dict(size=24),
        title_font_size=26
    )
    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(size=24),
        title_font_size=26
    )

    if differ_nodes:
        fig.update_layout(
            legend=dict(
                yanchor='top',
                xanchor='left',
                x=-0.34
        ))

    print('\nSuccessfully generated plot!')

    return fig


@Timer.timed
def boxplot_metric(metric_df, initial_id, metric_type, differ_nodes=False, nodes_list=None, max_users=None, num_bins=None, hnorm=None,
                  show_title=True, show_y_label = True, img_width=600, img_height=560, title='BoxPlot '):
    print(f'Generating the {metric_type} boxplot...')

    [y_values, x_values, title_complement] = config_histogram_plot(metric_type, differ_nodes)

    if 'id' in metric_df.columns:
        original_size = metric_df.id.size
        plt_metric = fix_size_conditions(original_size, initial_id, metric_df, original_size, max_users, nodes_list)
    else:
        original_size = metric_df.id2.size
        plt_metric = metric_df
    

    fig = px.box(
        plt_metric,
        x=x_values,
        y=y_values,
        color=x_values,
        color_discrete_sequence=px.colors.qualitative.G10,
        points='all',
        labels={
            'id': 'Node ID',
        }
    )

    if show_title:
        title_dict = {
            'text': title + title_complement,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        margin_dict['l'] = 10
        margin_dict['r'] = 10
        y_title = None
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10
        y_title=title_complement

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=18,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        yaxis_title=y_title,
        margin=margin_dict
    )

    fig.update_yaxes(
        tickfont=dict(size=24),
        title_font_size=26
    )

    if differ_nodes:
        fig.update_layout(
            legend=dict(
                yanchor='top',
                xanchor='left',
                x=-0.34
        ))

    print('\nSuccessfully generated plot!')

    return fig

def plot_metric_dist(metric_df, initial_id, metric_type, differ_nodes=False, nodes_list=None, max_users=None,
                    show_title=True, show_y_label = True, img_width=600, img_height=560, title='Distribution '):
    [x_values, cmap, title_complement] = config_histogram_plot(metric_type, differ_nodes)

    if 'id' in metric_df.columns:
        original_size = metric_df.id.size
    else:
        original_size = metric_df.id2.size

    hist_data = []
    group_labels = []

    if nodes_list:
        for node in nodes_list:
            data = fix_size_conditions(original_size, initial_id, metric_df, original_size, max_users, [node])
            hist_data.append(data[x_values].values)
            group_labels.append(f'Node {str(node)}')
    else:
        if 'id' in metric_df.columns:
            data = fix_size_conditions(original_size, initial_id, metric_df, original_size, max_users, nodes_list)
        else:
            data = metric_df
        hist_data = [data[x_values].values]
        group_labels = [f'{title_complement}']

    x_tick = freedman_diaconis(hist_data[0], returnas='width')
    num_bins = freedman_diaconis(hist_data[0], returnas='bins')

    if num_bins <= 40:
        pass
    elif 40 < num_bins <= 80:
        x_tick = int(x_tick * 2)
    elif 80 < num_bins <= 120:
        x_tick = int(x_tick * 4)
    elif 120 < num_bins <= 200:
        x_tick = int(x_tick * 9)
    elif 200 < num_bins <= 260:
        x_tick = int(x_tick * 11)
    elif 260 < num_bins <= 460:
        x_tick = int(x_tick * 14)
    else:
        x_tick = int(x_tick * 30)


    fig = ff.create_distplot(
        hist_data,
        group_labels,
        bin_size=[x_tick],
        colors=['#3366CC'],
        show_rug=False
    )

    if show_title:
        title_dict = {
            'text': title + title_complement,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        margin_dict['l'] = 10
        margin_dict['r'] = 10
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10

    y_title=None

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=18,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        yaxis_title=y_title,
        xaxis_title=title_complement,
        showlegend=False,
        margin=margin_dict
    )

    fig.update_yaxes(
        tickfont=dict(size=24),
        title_font_size=26
    )
    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(size=24),
        title_font_size=26
    )

    if differ_nodes:
        fig.update_layout(
            legend=dict(
                yanchor='top',
                xanchor='left',
                x=-0.34
        ))

    return fig
