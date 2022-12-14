# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:31:59 2022

@author: Benjamin Ojo
"""
# Import packages. 
import pandas as pd 
import os 

# Excel packages.
from openpyxl import Workbook as wb 
from openpyxl import load_workbook as lwb

# File name.
cont_folder = 'C:/Users/User1/Documents/Data_Project/excel_data-wrangler/excel_files/container_file'

# Print list of file in a folder. 
files = os.listdir(cont_folder)

# Container code 
codes = []

for file in files:
    extr = file.split(' ')[1].split('.')[0]
    codes.append(extr)

for num in range(len(codes)): 
    # loaing packages.
    xl = pd.read_excel('extract_2022-11.xlsx', sheet_name = codes[num],
                       engine='openpyxl', na_values=['nan'])
    
    print(f"FORMATING: {codes[num]},\n")
    
    # Getting the container numbers.
    c_list = []
    
    for i in range(4): 
        c = xl.iloc[i, :].dropna().to_list()
        c = [str(d) for d in c]
        c_list.append(c)
        
    for j in range(len(c_list)): 
        if len(c_list[j])>=1 and c_list[j][0][:3] == 'CON':
            code = c_list[j][0]
            code_idx = j
            header_idx = j + 1
            break
    
    # Column Header. 
    columns = xl.iloc[header_idx,:].to_list()
    
    # # converting first row to header. 
    xl.columns = columns
    
    # Deleting rows
    xl.drop([i for i in range(header_idx+1)], axis=0, inplace=True)
    
    # Reset_index
    xl.reset_index(drop = True)
    
    # Creating columns.
    xl['CONTAINER_CODE'] = code
    xl['SUPPLIER_NAME'] = ' '
    
    # Drop s/n column.
    del xl[xl.columns[0]]
    
    # Supplier and item code list 
    supplier = xl['DESCRIPTION'].fillna('re').to_list()
    item_code = xl['CODE'].fillna('re').to_list()
    quantity = xl['QUANTITY'].fillna('re').to_list()
    
    # Extracting Supplier name for row. 
    supplier_name = []
    
    for i in range(len(supplier)):
        if supplier[i] != 're' and item_code[i] == 're' and quantity[i] == 're':
            supplier_name.append(supplier[i])
        elif supplier[i] == 're' and item_code[i] == 're'and quantity[i] == 're':
            supplier_name.append('delete_row')
        else:
            cont=supplier_name[-1].replace('~', '')
            supplier_name.append(f'{cont}~')
    
    # Defining supplier name
    xl['SUPPLIER_NAME'] = supplier_name
    
    # Rows to Delete.
    delete_row = xl[xl['SUPPLIER_NAME'] == 'delete_row'].index.to_list()

    # Drop rows. 
    xl.drop(delete_row, axis = 0, inplace = True)
   
    # Reset index. 
    xl = xl.reset_index(drop = True)
    
    # Rows that aren't needed.
    sup_del = xl[xl['SUPPLIER_NAME'] == xl['DESCRIPTION']].index
    
    # Drop rows. 
    xl.drop(sup_del, axis = 0, inplace = True)

    
    # Reset index. 
    xl = xl.reset_index(drop = True)
    
    # Reordering columns 
    xl = xl.loc[:, xl.columns[-2:].to_list() + xl.columns[:-2].to_list()]
    
    # Saving file
    xl.to_csv(f'csv_files/{codes[num]}.csv', index = False)
    print(f'SAVING: {codes[num]}.csv', '\n\n')
    
    



    
    

    
    
    
