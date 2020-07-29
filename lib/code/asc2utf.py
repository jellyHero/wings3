# coding=utf-8
import sys

'''
目前只实现asc编码的字符，和双字节utf-8编码字符的互转。
如：
%c0%ae <--> .

用法：
$ python asc_utf.py %c0%ae
.
$ python asc_utf.py '.'
%c0%ae

'''

#把utf编码转换成asc字符,如%c0%ae转换成.
def utf_to_asc(target):
	binStr1 = bin(hexStr_to_hex(target.split('%')[1]))
	binStr2 = bin(hexStr_to_hex(target.split('%')[2]))
	binStr1 = to_bin(binStr1)
	binStr2 = to_bin(binStr2)
	asc_binStr = binStr1[-2:] + binStr2[2:]
	asc_bin = binStr_to_bin(asc_binStr)
	return chr(asc_bin)

#把asc字符转换成utf编码，如.转换成%c0%ae
def asc_to_utf(target):
	asc_binStr = chr_to_binStr(target)
	asc_binStr_sub1 = asc_binStr[:2]
	asc_binStr_sub2 = asc_binStr[2:]
	utf_binStr = '110000' + asc_binStr_sub1 + '10' + asc_binStr_sub2
	utf_binStr_sub1 = utf_binStr[:8]
	utf_binStr_sub2 =utf_binStr[8:]
	utf1 = hex(binStr_to_bin(utf_binStr_sub1))
	utf2 = hex(binStr_to_bin(utf_binStr_sub2))
	utf = utf1 + utf2
	return utf.replace('0x','%')


#把字符转换成其二进制
def chr_to_binStr(target):
	target_binStr = bin(ord(target))	#将字符转换成二进制
	target_binStr = to_bin(target_binStr)
	return target_binStr

#二进制，补全8位，并返回其字符串格式
def to_bin(target):
	target_binStr = target[2:]			#去除二进制前缀0b
	num = 8 - len(target_binStr)
	if num >= 0 :						#补全8位
		for i in range(0,num):
			target_binStr = '0' + target_binStr
	return target_binStr


#把二进制的字符串格式，转换成真正的二进制数字
def binStr_to_bin(target):
	bin_num = 0b00000000
	for i in range(0,8):
		if i == 0 :
			if target[i] == '1':
				bin_num = bin_num + 0b10000000
		if i == 1 :
			if target[i] == '1':
				bin_num = bin_num + 0b01000000
		if i == 2 :
			if target[i] == '1':
				bin_num = bin_num + 0b00100000
		if i == 3 :
			if target[i] == '1':
				bin_num = bin_num + 0b00010000
		if i == 4 :
			if target[i] == '1':
				bin_num = bin_num + 0b00001000
		if i == 5 :
			if target[i] == '1':
				bin_num = bin_num + 0b00000100
		if i == 6 :
			if target[i] == '1':
				bin_num = bin_num + 0b00000010
		if i == 7 :
			if target[i] == '1':
				bin_num = bin_num + 0b00000001
	return bin_num

#把16进制的字符串格式，转换成真正的10进制数字
def hexStr_to_hex(target):
	int_num = 0
	i = target[0]
	j = target[1]
	if i == '0':
		int_num = int_num + 0*16
	if i == '1':
		int_num = int_num + 1*16
	if i == '2':
		int_num = int_num + 2*16
	if i == '3':
		int_num = int_num + 3*16
	if i == '4':
		int_num = int_num + 4*16
	if i == '5':
		int_num = int_num + 5*16
	if i == '6':
		int_num = int_num + 6*16
	if i == '7':
		int_num = int_num + 7*16
	if i == '8':
		int_num = int_num + 8*16
	if i == '9':
		int_num = int_num + 9*16
	if i == 'a':
		int_num = int_num + 10*16
	if i == 'b':
		int_num = int_num + 11*16
	if i == 'c':
		int_num = int_num + 12*16
	if i == 'd':
		int_num = int_num + 13*16
	if i == 'e':
		int_num = int_num + 14*16
	if i == 'f':
		int_num = int_num + 15*16
	if j == '0':
		int_num = int_num + 0
	if j == '1':
		int_num = int_num + 1
	if j == '2':
		int_num = int_num + 2
	if j == '3':
		int_num = int_num + 3
	if j == '4':
		int_num = int_num + 4
	if j == '5':
		int_num = int_num + 5
	if j == '6':
		int_num = int_num + 6
	if j == '7':
		int_num = int_num + 7
	if j == '8':
		int_num = int_num + 8
	if j == '9':
		int_num = int_num + 9
	if j == 'a':
		int_num = int_num + 10
	if j == 'b':
		int_num = int_num + 11
	if j == 'c':
		int_num = int_num + 12
	if j == 'd':
		int_num = int_num + 13
	if j == 'e':
		int_num = int_num + 14
	if j == 'f':
		int_num = int_num + 15

	return int_num

if __name__ == '__main__':
    target = sys.argv[1]
    if '%' not in target :
        print(asc_to_utf(target))
    else :
        if target == '%':
            print(asc_to_utf(target))
        else:
            print(utf_to_asc(target))