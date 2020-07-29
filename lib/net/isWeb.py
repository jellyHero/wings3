import requests
import re
from conf.conf import User_Agent

def isWeb(ip_port=None,ip=None,port=None):
    if ip_port:
        pass
    else:
        ip_port = '{}:{}'.format(ip,port)
    result = {}
    headers = {'User_Agent':User_Agent}
    try:
        root_path = 'http://{}'.format(ip_port)
        # print(root_path)
        http_resp = requests.get(root_path,allow_redirects=False,timeout=5,headers=headers)
        text = http_resp.content.decode("utf-8","ignore")
        d = re.search('(?<=<title>).+?(?=</title>)', text, re.IGNORECASE)
        title = d.group()
        print('("{}","{}","{}")'.format(root_path, http_resp.status_code,title))
        result['http_web'] = '{} --> {}:{}'.format(root_path,http_resp.status_code,title)
    except Exception as  e:
        result['http_exception'] = "{}".format(e)
        pass
    try:
        root_path = 'https://{}'.format(ip_port)
        # print(root_path)
        https_resp = requests.get(root_path,allow_redirects=False,timeout=5,headers=headers,verify=False)
        text = https_resp.content.decode("utf-8","ignore")
        d = re.search('(?<=<title>).+?(?=</title>)', text, re.IGNORECASE)
        title = d.group()
        print('("{}","{}","{}")'.format(root_path, https_resp.status_code,title))
        result['https_web'] = '{} --> {}:{}'.format(root_path, https_resp.status_code,title)
    except Exception as  e:
        result['https_exception'] = "{}".format(e)
        pass
    # print(result)
    return result

if __name__ == "__main__":
    result = isWeb('www.qq.com')
    print(result)
    #("http://www.baidu.com","200")
    #("https://www.baidu.com","200")
    #{'http_web': 'http://www.baidu.com --> 200', 'https_web': 'https://www.baidu.com --> 200'}