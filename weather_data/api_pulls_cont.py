import pandas as pd 
import requests
import numpy as np 
import sys, json, pdb
from auth_token import token 


head = {"token": token}

data_sets = ['GHCND', 'GSOM', 'GSOY', 'NEXRAD2',
             'NEXRAD3', 'NORMAL_ANN', 'NORMAL_DLY',
             'NORMAL_HLY', 'NORMAL_MLY', 'PRECIP_15',
             'PRECIP_HLY']

data_types = pd.read_csv('datatype_names.csv')

params = {}

res =  requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/"+
                         "data?datasetid=GHCND"+"&startdate=2021-11-01"+
                         "&enddate=2021-11-30&limit=1000", headers=head).json()

print(res['metadata'])

# pdb.set_trace()
# print(res)