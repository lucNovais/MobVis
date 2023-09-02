from distutils.log import warn

def export_dataframe(df, path):
    """ Exports a DataFrame object to a specified format on a given path.

    ### Parameters:

    `df` (pandas.DataFrame): DataFrame of the object to be exported.
    `path` (str): Path (with filename and extention) where the file should be saved.
        - Supported extentions: .csv, .xlsx and .txt.
    """
    format = path.split('.')[-1] # Get only the file format

    if format == 'csv':
        df.to_csv(path, columns=df.columns, sep=',', index=False)
    elif format == 'xlsx':
        df.to_excel(path, columns=df.columns, index=False)
    elif format == 'txt':
        df.to_csv(path, columns=df.columns, sep=' ', index=False)
    else:
        warn('WARNING: The provided path does not contain a file with supported file extention, therefore, nothing was saved.')

def export_figure(figure, path):
    """ Exports a Plotly Figure object to a specified image format.

    ### Parameters:

    `figure` (plotly.graph_objects.Figure): Figure to be exported.
    `path` (str): Path (with filename and extention) where the figure should be saved.
    """

    try:
        figure.write_image(path)
    except ValueError:
        warn('WARNING: The provided path does not contain a file extention, therefore, the figure will be saved as: `figure.png`.')
        figure.write_image('figure.png')
