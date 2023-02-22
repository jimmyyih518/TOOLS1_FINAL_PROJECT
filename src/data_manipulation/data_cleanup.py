# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 21:09:03 2023
@author: MZ-Alienware
"""

import pandas as pd, numpy as np
import json
import re

"""
Data cleanup process:
    1.Read JSON file and convert to dataframe
    2.Remove unwanted columns
    3.Process columns
"""

## Turn off panda warnings
pd.set_option('mode.chained_assignment', None)

def clean_json_file(filename):
    with open(filename,'r') as f:
        data = json.loads(f.read()) 
    return clean_data(data)

def clean_data(list1):    

    
    data_df = pd.json_normalize(list1)
    
    ## List of columns to keep
    columns = ['buildingId','lotId','price','minBeds','minBaths','minArea','unitCount','isBuilding','address'
               ,'statusText','detailUrl','latLong.latitude','latLong.longitude','beds','baths','area','pgapt'
               ,'hdpData.homeInfo.city','hdpData.homeInfo.state','hdpData.homeInfo.latitude','hdpData.homeInfo.longitude'
               ,'hdpData.homeInfo.price','hdpData.homeInfo.bathrooms','hdpData.homeInfo.bedrooms','hdpData.homeInfo.livingArea'
               ,'hdpData.homeInfo.homeType','hdpData.homeInfo.homeStatus','hdpData.homeInfo.daysOnZillow'
               ,'additional_details.details','statusType','listingType','hasAdditionalAttributions','distance_to_waterfront'
               ,'query_city']

    ## Create a new dataframe that includes the columns indicated above
    data_df2 = data_df[columns]
    
    data_df2['additional_details.details'] = data_df2['additional_details.details'].fillna('NA')
    
   
    ## Clean up price
    #data_df2['price_final'] = data_df2['price'].apply(lambda x: proc_price(x)) # Moving this step to the notebook
    
    data_df2['price_final'] = data_df2['price']
    
    data_df2['bedroom_final'] = np.where(data_df2['hdpData.homeInfo.bedrooms'].isnull()
                                              ,data_df2['beds'],data_df2['hdpData.homeInfo.bedrooms'])
    
    data_df2['bathroom_final'] = np.where(data_df2['hdpData.homeInfo.bathrooms'].isnull()
                                               ,data_df2['baths'],data_df2['hdpData.homeInfo.bathrooms'])
    
    data_df2['sqft_final'] = np.where(data_df2['area'].isnull()
                                              ,data_df2['hdpData.homeInfo.livingArea'],data_df2['area'])
    



    data_df2['city_final'] = data_df2['hdpData.homeInfo.city']
    data_df2['state_final'] = data_df2['hdpData.homeInfo.state']
    data_df2['lat_final'] = np.where(data_df2['latLong.latitude'].isnull()
                                     ,data_df2['hdpData.homeInfo.latitude'],data_df2['latLong.latitude'])
    data_df2['long_final'] = np.where(data_df2['latLong.longitude'].isnull()
                                     ,data_df2['hdpData.homeInfo.longitude'],data_df2['latLong.longitude'])
    
    data_df2['homeType_final'] = data_df2['hdpData.homeInfo.homeType']
    data_df2['homeStatus_final'] = data_df2['hdpData.homeInfo.homeStatus']

    data_df2['distance_to_waterfront_final'] = data_df2['distance_to_waterfront']

    data_df2['additional_info'] = data_df2['additional_details.details'].apply(lambda x:parse_data(x))        

    
    data_df2 = pd.concat([data_df2, data_df2["additional_info"].apply(pd.Series)], axis=1)

    data_df2['garage_stalls'] = data_df2['garage_stalls'].fillna(0)
    data_df2['features'] = data_df2['features'].fillna('NA')
    data_df2['ind_HasPool'] = data_df2['features'].str.lower().str.contains('pool')
    data_df2['ind_GolfCourseNearby'] = data_df2['features'].str.lower().str.contains('golf')
    data_df2['ind_ShoppingNearby'] = data_df2['features'].str.lower().str.contains('shopping')
    data_df2['ind_Clubhouse'] = data_df2['features'].str.lower().str.contains('clubhouse')
    data_df2['ind_RecreationNearby'] = data_df2['features'].str.lower().str.contains('recreation')
    data_df2['ind_ParkNearby'] = data_df2['features'].str.lower().str.contains('park nearby')
    data_df2['ind_IsCornerLot'] = data_df2['features'].str.lower().str.contains('corner lot')
    data_df2['ind_IsCuldesac'] = data_df2['features'].str.lower().str.contains('cul-de-sac')


    data_df2['overview'] = data_df2['additional_details.details'] # Added this step to display on the notebook
    
    #data_df2.to_csv('data_df2.csv') # For testing only

    columns = ['price_final','bedroom_final','bathroom_final','sqft_final','city_final','state_final'
               ,'lat_final','long_final','homeType_final','homeStatus_final'
               ,'distance_to_waterfront_final'
               ,'additional_info'
               ,'garage_stalls','features'
               ,'ind_HasPool','ind_GolfCourseNearby','ind_ShoppingNearby','ind_Clubhouse','ind_RecreationNearby'
               ,'ind_ParkNearby','ind_IsCornerLot','ind_IsCuldesac'
               ,'overview','query_city'
               ]    
    
    ## Rename columns
    df_final = data_df2[columns]
    dict = {'price_final':'price','bedroom_final':'bedrooms','bathroom_final':'bathrooms'
               ,'sqft_final':'sqft'
               ,'city_final':'city','state_final':'state','lat_final':'latitude','long_final':'longitude'
               ,'homeType_final':'homeType','homeStatus_final':'homeStatus'
               ,'distance_to_waterfront_final':'distance_to_waterfront'
               ,'garage_stalls':'ind_HasGarage'
               }               

    df_final.rename(columns=dict,inplace=True)
    
    ## Remove rows with missing values in any column
    df_final.replace('', np.nan, inplace=True)
    df_final.dropna(inplace=True)
    

    ## Additional cleanup    
    df_final = df_final[df_final['sqft'] > 0]
    df_final = df_final[df_final['state'] != 'WA']

    ## Additional calculation
    #df_final['price/sqft'] = df_final['price'] / df_final['sqft'] # Moving this step to the notebook

    ## Replace inf values with 0
    df_final.replace([np.inf,-np.inf],0,inplace=True)
    
    return df_final

def remove_special_characters(string):
    return re.sub(r"[^a-zA-Z0-9]+", "", string)

def return_numeric(expr):
    for s in expr:
        output = str("".join(filter(str.isdigit, expr)))
        return float(output)

def proc_price(raw_input):
    return return_numeric(raw_input)

def parse_data(data):
    # Extract the number of garage stalls
    garage_stalls = re.search(r"Garage spaces: (\d+)", data)
    if garage_stalls:
        garage_stalls = int(garage_stalls.group(1))
    else:
        garage_stalls = None

    # Extract everything between "features: " to "Other property information"
    features = re.search(r"Lot features: (.*?)Other property information", data, re.DOTALL)
    if features:
        features = features.group(1)
    else:
        features = None

    return {
        "garage_stalls": garage_stalls,
        "features": features,
    }

def runTest():
    file = 'zillow_all_listings_scraped.json'
    # with open(file,'r') as f:
    #     data = json.loads(f.read())        

    df = clean_json_file(file)     
    #print(df.dtypes)
    
    print(df.head())
    #df.to_csv('zillow_data_clean.csv')
    return df
    
def removeOutliers(data, col):
    Q3 = np.quantile(data[col], 0.90)
    Q1 = np.quantile(data[col], 0.10)
    IQR = Q3 - Q1
 
    #print("IQR value for column %s is: %s" % (col, IQR))
    global outlier_free_list
    #global filtered_data
 
    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR
    outlier_free_list = [x for x in data[col] if (
        (x > lower_range) & (x < upper_range))]
    filtered_data = data.loc[data[col].isin(outlier_free_list)]    
    return filtered_data
##---------------------------------------------------------------------------##
#df = runTest()
#df.to_csv('df_test.csv')