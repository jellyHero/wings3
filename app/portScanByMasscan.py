# -*- coding: utf-8 -*-
import os
import re
#使用masscan扫描全端口
class Masscan:
	def __init__(self,target_ip):
		# os.system('echo "" > nohup.out')
		self.target_ip = target_ip
		# self.scan_result = target_ip.split('/')[0]+'_result.txt'
		# try:
		# 	os.system('rm -rf '+self.scan_result)
		# except:
		# 	pass

	#返回扫描结果
	def scan(self):
		cmd = 'masscan '+self.target_ip+' -p 0-65535'+' --rate=10000'
		r = os.popen(cmd)
		info_list = r.readlines()
		return info_list

	#使用正则，从字符串中得到ip:port
	def getExistPort(self,info):
		pattern_port = re.compile("Discovered open port (.*)/.*")
		pattern_ip = re.compile("/.* on (.*)")
		port = pattern_port.findall(info)[0]
		ip =pattern_ip.findall(info)[0].strip()
		return ip+':'+port

	#主函数，返回并保存结果
	def masscan_main(self):
		result = []
		info_list = self.scan()
		for info in info_list:
			port = self.getExistPort(info)
			if len(port) >= 1:
				result.append(port)
				# writeFile(self.scan_result,port+'\r\n')
			else:
				pass
		return result

if __name__=="__main__":
	for i in range(1,256):
		my_scan = Masscan('172.16.40.{}'.format(i))
		print(my_scan.masscan_main())

#     # ['192.168.1.1:8443', '192.168.1.1:53', '192.168.1.1:1990', '192.168.1.1:56377', '192.168.1.1:515', '192.168.1.1:3838']