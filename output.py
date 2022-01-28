# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 19:44:48 2022

@author: Sunny_Yaoyao
"""
import os
import pandas as pd
import json


def target_files(path, fmt):
    target = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            name, ext = os.path.splitext(fn)
            if ext in fmt:
                target.append(os.path.join(root, fn))
    return sorted(target, key=os.path.getmtime, reverse=False)

def load_json(file):
    if not os.path.isfile(file):
        data = {}
    else:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    return data

def combine_data(files):
    checked = load_json(os.path.join(os.getcwd(),'dl_files','已处理文件列表.json'))
    li = [pd.DataFrame()]
    for file in files:
        if file not in checked.keys():
            checked[file] = '1'
        else:
            continue    
        print(file)
        # lst=[pd.DataFrame()]
        
        filename = os.path.splitext(file.split('\\')[-1])[0]
        data_plate,date,month_rank,cate_1, cate_2,cate_3,cate_3_id = filename.split('_')
        
        df = pd.read_excel(file,index_col=None,header=0)       
        li.append(df)
        
    with open(os.path.join(os.getcwd(),'dl_files','已处理文件列表.json'), 'w') as f:
        json.dump(checked, f)
        
    return pd.concat(li, axis=0, ignore_index=True, sort=False)


if __name__ == '__main__':
    update_dir = os.path.join(os.getcwd(), 'dl_files')
    xls_files = target_files(update_dir,'.xls') 
    
    update_data = combine_data(xls_files)
    update_data[['一级类目','二级类目','三级类目','四级类目']]= update_data['细分类目'].str.split('>',expand=True)
    update_data.to_csv("csv/output.csv",index=False,header=True,encoding='utf-8-sig')
