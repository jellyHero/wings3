import re

#模拟burp，替换两个§中的内容
def replaceMarkStr(new,old):
    return  re.sub(r'§.*§',new,old)

