import os
import datetime
import pandas as pd

class FileLogger:
    def __init__(self, trace_name, root_name='processed_data_logs'):
        self.trace_name = trace_name
        self.root_name = root_name

        self.create_logs_folder()

    def create_logs_folder(self):
        print('Checking for the logs directory...')

        if not os.path.exists(self.root_name):
            print('Creating the logs directory...')

            try:
                os.mkdir(self.root_name)
            except OSError as e:
                print(f'Error while creating logs directory!\n{e}')
                return
            
            print('Logs directory created!')
        else:
            print('Logs directory found!')
        
        self.create_trace_logs_root()

    def create_trace_logs_root(self):
        curr_datet = datetime.datetime.now()

        trace_logs_root_name = f'_{curr_datet.year}-' \
                               f'{curr_datet.month}-' \
                               f'{curr_datet.day}_' \
                               f'{curr_datet.hour}:' \
                               f'{curr_datet.minute}:' \
                               f'{curr_datet.second}'
        
        trace_logs_root_name = self.root_name + '/' + self.trace_name + trace_logs_root_name

        try:
            os.mkdir(trace_logs_root_name)
            self.log_father_folder = trace_logs_root_name
        except OSError as e:
            print(f'Error while creating {self.trace_name} logs directory!\n{e}')
            return
        
        print(f'Successfully created logs folder for the {self.trace_name} trace!')
        self.create_preprocessing_folder()
        self.create_metrics_folder()
        self.create_visualizations_folder()

    def create_preprocessing_folder(self):
        preprocessed_folder = self.log_father_folder + '/preprocessed_data'

        try:
            os.mkdir(preprocessed_folder)
            self.preproc_father_folder = preprocessed_folder
        except OSError as e:
            print(f'Error while creating preprocessing directory!\n{e}')
            return

    def create_metrics_folder(self):
        metrics_folder = self.log_father_folder + '/metrics'

        try:
            os.mkdir(metrics_folder)
            os.mkdir(metrics_folder + '/spatial')
            os.mkdir(metrics_folder + '/temporal')
            os.mkdir(metrics_folder + '/social')

            self.metrics_father_folder = metrics_folder
        except OSError as e:
            print(f'Error while creating metrics directory!\n{e}')
            return

    def create_visualizations_folder(self):
        visualizations_folder = self.log_father_folder + '/visualizations'

        try:
            os.mkdir(visualizations_folder)
            os.mkdir(visualizations_folder + '/statistical')
            os.mkdir(visualizations_folder + '/geografical')
            os.mkdir(visualizations_folder + '/comparative')

            self.viz_father_folder = visualizations_folder
        except OSError as e:
            print(f'Error while creating visualizations directory!\n{e}')
            return

    def save_preprocessed_files(self, parsed_trace, parsing_info):
        parsed_file_name = self.preproc_father_folder + '/parsed_' + self.trace_name
        parsing_info_file_name = self.preproc_father_folder + '/parsing_info_' + self.trace_name

        parsing_info_dataframe = pd.DataFrame(parsing_info)

        parsed_trace.to_csv(parsed_file_name + '.csv', index=False)
        parsing_info_dataframe.to_csv(parsing_info_file_name + '.csv', index=False)

    def save_metric_files(self, metric_name, metric_type, metric_df, parameters=None):
        metric_file_name = self.metrics_father_folder + '/' + metric_type + '/' \
                           + metric_name + '_' + self.trace_name
        
        if parameters:
            parameters_file_name = self.metrics_father_folder + '/' + metric_type \
                                + '/parameters_' + self.trace_name

            parameters_dataframe = pd.DataFrame(parameters)
            parameters_dataframe.to_csv(parameters_file_name + '.csv', index=False)

        metric_df.to_csv(metric_file_name + '.csv', index=False)
    
    def save_plot_files(self, plot_name, plot_type, metric_name, figure):
        plot_file_name = self.viz_father_folder + '/' + plot_type + '/' \
                         + plot_name + '_' + metric_name +'_' + self.trace_name
        
        figure.write_image(plot_file_name + '.png')
