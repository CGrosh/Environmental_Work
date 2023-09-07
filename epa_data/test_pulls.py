import pandas as pd 
import requests, json, sys 
import numpy as np 
import pdb
import sqlite3 as db 
from tqdm import tqdm 


def concat_dict(dict_1, dict_2):

    dict_1_keys, dict_2_keys = list(dict_1.keys()), list(dict_2.keys())
    dict_return = dict_1.copy()
    
    if dict_1_keys != dict_2_keys:
        print('mismatch in keys')
        return dict_return 
    else:
        if type(dict_return[dict_1_keys[0]]) == type(list()):
            for key in dict_1_keys:
                dict_return[key].append(dict_2[key])
        else:
            for key in dict_1_keys:
                dict_return[key] = [dict_return[key], dict_2[key]]
        return dict_return 
    

def combine_dict_list(lst):
    ret_dict = lst[0].copy()
    for val in range(1,len(lst)):
        ret_dict = concat_dict(ret_dict, lst[val])
    return pd.DataFrame(ret_dict)


def query_gen(url_base, num_rows):
    # url_base will look like 
    # "https://data.epa.gov/efservice/rlps_ghg_emitter_gas/"

    samp_size = 10000
    batch_size = round(num_rows/samp_size)

    samp_range = []
    for val in range(1,batch_size+1):
        start = (val*samp_size)-samp_size
        end = (val*samp_size)
        if end >= num_rows:
            end = num_rows 
        else:
            end = end-1
        samp_range.append('{}:{}'.format(start, end))
    
    url = url_base+'/rows/'
    urls = [url+'{}/json'.format(i) for i in samp_range]

    data = pd.DataFrame()
    for i in tqdm(range(len(urls))):
        # print(urls[i])
        res = requests.get(urls[i]).json()
        if len(res) == 0:
            break
        else:
            data = data.append(combine_dict_list(res), ignore_index=True)
    
    return data


url_input = 'tri_facility_history'
data_sector = 'toxic_release'
url_pass = "https://data.epa.gov/efservice/"

url_full = url_pass+url_input

# res = requests.get(url_full+'rows/{}/json'.format('0:2'))

# print(res.json())

df_check = query_gen(url_full, 700000)

pdb.set_trace()


df_check.to_csv('data/epa_{}_{}_df.csv'.format(url_input, data_sector))

