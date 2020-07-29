# -*- coding: utf-8 -*-
import re
import random
import json
from lib.code.yaml2dict import yaml2dict_fromFile
from conf.conf import base_root
from lib.net.httpcon import httpreq


def randomInt(x, y):
    return random.randint(x, y)

def randomLowercase(r1):
    result = ''
    s = 'qwertyuioplkjhgfdsazxcvbnm'
    for i in range(0, r1):
        result += random.choice(s)
    return result

class YAML_file:
    def __init__(self,file_path):
        self.file_path = file_path
        self.yaml_dict = yaml2dict_fromFile(file_path)
        self.yamlArgs = {} #yaml文件中set定义的本地变量
        if 'set' in self.yaml_dict.keys():
            self.getYamlArgs()
        self.rules = self.yaml_dict['rules']

    def getYamlArgs(self):
        for i in self.yaml_dict['set'].keys():
            self.yamlArgs[i] = eval(self.yaml_dict['set'][i].strip())

class Rule:
    def __init__(self,rule):
        self.rule = rule
        self.req = {}
        self.getReq()
        self.expression = None
        self.search =None
        if 'expression' in self.rule.keys():
            self.expression = self.rule['expression']
        if 'search' in self.rule.keys():
            self.search = self.rule['search']

    def getReq(self):
        for key in self.rule.keys():
            if key != 'expression' and key != 'search':
                self.req[key] = self.rule[key]

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

yaml_file = YAML_file('{}payload/yaml/joomla-cnvd-2019-34135-rce.yml'.format(base_root))
print(yaml_file.yamlArgs)

for rule_dict in yaml_file.rules:
    rule = Rule(rule_dict)
    print(rule.req)
    print(rule.expression)
    print(rule.search)