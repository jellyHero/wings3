# -*- coding: utf-8 -*-
import os
from conf.conf import base_root



#读文件
def readFile(target_file):
	with open(target_file, 'r') as f:
		# print(f.readlines())
		return f.readlines()

#写文件
def writeFile(target_file,STR):
	with open(target_file, 'a') as f:
		f.write(STR)

# 删除文件
def clearFile(target_file):
	try:
		os.remove(target_file)
	except:
		pass

#文件去重
def getRemoveDupFile(target_file):
	try:
		cache_file = '{}.rd'.format(target_file)
		lines_seen = set()
		f = open(target_file, 'r', encoding='utf-8')
		outfiile = open(cache_file, 'a+', encoding='utf-8')
		for line in f:
			if line not in lines_seen:
				outfiile.write(line)
				lines_seen.add(line)
		return cache_file
	except Exception as e:
		print('Excepation! Return old file ! :: {}'.format(e))
		return target_file


# if __name__=="__main__":
# 	test_file = '{}payload/cache/test.txt'.format(base_root)
# 	print(getRemoveDupFile(test_file))
