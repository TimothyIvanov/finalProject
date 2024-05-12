import requests
import pandas as pd
from io import StringIO
from utils import timer

target_param = '00095'

class WaterSiteDataFetcher:
    def __init__(self, states, surface_water, final_filepath):
        self.states = states
        self.surface_water = surface_water
        self.target_param = target_param
        self.final_filepath = final_filepath

    #@timer
    #Fetch water site data from given state(s)
    def fetch_data(self, state):
        url = f'https://waterservices.usgs.gov/nwis/site?format=rdb&stateCD={state}&siteStatus=active&parameterCd={self.target_param}'
        response = requests.get(url)
        return response.text

    #@timer
    #Process sites into dataframe
    def filter_data(self, data):
        data = '\n'.join([line for line in data.splitlines() if '#' not in line])
        data = StringIO(data)
        df = pd.read_csv(data, delimiter='\t', usecols=['site_no', 'site_tp_cd'])
        df = df[df['site_tp_cd'].isin(self.surface_water)]
        return df

    #@timer
    #Save dataframe to CSV
    def save_data(self, df, filename):
        df.to_csv(filename, index=False)

    #@timer
    #Execute above
    def run(self):
        responses = [self.fetch_data(state) for state in self.states]
        combined_responses = '\n'.join(responses)
        filtered_df = self.filter_data(combined_responses)
        self.save_data(filtered_df, self.final_filepath)

@timer
#Get all sites that match state, site types, and have target_param column
def retrieve_sites():
    states = ['ca']
    site_types = ['ES', 'LK', 'OC', 'OC-CO', 'ST', 'ST-CA', 'ST-DCH', 'ST-TS', 'WE']
    final_filepath = 'ca_water_sites.csv'
    fetcher = WaterSiteDataFetcher(states, site_types, final_filepath)
    fetcher.run()

if __name__ == '__main__':
    retrieve_sites()
