from lib.file.file_Class import readFile
from conf import conf

#通过已知的对应表，来获取端口运行应用的信息
def getPortInfoFromKonwList(port):
    port_process_list = []
    for port_process in readFile('{}payload/others/port_process.txt'.format(conf.base_root)):
        port_process_line = port_process.split(':')
        if port == port_process_line[0]:
            port_process_list.append(port_process_line)
    return port_process_list


if __name__=="__main__":
    print(getPortInfoFromKonwList('8080'))
    #[['8080', 'httpd\n'], ['8080', 'java\n'], ['8080', 'java(jenkins.war)\n']]