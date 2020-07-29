# -*- coding: utf-8 -*-
import zipfile
import os
import requests
import re
import json
from bs4 import BeautifulSoup
import xlwt


class report:
    def __init__(self,file_path):
        self.file_path = file_path
        self.dest_dir = file_path.replace('.zip','')

    # 解压单个文件到目标文件夹
    def unzip_file(self,src_file=None,dest_dir=None,password=None):
        if src_file == None:
            src_file = self.file_path
        if dest_dir == None:
            dest_dir = self.dest_dir
        if password:
            password = password.encode()
        zf = zipfile.ZipFile(src_file)
        try:
            zf.extractall(path=dest_dir, pwd=password)
        except RuntimeError as e:
            print(e)
        zf.close()

    #获取vulnHtml的path路径
    def getVulnHtml(self):
        vulnHtml_path = self.dest_dir + '/vulnHtml/'
        return vulnHtml_path

    # 获取所有的vulnHtml
    def getAllFileFromPath(self,path=None):
        vulnHtml = []
        if path == None:
            path = self.getVulnHtml()
        for fpathe, dirs, fs in os.walk(path):
            for f in fs:
                FILE = os.path.join(fpathe, f)[len(path) - 1:]
                vulnHtml.append(FILE.replace('/',''))
        return vulnHtml

    #一键自动化
    def start(self):
        self.unzip_file()
        self.vulnHtml_path = self.getVulnHtml()
        self.vulnHtml = self.getAllFileFromPath(self.vulnHtml_path)

class vulnHtml:
    def __init__(self,vulnHtml):
        self.vulnHtml = vulnHtml
        self.nsfocusId = vulnHtml.split('vulnHtml/')[1].replace('.html','')
        self.vulnIp = self.getVulnIp()

    def getVulnIp(self,vulnHtml=None):
        vulnIp = []
        if vulnHtml == None:
            vulnHtml = self.vulnHtml
        fo = open(vulnHtml, "r+")
        req_obj = fo.read()
        soup = BeautifulSoup(req_obj, 'lxml')
        tags = soup.find_all('a')
        fo.close()
        for tag in tags:
            vulnIp.append(tag.string)
        return vulnIp

class vuln:
    def __init__(self,nsfocusId,nsfocus_ip='10.1.10.24',username='admin',passwd='admin@123'):
        self.nsfocusId = nsfocusId
        self.nsfocus_ip = nsfocus_ip
        self.username = username
        self.passwd = passwd
        self.session = requests.Session()

    def login(self):
        self.cookies = {}
        session = self.session
        paramsPost = {"csrfmiddlewaretoken": "qaqodSE7zcQHLlF4aycFN8Hp8R1xl8F6JvUO5cgk9hl0z6BF3Rv3Mo3kfsbmwerD",
                      "password": self.passwd, "username": self.username}
        headers = {"Origin": "{}".format(self.nsfocus_ip),
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "Connection": "close",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "Sec-Fetch-Site": "same-origin",
                   "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Cache-Control": "max-age=0",
                   "Upgrade-Insecure-Requests": "1", "Sec-Fetch-User": "?1", "Accept-Language": "zh-CN,zh;q=0.9",
                   "Content-Type": "application/x-www-form-urlencoded"}
        cookies = {"csrftoken": "Fe5Vhfm1gS6stJnzC4eLdFq7PKkKy8emrhfgBt5918NXSJ7r1eT1JMSiMrtcSe9Z","sessionid":"ooirv6u4ig64c3juwyy1a41f1x4h2o4x"}
        try:
            response = session.post("https://{}/accounts/login_view/".format(self.nsfocus_ip), data=paramsPost, headers=headers,cookies=cookies,verify=False)
            Set_Cookie = response.headers['Set-Cookie']
            csrftoken_patt = re.compile(r'csrftoken=(.*?);')
            sessionid_patt = re.compile(r'sessionid=(.*?);')
            self.cookies['csrftoken'] = csrftoken_patt.findall(Set_Cookie)[0]
            self.cookies['sessionid'] = sessionid_patt.findall(Set_Cookie)[0]
            requests.utils.add_dict_to_cookiejar(self.session.cookies,self.cookies)
        except:
            pass

    def getVulnDetail(self):
        try:
            response = self.session.get('https://{}/template/show_vul_desc?id={}'.format(self.nsfocus_ip,self.nsfocusId))
            vulnRisk_patt = re.compile(r'<th>危险分值</th>\n(.*?)</td>')
            try:
                vulnName_patt = re.compile(r'<img src=(.*?)\n')
                self.vulnName = vulnName_patt.findall(response.text)[0].split("'>")[1]
            except:
                vulnName_patt = re.compile(r'</img>(.*?)\n')
                self.vulnName = vulnName_patt.findall(response.text)[0]
            vulnRisk_num = float(vulnRisk_patt.findall(response.text)[0].split('<td>')[1])
            if 0 <= vulnRisk_num < 4:
                self.vulnRisk = '低'
            elif 4 <= vulnRisk_num < 7:
                self.vulnRisk = '中'
            elif 7 <= vulnRisk_num <= 10:
                self.vulnRisk = '高'
            else:
                self.vulnRisk = 'error'
        except:
            self.vulnName = self.nsfocusId
            self.vulnRisk = self.nsfocusId

class cmp_report:
    def __init__(self,old_report,new_report):
        self.result_file_xls = old_report.replace('.zip','/../result.xls')
        self.result_file_txt = old_report.replace('.zip', '/../result.txt')
        self.old_report = report(old_report)
        self.new_report = report(new_report)
        self.row_num = 0

    # 写文件
    def writeFile(self,STR,target_file=None):
        if target_file == None:
            target_file = self.result_file_txt
        with open(target_file, 'a') as f:
            f.write(STR)

    # 读文件
    def readFile(self,target_file=None):
        if target_file == None:
            target_file = self.result_file_txt
        with open(target_file, 'r') as f:
            # print(f.readlines())
            return f.readlines()

    #设置xls格式
    def set_style(self,name,height,bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height

        style.font = font
        return style

    #保存结果
    def write_excel(self,path=None):
        if path == None:
            path = self.result_file_xls
        # 创建工作簿
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建sheet
        data_sheet = workbook.add_sheet('demo')
        # row0 = [u'字段名称', u'大致时段', 'CRNTI', 'CELL-ID']
        # row1 = [u'测试', '15:50:33-15:52:14', 22706, 4190202]
        # 生成第一行和第二行
        row_num = 0
        for row in self.readFile():
            try:
                row_dict = json.loads(row)
                row = [row_dict['nsfocus_id'],row_dict['ip'],row_dict['vuln_name'],row_dict['vuln_risk'],row_dict['status']]
                for i in range(len(row)):
                    data_sheet.write(row_num, i, row[i], self.set_style('Times New Roman', 220, True))
                row_num = row_num + 1
            except:
                pass
        # 保存文件
        workbook.save(path)

    def OK(self,nsfocus_id,ip,vuln_name,vuln_risk):
        row = {'nsfocus_id':nsfocus_id,'ip':ip,'vuln_name':vuln_name.replace('</img>',''),'vuln_risk':vuln_risk,'status':u'已修复'}
        print(row)
        self.writeFile(json.dumps(row)+'\n')

    def NO(self,nsfocus_id,ip,vuln_name,vuln_risk):
        row = {'nsfocus_id': nsfocus_id, 'ip': ip, 'vuln_name': vuln_name.replace('</img>', ''), 'vuln_risk': vuln_risk,'status': u'未修复'}
        print(row)
        self.writeFile(json.dumps(row)+'\n')

    def start(self):
        self.old_report.start()
        self.new_report.start()
        old_report_vulnHtml_list = self.old_report.vulnHtml #老报告的所有漏洞网页列表
        new_report_vulnHtml_list = self.new_report.vulnHtml #新报告的所有漏洞网页列表

        for i in old_report_vulnHtml_list:
            #获取漏洞的信息
            nsfocus_id = i.replace('.html','')
            vuln_i = vuln(nsfocus_id)
            vuln_i.login()
            vuln_i.getVulnDetail()
            #打开老报告
            old_report_vulnHtml = vulnHtml(self.old_report.vulnHtml_path+i)
            old_vuln_ip_list = old_report_vulnHtml.getVulnIp()
            #如果该漏洞网页，在新报告中不存在，则写入已修复
            if i not in new_report_vulnHtml_list:
                for ok_ip in old_vuln_ip_list:
                    self.OK(nsfocus_id,ok_ip,vuln_i.vulnName,vuln_i.vulnRisk)
            else:
                for ip in old_vuln_ip_list:
                    new_report_vulnHtml = vulnHtml(self.new_report.vulnHtml_path + i)
                    new_vuln_ip_list = new_report_vulnHtml.getVulnIp()
                    #如果该ip，在新报告中不存在，则写入已修复，否则写入未修复
                    if ip not in new_vuln_ip_list:
                        self.OK(nsfocus_id,ip, vuln_i.vulnName, vuln_i.vulnRisk)
                    else:
                        self.NO(nsfocus_id,ip, vuln_i.vulnName, vuln_i.vulnRisk)
        self.write_excel()


old_report = '/Users/shellyzhang/Desktop/1/313_海豚TV云服务器_2020_07_23_html.zip'
new_report = '/Users/shellyzhang/Desktop/1/315_海豚TV云服务器_2020_07_28_html.zip'

myCmp = cmp_report(old_report,new_report)
myCmp.start()
# nsfocusid = '74530'
# vuln_i = vuln(nsfocusid)
# vuln_i.login()
# vuln_i.getVulnDetail()
