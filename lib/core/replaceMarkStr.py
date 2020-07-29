import re

#模拟burp，替换两个§中的内容
def replaceMarkStr(target_str,new):
    return  re.sub('§.*§',new,target_str)
