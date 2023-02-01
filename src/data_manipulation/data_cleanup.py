# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 21:09:03 2023
@author: MZ-Alienware
"""

import pandas as pd, numpy as np
import json
import re

"""
NOTES:
>>DONE calculate price/sqft
>>DONE remove rows where any(price,bedrooms,bath) is none
>>add include/exclude observation flag
"""

## Turn off panda warnings
pd.set_option('mode.chained_assignment', None)


def clean_json(json_file):
    ## Option2: using json_normalize
    with open(json_file,'r') as f:
        data = json.loads(f.read())    
    
    data_df = pd.json_normalize(data)
    
    ## List of columns to keep
    columns = ['buildingId','lotId','price','minBeds','minBaths','minArea','unitCount','isBuilding','address'
               ,'statusText','detailUrl','latLong.latitude','latLong.longitude','beds','baths','area','pgapt'
               ,'hdpData.homeInfo.city','hdpData.homeInfo.state','hdpData.homeInfo.latitude','hdpData.homeInfo.longitude'
               ,'hdpData.homeInfo.price','hdpData.homeInfo.bathrooms','hdpData.homeInfo.bedrooms','hdpData.homeInfo.livingArea'
               ,'hdpData.homeInfo.homeType','hdpData.homeInfo.homeStatus','hdpData.homeInfo.daysOnZillow'
               ,'additional_details.details','statusType','listingType','hasAdditionalAttributions']
    
    ## Create a new dataframe with columns indicated above
    data_df2 = data_df[columns]
    
    #data_df2.rename(columns = {'additional_details.summary':'additional_details_summary'}, inplace = True)
    
    ## Clean up price
    data_df2['price_final'] = data_df2['price'].apply(lambda x: proc_price(x))
    
    data_df2['bedroom_final'] = np.where(data_df2['hdpData.homeInfo.bedrooms'].isnull()
                                              ,data_df2['beds'],data_df2['hdpData.homeInfo.bedrooms'])
    data_df2['bathroom_final'] = np.where(data_df2['hdpData.homeInfo.bathrooms'].isnull()
                                               ,data_df2['baths'],data_df2['hdpData.homeInfo.bathrooms'])
    
    data_df2['has_garage_final'] = 0 # placeholder to indicate if garage is available
    data_df2['has_parking_final'] = 0 # placeholder to indicate if parking is available
    
    data_df2['sqft_final'] = np.where(data_df2['area'].isnull()
                                              ,data_df2['hdpData.homeInfo.livingArea'],data_df2['area'])
    
    data_df2['city_final'] = data_df2['hdpData.homeInfo.city']
    data_df2['state_final'] = data_df2['hdpData.homeInfo.state']
    data_df2['lat_final'] = np.where(data_df2['latLong.latitude'].isnull()
                                     ,data_df2['hdpData.homeInfo.latitude'],data_df2['latLong.latitude'])
    data_df2['long_final'] = np.where(data_df2['latLong.longitude'].isnull()
                                     ,data_df2['hdpData.homeInfo.longitude'],data_df2['latLong.longitude'])
    

    columns = ['price_final','bedroom_final','bathroom_final','has_garage_final'
               ,'has_parking_final','sqft_final','city_final','state_final'
               ,'lat_final','long_final'
               ]    
    
    ## Rename columns
    df_final = data_df2[columns]
    dict = {'price_final':'price','bedroom_final':'bedrooms','bathroom_final':'bathrooms'
               ,'has_garage_final':'has_garage','has_parking_final':'has_parking','sqft_final':'sqft'
               ,'city_final':'city','state_final':'state','lat_final':'latitude','long_final':'longitude'
               }
    df_final.rename(columns=dict,inplace=True)
    
    ## Remove rows with missing values in any column
    df_final.replace('', np.nan, inplace=True)
    df_final.dropna(inplace=True)
    
    ## Additional calculation
    df_final['price/sqft'] = df_final['price'] / df_final['sqft']
    
    #print(df_final)
    
    ## Export to csv
    df_final.to_csv('zillow_data.csv')
    return df_final

def remove_special_characters(string):
    return re.sub(r"[^a-zA-Z0-9]+", "", string)

def return_numeric(expr):
    for s in expr:
        output = str("".join(filter(str.isdigit, expr)))
        return float(output)

def proc_price(raw_input):
    return return_numeric(raw_input)

def proc_garage(raw_input):
    raw_input = remove_special_characters(raw_input)
    if raw_input.find('garage') != -1:
        return 1
    else:
        return 0


if __name__ == '__main__'    :
    
    clean_json('zillow_listing_data_CA_BC.json')
    