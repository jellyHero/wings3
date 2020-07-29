import socket


def connectSocket(ip,port):
    # 链接服务端
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    # 数据请求
    while True:
        msg = bytes(input(">>:"), encoding="utf8")
        s.sendall(msg)
        data = s.recv(1024)
        # repr格式化输出
        # print('Received', repr(data))
        print(data.decode('utf8'))
    s.close()

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 8001
    connectSocket(ip,port)