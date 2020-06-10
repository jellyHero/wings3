import re

#模拟burp，替换两个§中的内容
def replaceMarkStr(old,new):
    return  re.sub('§.*§',new,old)
