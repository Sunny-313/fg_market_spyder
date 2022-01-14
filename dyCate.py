# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:49:02 2022

@author: Sunny_Yaoyao
"""

import json
import os
import pandas as pd
import requests
import time
import random

def load_json(file):
    if not os.path.isfile(file):
        data = {}
    else:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    return data

def req_get(url, headers={}, params={}, cookies={}):
    r = requests.Request('GET', url, headers=headers, params=params, cookies=cookies)
    req = r.prepare()
    
    print('{}\n{}\r\n{}\r\n'.format(
        '-----------START-----------', 
        req.method + ' ' + req.url, 
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items())
        ))
    
    s = requests.Session()
    return s.send(req, timeout=10)

def make_path(*dirs):
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, *dirs)

def is_file(file):
    if os.path.isfile(file):
        print('File is already existed: %s' % file)
        return True
    return False

def save_xls(data, file):             
    with open(file, 'wb') as f:
        f.write(data)
    print(f"保存文件: {file}")
    print(f"文件大小: {round(os.path.getsize(file) / float(1024), 2)} KB")
    
dy_cate = load_json('raw_data/dy_cate.json')

'''将json文件解析DateFrame'''
df = pd.DataFrame(dy_cate)

'''
  - 根据飞瓜的前端显示将CateIds限制为3
  - 将美妆类目的筛选出来
'''
df['len'] = df.loc[~df['CateIds'].isnull()]['CateIds'].apply(lambda x:len(x))
df['rootCateId'] = df.loc[~df['CateIds'].isnull()]['CateIds'].apply(lambda x:x[0])
df = df[(df['len']==3)& (df['rootCateId'] =='115')]

'''对可变参数进行处理'''

cookies = {
    'CurrentRank_1231435': '1',
    'searchnew': '1',
    'FEIGUA': 'UserId=ec037c8ffb941a9da2450f705ccf08c0&NickName=f630425fc928a193f46be8e1d7441f13&checksum=0abd8ffbc634&FEIGUALIMITID=b315c99b6a6449f49027df063242a8a5',
    '46aa4766490e550d32fcafd86e541c3c': '11c014ebad67002f7ad1f454a99db94fc3f5b84015a990ffc0eaa9197a9d15844fb7c997149c9adf303046271c02de5e908f7542aa6f91a75a1902e26486a2afcdadf8c74fff9deb51ee67e1067bb63c044101a12c3b10892a3ebccf73882293fee7c5c573271754101a625efe49e5ac',
    'ASP.NET_SessionId': 'lp1hsvgn4bjs15g0n5zr0mf2',
    'Hm_lvt_876e559e9b273a58993289470c10403b': '1640828028,1641606130,1641791783,1641797424',
    'Hm_lpvt_876e559e9b273a58993289470c10403b': '1641800322',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://dy.feigua.cn/Member',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

params = (
    ('period', 'month'),
    ('cateid', 'undefined'),
    ('tagid', 'undefined'),
    ('sort', 'SalesCount'),
    ('datecode', ''),
    ('mainAgeId', 'undefined'),
    ('gender', 'undefined'),
    ('lowPrices', '0'),
    ('islowprice', '0'),
    ('goodPercent', 'undefined'),
    ('awemeSalesRatio', '-1'),
    ('mainSalesModel', '-1'),
    ('dhz_value', ''),
    ('shopsource', '20'),
    ('isNew', '0'),
    ('isUnfold', 'true'),
    ('cate0', '0'),
    ('cate1', '0'),
    ('cate2', '0'),
)
# params为元组类型，元组不可更改，需要将其转化为dict字典类型
p = dict(params)
# 将需要日期写在一个list中，用于遍历
# ['202112','202111','202110','202109','202108','202107','202106','202105','202104',
date =['202103','202102','202101']

for d in date:
    p['datecode'] = d
    for r in df.iterrows():
        cate_name = r[1]['DisplayName'].replace('>', '_')
        cate_name = cate_name.replace('/', '#')
        filename = '飞瓜数据_{}_{}_{}.xls'.format(d,cate_name,r[1]['CateIds'][2])
        
        file_path = make_path('dl_files',filename)
        if is_file(file_path):
            continue
        # 处理参数
        p['cate0'],p['cate1'],p['cate2']= r[1]['CateIds']
        
        try:
            response = req_get('https://dy.feigua.cn/Rank/ExportPromotionDouyin',headers=headers,params=p,cookies=cookies)                           
            save_xls(response.content,file_path)
        except Exception as e:
            print("Error: ", e)

        delay = random.randint(300000,1000000)/10000
        print('延迟时长 %f s' % delay)
        time.sleep(delay)
         



