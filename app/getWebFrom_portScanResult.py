import time
from lib.core.w_threadPool import MyThreadPool
from lib.net.isWeb import isWeb
from lib.file.file_Class import readFile,writeFile
from conf.conf import base_root

#ip_port_list格式如下：
#['192.168.1.1:8443', '192.168.1.1:53', '192.168.1.1:1990', '192.168.1.1:56377', '192.168.1.1:515', '192.168.1.1:3838']
def getWeb(ip_port_list=None,targetFile=None,resultFile=None):
    if targetFile:
        ip_port_list = readFile(targetFile)
    if resultFile == None:
        resultFile = '{}result/web_{}.txt'.format(base_root,time.time())

    getWebThread = MyThreadPool(isWeb,ip_port_list)
    getWebThread.start()
    writeFile(resultFile,'{}'.format(getWebThread.result))

if __name__ == "__main__":
    ip_port_list = ['www.baidu.com', 'www.qq.com', 'www.t00ls.net']
    getWeb(ip_port_list)