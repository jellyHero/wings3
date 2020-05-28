#神奇的unicode控制字符
#\u202E : 会将字符串进行翻转
#\u202D : 会将字符串互换位置


#得出单个字节的ascii数值的16进制，即url encode数值，返回str(数值)
def getAscNum(oneword):
    oneword = ord(oneword)
    return str(hex(oneword)).split('0x')[1]

#正序yield出string的ascii数值
def yieldLTRAscNum(target_str):
    str_len = len(target_str)
    for i in range(0,str_len):
        yield getAscNum(target_str[i])

#倒序yield出string的ascii数值
def yieldRTLAscNum(target_str):
    str_len = len(target_str)
    for i in range(str_len-1,-1,-1):
        yield getAscNum(target_str[i])

#得出string的L-T-R数值,返回str(数值)
def getLTRNum(target_str):
    result_str = ''
    for i in yieldLTRAscNum(target_str):
        result_str = result_str +'\\u00{}'.format(i)
    return result_str

#得出string的R-T-L数值,返回str(数值)
def getRTLNum(target_str):
    result_str = ''
    for i in yieldRTLAscNum(target_str):
        result_str = result_str +'\\u00{}'.format(i)
    return result_str


# target_str = 'moc.qq.hanbufei.xyz'
# print('Left To Right : {}'.format(getLTRNum(target_str)))
# print('Right To Left : {}'.format(getRTLNum(target_str)))
# #
# test1 = '\u006d\u006f\u0063\u002e\u0071\u0071\u002e\u0068\u0061\u006e\u0062\u0075\u0066\u0065\u0069\u002e\u0078\u0079\u007a'
# test2 = '\u202e'+test1
# print(test1)
# print(test2)

# test3 = '\u202e\u006d\u006f\u0063\u002e\u0071\u0071\u002e\u0068\u0061\u006e\u0062\u0075\u0066\u0065\u0069\u002e\u0078\u0079\u007a'
# print(test3)

# print('123\u202E654\u202Dabc')
# print('123\u202E654abc')