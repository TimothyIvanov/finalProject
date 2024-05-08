from dataretrieval import nwis

df, md = nwis.get_pmcodes()

df.to_csv('pmcodes.csv')