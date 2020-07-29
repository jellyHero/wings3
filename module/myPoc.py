# -*- coding: utf-8 -*-
import re
import random
import json
from lib.code.yaml2dict import yaml2dict_fromFile
from conf.conf import base_root
from lib.net.httpcon import httpreq


def randomInt(x,y):
    return random.randint(x,y)

def randomLowercase(r1):
    result = ''
    s = 'qwertyuioplkjhgfdsazxcvbnm'
    for i in range(0,r1):
        result += random.choice(s)
    return result


#编写这个的目的，主要是为了兼容xray的poc(兼容待完善)：https://github.com/chaitin/xray/tree/master/pocs
# 用一些简单的例子来解释大部分我们可能用到的表达式：
# response.body.bcontains(b'test')
# 返回包 body 包含 test，因为 body 是一个 bytes 类型的变量，所以我们需要使用 bcontains 方法，且其参数也是 bytes
# response.body.bcontains(bytes(r1+'some value'+r2))
# r1、r2是 randomLowercase 的变量，这里动态的判断 body 的内容
# response.content_type.contains('application/octet-stream') && response.body.bcontains(b'\x00\x01\x02')
# 返回包的 content-type 包含 application/octet-stream，且 body 中包含 0x000102 这段二进制串
# response.content_type.contains('zip') && r'^PK\x03\x04'.bmatches(response.body)
# 这个规则用来判断返回的内容是否是zip文件，需要同时满足条件：content-type 包含关键字 "zip"，且 body 匹配上正则r'^PK\x03\x04'（就是zip的文件头）。因为 startsWith 方法只支持字符串的判断，所以这里没有使用。
# response.status >= 300 && response.status < 400
# 返回包的 status code 在 300~400 之间
# (response.status >= 500 && response.status != 502) || r'<input value="(.+?)"'.bmatches(response.body)
# 返回包status code大于等于500且不等于502，或者Body包含表单
# response.headers['location']=="https://www.example.com"
# headers 中 Location 等于指定值，如果 Location 不存在，该表达式返回 false
# 'docker-distribution-api-version' in response.headers && response.headers['docker-distribution-api-version'].contains('registry/2.0')
# headers 中包含 docker-distribution-api-version 并且 value 包含指定字符串，如果不判断 in，后续的 contains 会出错。
# response.body.bcontains(bytes(response.url.path))
# body 中包含 url 的 path
class CEL_expression:
    def __init__(self,expression,response):
        self.expression = expression
        self.response = response

    def contains(self,target,val):
        if val in target:
            return True
        else:
            return False

    #处理cel表达式
    def deal_expression(self):
        result = False
        if self.expression == True:
            result = True
        else:
            result = False
        if '||'  in self.expression:
            expression_list = self.expression.split('||')
            for i in expression_list:
                if not self.deal_and(i):
                    result = False
            result = True
        else:
            result = self.deal_and(self.expression)
        # print(result)
        return result

    #处理只包含and（&&）的操作
    def deal_and(self,expression):
        result = False
        if '||'  in expression:
            raise('|| in deal_and !')
        if '&&' in expression :
            expression_list = expression.split('&&')
            for i in expression_list:
                i = i.replace(' ','')
                result = self.exec_exp(i)
        else:
            result = self.exec_exp(expression)
        return result

    #执行单个cel表达式，即无逻辑运输符（&&，||）的,待完善
    def exec_exp(self,expression):
        expression = expression.strip()
        #表达式中headers的头有时候是小写的，对不上响应包的头
        #改变一下表达式
        if 'headers[' in expression:
            re_headers = re.compile(r"headers\[.(.*?).\]")
            for i in re.findall(re_headers,expression):
                expression = expression.replace(i,i.title())
        result = False
        response = self.response
        try:
            if '.contains(' in expression:
                expression_tmp_list = expression.split('.contains')
                if 'content-type' in expression_tmp_list[0]:
                    result = self.contains(response.content-type,eval(expression.split('.contains(')[1][:-1]))
                if 'headers[' in expression_tmp_list[0]:
                    result = self.contains(eval(expression_tmp_list[0]), eval(expression.split('.contains(')[1][:-1]))
            if '.bcontains(' in expression:
                expression_tmp_list = expression.split('.bcontains')
                if 'body' in expression_tmp_list[0]:
                    result = self.contains(response.body,eval(expression.split('.bcontains(')[1][:-1]))
            if '.contains(' not in expression and '.bcontains(' not in expression:
                result = eval(expression)
            return result
        except Exception as e:
            print('[Error] Exception is : {}'.format(e))


#编写这个的目的，主要是为了兼容xray的poc(兼容待完善)
# yaml格式的poc，可以直接使用xray的在线生成：https://phith0n.github.io/xray-poc-generation/
class MyPoc_HTTP:
    def __init__(self,host,scheme='http',port=80,yaml_file=None):
        self.yaml_file = yaml_file
        self.initReqArgs()
        self.host = host
        self.scheme= scheme
        self.port = int(port)
        #把yaml文件转换成字典，保存到self.yaml_dict
        if yaml_file:
            self.yaml_dict = yaml2dict_fromFile(yaml_file)
        else:
            self.yaml_dict = {}

    #构造http请求，需要用到这些参数
    def initReqArgs(self):
        self.method = 'GET'
        self.scheme = 'http'
        self.host = None
        self.port = 80
        self.path = '/'
        self.headers = {'User_Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36(security test by hanfei)"}
        self.body = None
        self.follow_redirects = True


    #发起http请求
    def send(self):
        self.url = '{}://{}:{}{}'.format(self.scheme,self.host,self.port,self.path)
        return httpreq(self.url,headers=self.headers,body=self.body,location=self.follow_redirects)


    #将请求根据 rule 中的规则对请求变形
    def mutate_request_by_rule(self,rule):
        if 'method' in rule.keys():
            self.method = rule['method']
        if 'scheme' in rule.keys():
            self.scheme = rule['scheme']
        if 'host' in rule.keys():
            self.host = rule['host']
        if 'port' in rule.keys():
            self.port = int(rule['port'])
        if 'path' in rule.keys():
            self.path = rule['path']
        if 'headers' in rule.keys():
            self.headers = rule['headers']
        if 'body' in rule.keys():
            self.body = rule['body']
        if 'follow_redirects' in rule.keys():
            self.follow_redirects = rule['follow_redirects']

    #检查响应是否匹配 expression 部分的表达式
    #response.text(), response.status_code, response.headers
    def check_response(self,response,rule):
        my_cel =CEL_expression(rule['expression'],response)
        return my_cel.deal_expression()


    #获取poc中的set数据
    def setPocArgs(self):
        self.pocArgs = {}
        if 'set' in self.yaml_dict.keys():
            for i in  self.yaml_dict['set'].keys() :
                self.pocArgs[i] = eval(self.yaml_dict['set'][i].strip())
            print(self.pocArgs)

    # 对xray的poc文件进行变形
    def mutate_yaml_poc(self):
        self.setPocArgs()
        yaml_json = json.dumps(self.yaml_dict)
        for i in self.pocArgs.keys():
            print(i)
            yaml_json = yaml_json.replace('{{'+i+'}}','{}'.format(self.pocArgs[i]))
        print(yaml_json)
        self.yaml_dict = json.loads(yaml_json)
        print(self.yaml_dict)

    #将请求根据 rule 中的规则对请求变形，然后获取变形后的响应，再检查响应是否匹配 expression 部分的表达式。
    # 如果匹配，就进行下一个 rule，如果不匹配则退出执行。
    # 如果成功执行完了最后一个 rule，那么代表目标有漏洞，将 detail 中的信息附加到漏洞输出后就完成了单个 poc 的整个流程。
    def main(self):
        # self.mutate_yaml_poc()
        # self.setPocArgs()
        rules = self.yaml_dict['rules']
        for rule in rules:
            # print(rule)
            self.mutate_request_by_rule(rule)
            response = self.send()
            # print(response.headers)
            # print(response.text())
            if not self.check_response(response, rule):
                return False
        print('[FOUND]{} : {}'.format(self.yaml_dict['name'], self.url))
        return True

if __name__ == '__main__':
    scheme = 'http'
    host = 'www.baidu.com'
    port = 80
    # yaml_file = '{}payload/yaml/poc_yaml'.format(base_root)
    yaml_file = '{}payload/yaml/jboss-cve-2010-1871.yml'.format(base_root)
    mypoc = MyPoc_HTTP(host,scheme=scheme,port=port,yaml_file=yaml_file)
    # print(mypoc.yaml_dict)
    mypoc.main()