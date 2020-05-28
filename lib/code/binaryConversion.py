# coding=utf-8

#[+] 大小写转换 :
# str = "shelly"
# print(str.upper())          # 把所有字符中的小写字母转换成大写字母
# print(str.lower())          # 把所有字符中的大写字母转换成小写字母
# print(str.capitalize())     # 把第一个字母转化为大写字母，其余小写
# ------
# SHELLY
# shelly
# Shelly
# -----

#基本XOR方法，用来在特定情况下代替python的^符号
def binXORBin(bin1,bin2):
    if bin1 == bin2 :
        return '0'
    else:
        return '1'

#格式二进制字符串:去除ob和空格，并且如果不足8位，在前面添加0补齐
def capitalizeBin_str(bin_str):
    bin_str = bin_str.replace('0b', '').replace(' ', '')
    if len(bin_str) % 8 == 0:
        pass
    else:
        prex = 8 - len(bin_str)
        bin_str = '0' * prex + bin_str
    return bin_str

#格式16进制字符串:去除0x和空格,并且如果字符串只有1位，在前面补0
def capitalizeHex_str(hex_str):
    hex_str = hex_str.replace('0x', '').replace('0X', '').replace(' ', '')
    if len(hex_str)%2 == 0 :
        return hex_str
    elif len(hex_str) == 1:
        return '0' + hex_str
    else:
        exit()

# 16进制转换为10进制,输入的x应为字符串格式
# 如 print(hex2Int('a')) 或print(hex2Int('0x0a'))
# 10
def hex2Int(x):
    return int(x,16)

# 10进制转换为16进制
def int2Hex(x):
    return hex(x)

# 10进制转换为ascii码
def int2Asc(x):
    return chr(x)

# ascii码转换为10进制
def asc2Int(x):
    return ord(x)

#2进制字符串转换成16进制字符串，如：
# print(bin_str2Hex_str('1101'))
# 0d
def bin_str2Hex_str(bin_str):
    bin_str = capitalizeBin_str(bin_str)
    return capitalizeHex_str(int2Hex(int(bin_str, 2)).replace('0x', ''))

#16进制字符串转换成2进制字符串，如：
# print(hex_str2Bin_str('0d'))
# 00001101
def hex_str2Bin_str(hex_str):
    hex_str = capitalizeHex_str(hex_str)
    return capitalizeBin_str(bin(hex2Int(hex_str)))

#把字符串转换成二进制串，如：
# print(str2Bin('abc'))
# 011000010110001001100011
def str2Bin(s):
    result = ''
    for i in s :
        result = result + capitalizeBin_str(bin(ord(i)))#capitalizeBin_str(bin(ord(i)):把单个字符转换成二进制
    return result

#把二进制串转换成字符串，如：
# print(bin2Str('011000010110001001100011'))
# abc
def bin2Str(b):
    b = b.replace('0b', '').replace(' ','')
    if len(b)%8 == 0 :
        b_array = [b[i:i+8] for i in range(0,len(b),8)]
        # print(b_array)
        result = ''
        for i in b_array:
            result = result + chr(int(i, 2))#chr(int(i, 2)):把二进制转化成单个字符
        return  result
    else:
        exit()

#十六进制字符串转bytes,如：
# print(hexStringTobytes('7B216A634951170FF851D6CC68FC9537858795A28ED4AAC6'))
# b'{!jcIQ\x17\x0f\xf8Q\xd6\xcch\xfc\x957\x85\x87\x95\xa2\x8e\xd4\xaa\xc6'
def hexStringTobytes(str):
    str = capitalizeHex_str(str)
    return bytes.fromhex(str)

#bytes转十六进制字符串
# print(bytesToHexString(b'{!jcIQ\x17\x0f\xf8Q\xd6\xcch\xfc\x957\x85\x87\x95\xa2\x8e\xd4\xaa\xc6'))
# 7B216A634951170FF851D6CC68FC9537858795A28ED4AAC6
def bytesToHexString(bs):
    # return ''.join(['%02X ' % b for b in bs]) #这样也可以
    result = ''
    for b_int_str in bs:
        b_hex_str = '%02X ' % b_int_str #另一种方式，把10进制字符串转换成16进制字符串
        result = result + capitalizeHex_str(b_hex_str)
    return result

#改变bytes中指定位置的byte，如：
# print(changeByte(b'\x10\xcf\xf7\xaf\xc9\x94',2,b'\x00'))
# b'\x10\xcf\x00\xaf\xc9\x94'
def changeByte(byte_str,num,new_byte):
    if num > len(byte_str):
        exit()
    result = b''
    i_num = 0
    for i in byte_str:
        i = hexStringTobytes(hex(i))
        if i_num == num :
            byte_s = new_byte
        else:
            byte_s = i
        result = result + byte_s
        i_num = i_num + 1
    return result

# #把16进制字符串转换成2个2个一对的16进制数组，如：
# print(hex_str2Hex_arr('a1b2cd'))
# ['a1', 'b2', 'cd']
def hex_str2Hex_arr(hex_str):
    hex_str = capitalizeHex_str(hex_str)
    hex_str_arr = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]
    return hex_str_arr


#把16进制字符串转换为asc字符串，如：
# print(hex_str2Asc_str('425249414e3b2031323b20323b'))
# BRIAN; 12; 2;
def hex_str2Asc_str(hex_str):
    hex_str = capitalizeHex_str(hex_str)
    hex_str_arr = hex_str2Hex_arr(hex_str)
    result = ''
    for hex_c in hex_str_arr:
        hex_int = int(hex_c,16)
        result = result + int2Asc(hex_int)
    return result

#把asc字符串转换为16进制字符串，如：
# print(asc_str2Hex_str('BRIAN; 12; 2;'))
# 425249414e3b2031323b20323b
def asc_str2Hex_str(asc_str):
    asc_hex_arr = [[int2Hex(asc2Int(i))] for i in asc_str]
    result = ''
    for hex_c in asc_hex_arr:
        hex_c = capitalizeHex_str(hex_c[0])
        result = result + hex_c
    return result

#把二进制字符串进行XOR计算，如：
# print(bin_strXORBin_str('111','101'))
# '010'
def bin_strXORBin_str(bin_str1,bin_str2):
    bin_str1 = capitalizeBin_str(bin_str1)
    bin_str2 = capitalizeBin_str(bin_str2)
    if len(bin_str1) == len(bin_str2):
        result = ''
        for i in range(0,len(bin_str1)):
            result = result + binXORBin(bin_str1[i],bin_str2[i])
        return result
    else:
        exit()

#把16进制字符串进行XOR计算,如：
# result1 = hex_strXORHex_str('7b21','3973')
# print(result1)
# print(hex_str2Asc_str(result1))
# 4252
# BR
def hex_strXORHex_str(hex_str1,hex_str2):
    hex_str1 = capitalizeHex_str(hex_str1)
    hex_str2 = capitalizeHex_str(hex_str2)
    if len(hex_str1) == len(hex_str2):
        hex_arr1 = hex_str2Hex_arr(hex_str1)#把16进制两两分组
        hex_arr2 = hex_str2Hex_arr(hex_str2)
        result = ''
        for i in range(0,len(hex_arr1)):
            bin_str1 = hex_str2Bin_str(hex_arr1[i])#16进制转换成2进制
            bin_str2 = hex_str2Bin_str(hex_arr2[i])
            result_bin_str = bin_strXORBin_str(bin_str1,bin_str2)#2进制xor计算
            result_hex_str = bin_str2Hex_str(result_bin_str)#2进制转换成16进制
            result = result + result_hex_str
        return result
    else:
        exit()
#
# plain = 'jWFcdq+TVVDnwfx6NS+G1U2914eBrj+9/ttS8Fs0ss5MyA6g3IwLDAYbjd1TsgZabfDmxOtI0Lj0kjGg006Ea+xlBNZpX681irCkSSDwJoiMP5WTeZgvgAhu8GyY8t75rr6IoPmApmoA3PujbdcGEqQzTU+sM6AA1wGPY27wIfg='
# b64d = lambda x: base64.b64decode(x)
# x = b64d(plain)
# print(hex_str2Asc_str(bytesToHexString(x)))

# plain = '99'
# print(hex_str2Asc_str(plain))