import os

from lib.file.file_Class import writeFile

#初始化配置
def init_conf():
    try:
        r = os.popen('pwd')
        info_list = r.readlines()
        base_root = info_list[0].strip()+'/'
        writeFile('./conf/conf.py', 'OS="{}"\n'.format('linux'))
        writeFile('./conf/conf.py','base_root="{}"\n'.format(base_root))
    except:
        r = os.popen('chdir')
        info_list = r.readlines()
        base_root = info_list[0].strip() + '/'
        writeFile('./conf/conf.py', 'OS="{}"\n'.format('windows'))
        writeFile('./conf/conf.py', 'base_root="{}"\n'.format(base_root))
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36(security test by hanfei)'
    writeFile('./conf/conf.py', 'User_Agent="{}"\n'.format(User_Agent))

if __name__=="__main__":
    init_conf()