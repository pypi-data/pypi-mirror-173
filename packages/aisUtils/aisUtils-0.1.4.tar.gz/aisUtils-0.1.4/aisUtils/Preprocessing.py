# AIS preprocessing

import ais
import csv
import os
import pandas as pd
import numpy as np
import requests
from retrying import retry
import json
import os
import time
import random

# decoder
def decode(sourcePath, desPath, timestr):
    # 1. 创建文件对象
    ff = open(desPath,'a',encoding='utf-8',newline='' "")
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(ff)
    # 3. 构建列表头
    csv_writer.writerow(["timestamp", "MMSI","Lon","Lat","Cog","Sog"])

    with open(sourcePath,'r') as f:
        count = 0
        lines = f.readlines()
        sum = len(lines)
        # count = 0
        for line in lines:
            line = line.strip('\n')
            nmeamsg = line.split(',')
            #print(nmeamsg)
            if nmeamsg[0] == '!AIVDM':
                    if nmeamsg[1] == '1':
                        try:
                            decodedata = ais.decode(nmeamsg[5], int(nmeamsg[6].split('*')[0]))
                            #print(decodedata)
                            #break
                            #print(timestr + ' ' + str(decodedata['mmsi']) + ' ' + str(decodedata['x'])  + ' ' + str(decodedata['y']) + ' ' + str(decodedata['rot']) + ' ' + str(decodedata['sog']))
                            if decodedata['id'] == 1:
                                # 时间戳 MMSI 经度 纬度 对地航向 对地航速
                                #ff.write(timestr + ' ' + str(decodedata['mmsi']) + ' ' + str(decodedata['x'])  + ' ' + str(decodedata['y']) + ' ' + str(decodedata['cog']) + ' ' + str(decodedata['sog']))
                                #ff.write('\n\n')
                                resstr = timestr + '*' + str(decodedata['mmsi']) + '*' + str(decodedata['x'])  + '*' + str(decodedata['y']) + '*' + str(decodedata['cog']) + '*' + str(decodedata['sog'])
                                sstr = resstr.split('*')
                                #print(sstr)
                                # 4. 写入csv文件内容
                                csv_writer.writerow(sstr)
                        except:
                            pass
            else:
                if nmeamsg[0] == "$GPRMC":
                    timestr = '20' + nmeamsg[9][4:6] + '-' + nmeamsg[9][2:4] + '-' + nmeamsg[9][0:2] + ' ' + nmeamsg[1][0:2]+':'+nmeamsg[1][2:4]+':'+nmeamsg[1][4:6]
            count += 1
            if count % 10000 == 0:
                percent = int(count * 100 /sum)
                print("========= Decoding progress " + str(percent)+ '% =========')

    f.close()
    ff.close()
    print("File written successfully!")
    '''
    批量解码写入代码
    import os

    path = r'D:\code\python\data'
    fileList = os.listdir(path)
    data=fileList[0][:10]
    fileName = data + "_AIS_data.csv"
    print(fileName)

    '''  

# crawl
# read all filenames in the directory
def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            L.append(os.path.join(root, file))  
    return L 

# append mmsi in list and remove the same
def getMmsiList(path):
    mmsi = []
    # 统计出所有文件的MMSI
    files = file_name(path)
    for i in range(len(files)):
        nowFile = files[i]
        print(nowFile)
        data = pd.read_csv(nowFile)
        data = data.dropna()
        data_p = data.iloc[:, 1]
        data_p.columns = ['mmsi']
        
        for i in range(len(data_p)):
            if data_p[i] not in mmsi:
                mmsi.append(data_p[i])

    return mmsi

def writeMmsiList(desPath, mmsilist):
    ff = open(desPath,'a',encoding='utf-8',newline='' "")
    csv_writer = csv.writer(ff)
    csv_writer.writerow(["MMSI",""])
    for i in range(len(mmsilist)):
        #print(type(mmsi[i]))
        csv_writer.writerow([mmsilist[i], ""])
    print("File written successfully")


@retry(stop_max_attempt_number=10, wait_fixed=1000)
def _post_request(post_url, get_url_mine, post_data, post_headers):
    post_session = requests.session()
    post_session.post(post_url, data=post_data, headers=post_headers)
    post_response = post_session.get(
        get_url_mine, headers=post_headers, timeout=1)
    return post_response.content.decode()


def post_request(post_url, get_url_mine, post_data, post_headers):
    try:
        post_res = _post_request(
            post_url, get_url_mine, post_data, post_headers)
        # print('POST Request Content:\n', post_res)
    except Exception:
        post_res = 'Post Request Failed.'
    return post_res


def get_request(request_url, get_headers, cookie_para):
    get_session = requests.session()
    for k, v in cookie_para.items():
        get_session.cookies.set(k, v)
    get_response = get_session.get(request_url, headers=get_headers)
    return get_response.content.decode()


def save_post_data(post_res):
    try:
        with open('douban_post_res.html', 'w', encoding='utf-8') as f:
            f.write(post_res)
        print('Save Post Data Successfully.')
    except(IOError, TimeoutError):
        print('Save Post Data Failed.')


def parse_data(get_str):
    list_s1 = json.loads(get_str)
    list_s2 = list_s1['subject_collection_items']
    total = list_s1['total']
    count = list_s1['count']

    return list_s2, total, count


def file_exit_dec(file_name):
    try:
        os.remove(file_name)
    except IOError:
        print('File does not exit, now you can append the file by "with open"! ')


def save_data(list_data, file_name):
    try:
        with open(file_name, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
        print('Save Data Successfully!')
    except(IOError, Exception):
        print('Failed Saving The Data.')


def get_MMSI_from_file(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        headings = next(reader)
        columnMMSI = [row[0] for row in reader]
        return columnMMSI

def crawl(mmsiFileName, get_file_name):
    getShipInfo_url = 'https://ais.msa.gov.cn/api/app/baseOnMyshipsAISInfo/rtAndStaticData?mmsi={}&type=0&time={}'

    # ******************************************************************************************************
    # GET请求，获取AIS静态数据
    # 1、GET请求数据准备
    headers = {'User-Agent': 'ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Referer': 'https://ais.msa.gov.cn/',
            'token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJmMDQ0ZWRhOGYyZjU0NzVmYWNlNjVlYWQ4OGY2ZDU2NiIsImlhdCI6MTYzOTk5ODQ1NiwiZXhwIjoxNjQwMDA1NjU2fQ.-2-zWN3kp0FGDkDYfeNKWlo83NhjUweOWeLlS0q4qpGvZaGaCPQHwHRt0QXbEIy8-D2iC-fPwU2O3D_QqY1vzQ'
            }
    get_cookie = 'Hm_lvt_89a42a8529b1127d2cd6fa639511a328=1637650925,1637651122,1637651152; SERVERID=bbddf5345b978da05428502c7dbe55a1|1642336770|1642336770'
    cookie_para = {get_co.split('=')[0]: get_co.split('=')[1] for get_co in get_cookie.split('; ')}

    #mmsiFileName = "mmsiall.csv"
    ListMMSI = get_MMSI_from_file(mmsiFileName)

    #get_file_name = 'staticData.csv'


    def nowTime(): return int(round(time.time() * 1000))


    #file_exit_dec(get_file_name)

    get_session = requests.session()
    for k, v in cookie_para.items():
        get_session.cookies.set(k, v)
    get_session.headers.update(headers)

    df = pd.DataFrame()
    i = 0
    for mmsi in ListMMSI:
        get_url = getShipInfo_url.format(mmsi, nowTime())
        get_response = get_session.get(get_url)
        ret = get_response.content.decode()
        resDic = json.loads(ret)
        if resDic['code'] == 200 and resDic['message'] == '成功':
            staticDic = resDic['data']
            df = df.append(staticDic, ignore_index=True)
            #print(df)
        else:
            print("error")
        
        if i%30 == 0:
            df.to_csv(get_file_name, mode='a', index=None)
            df = df.drop(index=df.index)
        i += 1
        print("=============",i)
        time_sleep = random.random()
        time.sleep(time_sleep)

    df.to_csv(get_file_name, mode='a', index=None)

# match
def match(staticDataPath, aisPath, desPath):
    # 读取静态文件
    staticDataPath = r'D:/python/staticData.csv'
    staticData = pd.read_csv(staticDataPath)

    # 读取ais文件
    aisPath = r'D:/data/2021-08-28_output.csv'
    data = pd.read_csv(aisPath)

    data['shiptype'] = ''
    data['length'] = ''
    sum = 0

    mmsi_in_data_p = []
    shiptype_in_data_p = []
    length_in_data_p = []

    data_p = data.values
    staticData_p = staticData.values

    length_data = len(data)
    length_staticData = len(staticData)

    # 统计所有的mmsi号
    for i in range(length_data):
        if data_p[i][1] not in mmsi_in_data_p:
            mmsi_in_data_p.append(data_p[i][1])
    
    # 统计所有船长和船型
    flag = 0
    for i in range(len(mmsi_in_data_p)):
        for j in range(length_staticData):
            if mmsi_in_data_p[i] == staticData_p[j][0]:
                #print(mmsi_in_data_p[i])
                shiptype_in_data_p.append(staticData_p[j][7])
                length_in_data_p.append(staticData_p[j][17])
                sum += 1
                flag = 1
                break
            flag = 0
        if flag == 0:
            shiptype_in_data_p.append(-1)


    #   shiptype除去货物位
    for i in range(len(shiptype_in_data_p)):
        if shiptype_in_data_p[i] >= 10:
            shiptype_in_data_p[i] = int(shiptype_in_data_p[i] / 10)

    # 匹配到原表格并写成文件
    sum = 0
    for i in range(length_data):
        # print(i)
        iindex = mmsi_in_data_p.index(data_p[i][1])
        #data_p[i][6] = shiptype_in_data_p[iindex]
        #data_p[i][7] = length_in_data_p[iindex]
        data.loc[i, 'shiptype'] = shiptype_in_data_p[iindex]
        data.loc[i, 'length'] = length_in_data_p[iindex]

    ff = open(desPath,'a',encoding='utf-8',newline='' "")
    csv_writer = csv.writer(ff)
    csv_writer.writerow(["timestamp", "MMSI","Lon","Lat","Cog","Sog", 'Shiptype', 'Length'])
    for i in range(len(data)):
        csv_writer.writerow(data.loc[i])

# others
def filtering(sourcePath, desPath, max_Lon, min_Lon, max_Lat, min_Lat, speed, shiptype_list):
    data = pd.read_csv(sourcePath)
    data = data.dropna()
    data_p = data.values

    i = 0
    flag = 1

    while i < len(data_p):
        # print(i)
        # flag置为1
        flag = 1
        # 区域判断
        if (data_p[i][3] < min_Lat) or (data_p[i][3] > max_Lat) or (data_p[i][2] < min_Lon) or (data_p[i][2] > max_Lon):
            flag = 0
        # 速度判断 
        if data_p[i][5] <= speed[0] or data_p[i][5] > speed[1]:
            flag = 0
        # 船型判断
        #shiptype_list = [6, 7, 8]
        if data_p[i][6] not in shiptype_list:
            flag = 0
        if flag == 0:
            # 删除数据所在的行
            data_p = np.delete(data_p,i,0)
            i -= 1
        i += 1
    
    ff = open(desPath,'a',encoding='utf-8',newline='' "")
    csv_writer = csv.writer(ff)
    csv_writer.writerow(["timestamp", "MMSI","Lon","Lat","Cog","Sog", 'Shiptype', 'Length'])
    for i in range(len(data_p)):
        csv_writer.writerow(data_p[i])
