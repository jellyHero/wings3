# -*- coding: utf-8 -*-

import ssl
import requests
from  http.server import HTTPServer,BaseHTTPRequestHandler

class R_proxy(BaseHTTPRequestHandler):

    #通过自定义字符串创建响应页面
    def response_with_str(self, data_str):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        # self.send_header('Content-Length', str(len(data_str)))
        self.end_headers()
        self.wfile.write(data_str.encode('utf-8'))

    #代理请求，并返回响应包
    def req(self):
        try:
            if isinstance(self.request,ssl.SSLSocket):
                scheme = 'https://'
            else:
                scheme = 'http://'

            #url
            # self.url = scheme + self.headers['host'].strip() + self.path
            # print(scheme,self.headers['host'].strip(),self.path)
            #判断是否有http Body
            if self.headers.__contains__('Content-Length'):
                data = self.rfile.read(int(self.headers['Content-Length']))
            else:
                data = ''

            if self.command == 'CONNECT':
                pass

            print(self.command)
            req = requests.Request(method=self.command,url=self.path,headers=self.headers,data=data)
            s = requests.Session()
            prepped =req.prepare()

            # 不通过代理发出请求
            r= s.send(prepped,verify=False,allow_redirects=False,stream=True)
            #通过代理发出请求
            # r = s.send(prepped, verify=False, allow_redirects=False, stream=True,proxies={'http':'127.0.0.1:8888'})

            #设置响应头
            self.send_response(r.status_code)
            for key in r.headers:
                self.send_header(key,r.headers[key])
            self.end_headers()

            self.wfile.write(r.content)
        except Exception as e:
            exp = 'Exception : {}'.format(e)
            self.response_with_str(exp)

    def do_GET(self):
        self.req()
    def do_POST(self):
        self.req()
    def do_HEAD(self):
        self.req()
    def do_OPTIONS(self):
        self.req()
    def do_PUT(self):
        self.req()
    def do_DELETE(self):
        self.req()
    def do_MOVE(self):
        self.req()
    def do_TRACE(self):
        self.req()
    def do_CONNECT(self):
        self.req()

if __name__ == "__main__":
    http_server = HTTPServer(('', 3333), R_proxy)
    http_server.serve_forever()