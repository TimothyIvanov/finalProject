import pandas as pd
from dataretrieval import nwis
from utils import timer

class WaterDataProcessor:
    def __init__(self, filepath, target_param):
        self.filepath = filepath
        self.target_param = target_param
        self.df = self.load_site_data()
    
    @timer
    #Load site data
    def load_site_data(self):
        return pd.read_csv(self.filepath, dtype={'site_no': str}, low_memory=False)

    @timer
    #Filter out non-numeric columns after certain index
    def filter_columns_by_header(self, numeric_threshold):
        initial_columns = self.df.columns[:numeric_threshold].tolist()
        numeric_headers = [header for header in self.df.columns[numeric_threshold:] if header.isnumeric()]
        selected_columns = initial_columns + numeric_headers
        self.df = self.df[selected_columns]

    @timer
    #Remove missing target_param values and select non-empty float columns
    def preprocess_data(self):
        self.df = self.df[self.df[self.target_param].notna()]
        float_cols = self.df.select_dtypes(include=['float64']).columns
        self.df = self.df.dropna(subset=[col for col in float_cols if col != self.target_param], how='all')

    @timer
    #Apply a dynamic threshold for column data completeness
    def apply_completeness_threshold(self, threshold_ratio):
        threshold = self.df.shape[0] / threshold_ratio
        self.df = self.df.dropna(axis=1, thresh=threshold)

    @timer
    #Save filtered dataframe
    def save_data(self, filename):
        self.df.to_csv(filename, index=False)

@timer
#Filter out non-float data cols from dirty_data.csv, leave only rows with 00010 value and  another feature at given ratio
def process_data_from_sites():
    filepath = 'dirty_data.csv'
    target_param = '00010'
    target_to_feature_ratio = 20
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
    