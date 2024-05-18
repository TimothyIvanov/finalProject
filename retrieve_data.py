import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataretrieval import nwis
from utils import timer

class WaterDataFetcher:
    def __init__(self, filepath, start_date, end_date, output_file, num_workers=12):
        self.filepath = filepath
        self.start_date = start_date
        self.end_date = end_date
        self.output_file = output_file
        self.num_workers = num_workers

    @timer
    #Fetch water data for sites using NWIS API
    def fetch_data_for_sites(self, sites):
        df, _ = nwis.get_iv(sites=sites,
                            start=self.start_date,
                            end=self.end_date)
        df.reset_index(inplace=True)
        return df

    @timer
    #Parallelization to speed up API calls
    def parallel_retrieve_data(self):
        sites = pd.read_csv(self.filepath, dtype={'site_no': str})['site_no'].tolist()
        n = len(sites) // self.num_workers + (len(sites) % self.num_workers > 0)
        chunks = [sites[i:i + n] for i in range(0, len(sites), n)]

        results = []
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = {executor.submit(self.fetch_data_for_sites, chunk): chunk for chunk in chunks}
            for future in as_completed(futures):
                results.append(future.result())

        combined_df = pd.concat(results, ignore_index=True)
        return combined_df

    @timer
    #Save data to CSV
    def save_data(self, df):
        df.to_csv(self.output_file, index=False)

    def run(self):
        try:
            combined_df = self.parallel_retrieve_data()
            self.save_data(combined_df)
        except Exception as e:
            print(f"An error occurred: {e}")

@timer
#Get data from sites in ca_water_sites.csv within given date range using NWIS API
def retrieve_data_from_sites():
    filepath = 'ca_water_sites.csv'
    start_date = '2024-05-01'
    end_date = '2024-05-01'
    final_filepath = 'dirty_data.csv'
    fetcher = WaterDataFetcher(filepath, start_date, end_date, final_filepath)
    fetcher.run()

if __name__ == '__main__':
    retrieve_data_from_sites()
