# -*- coding: utf-8 -*-
import requests
import os
import json
import hashlib
from lib.file.file_Class import writeFile
from conf.conf import base_root
from lib.core.w_threadPool import MyThreadPool

def updataCmsPrintJson(url=None,json_path=None):
    if url == None:
        url = 'https://raw.githubusercontent.com/Lucifer1993/cmsprint/master/cmsprint.json'
    if json_path == None:
        json_path = '{}payload/others/cmsprint.json'.format(base_root)
    resp = requests.get(url,verify=False)
    try:
        os.system('rm -rf {}'.format(json_path+'.bak'))
        os.system('mv {} {}'.format(json_path,json_path+'.bak'))
    except:
        pass
    writeFile(json_path,resp.text)

#读文件
def readJsonFile(FILE):
    f = open(FILE, 'r+')
    str_json = f.read()
    temp = str_json.replace("'", '"')  # 将 单引号 替换为 双引号
    temp = json.loads(temp)  # loads 将 字符串 解码为 字典
    return temp

def getCMS_Name(sign_json,target_url):
    result = []
    if target_url[-1] == '/':               #剔除url结尾的/
        target_url = target_url[:-2]
    if sign_json['checksum']:
        target_url = target_url + sign_json['staticurl']
        try:
            print(target_url)
            resp = requests.get(target_url, timeout=10,verify=False)  # 默认超时时间为10s，可设置
            # print(resp.text)
            hh_md5 = hashlib.md5(resp.text.encode()).hexdigest()
            if hh_md5 == sign_json['checksum']:
                print('URL {} maybe is {}'.format(target_url,sign_json['remark']))
                result.append('{} :{} {}'.format(target_url,sign_json['cmsname'],sign_json['remark']))
            else:
                # print('URL {} is not {}'.format(target_url, sign_json['cmsname']))
                pass
        except Exception as e:
            print(e)
            pass
    if result == []:
        pass
    else:
        return result

def getCmsPrint(target_url,json_path=None,updata=False):
    if updata:
        updataCmsPrintJson(json_path=json_path)
    database_json = readJsonFile(json_path)
    database_list = database_json['RECORDS']
    getCmsPrint_pool = MyThreadPool(getCMS_Name,database_list,other_args=target_url)
    getCmsPrint_pool.start()
    print(getCmsPrint_pool.result)

if __name__ =='__main__':
    json_path = '{}payload/others/cmsprint.json'.format(base_root)

    target_url = 'http://stu.xmist.edu.cn/'
    # target_url = 'https://www.t00ls.net'  # 目标地址
    getCmsPrint(target_url,json_path=json_path,updata=False)

    # resp = requests.get('https://www.thzhjy.org.cn/jeecms/res/jeecms/img/login/llogo.jpg')
    # print(resp.text)
    # hh_md5 = hashlib.md5(resp.text.encode()).hexdigest()
    # print(hh_md5)