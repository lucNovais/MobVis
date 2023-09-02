from distutils.log import warn
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from plotly.subplots import make_subplots
from mobvis.utils import Timer

from mobvis.utils.Utils import freedman_diaconis
from mobvis.utils.Utils import fix_size_conditions
from mobvis.utils.Utils import config_metric_plot

@Timer.timed
def plot_metric_histogram(metric_df, metric_name, differ_nodes=False, specific_users=None,
                          users_to_display=None, hnorm=None, show_title=True, show_y_label = True,
                          img_width=600, img_height=560, title=' - Histogram', **kwargs):
    """ Generates a histogram of the given metric DataFrame.

    ### Parameters:

    `metric_df` (pandas.DataFrame): DataFrame corresponding to the extracted metric from some mobvis.metrics module.
    `metric_name` (str): Name of the metric on the DataFrame. (Ex.: TRVD, RADG, VIST etc).
    `differ_nodes` (bool): If each node needs to be differed on the plot.
    `specific_users` (int[]): Specific nodes ids that the plot will use data from.
    `users_to_display` (int): Maximum number of ids to be considered on the plot.
    `hnorm` (str): Plotly histogram norm. See https://plotly.github.io/plotly.py-docs/generated/plotly.express.histogram.html
    `show_title` (bool): If the graph title should appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `img_width` (float): Width of the generated image.
    `img_height` (float): Height of the generated image.
    `title` (str): Title of the graph.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.graph_objects.Figure): Plotly interactive histogram generated with the given data and parameters.
    """
    print(f'Generating the {metric_name} histogram...')

    [x_values, cmap, title_complement] = config_metric_plot(metric_name, differ_nodes)

    try:
        plt_metric = fix_size_conditions(
            df=metric_df,
            limit=None,
            users_to_display=users_to_display,
            specific_users=specific_users
        )
    except IndexError:
        warn("Could not generate plot!")
        return None

    fig = px.histogram(
        plt_metric,
        x=x_values,
        color=cmap,
        color_discrete_sequence=px.colors.qualitative.Dark2,
        marginal='rug',
        histnorm=hnorm,
        labels={
            x_values: title_complement
        },
        **kwargs
    )
    
    if show_title:
        title_dict = {
            'text': title_complement + title,
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
            size=20
        ),
        title_font_size=22,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        yaxis_title=y_title,
        xaxis_title=title_complement,
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

    print('\nSuccessfully generated histogram!')

    return fig


@Timer.timed
def boxplot_metric(metric_df, metric_name, differ_nodes=False, specific_users=None,
                   users_to_display=None, show_title=True, show_y_label = True,
                   img_width=600, img_height=560, title='BoxPlot ', **kwargs):
    """ Generates a boxplot of the given metric DataFrame.

    ### Parameters:

    `metric_df` (pandas.DataFrame): DataFrame corresponding to the extracted metric from some mobvis.metrics module.
    `metric_name` (str): Name of the metric on the DataFrame. (Ex.: TRVD, RADG, VIST etc).
    `differ_nodes` (bool): If each node needs to be differed on the plot.
    `specific_users` (int[]): Specific nodes ids that the plot will use data from.
    `users_to_display` (int): Maximum number of ids to be considered on the plot.
    `hnorm` (str): Plotly histogram norm. See https://plotly.github.io/plotly.py-docs/generated/plotly.express.histogram.html
    `show_title` (bool): If the graph title should appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `img_width` (float): Width of the generated image.
    `img_height` (float): Height of the generated image.
    `title` (str): Title of the graph.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.graph_objects.Figure): Plotly interactive boxplot generated with the given data and parameters.
    """
    print(f'Generating the {metric_name} boxplot...')

    [y_values, x_values, title_complement] = config_metric_plot(metric_name, differ_nodes)

    try:
        plt_metric = fix_size_conditions(
            df=metric_df,
            limit=None,
            users_to_display=users_to_display,
            specific_users=specific_users
        )
    except IndexError:
        warn("Could not generate plot!")
        return None

    fig = px.box(
        plt_metric,
        x=x_values,
        y=y_values,
        color=x_values,
        color_discrete_sequence=px.colors.qualitative.G10,
        points='all',
        labels={
            'id': 'Node ID',
        },
        **kwargs
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
        title_font_size=22,
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

    print('\nSuccessfully generated boxplot!')

    return fig

def plot_metric_dist(metric_df, metric_name, differ_nodes=False, specific_users=None,
                     bin_size_multiplier=1, users_to_display=None, show_title=True, show_y_label = True,
                     img_width=600, img_height=560, title=' - Distribution', **kwargs):
    """ Generates a distplot of the given metric DataFrame.

    ### Parameters:

    `metric_df` (pandas.DataFrame): DataFrame corresponding to the extracted metric from some mobvis.metrics module.
    `metric_name` (str): Name of the metric on the DataFrame. (Ex.: TRVD, RADG, VIST etc).
    `differ_nodes` (bool): If each node needs to be differed on the plot.
    `specific_users` (int[]): Specific nodes ids that the plot will use data from.
    `users_to_display` (int): Maximum number of ids to be considered on the plot.
    `show_title` (bool): If the graph title should appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `img_width` (float): Width of the generated image.
    `img_height` (float): Height of the generated image.
    `title` (str): Title of the graph.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.graph_objects.Figure): Plotly interactive distplot generated with the given data and parameters.
    """
    print(f'Generating the {metric_name} distplot...')

    [x_values, cmap, title_complement] = config_metric_plot(metric_name, differ_nodes)

    hist_data = []
    group_labels = []

    if specific_users:
        for node in specific_users:
            try:
                data = fix_size_conditions(metric_df, None, users_to_display, [node])
            except IndexError:
                warn("Could not generate plot!")
                return None
            hist_data.append(data[x_values].values)
            group_labels.append(f'Node {str(node)}')
    else:
        if 'id' in metric_df.columns:
            try:
                data = fix_size_conditions(metric_df, None, users_to_display, specific_users)
            except IndexError:
                warn("Could not generate plot!")
                return None
        else:
            data = metric_df
        hist_data = [list(data[x_values].values)]
        group_labels = [f'{title_complement}']

    try:
        b_size = [freedman_diaconis(hist_data[0], returnas='width') * bin_size_multiplier]
    except TypeError:
        print(f'WARNING: Something is wrong with your {metric_name}! Check the configuration parameters.')
        print("          Can't generate DISTPLOT on the given conditions, aborting...")
        return None

    fig = ff.create_distplot(
        hist_data,
        group_labels,
        bin_size=b_size,
        colors=['#3366CC'],
        show_rug=False
    )

    if show_title:
        title_dict = {
            'text': title_complement + title,
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
        title_font_size=22,
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
        title_font_size=22
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

    print('\nSuccessfully generated distplot!')

    return fig

def subplot_metric_histogram(metric_dfs, metric_name, plot_names, differ_nodes=False, specific_users=None,
                            users_to_display=None, hnorm=None, show_title=True, show_y_label = True,
                            img_width=1200, img_height=580, title=' - Histograms', **kwargs):
    """ Creates a subplot with many histograms of the given metric DataFrame.

    ### Parameters:

    `metric_dfs` (pandas.DataFrame): DataFrames corresponding to the extracted metrics from some mobvis.metrics module.
    `metric_name` (str): Name of the metric on the DataFrame. (Ex.: TRVD, RADG, VIST etc).
    `plot_names` (str[]): Specific names of each subplot that will be generated.
    `differ_nodes` (bool): If each node needs to be differed on the plot.
    `specific_users` (int[]): Specific nodes ids that the plot will use data from.
    `users_to_display` (int[]): Maximum number of ids to be considered on the plot.
    `hnorm` (str): Plotly histogram norm. See https://plotly.github.io/plotly.py-docs/generated/plotly.express.histogram.html
    `show_title` (bool): If the graph title should appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `img_width` (float): Width of the generated image.
    `img_height` (float): Height of the generated image.
    `title` (str): Title of the graph.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.graph_objects.Figure): Plotly interactive subplot with all histograms generated from the given data and parameters.
    """

    fig = make_subplots(rows=1, cols=2, subplot_titles=plot_names)

    [x_values, cmap, title_complement] = config_metric_plot(metric_name, differ_nodes)

    for i, metric_df in enumerate(metric_dfs):
        if i == 0:
            row = 1
            column = 1
        elif i == 1:
            row = 1
            column = 2
        
        fig.add_trace(
            go.Histogram(
                x=metric_df[x_values]
            )
            , row=row, col=column
        )

    fig.update_annotations(font_size=20)

    if show_title:
        title_dict = {
            'text': title_complement + title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=70, b=25)
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
            size=20
        ),
        title_font_size=22,
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
    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(size=24),
        title_font_size=26
    )

    if differ_nodes:
        fig.update_layout(
            legend=dict(
                yanchor='top',
                xanchor='center',
                x=-0.34
        ))
    else:
        fig.update_layout(showlegend=False)

    return fig
