#-*- coding: utf-8 -*-
import gevent
from gevent import socket,monkey
monkey.patch_all()


def server(ip,port):
    s = socket.socket()
    s.bind((ip, port))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        # socket会创建一个线程链接，这里会交给协程处理
        # 链接后通过gevent启动一个协程
        # 接收一个函数，与链接实例参数
        gevent.spawn(handle_request, cli)

#调用shell执行recv
def cmd_recv(recv):
    if recv == b'\n':
        return '\n'.encode('utf-8')
    try:
        recv = recv.decode('utf-8')
    except:
        pass
    import os
    cmd = '{}'.format(recv)
    r = os.popen(cmd)
    info_list = r.readlines()
    if info_list == None:
        info_list = []
    result = ''
    for i in info_list:
        result = result + i + '\n'
    if result == b'':
        result = '\n'.encode('utf-8')
    return result.encode('utf-8')

# 所有交互都由handle处理
def handle_request(conn):
    try:
        while True:
            recv = conn.recv(1024)
            if recv != b'':
                print("recv:", recv)
                data = cmd_recv(recv)
                if not data:
                    conn.send('\n'.encode('utf-8'))
                    # # 如果没有数据就关闭Client端
                    # conn.shutdown(socket.SHUT_WR)
                conn.send(data)
    # 如果出现异常就打印异常
    except Exception as  ex:
        print(ex)
    # 最后中断实例的conn
    finally:
        conn.close()
if __name__ == '__main__':
    ip = '0.0.0.0'
    server(ip,8001)