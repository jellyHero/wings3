# -*- coding: utf-8 -*-

#url必须以http或https开头，结尾不能是'/'
def formatUrl(url,req_type=None):
    if req_type:
        if req_type.upper() == 'HTTPS':
            req_type = 'https://'
        else:
            req_type = 'http://'
    else:
        req_type = 'http://'
    if '://' not in url :
        url = req_type + url
    if url[-1] == '/':
        url = url[0:-1]
    return url

#path必须以'/'开头
def formatPath(path):
    if path[0] == '/':
        pass
    else:
        path = '/' + path
    return path