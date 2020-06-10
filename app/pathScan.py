import requests
import os
import hashlib
import time

from conf.conf import base_root
from lib.net.formatUrl import formatUrl,formatPath
from lib.file.file_Class import readFile,writeFile
from lib.core.w_threadPool import MyThreadPool
from module.creatPathPayload import PathPayload

class PathScan:
    def __init__(self,url,resultFile,cachePath_txt=None,cacheFile_txt=None,notExistPath=None,existPath=None,sign_start_num=None,sign_end_num=None,maxconnections=None,onlyPath=None,wordsList_plus=None):
        self.url = formatUrl(url)
        self.resultFile = resultFile
        self.charset = ''
        if notExistPath:
            self.notExistPath = notExistPath
        else:
            self.notExistPath = ['/this_is_must_not_exist']
        if existPath:
            self.existPath = existPath
        else:
            self.existPath = []
        if cachePath_txt:
            self.cachePath_txt = cachePath_txt
        else:
            self.cachePath_txt = '{}payload/cache/path_payload.txt'.format(base_root)
        if cacheFile_txt:
            self.cacheFile_txt = cacheFile_txt
        else:
            self.cacheFile_txt = '{}payload/cache/file_payload.txt'.format(base_root)
        # 创建黑白名单的签名时，从此开始截取响应包,默认为0
        if sign_start_num:
            self.sign_start_num = sign_start_num
        else:
            self.sign_start_num = 0
        # 创建黑白名单的签名时，截取响应包到此为止,默认为30
        if sign_end_num:
            self.sign_end_num = sign_end_num
        else:
            self.sign_end_num = 30
        # 最大线程数，不建议设置太大，以防抗d设备或waf阻断,默认为5
        if maxconnections:
            self.maxconnections = maxconnections
        else:
            self.maxconnections = 5
        if wordsList_plus:
            self.wordsList_plus = wordsList_plus
        else:
            self.wordsList_plus = None

        #是否只扫描路径
        if onlyPath == None:
            self.onlyPath = False
        elif onlyPath == True:
            self.onlyPath = True
        else:
            self.onlyPath = False
        self.black_list = []
        self.white_list = []

    # url探测，待完善（如添加多种探测方式）
    def reqUrl(self,URL,session=None,headers=None):
        if session == None:
            session = requests.Session()
        if headers == None:
            headers = {"Cache-Control": "max-age=0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                   "Connection": "close", "X-Forwarded-For": "127.0.0.1", "Accept-Language": "zh-CN,zh;q=0.9"}
        try:
            response = session.get(URL, headers=headers)
            return response.status_code, response.content
        except Exception as e:
            if e == KeyboardInterrupt:
                os._exit(0)
            else:
                return ('exception', 'reqUrl exception')
        finally:
            pass

    # 判断reqUrl是否发生异常
    def isReqException(self, status_code):
        if str(status_code) == 'exception':
            return True
        else:
            return False

    # 根据响应码，判断是否存在，如果存在则返回true
    def status_codeIsExit(self, status_code):
        status_code_pre = str(status_code)[0:2]
        if status_code_pre == '20' or status_code_pre == '30' or status_code_pre == '50' or status_code == '403':
            return True
        else:
            return False

    # 得到网页的编码方式
    def getCharset(self, STR):
        try:
            result = str(STR, encoding='utf-8')
            self.charset = 'utf-8'
        except:
            try:
                result = str(STR, encoding='gbk')
                self.charset = 'gbk'
                pass
            except:
                self.charset = 'iso'
                pass

    # 取响应码和内容的前N字节，创建签名
    def creatSign(self, status_code, content):
        if len(self.charset) == 0:
            self.getCharset(content[self.sign_start_num:self.sign_end_num])
            # print('charset : ' + self.charset)
        status_code = str(status_code)
        # 使用响应内容的sign_start_num到sign_end_num字节来创建签名
        content = str(content[self.sign_start_num:self.sign_end_num], encoding=self.charset)
        src = status_code + content
        m2 = hashlib.md5()
        m2.update(src.encode(self.charset))
        return m2.hexdigest()

    # 使用一个确认不存在的路径，创造一个响应demo，反例:黑名单
    def creatNotExistDemo(self):
        if len(self.notExistPath) > 0:
            for PATH in self.notExistPath:
                status_code, content = self.reqUrl(self.url+formatPath(PATH))
                if not self.isReqException(status_code):
                    sign = self.creatSign(status_code, content)
                    self.black_list.append(sign)
                else:
                    pass
        else:
            pass

    # 使用一个确认存在的路径，创造一个响应demo，正例:白名单
    def creatExistDemo(self):
        if len(self.existPath) > 0:
            for PATH in self.existPath:
                status_code, content = self.reqUrl(self.url+formatPath(PATH))
                if not self.isReqException(status_code):
                    sign = self.creatSign(status_code, content)
                    self.white_list.append(sign)
                else:
                    pass
        else:
            pass

    # 判断响应是否在黑名单内
    def respIsInBlack_list(self, status_code, content):
        if len(self.black_list) > 0:
            if self.creatSign(status_code, content) in self.black_list:
                return True
            else:
                return False
        else:
            return False

    # 判断响应是否在白名单内
    def respIsInWhite_list(self, status_code, content):
        if len(self.white_list) > 0:
            if self.creatSign(status_code, content) in self.white_list:
                return True
            else:
                return False
        else:
            return False

    # 断言主函数:先判断是否在黑名单、再判断是否在白名单、最后采用响应码来进行不准确判断。
    def urlIsExist(self, status_code, content):
        if self.isReqException(status_code):
            return False
        elif self.respIsInBlack_list(status_code, content):
            return False
        elif self.respIsInWhite_list(status_code, content):
            return True
        elif self.status_codeIsExit(status_code):
            return True
        else:
            return False


    # 扫描url，如果存在，则返回此url，不存在则返回noFound
    def scan(self, URL):
        print(URL)
        status_code, content = self.reqUrl(URL)
        if self.urlIsExist(status_code, content):
            print('[FOUND]{}'.format(URL))
            time.sleep(1.5)#多线程写入文件时，可能存在条件竞争，添加睡眠时间尽可能防止其出现
            writeFile(self.resultFile,URL+'\n')
            time.sleep(1.5)#多线程写入文件时，可能存在条件竞争，添加睡眠时间尽可能防止其出现

    # 使用多线程，扫描路径
    def scan_path(self):
        path_payload = [self.url + formatPath(i.strip()) for i in readFile(self.cachePath_txt)]
        pathScanProcess = MyThreadPool(self.scan,path_payload,self.maxconnections)
        pathScanProcess.start()

    # 使用多线程，扫描文件
    def scan_file(self):
        file_payload = [self.url + formatPath(i.strip()) for i in readFile(self.cacheFile_txt)]
        fileScanProcess = MyThreadPool(self.scan,file_payload,self.maxconnections)
        fileScanProcess.start()

    #使用多线程，扫描额外的字典文件
    def scan_file_plus(self):
        file_payload = [self.url + formatPath(i.strip()) for i in readFile(self.wordsList_plus)]
        fileScanProcess = MyThreadPool(self.scan, file_payload, self.maxconnections)
        fileScanProcess.start()


    def start(self):
        self.creatExistDemo()
        self.creatNotExistDemo()
        if self.onlyPath:
            self.scan_path()
            if self.wordsList_plus:
                self.scan_file_plus()
        else:
            self.scan_path()
            self.scan_file()
            if self.wordsList_plus:
                self.scan_file_plus()


def pathScan(URL,resultFile=None,sign_start_num=None,sign_end_num=None,maxconnections=None,onlyPath=None,notExistPath=None,existPath=None,wordsFile=None,keyWords=None,Extension_AddList=None,Extension_DelList=None,wordsList_plus=None):
    if URL[-1] == '/':
        pass
    else:
        URL = URL+'/'
    if resultFile == None:
        resultFile = '{}result/{}_{}.txt'.format(base_root,URL.split('://')[1].split('/')[0],time.time())
    if sign_start_num == None:
        sign_start_num = 0  # 创建黑白名单的签名时，从此开始截取响应包
    if sign_end_num == None:
        sign_end_num = 30  # 创建黑白名单的签名时，截取响应包到此为止
    if maxconnections == None:
        maxconnections = 5  # 最大线程数，不建议设置太大，以防抗d设备或waf阻断

    # 是否只扫描路径
    if onlyPath == None:
        onlyPath = False
    elif onlyPath == True:
        onlyPath = True
    else:
        onlyPath = False

    if notExistPath == None:
        notExistPath = ['/this_is_must_not_exist']

    if existPath == None:
        existPath = []  # 人工设置存在的url，大多数情况下，建议设置为空

    if wordsFile == None:
        wordsFile = '{}payload/dict/common-words.txt'.format(base_root)
    if keyWords == None :
        keyWords = []
    if Extension_AddList == None:
        Extension_AddList = ['html','js']   #要扫描的文件后缀
    if Extension_DelList == None:
        Extension_DelList = []  #不扫描的文件后缀

    #删除历史扫描结果
    try:
        os.remove(resultFile)
    except:
        pass

    myPath = PathPayload(Extension_DelList=Extension_DelList, Extension_AddList=Extension_AddList,wordsFile=wordsFile,keyWords=keyWords)
    myPath.creatCachePathPayload()
    # print(myPath.cachePath_txt)
    myScan = PathScan(URL,resultFile,cachePath_txt=myPath.cachePath_txt,cacheFile_txt=myPath.cacheFile_txt,notExistPath=notExistPath,existPath=existPath,sign_start_num=sign_start_num,sign_end_num=sign_end_num,maxconnections=maxconnections,onlyPath=onlyPath,wordsList_plus=wordsList_plus)
    # print(myScan.cachePath_txt)
    myScan.start()

if __name__ == '__main__':
    last_time = time.time()
    URL = 'https://ac3f1fcb1f48870e802fcca1003900d0.web-security-academy.net/'  # 扫描目标
    pathScan(URL,wordsList_plus='/Users/shellyzhang/1_codeing/0_python/wings3/payload/dict/path_wordsList_plus.txt',onlyPath=True)
    print('scan path end.total time is {}'.format(time.time() - last_time))