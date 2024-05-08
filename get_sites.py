import requests
import pandas as pd
from io import StringIO

# Takes around a minute to run
states = ['ca']

# List of water site types to include
surface_water = ['ES', 'LK', 'OC', 'OC-CO', 'ST', 'ST-CA', 'ST-DCH', 'ST-TS', 'WE']

# Target parameter
target_param = '00010'

responses = []

for state in states:
    url = f'https://waterservices.usgs.gov/nwis/site?format=rdb&stateCD={state}&siteStatus=active&parameterCd={target_param}'
    response = requests.get(url)
    responses.append(response.text)

combined_responses = '\n'.join(responses)

# Remove comment lines and prepare data for DataFrame
data = '\n'.join([line for line in combined_responses.splitlines() if '#' not in line])
data = StringIO(data)

# Read the data into a DataFrame
df = pd.read_csv(data, delimiter='\t', usecols=['site_no', 'site_tp_cd'])

# Filter the DataFrame to only include desired site types
df = df[df['site_tp_cd'].isin(surface_water)]

# Select desired columns
df = df[['site_no', 'site_tp_cd']]

# Write to CSV
df.to_csv('ca_water_sites.csv', index=False)
