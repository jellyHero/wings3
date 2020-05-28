from lib.net.httpcon import httpreq_raw

def convert_arg_line_to_args(arg_line):
    return [arg_line]

#模仿sqlmap，从文件中获取http参数
def readArgsFromFile(file_path):
    new_arg_strings = []
    try:
        with open(file_path) as args_file:
            arg_strings = []
            for arg_line in args_file.read().splitlines():
                for arg in convert_arg_line_to_args(arg_line):
                    arg_strings.append(arg)
            new_arg_strings.extend(arg_strings)
            return new_arg_strings
    except Exception as e :
        print(e)

#模仿HackRequests，从burp复制的raw中获取http参数
def readArgsFromRaw(raw):
    raw = raw.split('\n')
    if raw[0] == '':
        raw = raw[1:]
    if raw[-1] == '':
        raw = raw[:-1]
    new_arg_strings = []
    arg_strings = []
    for arg_line in raw:
        for arg in convert_arg_line_to_args(arg_line):
            arg_strings.append(arg)
    new_arg_strings.extend(arg_strings)
    return new_arg_strings



#从http的参数列表中，获取http请求参数
def getHTTPReqArgsFrom_argsList(ArgsList,ssl=False):
    '''
    argsList = ['POST /dvwa/vulnerabilities/sqli/?id=§1§&Submit=Submit HTTP/1.1', 'Host: 10.178.31.61', 'Connection: close', '', 'test=321']
    host = get_headerArg_From_argsList('Host',argsList)
    print(host)
    >Host: 10.178.31.61
    '''

    def get_headerArg_From_argsList(headerArg, argsList):
        num = len(headerArg)
        for arg in argsList:
            # print(arg[:num+1])
            if arg[:num + 1] == headerArg + ':':
                return arg
        return None

    method= ArgsList[0].split(' ')[0]
    scheme = 'http'
    if ssl:
        scheme='https'
    host_line = get_headerArg_From_argsList('Host',ArgsList)
    host = host_line.replace('Host:','').split(':')[0].replace(' ','')
    try:
        port = host_line.split(':')[2].replace(' ','')
    except:
        port = 80
    path = ArgsList[0].split(' ')[1]
    headers = {}
    body = None
    if method == 'GET':
        for arg in ArgsList[1:]:
            if arg == '':
                pass
            headers[arg.split(':',1)[0]] = arg.split(':',1)[1].replace(' ','')
        body = None
    if method == 'POST':
        for arg in ArgsList[1:-2]:
            if arg == '':
                pass
            headers[arg.split(':', 1)[0]] = arg.split(':', 1)[1].replace(' ', '')
        body = ArgsList[-1]
    return method,scheme,host,port,path,headers,body

#使用http请求参数列表，发起http请求,输入参数列表的格式如下
#['GET /dvwa/vulnerabilities/xss_r/?name=123 HTTP/1.1', 'Host: 10.178.31.61', 'Cookie: security=low; PHPSESSID=ol5ao8q989b8ajs9inu1bnosv5']
def httReq_fromArgslist(argsList,ssl=False):
    if ssl:
        ssl = 'https'
    method, scheme, host, port, path, headers, body = getHTTPReqArgsFrom_argsList(argsList,ssl)
    hh = httpreq_raw(method, scheme, host, port, path, headers=headers, body=body)
    return hh

#使用burp的raw字符串，发起http请求
def httReq_fromBurpRaw(raw,ssl=False):
    if ssl:
        ssl = 'https'
    argsList = readArgsFromRaw(raw)
    # print(argsList)
    method, scheme, host, port, path, headers, body = getHTTPReqArgsFrom_argsList(argsList,ssl)
    hh = httpreq_raw(method, scheme, host, port, path, headers=headers, body=body)
    return hh

#使用file文件，发起http请求
def httReq_fromFile(filePath,ssl=False):
    if ssl:
        ssl = 'https'
    argsList = readArgsFromFile(filePath)
    method, scheme, host, port, path, headers, body = getHTTPReqArgsFrom_argsList(argsList,ssl)
    hh = httpreq_raw(method, scheme, host, port, path, headers=headers, body=body)
    return hh




# target = '''
# GET /dvwa/vulnerabilities/xss_r/?name=123 HTTP/1.1
# Host: 10.178.31.61
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Connection: close
# Referer: http://10.178.31.61/dvwa/vulnerabilities/xss_r/
# Cookie: security=low; PHPSESSID=ol5ao8q989b8ajs9inu1bnosv5
# Upgrade-Insecure-Requests: 1
# '''
# hh = httReq_fromBurpRaw(target)
# test = hh.text()


# file_path = '/Users/shellyzhang/sql.txt'
# # hh = httReq_fromFile(file_path)
# test = hh.text()