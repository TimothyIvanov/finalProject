import pandas as pd
from dataretrieval import nwis
from time import time

def timer_func(func): 
    #This function shows the execution time of the function object passed
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 

class WaterDataProcessor:
    def __init__(self, filepath, start_date, end_date, target_param):
        self.filepath = filepath
        self.sites = self.load_site_data()
        self.start_date = start_date
        self.end_date = end_date
        self.target_param = target_param
        self.df = None
    
    @timer_func
    #Load site data
    def load_site_data(self):
        return pd.read_csv(self.filepath, dtype={'site_no': str})['site_no'].tolist()

    @timer_func
    #Retrieve water data from NWIS service
    def retrieve_data(self):
        self.df, _ = nwis.get_iv(sites=self.sites,
                                 start=self.start_date,
                                 end=self.end_date)
        self.df.reset_index(inplace=True)

    @timer_func
    #Filter out non-numeric columns after certain index
    def filter_columns_by_header(self, numeric_threshold):
        initial_columns = self.df.columns[:numeric_threshold].tolist()
        numeric_headers = [header for header in self.df.columns[numeric_threshold:] if header.isnumeric()]
        selected_columns = initial_columns + numeric_headers
        self.df = self.df[selected_columns]

    @timer_func
    #Remove missing target_param values and select non-empty float columns
    def preprocess_data(self):
        self.df = self.df[self.df[self.target_param].notna()]
        float_cols = self.df.select_dtypes(include=['float64']).columns
        self.df = self.df.dropna(subset=[col for col in float_cols if col != self.target_param], how='all')

    @timer_func
    #Apply a dynamic threshold for column data completeness
    def apply_completeness_threshold(self, threshold_ratio):
        threshold = self.df.shape[0] / threshold_ratio
        self.df = self.df.dropna(axis=1, thresh=threshold)

    @timer_func
    #Save filtered dataframe
    def save_data(self, filename):
        self.df.to_csv(filename, index=False)

@timer_func
def main():
    file_name = 'ca_water_sites.csv'
    start_date = '2024-05-01'
    end_date = '2024-05-02'
    target_param = '00010'
    final_file_name = 'filtered_data.csv'

    try:
        processor = WaterDataProcessor(file_name, start_date, end_date, target_param)
        processor.retrieve_data()
        processor.filter_columns_by_header(2)
        processor.preprocess_data()
        processor.apply_completeness_threshold(20)
        processor.save_data(final_file_name)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()