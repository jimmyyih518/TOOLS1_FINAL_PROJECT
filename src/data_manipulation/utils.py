import pandas as pd
import json

def get_json_record(filename, record_name):
    with open(filename,'r') as f:
        data = json.loads(f.read()) 
    for item in data:
        output = {record_name:item[record_name]}
        yield output
        
def json_to_column(filename, record_name):
    df_col = get_json_record(filename, record_name)
    return pd.DataFrame(df_col)
        
        