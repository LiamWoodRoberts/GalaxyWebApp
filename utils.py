import json
import io
import numpy as np

def parse_table(output):
    '''takes prediction output of galaxy_api and returns columns and values
    in row format for easy html table parsing'''
    rows = [['']+list(output.keys())]
    for row in range(3):
        row_name = [list(output[list(output.keys())[0]].keys())[row]]
        rows.append(row_name+[round(list(output[col].values())[row],3) for col in output.keys()])   
    return rows[0],rows[1:]

def parse_response(r):
    '''accepts galaxy_api response and returns:
    
    image_path - path to random image
    cols - column names of prediction table
    parsed_pred - rounded row values for prediction table
    '''
    index = r['index']
    df = json.loads(r['df'])
    cols,values = parse_table(df)
    return index,cols,values