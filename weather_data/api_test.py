import pandas as pd 
import requests
import numpy as np 
import sys, json
from auth_token import token 


head = {"token": token}
response =  requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&"+\
"locationid=FIPS:24&startdate=2021-11-01&enddate=2021-11-30&limit=1000", headers=head)
res = response.json()

precip, snow = [], []
temp_max, temp_min = [], []

for stamp in res['results']:
    if stamp['datatype'] =='PRCP':
        precip.append(stamp)
    elif stamp['datatype'] =='SNOW':
        snow.append(stamp)
    elif stamp['datatype'] =='TMAX':
        temp_max.append(stamp)
    elif stamp['datatype'] =='TMIN':
        temp_min.append(stamp)

precip_df = pd.DataFrame({'date': [stamp['date'] for stamp in precip], 'station': [stamp['station'] for stamp in precip], \
    'precip_amt': [stamp['value'] for stamp in precip]})
snow_df = pd.DataFrame({'date': [stamp['date'] for stamp in snow], 'station': [stamp['station'] for stamp in snow], \
    'snow_amt': [stamp['value'] for stamp in snow]})
temp_max_df = pd.DataFrame({'date': [stamp['date'] for stamp in temp_max], 'station': [stamp['station'] for stamp in temp_max], \
    'max_temp': [stamp['value'] for stamp in temp_max]})
temp_min_df = pd.DataFrame({'date': [stamp['date'] for stamp in temp_min], 'station': [stamp['station'] for stamp in temp_min], \
    'min_temp': [stamp['value'] for stamp in temp_min]})

comb_weath = precip_df.merge(snow_df, how='outer', on=['date', 'station'])
comb_temp = temp_max_df.merge(temp_min_df, how='outer', on=['date', 'station'])

comb_all = comb_weath.merge(comb_temp, how='outer', on=['date', 'station'])
comb_all['date'] = comb_all['date'].str[:10]
print(comb_all.min_temp.value_counts())
print(comb_all.head())