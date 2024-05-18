import pandas as pd
from utils import timer
from retrieve_sites import target_param

class WaterDataProcessor:
    def __init__(self, filepath, target_param):
        self.filepath = filepath
        self.target_param = target_param
        self.df = self.load_site_data()
    
    @timer
    def load_site_data(self):
        return pd.read_csv(self.filepath, dtype={'site_no': str}, low_memory=False)

    @timer
    def filter_columns_by_header(self, numeric_threshold):
        initial_columns = self.df.columns[:numeric_threshold].tolist()
        numeric_headers = [header for header in self.df.columns[numeric_threshold:] if header.isnumeric()]
        selected_columns = initial_columns + numeric_headers
        self.df = self.df[selected_columns]

    @timer
    def preprocess_data(self):
        self.df.replace(-999999.0, pd.NA, inplace=True) #-999999.0 used as NA/error
        self.df = self.df[self.df[self.target_param].notna()]
        float_cols = self.df.select_dtypes(include=['float64']).columns
        self.df = self.df.dropna(subset=[col for col in float_cols if col != self.target_param], how='all')

    @timer
    def apply_completeness_threshold(self, threshold_ratio):
        threshold = self.df.shape[0] * threshold_ratio
        self.df = self.df.dropna(axis=1, thresh=threshold)

    @timer
    def save_data(self, filename):
        self.df.to_csv(filename, index=False)

@timer
def process_data_from_sites(target_param = target_param):
    filepath = 'dirty_data.csv'
    target_param = target_param
    target_to_feature_ratio = 0.05
    final_filepath = 'clean_data.csv'

    try:
        processor = WaterDataProcessor(filepath, target_param)
        processor.filter_columns_by_header(2)
        processor.preprocess_data()
        processor.apply_completeness_threshold(target_to_feature_ratio)
        processor.save_data(final_filepath)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    process_data_from_sites()
