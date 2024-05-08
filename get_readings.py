import pandas as pd
from dataretrieval import nwis

# Load site data
data = 'ca_water_sites.csv'
sites = pd.read_csv(data, dtype={'site_no': str})['site_no']
sites_list = sites.tolist()

# Define the timeframe
start_date = '2024-05-01'
end_date = '2024-05-02'
target_param = '00010'

# DataFrame to store the results
results_df = pd.DataFrame()

df, md = nwis.get_iv(sites=sites_list,
                     start=start_date,
                     end=end_date)

# Filter to keep rows where '00010' is not NaN
df = df[df[target_param].notna()]

# Identify float64 columns starting from the third column
float_cols = df.iloc[:, 2:].select_dtypes(include=['float64']).columns.tolist()

# Combine the first two columns with the float64 columns from the third column onwards
selected_columns = df.columns[:2].tolist() + float_cols
df = df[selected_columns]

# Exclude '00010' from the columns to check for all NaNs
float_cols_to_check = [col for col in float_cols if col != target_param]

# Remove rows where all float64 values, excluding '00010', are NaN
df = df.dropna(subset=float_cols_to_check, how='all')

threshold = df.shape[0] / 20

df = df.dropna(axis=1, thresh=threshold)

# Identifying numeric headers beyond the second column
numeric_headers = [header for header in df.columns[2:] if header.isnumeric()]

# Preparing the list of columns to keep: first two columns and additional numeric columns
to_keep = df.columns[:2].tolist() + numeric_headers

# Creating a new DataFrame with the specified columns
df = df[to_keep]

# Save the filtered data to CSV
df.to_csv('filtered_data.csv')

# Print data types to confirm
print(df.dtypes)
