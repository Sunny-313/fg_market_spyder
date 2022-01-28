# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 18:06:08 2022

@author: Sunny_Yaoyao
"""

import os
import pandas as pd
import json
import re

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

def concat_data(*dirs,fmt=[]):
    root = os.path.abspath('')
    files = target_files(os.path.join(root,*dirs),fmt)

    def decorator(func):
        def wrapper(*args, **kwarge):
            sub_dir = os.path.join(root,'dl_files')
            checked = load_json(os.path.join(sub_dir,'已处理文件列表.json'))
            li = [pd.DataFrame()]
            for f in files:
                if f not in checked.keys():
                    checked[f] = '1'
                else:
                    continue
                kwarge['file'] = f
                df = func(*args, **kwarge)
                li.append(df)
            with open(os.path.join(sub_dir,'已处理文件列表.json'),'w')as f:
                json.dump(checked,f)
            return pd.concat(li,axis=0,ignore_index=True,sort=False)
        return wrapper
    return decorator    
@concat_data('dl_files',fmt=['.xls'])
def read_xls(file = None):
    print('正在打开：{}'.format(file))
    filename = os.path.splitext(file.split('\\')[-1])[0]
    data_plate,date,month_rank,cate_1, cate_2,cate_3,cate_3_id = filename.split('_')
    df = pd.read_excel(file,index_col=None,header=0)
    df['抖音浏览量'].replace('--',0,inplace=True)
    df['抖音浏览量'] = df['抖音浏览量'].astype(int)
    df['日期'] = date
    # df[['价格','价格_sub']]=df['商品券后价'].split('-',expand = True)
    # df[['一级类目','二级类目','三级类目','四级类目']] = df['细分类目'].str.split('>',expand=True)
    df['商品ID'] = df['商品链接'].map(lambda x:re.split('=|&',x)[1])
    return df

    
if __name__ == '__main__':
    file = read_xls()
    file.drop_duplicates()
    file[['价格','价格_sub']]=file['商品券后价'].str.split('-',expand = True)
    file[['一级类目','二级类目','三级类目','四级类目']] = file['细分类目'].str.split('>',expand=True)
    file.to_csv(os.path.abspath('csv\\output.csv'),index=False,encoding='utf-8-sig')
    