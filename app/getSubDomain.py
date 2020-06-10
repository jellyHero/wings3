import dns.resolver
import requests
import re

from lib.code.deduplication import  deduplication_list
from lib.core.w_threadPool import MyThreadPool
from conf.conf import base_root
from lib.file.file_Class import readFile

#通过dns判断域名是否存在
def isExist_from_NS(word,domain):
    target = '{}.{}'.format(word,domain)
    try:
        A = dns.resolver.query(target, 'A')
        print('{} is exist'.format(target))
    except:
        print('{} is not exist'.format(target))
        return False
    return word

#通过dns获得域名的ip,返回字典格式结果，如下：
#print(getIp_from_NS('qq.com'))
#['61.129.7.47', '183.3.226.35', '123.151.137.18']
def getIp_from_NS(domain):
    result = []
    try:
        A = dns.resolver.query(domain, 'A')
        for i in A.response.answer:
            for j in i.items:
                if j.rdtype == 1:
                    result.append(j.address)
                    print('{} : {}'.format(domain,j.address))
        return deduplication_list(result)
    except:
        return None

#获得对应的ip
def addIPtoSubdomain(subDomain_list):
    result = {}
    print('---------------')
    print('---------------')
    for i in subDomain_list:
        result[i] = getIp_from_NS(i)
    return result

#爆破：仅使用长度为1或2的字符串进行
def getSubDomainFrom_NsBrute(domain,key_words=None):
    payload = []
    if key_words == None:
        key_words = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    for i in key_words:
        payload.append(i)
        for j in key_words:
            payload.append('{}{}'.format(i,j))
    MyThread = MyThreadPool(isExist_from_NS, payload, other_args=domain)
    MyThread.start()
    result = deduplication_list(MyThread.result)
    return ['{}.{}'.format(i,domain) for i in result if i]

#爆破：使用字典进行，默认采用内置的common-words.txt和猪猪侠wydomain里的高效字典wydomain.txt
def getSubDomainFrom_file(domain,file_name=None):
    if file_name == None:
        file_name1 = '{}payload/dict/common-words.txt'.format(base_root)
        file_name2 = '{}payload/dict/wydomain.txt'.format(base_root)
        payload = readFile(file_name1)
        payload.extend(readFile(file_name2))
        payload = deduplication_list(payload)
    else:
        payload = readFile(file_name)
    MyThread = MyThreadPool(isExist_from_NS, payload, other_args=domain)
    MyThread.start()
    result = deduplication_list(MyThread.result)
    return ['{}.{}'.format(i,domain) for i in result if i]

#从crt.sh网站获取子域名信息,例如：https://crt.sh/?q=qq.com
def getSubDomainFrom_crt_sh(domain):
    try:
        url = 'https://crt.sh/?q=qq.com'.replace('qq.com',domain)
        resp = requests.get(url,verify=False)
        pattern = re.compile(r'<TD style="text\-align\:center;white\-space\:nowrap">.*?</TD>\n    <TD>(.*?)</TD>')
        temp_result = pattern.findall(resp.text)
        result = []
        for i in temp_result:
            if '<BR>' in i:
                result.extend(i.split('<BR>'))
            else:
                result.append(i)
    except:
        result = []
    result = deduplication_list(result)
    try:
        result.remove('*.{}'.format(domain))
    except:
        pass
    return result

#main函数，采用多种方式获取子域名列表，去重
def getSubDomain(domain,file_name=None,key_words=None):
    subDomain = getSubDomainFrom_crt_sh(domain) #从crt.sh网站获取
    subDomain.extend(getSubDomainFrom_NsBrute(domain,key_words)) #2长度爆破
    subDomain.extend(getSubDomainFrom_file(domain, file_name)) #字典爆破
    subDomain = deduplication_list(subDomain)
    try:
        subDomain.remove('*.{}'.format(domain))
    except:
        pass
    return subDomain


#在main函数基础上，进行递归查询，去重，并获得对应的ip
def getSubDomain2(domain,file_name=None,key_words=None,times=None):
    if times == None:
        times = 2
    if type(times) == int:
        pass
    else:
        raise Exception('times is not int')
    i = 1
    while True:
        if i == times:
            break
        pass


if __name__ == '__main__':
    target = 'wj.qq.com'
    result = getSubDomain(target)
    print(addIPtoSubdomain(result))